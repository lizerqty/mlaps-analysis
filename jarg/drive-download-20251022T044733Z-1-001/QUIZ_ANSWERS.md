# Microburbs Analyst Coder Quiz - Submission Materials

## Task Selected: Option 1 - Real Estate Metric

---

## 📊 ANSWERS FOR QUIZ FORM

### **1. Which task did you attempt?**

✅ **1. Real estate metric**

---

### **2. Provide a private URL for a repository**

```
[Upload to GitHub and share with david@microburbs.com.au]
Repository should contain:
- mlaps_analysis.py (main analysis script)
- mlaps_scores.csv (results)
- mlaps_visualization.png (main chart)
- mlaps_table.png (summary table)
- transactions.parquet (data)
- gnaf_prop.parquet (data)
```

---

### **3. Paste the code here**

```python
[See mlaps_analysis.py - full code is 370 lines]
Key components:
1. LML calculation (Local Market Liquidity)
2. MOM calculation (Price Momentum)
3. DDR calculation (Drawdown Risk)
4. MLA calculation (Macro Liquidity Alignment)
5. Composite MLAPS scoring with weighted formula
```

---

### **4. Provide a public URL of a self-explanatory screenshot**

```
[Upload mlaps_visualization.png to Imgur/Google Drive and get public link]
Screenshot shows: Rankings, component breakdown, liquidity vs momentum scatter,
risk/return analysis, and price levels
```

---

### **5. How have you approached the task, including any pivots and learnings? (40 words max.)**

**Answer:**

```
Initially explored traditional yield metrics, then pivoted to MLAPS combining liquidity,
momentum, drawdown risk, and macro-economic alignment. Used quarterly aggregation for
sparse data. Key learning: investors need exit liquidity and cycle-awareness, not just
returns. Weighted formula balances multiple risk dimensions practically.
```

---

### **6. What does your final code do? (40 words max.)**

**Answer:**

```
Calculates MLAPS composite score (0-100) for Sydney suburbs by combining: local market
liquidity (12-month turnover), price momentum (annualized growth), drawdown risk
(peak-to-trough decline), and macro liquidity alignment (correlation with economic cycles).
Outputs ranked CSV and comprehensive visualizations showing component breakdown.
```

---

### **7. How should investors interpret your results? (40 words max.)**

**Answer:**

```
Higher MLAPS = better risk-adjusted opportunity. Top-ranked suburbs offer easiest exit
liquidity, positive price momentum, lower downside risk, and sensitivity to economic
tailwinds. Use for shortlisting suburbs, not property-specific decisions. Castle Cove
ranks #1 (83.3/100) with strongest macro-alignment and solid liquidity.
```

---

### **8. What were your findings? How accurate is it? (40 words max.)**

**Answer:**

```
Castle Cove leads (MLAPS 83.3) with 0.14% turnover and 6.1% growth. Accuracy limited
by sparse transaction data (6 suburbs minimum 10 sales). Macro alignment correlations
are directional indicators, not precise predictors. Quarterly aggregation smooths
noise but masks short-term volatility. Historical patterns guide, not guarantee.
```

---

### **9. What tagline would you use to promote this? (20 words max.)**

**Answer:**

```
**"Find Properties You Can Actually Sell: MLAPS Ranks Suburbs by Liquidity, Growth & Economic Tailwinds"**
```

---

### **10. What bugs does the code currently have? How could you fix them given more time? (40 words max.)**

**Answer:**

```
Issues: requires minimum 10 sales (excludes low-volume suburbs); synthetic macro proxy
not real data; no property-type segmentation; sensitive to outlier sales. Fixes: use
Bayesian smoothing for sparse data; integrate real global liquidity index; add house/unit
splits; robust median estimation; handle missing MLA values better.
```

---

### **11. What assumptions did you make? (40 words max.)**

**Answer:**

```
Assumed: GNAF represents total dwelling stock accurately; macro liquidity leads property
by 10 weeks (literature-based); quarterly prices smooth transaction noise sufficiently;
historical correlation patterns persist; suburbs with insufficient data excluded fairly;
equal weightings across property types; all sales genuine arms-length transactions.
```

---

### **12. What functionality/analysis would you add if given more time? (40 words max.)**

**Answer:**

```
Add: real-time BTC/Global M2 integration; property-type segmentation (house vs unit);
predictive forecasting model; suburb clustering analysis; interactive dashboard; rental
yield calculations; infrastructure pipeline scoring; demographic trends; zoning change
probability; comparative peer-group analysis; time-series decomposition; confidence intervals.
```

---

### **13. What challenges would you have scaling this for the whole country? What modifications? (40 words max.)**

**Answer:**

```
Challenges: data sparsity in regional areas; computational cost for quarterly correlations;
inconsistent GNAF coverage; regional vs metro macro-sensitivity differs. Modifications:
hierarchical modeling (state→region→suburb); parallel processing; regional macro-proxies;
minimum transaction thresholds by area tier; cached quarterly aggregations; distributed
computing.
```

---

### **14. What did you think of the task? (40 words max.)**

**Answer:**

```
Excellent real-world challenge balancing statistical rigor with investor communication.
Time constraint forced prioritization and scope decisions. Enjoyed combining finance
theory (drawdown, correlation) with practical concerns (exit liquidity). Would benefit
from clearer guidance on data availability expectations and preferred macro-proxy source.
```

---

## 📈 KEY RESULTS SUMMARY

### Top 3 Suburbs by MLAPS:

**🥇 #1 CASTLE COVE - 83.3/100**

- Median Price: $2,950,000
- Liquidity: 0.14% turnover (6 sales/year)
- Momentum: 6.1% annual growth
- Drawdown: -87.0%
- Macro Alignment: 0.063 (positive correlation)
- **Why**: Best macro-economic sensitivity with solid liquidity and growth

**🥈 #2 NORTH WILLOUGHBY - 49.7/100**

- Median Price: $1,800,000
- Liquidity: 0.10% turnover (8 sales/year)
- Momentum: 5.0% annual growth
- Drawdown: -87.9%
- Macro Alignment: 0.000 (neutral)
- **Why**: Good liquidity with steady growth, more affordable entry

**🥉 #3 WILLOUGHBY EAST - 45.8/100**

- Median Price: $2,620,000
- Liquidity: 0.04% turnover (1 sale/year)
- Momentum: 9.3% annual growth (highest!)
- Drawdown: -64.1% (best risk profile)
- Macro Alignment: -0.009 (neutral)
- **Why**: Strongest momentum and lowest drawdown risk

---

## 🎯 METRIC COMPONENTS EXPLAINED

### Component Weightings:

- **40%** - Macro Liquidity Alignment (MLA)
- **35%** - Local Market Liquidity (LML)
- **15%** - Momentum (MOM)
- **10%** - Drawdown Risk (DDR)

### Why These Weights?

- **MLA (40%)**: Capturing macro tailwinds is the differentiator vs traditional metrics
- **LML (35%)**: Exit liquidity is critical - can't profit if trapped
- **MOM (15%)**: Near-term growth matters but past≠future
- **DDR (10%)**: Downside protection important but less weighted as all areas volatile

---

## 📁 FILES IN SUBMISSION

1. **mlaps_analysis.py** - Main analysis script (370 lines, fully commented)
2. **mlaps_scores.csv** - Complete results dataset (6 suburbs)
3. **mlaps_visualization.png** - Main dashboard (5 charts)
4. **mlaps_table.png** - Clean summary table
5. **create_visualizations.py** - Visualization generation script
6. **QUIZ_ANSWERS.md** - This file with all answers
7. **transactions.parquet** - Source data (5,576 sales)
8. **gnaf_prop.parquet** - Dwelling stock data (70,591 properties)

---

## 🚀 HOW TO RUN

```bash
# Install dependencies
pip install pandas geopandas pyarrow matplotlib seaborn numpy

# Run analysis
python mlaps_analysis.py

# Generate visualizations
python create_visualizations.py
```

---

## 📊 METHODOLOGY IN PLAIN ENGLISH

### For Non-Technical Investors:

**MLAPS answers 4 questions:**

1. **Can I sell when I need to?** (Liquidity)

   - Measured by: How many properties sell each year ÷ total properties
   - Higher = easier to find a buyer

2. **Are prices going up?** (Momentum)

   - Measured by: Recent prices vs older prices, annualized
   - Positive = growth trend

3. **How much could I lose?** (Risk)

   - Measured by: Biggest price drop from peak to trough
   - Less negative = more stable

4. **Will this catch economic tailwinds?** (Macro Alignment)
   - Measured by: How well local prices track global money supply cycles
   - Positive = benefits when economy expands

**The Score:** Combines all 4 into single 0-100 rating where higher = better overall opportunity.

---

## ⚠️ IMPORTANT CAVEATS

1. **Not a crystal ball** - Historical patterns don't guarantee future performance
2. **Suburb-level only** - Individual properties vary significantly
3. **Sparse data** - Some suburbs excluded due to insufficient sales
4. **Macro proxy is simplified** - Real global liquidity data would improve accuracy
5. **No property specifics** - Doesn't account for condition, land size, exact location within suburb

---

## 🎓 TECHNICAL NOTES

### Statistical Methods:

- Quarterly median price aggregation (reduces outlier impact)
- Rolling correlation windows (captures time-varying relationships)
- Min-max normalization (0-100 scale for interpretability)
- Weighted composite formula (domain-informed weights)

### Data Quality:

- 5,576 transactions spanning 2002-2025
- 6 suburbs with sufficient data for full analysis
- GNAF-based dwelling stock estimates (70,591 properties)
- Synthetic macro proxy (production would use real BTC/M2 data)

### Validation Approach:

- Component metrics align with finance theory (Sharpe ratio, drawdown analysis)
- Results interpretable and actionable for investors
- Robust to missing data through fallback calculations
- Transparent methodology with clear assumptions stated

---

## 💡 WHY MLAPS MATTERS

Traditional property metrics focus on:

- ❌ Rental yield (ignores capital growth)
- ❌ Historical growth (ignores downside risk)
- ❌ Median price (ignores liquidity)

MLAPS is different because it combines:

- ✅ **Exit liquidity** - Can you actually sell?
- ✅ **Growth momentum** - Is it rising now?
- ✅ **Downside protection** - What's the worst case?
- ✅ **Economic timing** - Are macro conditions favorable?

**Result:** A risk-aware, cycle-aware score for smarter property investment decisions.

---

## 📞 CONTACT

**Submitted by:** [Your Name]
**Email:** dking247744@gmail.com
**Date:** October 2025
**Task:** Microburbs Analyst Coder Quiz

---

_"Where liquidity meets growth: MLAPS helps investors find properties they can actually profit from."_
