# ⚡ MLAPS v2 Quick Start

## 🚀 Run in 3 Steps

### Step 1: Generate Improved Scores

```bash
python mlaps_analysis_v2.py
```

**Output:** `mlaps_scores_v2.csv` with all improvements

### Step 2: Launch Dashboard

```bash
python run_dashboard.py
```

**Opens:** http://localhost:8000/mlaps_dashboard.html automatically

### Step 3: Load Data

1. Click "Choose CSV File"
2. Select `mlaps_scores_v2.csv`
3. Explore interactive charts!

---

## 🎯 What's Fixed in v2

| Issue          | v1                 | v2                       | ✅    |
| -------------- | ------------------ | ------------------------ | ----- |
| **Drawdowns**  | -87% (unrealistic) | -35% (realistic)         | FIXED |
| **Units**      | "0.14%" (unclear)  | "0.14% per year" (clear) | FIXED |
| **Statistics** | No p-values        | P-values + CIs           | ADDED |
| **Outliers**   | Sensitive          | Winsorized               | FIXED |
| **Dashboard**  | None               | Interactive HTML         | ADDED |

---

## 📊 Key Results

```
#1 - CASTLE COVE: 62.5/100
├─ Liquidity:     0.14% per year (6 sales)
├─ Momentum:      6.1% p.a.
├─ Drawdown:      -35.0% (smoothed, realistic!)
└─ Macro Align:   0.010 (NS, p=0.87)
Price: $2,950,000
```

---

## 💻 Share Your Code

### Method 1: Dashboard (Easy!)

1. Open "Code Share" tab
2. Paste your Python code
3. Click "Generate Local Share URL"
4. Copy & share the URL

### Method 2: GitHub Gist

1. Go to https://gist.github.com
2. Paste your code
3. Create public gist
4. Share URL

---

## 📁 New Files

- `mlaps_analysis_v2.py` - Improved analysis (all fixes)
- `mlaps_scores_v2.csv` - Results with realistic metrics
- `mlaps_dashboard.html` - Interactive dashboard
- `run_dashboard.py` - Server launcher
- `DASHBOARD_GUIDE.md` - Complete guide
- `IMPROVEMENTS_V2.md` - Detailed changelog
- `QUICK_START_V2.md` - This file

---

## ✅ Verification Checklist

Run these to verify everything works:

```bash
# 1. Check Python version
python --version  # Should be 3.6+

# 2. Install dependencies (if needed)
pip install pandas geopandas pyarrow matplotlib seaborn scipy

# 3. Run analysis
python mlaps_analysis_v2.py
# ✓ Should complete in ~10 seconds
# ✓ Creates mlaps_scores_v2.csv

# 4. Launch dashboard
python run_dashboard.py
# ✓ Opens browser automatically
# ✓ Shows http://localhost:8000

# 5. Test dashboard
# ✓ Upload CSV
# ✓ See 4 interactive charts
# ✓ View data table
# ✓ Read methodology
# ✓ Test code sharing
```

---

## 🎯 For Investors

**What MLAPS v2 Tells You:**

- **High Score (60+)**: Strong overall opportunity

  - Example: Castle Cove (62.5) = Best combo of liquidity + growth

- **High Liquidity (>0.10%/yr)**: Easy to buy/sell

  - Example: Castle Cove (0.14%/yr) = 6 sales annually

- **High Momentum (>5% p.a.)**: Rising prices

  - Example: Willoughby East (9.3% p.a.) = Strongest growth

- **Better Drawdown (>-30%)**: Lower risk
  - Example: Willoughby East (-28.6%) = Most stable

---

## 🐛 Troubleshooting

### Dashboard won't load

```bash
# Try different port
python -m http.server 8001
# Open: http://localhost:8001/mlaps_dashboard.html
```

### Charts not showing

- Make sure CSV is uploaded
- Check browser console for errors
- Try refreshing page

### Code sharing not working

- URL might be too long (use GitHub Gist instead)
- Try smaller code snippet
- Check browser supports base64

---

## 📚 Learn More

- **Complete Guide**: Read `DASHBOARD_GUIDE.md`
- **All Changes**: Read `IMPROVEMENTS_V2.md`
- **Methodology**: Open dashboard → "Methodology" tab
- **Questions**: Check `README.md` or `QUIZ_ANSWERS.md`

---

## 🎉 You're Ready!

**Everything is working if you see:**
✅ Dashboard loads at localhost:8000  
✅ Charts render when CSV uploaded  
✅ Rankings show realistic drawdowns (-28% to -35%)  
✅ Units labeled clearly (% per year, % p.a.)  
✅ Code sharing generates URLs

---

**🏆 MLAPS v2: Production-Ready!**

_All feedback implemented | Dashboard functional | Ready to deploy_
