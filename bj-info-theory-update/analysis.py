import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from .information import InformationTheory

class Analyzer:
    def __init__(self):
        self.info_theory = InformationTheory()
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)
    
    def analyze_ev_vs_count(self, df, save_path='plots/ev_vs_count.png'):
        df['tc_bin'] = pd.cut(df['true_count'], bins=np.arange(-10, 11, 1))
        ev_by_count = df.groupby('tc_bin')['result'].agg(['mean', 'std', 'count'])
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        tc_values = [interval.mid for interval in ev_by_count.index]
        ax.plot(tc_values, ev_by_count['mean'], 'o-', linewidth=2, markersize=8)
        ax.axhline(y=0, color='r', linestyle='--', alpha=0.5)
        ax.set_xlabel('True Count', fontsize=12)
        ax.set_ylabel('Expected Value', fontsize=12)
        ax.set_title('Expected Value vs True Count', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        slope, intercept = np.polyfit(tc_values, ev_by_count['mean'], 1)
        ax.plot(tc_values, slope * np.array(tc_values) + intercept, 
                'r--', alpha=0.5, label=f'Linear fit: {slope:.4f}x + {intercept:.4f}')
        ax.legend()
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return ev_by_count
    
    def compare_counting_systems(self, results_dict, save_path='plots/system_comparison.png'):
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        systems = list(results_dict.keys())
        colors = ['blue', 'green', 'red']
        
        for idx, system in enumerate(systems):
            df = results_dict[system]
            df['tc_bin'] = pd.cut(df['true_count'], bins=np.arange(-10, 11, 1))
            ev_by_count = df.groupby('tc_bin')['result'].mean()
            tc_values = [interval.mid for interval in ev_by_count.index]
            
            axes[0, 0].plot(tc_values, ev_by_count, 'o-', label=system.upper(), 
                           color=colors[idx], linewidth=2)
        
        axes[0, 0].axhline(y=0, color='black', linestyle='--', alpha=0.3)
        axes[0, 0].set_xlabel('True Count')
        axes[0, 0].set_ylabel('Expected Value')
        axes[0, 0].set_title('EV Comparison Across Systems')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        for idx, system in enumerate(systems):
            df = results_dict[system]
            axes[0, 1].hist(df['true_count'], bins=50, alpha=0.5, 
                           label=system.upper(), color=colors[idx])
        
        axes[0, 1].set_xlabel('True Count')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].set_title('True Count Distribution')
        axes[0, 1].legend()
        
        for idx, system in enumerate(systems):
            df = results_dict[system]
            cumulative_returns = df['result'].cumsum()
            axes[1, 0].plot(cumulative_returns, label=system.upper(), 
                           color=colors[idx], linewidth=1.5)
        
        axes[1, 0].set_xlabel('Hand Number')
        axes[1, 0].set_ylabel('Cumulative Return')
        axes[1, 0].set_title('Cumulative Returns')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        system_stats = []
        for system in systems:
            df = results_dict[system]
            system_stats.append({
                'System': system.upper(),
                'Mean EV': df['result'].mean(),
                'Std Dev': df['result'].std(),
                'Sharpe': df['result'].mean() / df['result'].std() if df['result'].std() > 0 else 0
            })
        
        stats_df = pd.DataFrame(system_stats)
        axes[1, 1].axis('off')
        table = axes[1, 1].table(cellText=stats_df.values,
                                colLabels=stats_df.columns,
                                cellLoc='center',
                                loc='center',
                                bbox=[0, 0, 1, 1])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return stats_df
    
    def information_vs_advantage(self, df, save_path='plots/information_vs_advantage.png'):
        df['mutual_info'] = df.apply(
            lambda row: self.info_theory.information_from_count(
                row['true_count'], row['cards_seen']
            ), axis=1
        )
        
        df['tc_bin'] = pd.cut(df['true_count'], bins=np.arange(-10, 11, 1))
        grouped = df.groupby('tc_bin').agg({
            'result': 'mean',
            'mutual_info': 'mean'
        })
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        mutual_info_values = grouped['mutual_info'].values
        ev_values = grouped['result'].values
        
        ax1.scatter(mutual_info_values, ev_values, alpha=0.6, s=100)
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            mutual_info_values, ev_values
        )
        
        x_line = np.linspace(mutual_info_values.min(), mutual_info_values.max(), 100)
        ax1.plot(x_line, slope * x_line + intercept, 'r--', linewidth=2,
                label=f'Fit: {slope:.4f}x + {intercept:.4f}\nR²={r_value**2:.3f}')
        
        ax1.set_xlabel('Mutual Information (bits)', fontsize=12)
        ax1.set_ylabel('Expected Value', fontsize=12)
        ax1.set_title('EV vs Mutual Information', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        tc_values = [interval.mid for interval in grouped.index]
        ax2.plot(tc_values, mutual_info_values, 'o-', linewidth=2, markersize=8)
        ax2.set_xlabel('True Count', fontsize=12)
        ax2.set_ylabel('Mutual Information (bits)', fontsize=12)
        ax2.set_title('Information Gained vs True Count', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return slope, intercept, r_value**2