#!/bin/bash
#
# Stock Screener Runner
# Saves all results to Desktop with timestamps
#

# Generate timestamp for output files
TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")

# Activate virtual environment
source ~/.claude/skills/stock-screener/venv/bin/activate

# Run screening and save log to Desktop with timestamp
cd ~/.claude/skills/stock-screener
python run_real_screening.py 2>&1 | tee ~/Desktop/screening_output_${TIMESTAMP}.log

echo ""
echo "Results saved to:"
echo "  📊 CSV: ~/Desktop/screening_results_${TIMESTAMP}.csv"
echo "  📝 Top 10: ~/Desktop/TOP_10_STOCKS_${TIMESTAMP}.md"
echo "  📄 Log: ~/Desktop/screening_output_${TIMESTAMP}.log"
