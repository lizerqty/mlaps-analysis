import geopandas as gpd
import pandas as pd

print("=" * 80)
print("EXPLORING DATA FILES")
print("=" * 80)

# Read PARQUET files
print("\n### 1. GNAF PROPERTIES ###")
try:
    gnaf = pd.read_parquet('gnaf_prop.parquet')
    print(f"Rows: {len(gnaf):,}")
    print(f"Columns: {list(gnaf.columns)}")
    print("\nFirst few rows:")
    print(gnaf.head())
    print("\nData types:")
    print(gnaf.dtypes)
    print("\nSample record:")
    print(gnaf.iloc[0])
except Exception as e:
    print(f"Error reading gnaf_prop.parquet: {e}")

print("\n" + "=" * 80)
print("\n### 2. TRANSACTIONS ###")
try:
    transactions = pd.read_parquet('transactions.parquet')
    print(f"Rows: {len(transactions):,}")
    print(f"Columns: {list(transactions.columns)}")
    print("\nFirst few rows:")
    print(transactions.head())
    print("\nData types:")
    print(transactions.dtypes)
    if len(transactions) > 0:
        print("\nSample record:")
        print(transactions.iloc[0])
except Exception as e:
    print(f"Error reading transactions.parquet: {e}")

print("\n" + "=" * 80)
print("\n### 3. CADASTRE (Property Boundaries) ###")
try:
    cadastre = gpd.read_file('cadastre.gpkg')
    print(f"Rows: {len(cadastre):,}")
    print(f"Columns: {list(cadastre.columns)}")
    print(f"CRS: {cadastre.crs}")
    print("\nFirst few rows:")
    print(cadastre.head())
    print("\nData types:")
    print(cadastre.dtypes)
    if len(cadastre) > 0:
        print("\nSample record:")
        print(cadastre.iloc[0])
        print("\nGeometry type:")
        print(cadastre.geometry.geom_type.value_counts())
except Exception as e:
    print(f"Error reading cadastre.gpkg: {e}")

print("\n" + "=" * 80)
print("\n### 4. ROADS ###")
try:
    roads = gpd.read_file('roads.gpkg')
    print(f"Rows: {len(roads):,}")
    print(f"Columns: {list(roads.columns)}")
    print(f"CRS: {roads.crs}")
    print("\nFirst few rows:")
    print(roads.head())
    if len(roads) > 0:
        print("\nGeometry type:")
        print(roads.geometry.geom_type.value_counts())
except Exception as e:
    print(f"Error reading roads.gpkg: {e}")

print("\n" + "=" * 80)
print("EXPLORATION COMPLETE")
print("=" * 80)

