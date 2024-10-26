import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.special import logsumexp
from sklearn.mixture import GaussianMixture # just for checking if sklearn thing works or not
from sklearn.manifold import TSNE

class GMM:
    def __init__(self, n_components, max_iter=100, tol=1e-3, reg_covar=1e-6):
        self.n_components = n_components
        self.max_iter = max_iter
        self.tol = tol
        self.reg_covar = reg_covar
        self.weights = None
        self.means = None
        self.covariances = None

    def initialize(self, X):
        n_samples, n_features = X.shape
        self.weights = np.full(self.n_components, 1 / self.n_components)# Initializing weights to be uniform
        random_indices = np.random.choice(n_samples, self.n_components, replace=False)# Randomly selecting initial means
        self.means = X[random_indices]
        covariance_matrix = np.cov(X.T) # covariances
        identity_matrix = self.reg_covar * np.eye(n_features)
        self.covariances = [covariance_matrix + identity_matrix for _ in range(self.n_components)]

    def e_step(self, X):
        n_samples = X.shape[0]
        log_resp = np.zeros((n_samples, self.n_components))
        for k in range(self.n_components):
            log_resp[:, k] = np.log(self.weights[k] + 1e-300) + self._log_multivariate_normal_pdf(X, self.means[k], self.covariances[k])
        log_resp_norm = logsumexp(log_resp, axis=1)
        log_resp -= log_resp_norm[:, np.newaxis]
        return np.exp(log_resp)

    def m_step(self, X, responsibilities):
        n_samples, n_features = X.shape
        self.weights = responsibilities.sum(axis=0) / n_samples
        self.weights = np.clip(self.weights, 1e-10, 1)
        self.weights /= self.weights.sum()
        for k in range(self.n_components):
            resp_k = responsibilities[:, k]
            resp_sum = resp_k.sum()
            if resp_sum > 0:
                self.means[k] = (X * resp_k[:, np.newaxis]).sum(axis=0) / resp_sum
                diff = X - self.means[k]
                self.covariances[k] = np.dot(resp_k * diff.T, diff) / resp_sum + self.reg_covar * np.eye(n_features)
            else:
                self.means[k] = X.mean(axis=0)
                self.covariances[k] = np.cov(X.T) + self.reg_covar * np.eye(n_features)

    def fit(self, X):
        self.initialize(X)
        prev_log_likelihood = -np.inf
        for _ in range(self.max_iter):
            responsibilities = self.e_step(X)
            self.m_step(X, responsibilities)
            log_likelihood = self.getLikelihood(X)
            if np.isfinite(log_likelihood):
                change_in_log_likelihood = np.abs(log_likelihood - prev_log_likelihood)
                if change_in_log_likelihood < self.tol:
                    break
            prev_log_likelihood = log_likelihood

    def _log_multivariate_normal_pdf(self, X, mean, cov):
        n_samples, n_features = X.shape
        diff = X - mean
        try:
            chol = np.linalg.cholesky(cov)
            log_det = 2 * np.sum(np.log(np.diag(chol)))
            quad_form = np.sum(np.linalg.solve(chol, diff.T)**2, axis=0)
        except np.linalg.LinAlgError:
            return -np.inf * np.ones(n_samples)
        return -0.5 * (n_features * np.log(2 * np.pi) + log_det + quad_form)

    def getParams(self):
        return {
            'weights': self.weights,
            'means': self.means,
            'covariances': self.covariances
        }

    def getMembership(self, X):
        return self.e_step(X)

    def getLikelihood(self, X):
        n_samples = X.shape[0]
        log_likelihood = np.zeros((n_samples, self.n_components))
        # Computing log-likelihood for each component
        for k in range(self.n_components):
            weight_term = np.log(self.weights[k] + 1e-300)
            pdf_term = self._log_multivariate_normal_pdf(X, self.means[k], self.covariances[k])
            log_likelihood[:, k] = weight_term + pdf_term
        # computing total log-likelihood by Normalizing log-likelihood
        log_likelihood_normalized = logsumexp(log_likelihood, axis=1)
        total_log_likelihood = np.sum(log_likelihood_normalized)
        
        return total_log_likelihood


    def bic(self, X):
        n_samples, n_features = X.shape
        n_parameters = (
            self.n_components * (n_features + n_features * (n_features + 1) / 2) +
            self.n_components - 1
        )
        log_likelihood = self.getLikelihood(X)
        # Calculating BIC
        bic_value = -2 * log_likelihood + n_parameters * np.log(n_samples)
        return bic_value


    def aic(self, X):
        n_samples, n_features = X.shape
        n_parameters = (
            self.n_components * (n_features + n_features * (n_features + 1) / 2) +
            self.n_components - 1
        )
        log_likelihood = self.getLikelihood(X)
        # Calculating AIC
        aic_value = -2 * log_likelihood + 2 * n_parameters
        return aic_value
