# How to Use MLAPS Dashboard

## 1. Install Requirements

```bash
pip install pandas geopandas pyarrow scipy numpy
```

## 2. Generate Suburb Rankings

```bash
python mlaps_analysis_v2.py
```

**What this does:** Analyzes property data and creates `mlaps_scores_v2.csv` with suburb rankings.

**Output:** Console shows top suburbs with MLAPS scores.

## 3. View Interactive Dashboard

```bash
python run_dashboard.py
```

**What happens:**

- Opens browser automatically to dashboard
- If not, manually open: `http://localhost:8000/mlaps_dashboard.html`

## 4. Load Data into Dashboard

1. Click **"CHOOSE CSV FILE"** button
2. Select `mlaps_scores_v2.csv`
3. Explore the charts:
   - **Dashboard tab**: Rankings, components, scatter plots
   - **Data Explorer tab**: Detailed suburb table
   - **Methodology tab**: How it works

## 5. Interpret Results

**MLAPS Score:**

- 60-80 = Strong opportunity
- 40-60 = Moderate
- 20-40 = Weak

**Top suburb gets highest score** based on:

- Exit liquidity (can you sell?)
- Price momentum (prices rising?)
- Downside risk (how much could you lose?)
- Macro sensitivity (catches economic tailwinds?)

---

## That's It!

Three commands, four clicks, done.

Questions? Check the **Methodology** tab in the dashboard.
