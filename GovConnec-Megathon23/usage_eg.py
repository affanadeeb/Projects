from datetime import datetime, timedelta

# Define your area of interest
aoi = {
    'type': 'Polygon',
    'coordinates': [[
        [78.4746, 17.3616],  # Example coordinates for a rice field in India
        [78.4746, 17.3706],
        [78.4836, 17.3706],
        [78.4836, 17.3616],
        [78.4746, 17.3616]
    ]]
}

# Create detector instance
detector = PaddyGrowthDetector(
    aoi_geometry=aoi,
    start_date='2024-01-01',
    end_date='2024-03-01'
)

# Process single date
def process_single_date():
    # Download and process imagery
    results = detector.process_image_series()
    
    if results:
        latest_result = results[-1]
        
        # Generate visualizations
        fig = detector.visualize_results(
            latest_result['classified_map'],
            latest_result['indices'],
            latest_result['anomalies']
        )
        
        # Save visualization
        fig.savefig('paddy_analysis_results.png')
        
        # Print detailed report
        print("\nGrowth Stage Analysis Report:")
        print_report(latest_result['report'])
        
        # Save report to CSV
        save_report_to_csv(latest_result['report'], 'paddy_analysis_report.csv')

def print_report(report):
    """Print formatted analysis report"""
    print("\nGrowth Stage Distribution:")
    for stage, percentage in report['growth_stage_distribution'].items():
        print(f"{stage}: {percentage:.2f}%")
    
    print("\nHealth Metrics:")
    for index_name, metrics in report['health_metrics'].items():
        print(f"\n{index_name.upper()}:")
        for metric_name, value in metrics.items():
            print(f"  {metric_name}: {value:.3f}")
    
    print(f"\nAnomalies detected in {report['anomalies']['total_percentage']:.2f}% of the area")

def save_report_to_csv(report, filename):
    """Save report to CSV file"""
    # Flatten the nested dictionary
    flat_data = {}
    
    # Growth stage distribution
    for stage, value in report['growth_stage_distribution'].items():
        flat_data[f'growth_stage_{stage}'] = value
    
    # Health metrics
    for index_name, metrics in report['health_metrics'].items():
        for metric_name, value in metrics.items():
            flat_data[f'{index_name}_{metric_name}'] = value
    
    # Anomalies
    flat_data['anomalies_percentage'] = report['anomalies']['total_percentage']
    
    # Save to CSV
    pd.DataFrame([flat_data]).to_csv(filename, index=False)

# Function to monitor temporal changes
def monitor_temporal_changes(detector, interval_days=10):
    """Monitor changes over time with specified interval"""
    start_date = datetime.strptime(detector.start_date, '%Y-%m-%d')
    end_date = datetime.strptime(detector.end_date, '%Y-%m-%d')
    
    temporal_data = []
    current_date = start_date
    
    while current_date <= end_date:
        detector.start_date = current_date.strftime('%Y-%m-%d')
        detector.end_date = (current_date + timedelta(days=1)).strftime('%Y-%m-%d')
        
        results = detector.process_image_series()
        if results:
            result = results[0]
            temporal_data.append({
                'date': current_date,
                'growth_stages': result['classified_map'],
                'indices': result['indices'],
                'report': result['report']
            })
        
        current_date += timedelta(days=interval_days)
    
    return temporal_data

# Function to analyze temporal trends
def analyze_temporal_trends(temporal_data):
    """Analyze and visualize temporal trends in paddy growth"""
    dates = [data['date'] for data in temporal_data]
    
    # Prepare data for plotting
    stage_changes = {
        stage: [data['report']['growth_stage_distribution'].get(stage, 0) 
               for data in temporal_data]
        for stage in temporal_data[0]['report']['growth_stage_distribution'].keys()
    }
    
    # Plot temporal changes
    plt.figure(figsize=(12, 6))
    for stage, percentages in stage_changes.items():
        plt.plot(dates, percentages, label=stage, marker='o')
    
    plt.xlabel('Date')
    plt.ylabel('Percentage of Area')
    plt.title('Temporal Changes in Growth Stages')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('temporal_changes.png')

# Function to export results in GIS-compatible format
def export_to_geotiff(result, output_path):
    """Export results to GeoTIFF format"""
    with rasterio.open('template.tif') as src:
        metadata = src.meta.copy()
        
        # Update metadata for classification results
        metadata.update(
            dtype=rasterio.float32,
            count=1,
            nodata=-9999
        )
        
        # Save classified map
        with rasterio.open(f'{output_path}/classified_map.tif', 'w', **metadata) as dst:
            dst.write(result['classified_map'].astype(rasterio.float32), 1)
        
        # Save NDVI
        with rasterio.open(f'{output_path}/ndvi.tif', 'w', **metadata) as dst:
            dst.write(result['indices']['ndvi'].astype(rasterio.float32), 1)
        
        # Save anomalies
        with rasterio.open(f'{output_path}/anomalies.tif', 'w', **metadata) as dst:
            dst.write(result['anomalies'].astype(rasterio.float32), 1)

if __name__ == "__main__":
    # Process single date analysis
    process_single_date()
    
    # Monitor temporal changes
    temporal_data = monitor_temporal_changes(detector, interval_days=10)
    analyze_temporal_trends(temporal_data)
    
    # Export results
    if temporal_data:
        export_to_geotiff(temporal_data[-1], 'output_data')