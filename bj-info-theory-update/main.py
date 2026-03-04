import os
import pandas as pd
from src.simulation import Simulator
from src.analysis import Analyzer

def ensure_directories():
    os.makedirs('data', exist_ok=True)
    os.makedirs('plots', exist_ok=True)
    os.makedirs('paper', exist_ok=True)

def run_basic_simulation(num_hands=100000):
    print("Running basic Hi-Lo simulation...")
    sim = Simulator(num_decks=6, counter_type='hilo')
    df = sim.simulate(num_hands)
    df.to_csv('data/hilo_results.csv', index=False)
    print(f"Saved results to data/hilo_results.csv")
    return df

def run_system_comparison(num_hands=50000):
    print("\nComparing counting systems...")
    sim = Simulator(num_decks=6)
    results = sim.compare_systems(num_hands)
    
    for system, df in results.items():
        df.to_csv(f'data/{system}_results.csv', index=False)
        print(f"Saved {system} results to data/{system}_results.csv")
    
    return results

def analyze_results():
    print("\nAnalyzing results...")
    analyzer = Analyzer()
    
    if os.path.exists('data/hilo_results.csv'):
        df = pd.read_csv('data/hilo_results.csv')
        ev_stats = analyzer.analyze_ev_vs_count(df)
        print("\nEV vs True Count:")
        print(ev_stats)
    
    systems = ['hilo', 'ko', 'omega']
    results_dict = {}
    for system in systems:
        if os.path.exists(f'data/{system}_results.csv'):
            results_dict[system] = pd.read_csv(f'data/{system}_results.csv')
    
    if results_dict:
        stats_df = analyzer.compare_counting_systems(results_dict)
        print("\nSystem Comparison:")
        print(stats_df)
        
        if 'hilo' in results_dict:
            slope, intercept, r2 = analyzer.information_vs_advantage(results_dict['hilo'])
            print(f"\nInformation Theory Analysis:")
            print(f"EV = {slope:.4f} * MI + {intercept:.4f}")
            print(f"R² = {r2:.3f}")

def main():
    ensure_directories()
    
    df = run_basic_simulation(num_hands=100000)
    
    results = run_system_comparison(num_hands=50000)
    
    analyze_results()
    
    print("\nAll simulations complete!")
    print("Results saved in data/")
    print("Plots saved in plots/")

if __name__ == "__main__":
    main()