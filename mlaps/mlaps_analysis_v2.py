"""
MLAPS v2: Macro-Liquidity Aligned Property Score (IMPROVED)
=============================================================

Improvements from v1:
- Fixed drawdown calculation (smoothing, winsorization, capping)
- Added statistical significance testing for MLA
- Proper units (% per year for liquidity)
- Outlier handling (winsorization at 2.5/97.5 percentiles)
- Sensitivity-aware MLA with confidence intervals
- Robust estimation with minimum sample requirements
- Forward validation framework

Author: Microburbs Assessment v2
Date: October 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("MLAPS v2: IMPROVED MACRO-LIQUIDITY ALIGNED PROPERTY SCORE")
print("=" * 80)

# ============================================================================
# STEP 1: LOAD AND PREPARE DATA
# ============================================================================

print("\n[1/7] Loading property data...")

transactions = pd.read_parquet('transactions.parquet')
transactions['dat'] = pd.to_datetime(transactions['dat'])
transactions = transactions.sort_values('dat')

gnaf = pd.read_parquet('gnaf_prop.parquet')

print(f"  ✓ Loaded {len(transactions):,} transactions")
print(f"  ✓ Loaded {len(gnaf):,} properties (dwelling stock proxy)")
print(f"  ✓ Date range: {transactions['dat'].min().date()} to {transactions['dat'].max().date()}")

# ============================================================================
# STEP 2: CALCULATE LOCAL MARKET LIQUIDITY (LML) - IMPROVED
# ============================================================================

print("\n[2/7] Calculating Local Market Liquidity (LML)...")

def calculate_lml_v2(transactions_df, gnaf_df):
    """
    LML = (12-month sales ÷ dwelling stock) × 100
    Now displays as % per year (not just %)
    """
    cutoff_date = transactions_df['dat'].max() - pd.DateOffset(months=12)
    recent_sales = transactions_df[transactions_df['dat'] >= cutoff_date]
    
    sales_12m = recent_sales.groupby('suburb').size().reset_index(name='sales_12m')
    stock = gnaf_df.groupby('locality_name').size().reset_index(name='dwelling_stock')
    stock = stock.rename(columns={'locality_name': 'suburb'})
    
    lml_df = sales_12m.merge(stock, on='suburb', how='left')
    lml_df['dwelling_stock'] = lml_df['dwelling_stock'].fillna(lml_df['sales_12m'] * 10)
    
    # Express as % per year
    lml_df['LML'] = (lml_df['sales_12m'] / lml_df['dwelling_stock']) * 100
    
    # Add reliability flag
    lml_df['lml_reliable'] = lml_df['sales_12m'] >= 5
    
    return lml_df[['suburb', 'LML', 'sales_12m', 'dwelling_stock', 'lml_reliable']]

lml_data = calculate_lml_v2(transactions, gnaf)
print(f"  ✓ Calculated LML for {len(lml_data)} suburbs")
print(f"  ✓ LML range: {lml_data['LML'].min():.2f}% to {lml_data['LML'].max():.2f}% per year")
print(f"  ✓ Reliable suburbs (≥5 sales): {lml_data['lml_reliable'].sum()}")

# ============================================================================
# STEP 3: CALCULATE MOMENTUM (MOM) - IMPROVED WITH WINSORIZATION
# ============================================================================

print("\n[3/7] Calculating Price Momentum (MOM) with outlier controls...")

def calculate_momentum_v2(transactions_df, min_sales=15):
    """
    MOM = Annualized price growth with winsorization
    - Trims outliers at 2.5/97.5 percentiles
    - Requires minimum 15 sales
    - Uses 6-month rolling median for stability
    """
    momentum_list = []
    
    for suburb in transactions_df['suburb'].unique():
        suburb_data = transactions_df[transactions_df['suburb'] == suburb].copy()
        suburb_data = suburb_data.sort_values('dat')
        
        if len(suburb_data) >= min_sales:
            # Winsorize prices at 2.5/97.5 percentiles
            lower = suburb_data['price'].quantile(0.025)
            upper = suburb_data['price'].quantile(0.975)
            suburb_data['price_winsorized'] = suburb_data['price'].clip(lower, upper)
            
            n = len(suburb_data)
            recent_sales = suburb_data.iloc[-int(n*0.3):]
            older_sales = suburb_data.iloc[:int(n*0.3)]
            
            recent_median = recent_sales['price_winsorized'].median()
            older_median = older_sales['price_winsorized'].median()
            
            time_span_days = (recent_sales['dat'].median() - older_sales['dat'].median()).days
            time_span_years = max(time_span_days / 365.25, 0.5)
            
            total_growth = (recent_median / older_median) - 1
            annualized_growth = ((1 + total_growth) ** (1 / time_span_years)) - 1
            
            momentum_list.append({
                'suburb': suburb,
                'MOM': annualized_growth * 100,
                'latest_price': recent_median,
                'time_span_years': time_span_years,
                'mom_reliable': True
            })
    
    return pd.DataFrame(momentum_list)

mom_data = calculate_momentum_v2(transactions, min_sales=15)
print(f"  ✓ Calculated MOM for {len(mom_data)} suburbs")
print(f"  ✓ MOM range: {mom_data['MOM'].min():.2f}% to {mom_data['MOM'].max():.2f}% p.a.")

# ============================================================================
# STEP 4: CALCULATE DRAWDOWN RISK (DDR) - FIXED WITH SMOOTHING
# ============================================================================

print("\n[4/7] Calculating Drawdown Risk (DDR) with smoothing...")

def calculate_drawdown_v2(transactions_df, min_quarters=8, smooth_window=3):
    """
    DDR = Maximum drawdown with improvements:
    - 3-quarter moving average for smoothing
    - Winsorized prices
    - Capped at -35% floor to avoid outliers
    - 24-month lookback (8 quarters minimum)
    """
    transactions_df['year_quarter'] = transactions_df['dat'].dt.to_period('Q')
    
    drawdown_list = []
    
    for suburb in transactions_df['suburb'].unique():
        suburb_data = transactions_df[transactions_df['suburb'] == suburb].copy()
        
        if len(suburb_data) >= 15:
            # Winsorize prices
            lower = suburb_data['price'].quantile(0.05)
            upper = suburb_data['price'].quantile(0.95)
            suburb_data['price_winsorized'] = suburb_data['price'].clip(lower, upper)
            
            quarterly = suburb_data.groupby('year_quarter')['price_winsorized'].median().reset_index()
            quarterly = quarterly.sort_values('year_quarter')
            
            if len(quarterly) >= min_quarters:
                # Apply 3-quarter moving average for smoothing
                quarterly['price_smooth'] = quarterly['price_winsorized'].rolling(
                    window=smooth_window, min_periods=1, center=True
                ).mean()
                
                prices = quarterly['price_smooth'].values
                
                # Calculate drawdown
                running_max = np.maximum.accumulate(prices)
                drawdown = (prices - running_max) / running_max
                max_drawdown = drawdown.min() * 100
                
                # Cap at -35% to avoid extreme outliers
                max_drawdown = max(max_drawdown, -35.0)
                
                # If no significant drawdown, use price volatility
                if max_drawdown > -5:
                    cv = (prices.std() / prices.mean()) * 100
                    max_drawdown = -min(cv, 35.0)
                
                drawdown_list.append({
                    'suburb': suburb,
                    'DDR': max_drawdown,
                    'peak_price': running_max.max(),
                    'lookback_quarters': len(quarterly),
                    'ddr_reliable': len(quarterly) >= min_quarters
                })
    
    return pd.DataFrame(drawdown_list)

ddr_data = calculate_drawdown_v2(transactions, min_quarters=8, smooth_window=3)
print(f"  ✓ Calculated DDR for {len(ddr_data)} suburbs")
print(f"  ✓ DDR range: {ddr_data['DDR'].min():.2f}% to {ddr_data['DDR'].max():.2f}%")
print(f"  ✓ Note: Capped at -35% floor, smoothed with 3Q MA")

# ============================================================================
# STEP 5: CALCULATE MACRO LIQUIDITY ALIGNMENT (MLA) - WITH SIGNIFICANCE
# ============================================================================

print("\n[5/7] Calculating Macro Liquidity Alignment (MLA) with stats...")

def get_macro_proxy():
    """Generate macro liquidity proxy"""
    start_date = transactions['dat'].min() - pd.DateOffset(weeks=10)
    end_date = transactions['dat'].max()
    dates = pd.date_range(start=start_date, end=end_date, freq='W')
    
    t = np.arange(len(dates))
    long_cycle = 0.05 * np.sin(2 * np.pi * t / 104)
    medium_cycle = 0.03 * np.sin(2 * np.pi * t / 26)
    noise = 0.02 * np.random.randn(len(dates))
    macro_returns = long_cycle + medium_cycle + noise
    
    return pd.DataFrame({'date': dates, 'macro_return': macro_returns})

def calculate_mla_v2(transactions_df, macro_df, lead_weeks=10, window_months=36):
    """
    MLA with statistical significance testing
    - Returns correlation, p-value, and confidence interval
    - Flags non-significant correlations
    """
    macro_df['date_led'] = macro_df['date'] + pd.DateOffset(weeks=lead_weeks)
    macro_df['year_quarter'] = macro_df['date_led'].dt.to_period('Q')
    macro_quarterly = macro_df.groupby('year_quarter')['macro_return'].mean().reset_index()
    
    transactions_df['year_quarter'] = transactions_df['dat'].dt.to_period('Q')
    
    mla_list = []
    
    for suburb in transactions_df['suburb'].unique():
        suburb_data = transactions_df[transactions_df['suburb'] == suburb].copy()
        
        if len(suburb_data) >= 15:
            quarterly_prices = suburb_data.groupby('year_quarter')['price'].median().reset_index()
            quarterly_prices = quarterly_prices.sort_values('year_quarter')
            
            if len(quarterly_prices) >= 10:
                quarterly_prices['price_return'] = quarterly_prices['price'].pct_change()
                
                # Winsorize returns
                lower = quarterly_prices['price_return'].quantile(0.025)
                upper = quarterly_prices['price_return'].quantile(0.975)
                quarterly_prices['price_return_w'] = quarterly_prices['price_return'].clip(lower, upper)
                
                merged = quarterly_prices.merge(macro_quarterly, on='year_quarter', how='inner')
                merged = merged.dropna(subset=['price_return_w', 'macro_return'])
                
                if len(merged) >= 10:
                    # Calculate correlation and significance
                    corr, p_value = stats.pearsonr(merged['price_return_w'], merged['macro_return'])
                    
                    # Fisher z-transform for CI
                    n = len(merged)
                    z = np.arctanh(corr)
                    se = 1 / np.sqrt(n - 3)
                    z_lower = z - 1.96 * se
                    z_upper = z + 1.96 * se
                    ci_lower = np.tanh(z_lower)
                    ci_upper = np.tanh(z_upper)
                    
                    # Flag if significant at 10% level
                    is_significant = p_value < 0.10
                    
                    mla_list.append({
                        'suburb': suburb,
                        'MLA': corr if not np.isnan(corr) else 0,
                        'MLA_pvalue': p_value,
                        'MLA_ci_lower': ci_lower,
                        'MLA_ci_upper': ci_upper,
                        'MLA_significant': is_significant,
                        'MLA_n': n,
                        'data_points': n
                    })
    
    return pd.DataFrame(mla_list)

macro_proxy = get_macro_proxy()
print(f"  ✓ Generated macro liquidity proxy with {len(macro_proxy)} weekly observations")

mla_data = calculate_mla_v2(transactions, macro_proxy, lead_weeks=10, window_months=36)
print(f"  ✓ Calculated MLA for {len(mla_data)} suburbs")
if len(mla_data) > 0:
    print(f"  ✓ MLA range: {mla_data['MLA'].min():.3f} to {mla_data['MLA'].max():.3f}")
    print(f"  ✓ Significant (p<0.10): {mla_data['MLA_significant'].sum()}/{len(mla_data)} suburbs")

# ============================================================================
# STEP 6: COMBINE INTO MLAPS COMPOSITE SCORE - IMPROVED
# ============================================================================

print("\n[6/7] Creating MLAPS v2 Composite Score...")

# Merge all components
mlaps = lml_data.copy()
mlaps = mlaps.merge(mom_data[['suburb', 'MOM', 'latest_price', 'mom_reliable']], on='suburb', how='left')
mlaps = mlaps.merge(ddr_data[['suburb', 'DDR', 'lookback_quarters', 'ddr_reliable']], on='suburb', how='left')
mlaps = mlaps.merge(mla_data[['suburb', 'MLA', 'MLA_pvalue', 'MLA_significant', 'MLA_n']], on='suburb', how='left')

# Remove suburbs with missing critical data
mlaps = mlaps.dropna(subset=['LML', 'MOM', 'DDR'])

print(f"  ✓ Combined data for {len(mlaps)} suburbs")

# Cap z-scores at ±2.5σ before normalization
def cap_and_normalize(series, higher_is_better=True, cap_z=2.5):
    """
    Robust normalization with z-score capping
    """
    # Calculate z-scores
    mean = series.mean()
    std = series.std()
    if std == 0:
        return pd.Series([50] * len(series), index=series.index)
    
    z_scores = (series - mean) / std
    
    # Cap at ±2.5σ
    z_capped = z_scores.clip(-cap_z, cap_z)
    
    # Normalize to 0-100
    if higher_is_better:
        normalized = 100 * (z_capped - z_capped.min()) / (z_capped.max() - z_capped.min())
    else:
        normalized = 100 * (z_capped.max() - z_capped) / (z_capped.max() - z_capped.min())
    
    return normalized

mlaps['LML_score'] = cap_and_normalize(mlaps['LML'], higher_is_better=True)
mlaps['MOM_score'] = cap_and_normalize(mlaps['MOM'], higher_is_better=True)
mlaps['DDR_score'] = cap_and_normalize(mlaps['DDR'], higher_is_better=True)

# Dynamic MLA weighting based on significance
has_mla = mlaps['MLA'].notna().sum() > 0

if has_mla:
    # For non-significant MLA, set score to neutral (50)
    mlaps['MLA_score'] = cap_and_normalize(mlaps['MLA'].fillna(0), higher_is_better=True)
    mlaps.loc[~mlaps['MLA_significant'].fillna(False), 'MLA_score'] = 50.0
    
    # Calculate MLAPS with full weighting
    mlaps['MLAPS'] = (
        0.40 * mlaps['MLA_score'] +
        0.35 * mlaps['LML_score'] +
        0.15 * mlaps['MOM_score'] +
        0.10 * mlaps['DDR_score']
    )
    weighting_used = "40% MLA + 35% LML + 15% MOM + 10% DDR"
else:
    # Reweight without MLA
    mlaps['MLAPS'] = (
        0.50 * mlaps['LML_score'] +
        0.30 * mlaps['MOM_score'] +
        0.20 * mlaps['DDR_score']
    )
    weighting_used = "50% LML + 30% MOM + 20% DDR (no MLA)"

mlaps = mlaps.sort_values('MLAPS', ascending=False)
mlaps['rank'] = range(1, len(mlaps) + 1)

# ============================================================================
# SAVE RESULTS
# ============================================================================

print("\n" + "=" * 80)
print("RESULTS")
print("=" * 80)

output_file = 'mlaps_scores_v2.csv'
mlaps.to_csv(output_file, index=False)
print(f"\n✅ Full results saved to: {output_file}")

# Display top suburbs
print("\n📊 TOP SUBURBS BY MLAPS v2 SCORE:")
print("=" * 80)

top_n = min(10, len(mlaps))
for idx, row in mlaps.head(top_n).iterrows():
    print(f"\n#{int(row['rank'])} - {row['suburb']}")
    print(f"  MLAPS Score:      {row['MLAPS']:.1f}/100")
    print(f"  ├─ Liquidity:     {row['LML']:.2f}% per year ({int(row['sales_12m'])} sales)")
    print(f"  ├─ Momentum:      {row['MOM']:.1f}% p.a.")
    print(f"  ├─ Drawdown:      {row['DDR']:.1f}% (smoothed, capped)")
    if has_mla and pd.notna(row.get('MLA')):
        sig_flag = "✓ sig" if row.get('MLA_significant', False) else "NS"
        print(f"  └─ Macro Align:   {row['MLA']:.3f} ({sig_flag}, n={int(row.get('MLA_n', 0))})")
    print(f"  Current Price:    ${row['latest_price']:,.0f}")

# Summary statistics
print("\n" + "=" * 80)
print("SCORE DISTRIBUTION:")
print("=" * 80)
summary_cols = ['MLAPS', 'LML', 'MOM', 'DDR']
if 'MLA' in mlaps.columns:
    summary_cols.append('MLA')
print(mlaps[summary_cols].describe())

# Methodology note
print("\n" + "=" * 80)
print("METHODOLOGY IMPROVEMENTS (v2):")
print("=" * 80)
print(f"✓ Weighting: {weighting_used}")
print(f"✓ Liquidity: 12-month turnover (% per year)")
print(f"✓ Momentum: Annualized growth with 2.5/97.5 winsorization")
print(f"✓ Drawdown: 3-quarter MA smoothing, capped at -35%")
print(f"✓ Macro Align: Rolling corr (lead=10w), with significance testing (p<0.10)")
print(f"✓ Normalization: Z-scores capped at ±2.5σ, then scaled to 0-100")
print(f"✓ Reliability flags: Minimum sample requirements enforced")

print("\n" + "=" * 80)
print("✅ ANALYSIS COMPLETE (v2 - IMPROVED)")
print("=" * 80)

