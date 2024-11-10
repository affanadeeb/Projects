import rasterio
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from datetime import datetime, timedelta
import pandas as pd
from rasterio.plot import show
import seaborn as sns
import ee
import geopy
from sentinelsat import SentinelAPI
from sklearn.ensemble import RandomForestClassifier
from scipy import ndimage
import warnings
import os
from skimage import morphology
from atmospheric_correction import process_atmospheric_correction

class PaddyGrowthDetector:
    def __init__(self, aoi_geometry, start_date, end_date):
        """
        Initialize detector with area of interest and date range
        
        Parameters:
        aoi_geometry: GeoJSON geometry of area of interest
        start_date: Start date for analysis (YYYY-MM-DD)
        end_date: End date for analysis (YYYY-MM-DD)
        """
        self.aoi = aoi_geometry
        self.start_date = start_date
        self.end_date = end_date
        self.initialize_apis()

    def initialize_apis(self):
        """Initialize Earth Engine and Sentinel APIs"""
        try:
            ee.Initialize()
            self.ee_initialized = True
        except Exception as e:
            print(f"Earth Engine initialization failed: {e}")
            self.ee_initialized = False

        try:
            # Initialize Sentinel API with your credentials
            self.sentinel_api = SentinelAPI(
                os.getenv('COPERNICUS_USER'),
                os.getenv('COPERNICUS_PASSWORD'),
                'https://scihub.copernicus.eu/dhus'
            )
        except Exception as e:
            print(f"Sentinel API initialization failed: {e}")

    def download_sentinel_imagery(self):
        """Download Sentinel-2 imagery for the specified area and date range"""
        products = self.sentinel_api.query(
            self.aoi,
            date=(self.start_date, self.end_date),
            platformname='Sentinel-2',
            cloudcoverpercentage=(0, 20)
        )
        
        downloaded_files = []
        for product_id, product_info in products.items():
            try:
                self.sentinel_api.download(product_id)
                downloaded_files.append(product_info['title'])
            except Exception as e:
                print(f"Download failed for {product_id}: {e}")
        
        return downloaded_files

    def apply_cloud_mask(self, image_data, qa_band):
        """
        Apply cloud masking using QA band
        
        Parameters:
        image_data: Satellite image data
        qa_band: Quality assessment band
        """
        # Sentinel-2 specific cloud masking
        cloud_bitmask = 1 << 10
        cirrus_bitmask = 1 << 11
        
        mask = ((qa_band & cloud_bitmask) == 0) & ((qa_band & cirrus_bitmask) == 0)
        return np.where(mask, image_data, np.nan)

    def atmospheric_correction(self, image_data, metadata):
        """
        Apply atmospheric correction using Dark Object Subtraction (DOS)
        and Top of Atmosphere (TOA) correction
        """
        # Implementation of DOS correction
        def dark_object_subtraction(band_data):
            # Find darkest pixel (1st percentile to avoid outliers)
            dark_object = np.percentile(band_data[~np.isnan(band_data)], 1)
            return np.maximum(band_data - dark_object, 0)

        # Apply TOA correction using sensor-specific coefficients
        def toa_correction(band_data, band_metadata):
            radiance_mult = band_metadata['RADIANCE_MULT']
            radiance_add = band_metadata['RADIANCE_ADD']
            sun_elevation = metadata['SUN_ELEVATION']
            
            # Convert DN to radiance
            radiance = band_data * radiance_mult + radiance_add
            
            # Convert radiance to reflectance
            reflectance = (np.pi * radiance) / (metadata['ESUN'] * np.sin(np.radians(sun_elevation)))
            
            return reflectance

        corrected_bands = {}
        for band_name, band_data in image_data.items():
            if band_name in metadata['BAND_METADATA']:
                # Apply DOS correction
                dos_corrected = dark_object_subtraction(band_data)
                
                # Apply TOA correction
                toa_corrected = toa_correction(dos_corrected, metadata['BAND_METADATA'][band_name])
                
                corrected_bands[band_name] = toa_corrected
                
        return corrected_bands

    def calculate_indices(self, nir_band, red_band, green_band, swir_band):
        """
        Calculate multiple vegetation indices
        """
        indices = {}
        
        # NDVI (Normalized Difference Vegetation Index)
        indices['ndvi'] = (nir_band - red_band) / (nir_band + red_band + 1e-8)
        
        # EVI (Enhanced Vegetation Index)
        indices['evi'] = 2.5 * ((nir_band - red_band) / 
                               (nir_band + 6 * red_band - 7.5 * blue_band + 1))
        
        # NDWI (Normalized Difference Water Index)
        indices['ndwi'] = (green_band - nir_band) / (green_band + nir_band + 1e-8)
        
        # LSWI (Land Surface Water Index)
        indices['lswi'] = (nir_band - swir_band) / (nir_band + swir_band + 1e-8)
        
        return indices

    def classify_growth_stages_advanced(self, indices, temporal_data=None):
        """
        Advanced growth stage classification using multiple indices and machine learning
        """
        # Prepare features for classification
        features = np.stack([
            indices['ndvi'].ravel(),
            indices['evi'].ravel(),
            indices['ndwi'].ravel(),
            indices['lswi'].ravel()
        ]).T

        # Remove invalid values
        valid_mask = ~np.isnan(features).any(axis=1)
        valid_features = features[valid_mask]

        # Define growth stages based on known characteristics
        # Training data would typically come from ground truth data
        growth_stages = {
            'flooding': {'ndvi': (-1, 0.2), 'ndwi': (0.3, 1.0)},
            'early_vegetative': {'ndvi': (0.2, 0.4), 'evi': (0.2, 0.4)},
            'tillering': {'ndvi': (0.4, 0.6), 'evi': (0.4, 0.6)},
            'reproductive': {'ndvi': (0.6, 0.8), 'evi': (0.6, 0.8)},
            'ripening': {'ndvi': (0.3, 0.6), 'evi': (0.3, 0.5)}
        }

        # Train Random Forest classifier
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        
        # Generate synthetic training data based on growth stage characteristics
        X_train = []
        y_train = []
        
        for stage, thresholds in growth_stages.items():
            n_samples = 1000
            stage_features = np.random.uniform(
                low=[thresh[0] for thresh in thresholds.values()],
                high=[thresh[1] for thresh in thresholds.values()],
                size=(n_samples, len(thresholds))
            )
            X_train.extend(stage_features)
            y_train.extend([stage] * n_samples)

        clf.fit(X_train, y_train)
        
        # Predict growth stages
        predictions = clf.predict(valid_features)
        
        # Convert back to image shape
        classified_map = np.full(indices['ndvi'].shape, np.nan)
        classified_map.ravel()[valid_mask] = predictions
        
        return classified_map

    def detect_anomalies(self, indices, temporal_data=None):
        """
        Detect anomalies in paddy growth using statistical methods
        """
        anomalies = {}
        
        # Calculate z-scores for each index
        for index_name, index_data in indices.items():
            z_score = (index_data - np.nanmean(index_data)) / np.nanstd(index_data)
            anomalies[index_name] = np.abs(z_score) > 2  # Flag values > 2 standard deviations
            
        # Combine anomalies from different indices
        combined_anomalies = np.logical_or.reduce(list(anomalies.values()))
        
        # Apply spatial filtering to remove noise
        combined_anomalies = morphology.remove_small_objects(combined_anomalies, min_size=10)
        
        return combined_anomalies

    def generate_report(self, classified_map, indices, anomalies):
        """
        Generate a comprehensive analysis report
        """
        report = {
            'growth_stage_distribution': {},
            'health_metrics': {},
            'anomalies': {}
        }
        
        # Calculate growth stage distribution
        unique_stages, counts = np.unique(classified_map[~np.isnan(classified_map)], 
                                        return_counts=True)
        total_valid = np.sum(counts)
        
        for stage, count in zip(unique_stages, counts):
            report['growth_stage_distribution'][stage] = count / total_valid * 100
            
        # Calculate health metrics
        for index_name, index_data in indices.items():
            report['health_metrics'][index_name] = {
                'mean': np.nanmean(index_data),
                'std': np.nanstd(index_data),
                'median': np.nanmedian(index_data)
            }
            
        # Summarize anomalies
        report['anomalies']['total_percentage'] = (
            np.sum(anomalies) / np.size(anomalies) * 100
        )
        
        return report

    def visualize_results(self, classified_map, indices, anomalies):
        """
        Create comprehensive visualization of results
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 15))
        
        # Plot growth stages
        im1 = axes[0, 0].imshow(classified_map, cmap='viridis')
        axes[0, 0].set_title('Growth Stages')
        plt.colorbar(im1, ax=axes[0, 0])
        
        # Plot NDVI
        im2 = axes[0, 1].imshow(indices['ndvi'], cmap='RdYlGn')
        axes[0, 1].set_title('NDVI')
        plt.colorbar(im2, ax=axes[0, 1])
        
        # Plot EVI
        im3 = axes[1, 0].imshow(indices['evi'], cmap='RdYlGn')
        axes[1, 0].set_title('EVI')
        plt.colorbar(im3, ax=axes[1, 0])
        
        # Plot anomalies
        im4 = axes[1, 1].imshow(anomalies, cmap='RdYlGn')
        axes[1, 1].set_title('Anomalies')
        plt.colorbar(im4, ax=axes[1, 1])
        
        plt.tight_layout()
        return fig

    def process_image_series(self):
        """
        Process a series of images for the given time period
        """
        # Download imagery
        image_files = self.download_sentinel_imagery()
        
        results = []
        for image_file in image_files:
            with rasterio.open(image_file) as src:
                # Read all required bands
                bands = {
                    'nir': src.read(4),
                    'red': src.read(3),
                    'green': src.read(2),
                    'swir': src.read(5),
                    'qa': src.read(6)
                }
                
                # Apply cloud mask
                for band_name in ['nir', 'red', 'green', 'swir']:
                    bands[band_name] = self.apply_cloud_mask(bands[band_name], bands['qa'])
                
                # Apply atmospheric correction
                metadata = src.meta
                corrected_bands = self.atmospheric_correction(bands, metadata)
                
                # Calculate indices
                indices = self.calculate_indices(
                    corrected_bands['nir'],
                    corrected_bands['red'],
                    corrected_bands['green'],
                    corrected_bands['swir']
                )
                
                # Classify growth stages
                classified_map = self.classify_growth_stages_advanced(indices)
                
                # Detect anomalies
                anomalies = self.detect_anomalies(indices)
                
                # Generate report
                report = self.generate_report(classified_map, indices, anomalies)
                
                results.append({
                    'date': src.tags()['TIFFTAG_DATETIME'],
                    'classified_map': classified_map,
                    'indices': indices,
                    'anomalies': anomalies,
                    'report': report
                })
        
        return results

# Example usage
def main():
    # Define area of interest (GeoJSON format)
    aoi = {
        'type': 'Polygon',
        'coordinates': [[
            [longitude1, latitude1],
            [longitude2, latitude2],
            [longitude3, latitude3],
            [longitude1, latitude1]
        ]]
    }
    
    # Create detector instance
    detector = PaddyGrowthDetector(
        aoi_geometry=aoi,
        start_date='2024-01-01',
        end_date='2024-03-01'
    )
    
    # Process images and get results
    results = detector.process_image_series()
    
    # Visualize results for the latest image
    latest_result = results[-1]
    fig = detector.visualize_results(
        latest_result['classified_map'],
        latest_result['indices'],
        latest_result['anomalies']
    )
    plt.show()
    
    # Print report
    print("\nGrowth Stage Analysis Report:")
    print(latest_result['report'])

if __name__ == "__main__":
    main()