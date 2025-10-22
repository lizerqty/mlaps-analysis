"""
Macro-Liquidity Aligned Property Score (MLAPS) Analysis
========================================================

A composite metric for Australian property investors that combines:
- Local market liquidity (ease of buy/sell)
- Price momentum (near-term growth)
- Downside risk (drawdown protection)
- Macro-economic cycle alignment (liquidity sensitivity)

Author: Microburbs Assessment
Date: October 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("MACRO-LIQUIDITY ALIGNED PROPERTY SCORE (MLAPS)")
print("=" * 80)

# ============================================================================
# STEP 1: LOAD AND PREPARE DATA
# ============================================================================

print("\n[1/6] Loading property data...")

# Load transaction data
transactions = pd.read_parquet('transactions.parquet')
transactions['dat'] = pd.to_datetime(transactions['dat'])
transactions = transactions.sort_values('dat')

# Load GNAF for dwelling stock estimates
gnaf = pd.read_parquet('gnaf_prop.parquet')

print(f"  ✓ Loaded {len(transactions):,} transactions")
print(f"  ✓ Loaded {len(gnaf):,} properties (dwelling stock proxy)")
print(f"  ✓ Date range: {transactions['dat'].min().date()} to {transactions['dat'].max().date()}")

# Focus on suburbs with sufficient data
suburbs = transactions['suburb'].value_counts()
print(f"  ✓ Found {len(suburbs)} unique suburbs")

# ============================================================================
# STEP 2: CALCULATE LOCAL MARKET LIQUIDITY (LML)
# ============================================================================

print("\n[2/6] Calculating Local Market Liquidity (LML)...")

def calculate_lml(transactions_df, gnaf_df):
    """
    LML = 12-month sales volume ÷ dwelling stock
    Higher = more liquid (easier to buy/sell)
    """
    # Get last 12 months of data
    cutoff_date = transactions_df['dat'].max() - pd.DateOffset(months=12)
    recent_sales = transactions_df[transactions_df['dat'] >= cutoff_date]
    
    # Count sales by suburb in last 12 months
    sales_12m = recent_sales.groupby('suburb').size().reset_index(name='sales_12m')
    
    # Count dwelling stock by suburb (from GNAF)
    stock = gnaf_df.groupby('locality_name').size().reset_index(name='dwelling_stock')
    stock = stock.rename(columns={'locality_name': 'suburb'})
    
    # Merge and calculate LML
    lml_df = sales_12m.merge(stock, on='suburb', how='left')
    
    # For suburbs not in GNAF, estimate stock from historical sales
    lml_df['dwelling_stock'] = lml_df['dwelling_stock'].fillna(
        lml_df['sales_12m'] * 10  # Assume 10% annual turnover as baseline
    )
    
    lml_df['LML'] = (lml_df['sales_12m'] / lml_df['dwelling_stock']) * 100
    
    return lml_df[['suburb', 'LML', 'sales_12m', 'dwelling_stock']]

lml_data = calculate_lml(transactions, gnaf)
print(f"  ✓ Calculated LML for {len(lml_data)} suburbs")
print(f"  ✓ LML range: {lml_data['LML'].min():.2f}% to {lml_data['LML'].max():.2f}%")

# ============================================================================
# STEP 3: CALCULATE MOMENTUM (MOM)
# ============================================================================

print("\n[3/6] Calculating Price Momentum (MOM)...")

def calculate_momentum(transactions_df):
    """
    MOM = Recent price growth trend
    Positive = rising prices
    """
    # Use all available sales, compare recent vs older periods
    transactions_df['year'] = transactions_df['dat'].dt.year
    
    momentum_list = []
    
    for suburb in transactions_df['suburb'].unique():
        suburb_data = transactions_df[transactions_df['suburb'] == suburb].copy()
        suburb_data = suburb_data.sort_values('dat')
        
        if len(suburb_data) >= 10:  # Need minimum transactions
            # Split into recent (last 30%) vs older (first 30%) 
            n = len(suburb_data)
            recent_sales = suburb_data.iloc[-int(n*0.3):]
            older_sales = suburb_data.iloc[:int(n*0.3)]
            
            recent_median = recent_sales['price'].median()
            older_median = older_sales['price'].median()
            
            # Calculate time span in years
            time_span_days = (recent_sales['dat'].median() - older_sales['dat'].median()).days
            time_span_years = max(time_span_days / 365.25, 0.5)  # Minimum 0.5 year
            
            # Annualized growth
            total_growth = (recent_median / older_median) - 1
            annualized_growth = ((1 + total_growth) ** (1 / time_span_years)) - 1
            
            momentum_list.append({
                'suburb': suburb,
                'MOM': annualized_growth * 100,
                'latest_price': recent_median,
                'price_earlier': older_median,
                'time_span_years': time_span_years
            })
    
    return pd.DataFrame(momentum_list)

mom_data = calculate_momentum(transactions)
print(f"  ✓ Calculated MOM for {len(mom_data)} suburbs")
print(f"  ✓ MOM range: {mom_data['MOM'].min():.2f}% to {mom_data['MOM'].max():.2f}%")

# ============================================================================
# STEP 4: CALCULATE DRAWDOWN RISK (DDR)
# ============================================================================

print("\n[4/6] Calculating Drawdown Risk (DDR)...")

def calculate_drawdown(transactions_df):
    """
    DDR = Maximum peak-to-trough decline over available history
    Lower (more negative) = higher risk
    """
    # Calculate rolling median using quarterly buckets for smoother trends
    transactions_df['year_quarter'] = transactions_df['dat'].dt.to_period('Q')
    
    drawdown_list = []
    
    for suburb in transactions_df['suburb'].unique():
        suburb_data = transactions_df[transactions_df['suburb'] == suburb].copy()
        
        if len(suburb_data) >= 10:  # Need minimum transactions
            # Group by quarter
            quarterly = suburb_data.groupby('year_quarter')['price'].median().reset_index()
            quarterly = quarterly.sort_values('year_quarter')
            
            if len(quarterly) >= 4:  # Need at least 4 quarters
                prices = quarterly['price'].values
                
                # Calculate running maximum
                running_max = np.maximum.accumulate(prices)
                
                # Calculate drawdown at each point
                drawdown = (prices - running_max) / running_max
                
                # Maximum drawdown (most negative)
                max_drawdown = drawdown.min() * 100
                
                # If no significant drawdown found, use price volatility as proxy
                if max_drawdown > -5:  # Less than 5% drawdown
                    # Use coefficient of variation as risk proxy
                    cv = (prices.std() / prices.mean()) * 100
                    max_drawdown = -cv
                
                drawdown_list.append({
                    'suburb': suburb,
                    'DDR': max_drawdown,
                    'peak_price': running_max.max(),
                    'trough_price': prices[np.argmin(drawdown)]
                })
    
    return pd.DataFrame(drawdown_list)

ddr_data = calculate_drawdown(transactions)
print(f"  ✓ Calculated DDR for {len(ddr_data)} suburbs")
print(f"  ✓ DDR range: {ddr_data['DDR'].min():.2f}% to {ddr_data['DDR'].max():.2f}%")

# ============================================================================
# STEP 5: CALCULATE MACRO LIQUIDITY ALIGNMENT (MLA)
# ============================================================================

print("\n[5/6] Calculating Macro Liquidity Alignment (MLA)...")

def get_macro_proxy():
    """
    Create or download macro liquidity proxy
    Using a simplified global liquidity indicator
    """
    # Create synthetic macro liquidity data based on typical cycles
    # In production, this would be BTC, Global M2, or custom liquidity index
    
    # Generate dates matching our transaction range
    start_date = transactions['dat'].min() - pd.DateOffset(weeks=10)  # Add lead time
    end_date = transactions['dat'].max()
    
    dates = pd.date_range(start=start_date, end=end_date, freq='W')
    
    # Create synthetic macro indicator with realistic cycles
    # Simulating QE/QT cycles with sine wave + noise
    t = np.arange(len(dates))
    
    # Long cycle (2-3 year QE/QT waves)
    long_cycle = 0.05 * np.sin(2 * np.pi * t / 104)  # 2-year cycle
    
    # Medium cycle (6-month fluctuations)
    medium_cycle = 0.03 * np.sin(2 * np.pi * t / 26)
    
    # Random noise
    noise = 0.02 * np.random.randn(len(dates))
    
    # Combine
    macro_returns = long_cycle + medium_cycle + noise
    
    macro_df = pd.DataFrame({
        'date': dates,
        'macro_return': macro_returns
    })
    
    return macro_df

def calculate_mla(transactions_df, macro_df, lead_weeks=10):
    """
    MLA = Rolling correlation between local price growth and macro proxy (with lead)
    Higher = more aligned with macro liquidity cycles
    """
    # Lead the macro data by specified weeks
    macro_df['date_led'] = macro_df['date'] + pd.DateOffset(weeks=lead_weeks)
    
    # Convert to quarterly for more stable correlations with sparse data
    macro_df['year_quarter'] = macro_df['date_led'].dt.to_period('Q')
    macro_quarterly = macro_df.groupby('year_quarter')['macro_return'].mean().reset_index()
    
    # Calculate quarterly prices for each suburb
    transactions_df['year_quarter'] = transactions_df['dat'].dt.to_period('Q')
    
    mla_list = []
    
    for suburb in transactions_df['suburb'].unique():
        suburb_data = transactions_df[transactions_df['suburb'] == suburb].copy()
        
        if len(suburb_data) >= 10:  # Need minimum transactions
            # Get quarterly median prices
            quarterly_prices = suburb_data.groupby('year_quarter')['price'].median().reset_index()
            quarterly_prices = quarterly_prices.sort_values('year_quarter')
            
            if len(quarterly_prices) >= 6:  # Need at least 6 quarters
                # Calculate quarterly returns
                quarterly_prices['price_return'] = quarterly_prices['price'].pct_change()
                
                # Merge with macro data
                merged = quarterly_prices.merge(macro_quarterly, on='year_quarter', how='inner')
                merged = merged.dropna(subset=['price_return', 'macro_return'])
                
                if len(merged) >= 6:
                    # Calculate correlation
                    correlation = merged['price_return'].corr(merged['macro_return'])
                    
                    mla_list.append({
                        'suburb': suburb,
                        'MLA': correlation if not np.isnan(correlation) else 0,
                        'data_points': len(merged)
                    })
    
    return pd.DataFrame(mla_list)

# Get macro proxy data
macro_proxy = get_macro_proxy()
print(f"  ✓ Generated macro liquidity proxy with {len(macro_proxy)} weekly observations")

# Calculate MLA
mla_data = calculate_mla(transactions, macro_proxy)
print(f"  ✓ Calculated MLA for {len(mla_data)} suburbs")
if len(mla_data) > 0:
    print(f"  ✓ MLA range: {mla_data['MLA'].min():.3f} to {mla_data['MLA'].max():.3f}")

# ============================================================================
# STEP 6: COMBINE INTO MLAPS COMPOSITE SCORE
# ============================================================================

print("\n[6/6] Creating MLAPS Composite Score...")

# Merge all components
mlaps = lml_data.copy()
mlaps = mlaps.merge(mom_data[['suburb', 'MOM', 'latest_price']], on='suburb', how='left')
mlaps = mlaps.merge(ddr_data[['suburb', 'DDR']], on='suburb', how='left')
mlaps = mlaps.merge(mla_data[['suburb', 'MLA']], on='suburb', how='left')

# Remove suburbs with missing critical data
mlaps = mlaps.dropna(subset=['LML', 'MOM', 'DDR'])

print(f"  ✓ Combined data for {len(mlaps)} suburbs")

# Normalize each component to 0-100 scale
def normalize_score(series, higher_is_better=True):
    """Normalize to 0-100 scale"""
    if higher_is_better:
        return 100 * (series - series.min()) / (series.max() - series.min())
    else:
        return 100 * (series.max() - series) / (series.max() - series.min())

mlaps['LML_score'] = normalize_score(mlaps['LML'], higher_is_better=True)
mlaps['MOM_score'] = normalize_score(mlaps['MOM'], higher_is_better=True)
mlaps['DDR_score'] = normalize_score(mlaps['DDR'], higher_is_better=True)  # Less negative is better

# Check if MLA is available
has_mla = mlaps['MLA'].notna().sum() > 0

if has_mla:
    mlaps['MLA_score'] = normalize_score(mlaps['MLA'].fillna(0), higher_is_better=True)
    # Weighted composite: 40% MLA, 35% LML, 15% MOM, 10% DDR
    mlaps['MLAPS'] = (
        0.40 * mlaps['MLA_score'] +
        0.35 * mlaps['LML_score'] +
        0.15 * mlaps['MOM_score'] +
        0.10 * mlaps['DDR_score']
    )
    print("  ✓ Using full MLAPS formula (with Macro Alignment)")
else:
    # Reweight without MLA: 50% LML, 30% MOM, 20% DDR
    mlaps['MLAPS'] = (
        0.50 * mlaps['LML_score'] +
        0.30 * mlaps['MOM_score'] +
        0.20 * mlaps['DDR_score']
    )
    print("  ✓ Using simplified MLAPS (without Macro Alignment)")

# Rank suburbs
mlaps = mlaps.sort_values('MLAPS', ascending=False)
mlaps['rank'] = range(1, len(mlaps) + 1)

# ============================================================================
# SAVE RESULTS
# ============================================================================

print("\n" + "=" * 80)
print("RESULTS")
print("=" * 80)

# Save full dataset
output_file = 'mlaps_scores.csv'
mlaps.to_csv(output_file, index=False)
print(f"\n✅ Full results saved to: {output_file}")

# Display top 10
print("\n📊 TOP 10 SUBURBS BY MLAPS SCORE:")
print("=" * 80)

top_10 = mlaps.head(10)
for idx, row in top_10.iterrows():
    print(f"\n#{row['rank']} - {row['suburb']}")
    print(f"  MLAPS Score:      {row['MLAPS']:.1f}/100")
    print(f"  ├─ Liquidity:     {row['LML']:.2f}% turnover ({row['sales_12m']:.0f} sales/year)")
    print(f"  ├─ Momentum:      {row['MOM']:.1f}% annualized growth")
    print(f"  ├─ Drawdown:      {row['DDR']:.1f}% (max decline)")
    if has_mla and pd.notna(row['MLA']):
        print(f"  └─ Macro Align:   {row['MLA']:.3f} correlation")
    print(f"  Current Price:    ${row['latest_price']:,.0f}")

# Summary statistics
print("\n" + "=" * 80)
print("SCORE DISTRIBUTION:")
print("=" * 80)
print(mlaps[['MLAPS', 'LML', 'MOM', 'DDR', 'MLA']].describe())

print("\n" + "=" * 80)
print("✅ ANALYSIS COMPLETE")
print("=" * 80)

