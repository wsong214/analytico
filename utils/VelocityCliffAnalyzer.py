import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Optional, Tuple
import logging

class VelocityCliffAnalyzer:
    """
    Analyzer for velocity cliff phenomenon in baseball pitching.
    """
    
    def __init__(self, data_pipeline):
        """
        Initialize the analyzer.
        
        Args:
            data_pipeline: Data pipeline instance
        """
        self.data_pipeline = data_pipeline
        self.logger = data_pipeline.logger
    
    def analyze_pitcher(self, player_name: str, start_year: int, end_year: int, 
                       pitch_type: str = 'FF') -> Optional[pd.DataFrame]:
        """
        Analyze a pitcher's velocity cliff.
        
        Args:
            player_name (str): Player name (e.g., "Jack Flaherty")
            start_year (int): Starting year for analysis
            end_year (int): Ending year for analysis
            pitch_type (str): Pitch type to analyze (default: 'FF' for fastball)
            
        Returns:
            Optional[pd.DataFrame]: Prepared data for analysis
        """
        # Parse player name
        name_parts = player_name.split()
        if len(name_parts) < 2:
            self.logger.error("Player name must include first and last name")
            return None
        
        first_name, last_name = name_parts[0], name_parts[-1]
        
        # Get pitcher data
        pitcher_data = self.data_pipeline.get_pitcher_data_by_name(
            first_name, last_name, start_year, end_year
        )
        
        if len(pitcher_data) == 0:
            self.logger.error(f"No data found for {player_name}")
            return None
        
        # Prepare data for velocity analysis
        analysis_data = self.data_pipeline.prepare_velocity_analysis_data(
            pitcher_data, pitch_type
        )
        
        return analysis_data
    
    def plot_pitch_summary(self, player_data: pd.DataFrame, player_name: str):
        """
        Plot pitch type summary statistics.
        
        Args:
            player_data (pd.DataFrame): Player data
            player_name (str): Player name for title
        """
        summary = self.data_pipeline.get_pitch_summary(player_data)
        
        plt.figure(figsize=(12, 8))
        
        # Plot velocity by pitch type
        plt.subplot(2, 2, 1)
        velocity_means = summary['release_speed_mean']
        velocity_means.plot(kind='bar')
        plt.title('Average Velocity by Pitch Type')
        plt.ylabel('Velocity (mph)')
        plt.xticks(rotation=45)
        
        # Plot wOBA by pitch type
        plt.subplot(2, 2, 2)
        woba_means = summary['estimated_woba_using_speedangle_mean']
        woba_means.plot(kind='bar')
        plt.title('Average wOBA by Pitch Type')
        plt.ylabel('wOBA')
        plt.xticks(rotation=45)
        
        # Plot pitch count by type
        plt.subplot(2, 2, 3)
        pitch_counts = summary['release_speed_count']
        pitch_counts.plot(kind='bar')
        plt.title('Pitch Count by Type')
        plt.ylabel('Number of Pitches')
        plt.xticks(rotation=45)
        
        # Plot velocity vs wOBA scatter
        plt.subplot(2, 2, 4)
        plt.scatter(summary['release_speed_mean'], summary['estimated_woba_using_speedangle_mean'])
        plt.xlabel('Average Velocity (mph)')
        plt.ylabel('Average wOBA')
        plt.title('Velocity vs wOBA by Pitch Type')
        
        plt.tight_layout()
        plt.suptitle(f'{player_name} - Pitch Summary', y=1.02)
        plt.show()
    
    def plot_velocity_woba_relationship(self, fastball_data: pd.DataFrame, player_name: str):
        """
        Plot velocity vs wOBA relationship for fastballs.
        
        Args:
            fastball_data (pd.DataFrame): Fastball data
            player_name (str): Player name for title
        """
        plt.figure(figsize=(10, 6))
        
        x_column = 'release_speed'
        y_column = 'estimated_woba_using_speedangle'
        
        plt.scatter(fastball_data[x_column], fastball_data[y_column], alpha=0.6)
        plt.xlabel('Release Speed (mph)')
        plt.ylabel('Estimated wOBA')
        plt.title(f'{player_name} - Velocity vs wOBA (Fastballs)')
        plt.grid(True)
        plt.show()
    
    def perform_cusum_analysis(self, fastball_data: pd.DataFrame, player_name: str, generate_plots: bool = True) -> float:
        """
        Perform CUSUM analysis to detect velocity threshold.
        
        Args:
            fastball_data (pd.DataFrame): Fastball data
            player_name (str): Player name for title
            
        Returns:
            float: Detected velocity threshold
        """
        x_column = 'release_speed'
        y_column = 'estimated_woba_using_speedangle'
        
        # Sort by velocity
        fastball_data_sorted = fastball_data.sort_values(by=x_column).reset_index(drop=True)
        
        x_data = fastball_data_sorted[x_column]
        y_data = fastball_data_sorted[y_column]
        
        # Compute rolling mean to smooth fluctuations
        window_size = 10
        y_smoothed = y_data.rolling(window=window_size, center=True, min_periods=1).mean()
        
        # Compute target value (baseline wOBA)
        target = y_smoothed.mean()
        
        # Compute deviations from target
        deviations = y_smoothed - target
        
        # Set CUSUM parameters
        k = 0.005  # Drift parameter
        h = 0.02   # Decision threshold
        
        # Compute CUSUM with one-sided detection
        cusum = np.maximum(0, np.cumsum(deviations - k))
        
        # Identify velocity threshold
        threshold_idx = np.argmax(cusum)
        velocity_threshold = x_data.iloc[threshold_idx]
        
        # Plot results (if requested)
        if generate_plots:
            plt.figure(figsize=(12, 8))
            
            # Plot 1: Scatter plot with LOWESS smoothing
            plt.subplot(2, 1, 1)
            plt.scatter(x_data, y_data, alpha=0.4, label='Raw Data')
            
            # Add LOWESS smoothing
            try:
                from statsmodels.nonparametric.smoothers_lowess import lowess
                lowess_frac = 0.2
                lowess_fit = lowess(y_data, x_data, frac=lowess_frac)
                x_lowess, y_lowess = zip(*lowess_fit)
                plt.plot(x_lowess, y_lowess, color='orange', linewidth=2, label='LOWESS Smoothing')
            except ImportError:
                self.logger.warning("statsmodels not available, skipping LOWESS smoothing")
            
            plt.axhline(target, color='red', linestyle='--', label='Baseline wOBA')
            plt.axvline(velocity_threshold, color='purple', linestyle='--', 
                       label=f'Velocity Threshold: {velocity_threshold:.1f} mph')
            plt.xlabel('Release Speed (mph)')
            plt.ylabel('Estimated wOBA')
            plt.title(f'{player_name} - Velocity vs wOBA Analysis')
            plt.legend()
            plt.grid(True)
            
            # Plot 2: CUSUM analysis
            plt.subplot(2, 1, 2)
            plt.plot(x_data, cusum, label='CUSUM', color='blue')
            plt.axhline(h, color='green', linestyle='--', label='CUSUM Decision Threshold')
            plt.axvline(velocity_threshold, color='purple', linestyle='--', 
                       label=f'Velocity Threshold: {velocity_threshold:.1f} mph')
            plt.xlabel('Release Speed (mph)')
            plt.ylabel('Cumulative Sum')
            plt.title('CUSUM Analysis for Performance Decline Detection')
            plt.legend()
            plt.grid(True)
            
            plt.tight_layout()
            plt.show()
        
        self.logger.info(f"Detected performance decline at velocity: {velocity_threshold:.1f} mph")
        return velocity_threshold
    
    def perform_bayesian_changepoint_analysis(self, fastball_data: pd.DataFrame, 
                                            player_name: str, generate_plots: bool = True) -> float:
        """
        Perform Bayesian changepoint analysis.
        
        Args:
            fastball_data (pd.DataFrame): Fastball data
            player_name (str): Player name for title
            
        Returns:
            float: Detected velocity threshold
        """
        x_column = 'release_speed'
        y_column = 'estimated_woba_using_speedangle'
        
        # Sort by velocity
        fastball_data_sorted = fastball_data.sort_values(by=x_column).reset_index(drop=True)
        
        x_data = fastball_data_sorted[x_column].values
        y_data = fastball_data_sorted[y_column].values
        
        # Smooth fluctuations
        window_size = 10
        y_smoothed = pd.Series(y_data).rolling(window=window_size, center=True, min_periods=1).mean()
        
        # Bayesian changepoint detection
        import scipy.stats as stats
        
        def log_likelihood(y, mu1, mu2, sigma, cp):
            """Compute log-likelihood given a change point"""
            n1, n2 = cp, len(y) - cp
            log_lik1 = np.sum(stats.norm.logpdf(y[:n1], mu1, sigma))
            log_lik2 = np.sum(stats.norm.logpdf(y[n1:], mu2, sigma))
            return log_lik1 + log_lik2
        
        def bayesian_changepoint(y, n_samples=5000):
            """Use MCMC to estimate change point"""
            n = len(y)
            cp_samples = []
            
            # Initialize parameters
            cp = n // 2
            mu1, mu2 = np.mean(y[:cp]), np.mean(y[cp:])
            sigma = np.std(y)
            
            for _ in range(n_samples):
                # Propose new changepoint
                cp_new = np.random.randint(5, n-5)  # Avoid edges
                
                # Compute likelihoods
                mu1_new, mu2_new = np.mean(y[:cp_new]), np.mean(y[cp_new:])
                log_lik_old = log_likelihood(y, mu1, mu2, sigma, cp)
                log_lik_new = log_likelihood(y, mu1_new, mu2_new, sigma, cp_new)
                
                # Compute acceptance probability
                alpha = np.exp(log_lik_new - log_lik_old)
                if np.random.rand() < alpha:
                    cp = cp_new
                    mu1, mu2 = mu1_new, mu2_new
                
                cp_samples.append(cp)
            
            # Return most frequent change point
            return np.bincount(cp_samples).argmax()
        
        # Run Bayesian changepoint detection
        change_point_index = bayesian_changepoint(y_smoothed)
        change_point_value = x_data[change_point_index]
        
        # Plot results (if requested)
        if generate_plots:
            plt.figure(figsize=(12, 6))
            
            plt.scatter(x_data, y_data, alpha=0.4, label='Raw Data')
            plt.plot(x_data, y_smoothed, color='orange', linewidth=2, label='Smoothed wOBA')
            plt.axvline(change_point_value, color='red', linestyle='--', 
                       label=f'Change Point: {change_point_value:.1f} mph')
            
            plt.xlabel('Release Speed (mph)')
            plt.ylabel('Estimated wOBA')
            plt.title(f'{player_name} - Bayesian Change Point Detection')
            plt.legend()
            plt.grid(True)
            plt.show()
        
        self.logger.info(f"Detected velocity change point: {change_point_value:.1f} mph")
        return change_point_value
    
    def run_full_analysis(self, player_name: str, start_year: int, end_year: int, 
                         pitch_type: str = 'FF', generate_plots: bool = True) -> dict:
        """
        Run complete velocity cliff analysis.
        
        Args:
            player_name (str): Player name
            start_year (int): Starting year
            end_year (int): Ending year
            pitch_type (str): Pitch type to analyze
            generate_plots (bool): Whether to generate and display plots
            
        Returns:
            dict: Analysis results
        """
        self.logger.info(f"Starting velocity cliff analysis for {player_name} ({start_year}-{end_year})")
        
        # Get pitcher data
        pitcher_data = self.analyze_pitcher(player_name, start_year, end_year, pitch_type)
        
        if pitcher_data is None or len(pitcher_data) == 0:
            return {'error': 'No data found for player'}
        
        # Plot pitch summary (if requested)
        if generate_plots:
            self.plot_pitch_summary(pitcher_data, player_name)
        
        # Get fastball data
        fastball_data = self.data_pipeline.get_pitch_type_data(pitcher_data, pitch_type)
        
        if len(fastball_data) == 0:
            return {'error': f'No {pitch_type} data found'}
        
        # Plot velocity vs wOBA relationship (if requested)
        if generate_plots:
            self.plot_velocity_woba_relationship(fastball_data, player_name)
        
        # Perform CUSUM analysis
        cusum_threshold = self.perform_cusum_analysis(fastball_data, player_name, generate_plots)
        
        # Perform Bayesian changepoint analysis
        bayesian_threshold = self.perform_bayesian_changepoint_analysis(fastball_data, player_name, generate_plots)
        
        # Compile results
        results = {
            'player_name': player_name,
            'years': f"{start_year}-{end_year}",
            'total_pitches': len(pitcher_data),
            'fastball_pitches': len(fastball_data),
            'cusum_threshold': cusum_threshold,
            'bayesian_threshold': bayesian_threshold,
            'average_threshold': (cusum_threshold + bayesian_threshold) / 2
        }
        
        self.logger.info(f"Analysis complete. Average threshold: {results['average_threshold']:.1f} mph")
        return results 