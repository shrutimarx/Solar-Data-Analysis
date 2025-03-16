import requests
import pandas as pd
from pyproj import Transformer


# File paths
input_file = "YOUR INPUT FILE. e.g. Atlanta_Fire_Stations.csv"
output_file = "YOUR OUTPUT FILE"

# Load CSV file
df = pd.read_csv(input_file)

# Transform X, Y to Latitude, Longitude
transformer = Transformer.from_crs("EPSG:2240", "EPSG:4326", always_xy=True)
df["Longitude"], df["Latitude"] = transformer.transform(df["X"].values, df["Y"].values)

# Google Solar API Key 
API_KEY = "YOUR API KEY"

# API Base URL
BASE_URL = "https://solar.googleapis.com/v1/buildingInsights:findClosest?location.latitude={}&location.longitude={}&requiredQuality=HIGH&key={}"

# Create empty columns for solar data
df["solar_max_panels"] = None
df["solar_max_area_m2"] = None
df["solar_max_sunshine_hours"] = None

# Loop through each row and fetch solar potential data
for index, row in df.iterrows():
    url = BASE_URL.format(row["Latitude"], row["Longitude"], API_KEY)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        solar_potential = data.get("solarPotential", {})

        # Extract relevant data
        df.at[index, "solar_max_panels"] = solar_potential.get("maxArrayPanelsCount", None)
        df.at[index, "solar_max_area_m2"] = solar_potential.get("maxArrayAreaMeters2", None)
        df.at[index, "solar_max_sunshine_hours"] = solar_potential.get("maxSunshineHoursPerYear", None)

        print(f"Processed Station {index + 1}: Solar Data Retrieved ✅")
    else:
        print(f"Error for Station {index + 1}: {response.status_code}")


# Create a financial analysis DataFrame
financial_df = df[["Name", "Latitude", "Longitude", "solar_max_panels"]].copy()

# These are just industry estimates

COST_PER_PANEL = 300  # Average cost per panel ($)
PANEL_WATTAGE = 400  # Average wattage per panel (W)
HOURS_PER_YEAR = 1561  # Approximate annual sunshine hours
ENERGY_COST_PER_KWH = 0.13  # Average electricity cost per kWh ($)
EFFICIENCY = 0.20  # 20% panel efficiency

# Calculate financial metrics
financial_df["installation_cost"] = financial_df["solar_max_panels"] * COST_PER_PANEL
financial_df["annual_energy_production_kwh"] = (financial_df["solar_max_panels"] * PANEL_WATTAGE * HOURS_PER_YEAR * EFFICIENCY) / 1000
financial_df["annual_savings"] = financial_df["annual_energy_production_kwh"] * ENERGY_COST_PER_KWH
financial_df["payback_period_years"] = financial_df["installation_cost"] / financial_df["annual_savings"]


# Merge the financial_df with the original df
df = pd.merge(df, financial_df, on=["Name", "Latitude", "Longitude"], how="left")

df.to_csv(output_file, index=False)

print(f"\n✅ Data with solar and financial analysis saved to {output_file}")


