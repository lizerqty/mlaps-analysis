# MLAPS v2: Macro-Liquidity Aligned Property Score

A professional investment analytics tool for Australian residential property markets.

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
pip install pandas geopandas pyarrow matplotlib seaborn scipy numpy
```

### Step 2: Run Analysis

```bash
python mlaps_analysis_v2.py
```

This creates `mlaps_scores_v2.csv` with suburb rankings.

### Step 3: View Dashboard

```bash
python run_dashboard.py
```

Opens your browser to: `http://localhost:8000/mlaps_dashboard.html`

Upload the CSV file to see interactive charts.

---

## 📊 What is MLAPS?

MLAPS ranks suburbs (0-100 score) by combining:

- **40%** Macro Liquidity Alignment - Sensitivity to economic cycles
- **35%** Local Market Liquidity - How easy to buy/sell
- **15%** Price Momentum - Recent growth trends
- **10%** Drawdown Risk - Downside protection

**Higher score = Better risk-adjusted opportunity**

---

## 📁 Files

- `mlaps_analysis_v2.py` - Main analysis script (run this first)
- `mlaps_dashboard.html` - Interactive dashboard (JP Morgan-style)
- `run_dashboard.py` - Local web server
- `transactions.parquet` - Property sales data
- `gnaf_prop.parquet` - Dwelling stock data
- `mlaps_scores_v2.csv` - Results (generated after running analysis)

---

## 💡 Example Results

```
#1 CASTLE COVE - Score: 62.5/100
├─ Liquidity: 0.14% per year
├─ Momentum: 6.1% p.a.
├─ Drawdown: -35.0%
└─ Macro Align: 0.010 (not significant)
Price: $2,950,000
```

---

## 🎯 For Investors

**Use MLAPS to:**

- Shortlist suburbs for further research
- Compare risk/return profiles
- Time macro economic cycles
- Avoid liquidity traps

**Important:** This is a screening tool, not a substitute for property-specific due diligence.

---

## ⚠️ Limitations

- Requires minimum transaction volumes (sparse data areas excluded)
- Macro proxy is synthetic (production should use real BTC/Global M2 data)
- No property-type segmentation (houses vs units combined)
- Suburb-level only (individual properties vary)
- Historical patterns don't guarantee future results

---

## 📧 Contact

Microburbs Assessment | October 2025

**Note:** This repository is shared with david@microburbs.com.au as part of the technical assessment.
