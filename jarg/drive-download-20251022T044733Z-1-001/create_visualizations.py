"""
Create visualizations for MLAPS analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load results
mlaps = pd.read_csv('mlaps_scores.csv')
mlaps = mlaps.sort_values('MLAPS', ascending=False)

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (16, 12)
plt.rcParams['font.size'] = 10

# Create comprehensive visualization
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 2, hspace=0.35, wspace=0.3)

# 1. MLAPS Rankings
ax1 = fig.add_subplot(gs[0, :])
colors = plt.cm.RdYlGn(mlaps['MLAPS'] / 100)
bars = ax1.barh(mlaps['suburb'], mlaps['MLAPS'], color=colors, edgecolor='black', linewidth=1.5)
ax1.set_xlabel('MLAPS Score (0-100)', fontsize=12, fontweight='bold')
ax1.set_title('MLAPS Rankings: Which Suburbs Offer Best Risk-Adjusted, Cycle-Aware Returns?', 
              fontsize=14, fontweight='bold')
ax1.grid(axis='x', alpha=0.3)
ax1.set_xlim(0, 100)
for i, (idx, row) in enumerate(mlaps.iterrows()):
    ax1.text(row['MLAPS'] + 2, i, f"{row['MLAPS']:.1f}", va='center', fontweight='bold', fontsize=11)

# 2. Component Breakdown
ax2 = fig.add_subplot(gs[1, 0])
components_data = mlaps[['suburb', 'MLA_score', 'LML_score', 'MOM_score', 'DDR_score']].set_index('suburb')
weights = {'MLA_score': 0.40, 'LML_score': 0.35, 'MOM_score': 0.15, 'DDR_score': 0.10}
weighted_components = components_data * pd.Series(weights)

labels = ['Macro Align (40%)', 'Liquidity (35%)', 'Momentum (15%)', 'Risk (10%)']
colors_comp = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']

bottom = np.zeros(len(weighted_components))
for i, (col, label, color) in enumerate(zip(weighted_components.columns, labels, colors_comp)):
    ax2.barh(weighted_components.index, weighted_components[col], 
             left=bottom, label=label, color=color, edgecolor='black', linewidth=0.5)
    bottom += weighted_components[col].values

ax2.set_xlabel('Weighted Component Contribution', fontsize=11, fontweight='bold')
ax2.set_title('What Drives Each Suburb\'s MLAPS Score?', fontsize=13, fontweight='bold')
ax2.legend(loc='lower right', fontsize=10, framealpha=0.9)
ax2.grid(axis='x', alpha=0.3)

# 3. Scatter: Liquidity vs Momentum
ax3 = fig.add_subplot(gs[1, 1])
scatter = ax3.scatter(mlaps['LML'], mlaps['MOM'], s=mlaps['MLAPS']*8, 
                      c=mlaps['MLAPS'], cmap='RdYlGn', alpha=0.7, edgecolor='black', linewidth=2)
ax3.set_xlabel('Local Market Liquidity (% annual turnover)', fontsize=11, fontweight='bold')
ax3.set_ylabel('Price Momentum (% per annum)', fontsize=11, fontweight='bold')
ax3.set_title('Liquidity vs Growth (bubble size = MLAPS)', fontsize=13, fontweight='bold')
ax3.grid(True, alpha=0.3)
for idx, row in mlaps.iterrows():
    ax3.annotate(row['suburb'], (row['LML'], row['MOM']), 
                fontsize=9, ha='center', va='bottom', fontweight='bold')
cbar = plt.colorbar(scatter, ax=ax3)
cbar.set_label('MLAPS Score', fontsize=10, fontweight='bold')

# 4. Risk vs Return
ax4 = fig.add_subplot(gs[2, 0])
scatter2 = ax4.scatter(mlaps['DDR'], mlaps['MOM'], s=mlaps['LML']*1500,
                       c=mlaps['MLA'], cmap='coolwarm', alpha=0.7, edgecolor='black', linewidth=2)
ax4.set_xlabel('Drawdown Risk (% max decline)', fontsize=11, fontweight='bold')
ax4.set_ylabel('Price Momentum (% p.a.)', fontsize=11, fontweight='bold')
ax4.set_title('Risk vs Return (bubble = liquidity, color = macro alignment)', 
              fontsize=13, fontweight='bold')
ax4.grid(True, alpha=0.3)
ax4.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
for idx, row in mlaps.iterrows():
    ax4.annotate(row['suburb'], (row['DDR'], row['MOM']), 
                fontsize=9, ha='center', va='bottom', fontweight='bold')
cbar2 = plt.colorbar(scatter2, ax=ax4)
cbar2.set_label('Macro Alignment', fontsize=10, fontweight='bold')

# 5. Price Accessibility vs MLAPS
ax5 = fig.add_subplot(gs[2, 1])
colors_price = ['#2ecc71' if p < 2000000 else '#f39c12' if p < 2500000 else '#e74c3c' 
                for p in mlaps['latest_price']]
bars2 = ax5.barh(mlaps['suburb'], mlaps['latest_price']/1000000, 
                color=colors_price, alpha=0.7, edgecolor='black', linewidth=1.5)
ax5.set_xlabel('Median Price ($M)', fontsize=11, fontweight='bold')
ax5.set_title('Price Levels by Suburb', fontsize=13, fontweight='bold')
ax5.grid(axis='x', alpha=0.3)
for i, (idx, row) in enumerate(mlaps.iterrows()):
    ax5.text(row['latest_price']/1000000 + 0.1, i, 
            f"${row['latest_price']/1000000:.2f}M\n(#{row['rank']})", 
            va='center', fontsize=9, fontweight='bold')

plt.suptitle('MLAPS: Macro-Liquidity Aligned Property Score - Full Analysis', 
             fontsize=16, fontweight='bold', y=0.995)

# Add footer
fig.text(0.5, 0.01, 
         'MLAPS = 40% Macro Alignment + 35% Liquidity + 15% Momentum + 10% Risk Protection | Microburbs Assessment October 2025',
         ha='center', fontsize=9, style='italic', color='gray')

plt.savefig('mlaps_visualization.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Visualization saved to mlaps_visualization.png")

# Create simple summary table image
fig2, ax = plt.subplots(figsize=(12, 6))
ax.axis('tight')
ax.axis('off')

# Prepare table data
table_data = []
table_data.append(['Rank', 'Suburb', 'MLAPS', 'Liquidity', 'Momentum', 'Risk', 'Macro\nAlign', 'Price'])
for idx, row in mlaps.iterrows():
    table_data.append([
        f"#{int(row['rank'])}",
        row['suburb'],
        f"{row['MLAPS']:.1f}",
        f"{row['LML']:.2f}%",
        f"{row['MOM']:.1f}%",
        f"{row['DDR']:.1f}%",
        f"{row['MLA']:.3f}" if pd.notna(row['MLA']) else 'N/A',
        f"${row['latest_price']/1000:.0f}k"
    ])

table = ax.table(cellText=table_data, cellLoc='center', loc='center', 
                colWidths=[0.08, 0.18, 0.10, 0.12, 0.12, 0.10, 0.12, 0.12])
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2.5)

# Style header row
for i in range(8):
    cell = table[(0, i)]
    cell.set_facecolor('#2c3e50')
    cell.set_text_props(weight='bold', color='white')

# Style data rows
for i in range(1, len(table_data)):
    for j in range(8):
        cell = table[(i, j)]
        if i % 2 == 0:
            cell.set_facecolor('#ecf0f1')
        else:
            cell.set_facecolor('white')
        
        # Color rank column
        if j == 0:
            if i <= 1:
                cell.set_facecolor('#f39c12')
                cell.set_text_props(weight='bold', color='white')
            elif i <= 3:
                cell.set_facecolor('#95a5a6')
                cell.set_text_props(weight='bold')

plt.title('MLAPS Suburb Rankings - Complete Scorecard', 
          fontsize=14, fontweight='bold', pad=20)

plt.savefig('mlaps_table.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Table saved to mlaps_table.png")

print("\n✅ All visualizations created successfully!")
plt.show()

