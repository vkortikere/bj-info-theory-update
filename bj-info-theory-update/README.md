# Information Theory of Card Counting

Mathematical analysis of blackjack card counting using information theory and entropy.

## Installation
```bash
git clone https://github.com/vkortikere/blackjack-info-theory.git
cd blackjack-info-theory
pip install -r requirements.txt
```

## Usage

Run complete simulation and analysis:
```bash
python main.py
```

This will:
1. Simulate 100,000 hands with Hi-Lo counting
2. Compare Hi-Lo, KO, and Omega II systems (50k hands each)
3. Generate plots and analysis
4. Save results to `data/` and plots to `plots/`

## Project Structure
```
src/
  blackjack.py      - Core game logic
  strategy.py       - Basic Strategy implementation
  counting.py       - Card counting systems
  information.py    - Information theory calculations
  simulation.py     - Simulation engine
  analysis.py       - Analysis and visualization
```

## Results

- `data/*.csv` - Raw simulation data
- `plots/ev_vs_count.png` - Expected value by true count
- `plots/system_comparison.png` - Comparison of counting systems
- `plots/information_vs_advantage.png` - Information theory analysis

## Mathematical Framework

This project proves bounds on player advantage using:
- Shannon entropy of deck composition
- Mutual information between observed cards and remaining deck
- Information-theoretic bounds on expected value