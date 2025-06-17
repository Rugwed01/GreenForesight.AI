import pandas as pd
import os

# === Load Emission Table ===
csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "emissions_table.csv")
emissions_df = pd.read_csv(csv_path)
emissions_df.columns = emissions_df.columns.str.strip().str.replace('\ufeff', '')

# Confirm structure
assert 'Activity' in emissions_df.columns and 'Option' in emissions_df.columns, "❌ Required columns not found!"

# === New CHOICE_MAP with (Activity, Option) pairs ===
CHOICE_MAP = {
    "Meat": {
        "Yes": ("Meat", "Meat daily"),
        "No": ("Meat", "No meat"),
        "Occasionally": ("Meat", "Occasional meat")
    },
    "Transport": {
        "Car": ("Transport", "Car"),
        "Public Transport": ("Transport", "Public Transport"),
        "Bike/Walk": ("Transport", "Cycle/Walk"),
        "Electric Vehicle": ("Transport", "Electric Vehicle")
    },
    "Plastic": {
        "Frequently": ("Plastic", "Frequent"),
        "Rarely": ("Plastic", "Rare"),
        "Never": ("Plastic", "Never")
    },
    "Energy": {
        "Coal-based": ("Energy", "Coal"),
        "Mixed": ("Energy", "Mixed"),
        "Solar/Renewable": ("Energy", "Solar")
    },
    "Flights": {
        "Frequent": ("Flights", "Frequent"),
        "Occasional": ("Flights", "Occasional"),
        "Never": ("Flights", "None")
    },
    "Water": {
        "High": ("Water", "High"),
        "Moderate": ("Water", "Moderate"),
        "Low": ("Water", "Low")
    },
    "Shopping": {
        "Often": ("Shopping", "Often"),
        "Sometimes": ("Shopping", "Sometimes"),
        "Never": ("Shopping", "Never")
    }
}

# === Updated Simulation Logic ===
def simulate_impact(meat, transport, plastic, energy, flights, water, shopping):
    user_inputs = {
        "Meat": CHOICE_MAP["Meat"].get(meat),
        "Transport": CHOICE_MAP["Transport"].get(transport),
        "Plastic": CHOICE_MAP["Plastic"].get(plastic),
        "Energy": CHOICE_MAP["Energy"].get(energy),
        "Flights": CHOICE_MAP["Flights"].get(flights),
        "Water": CHOICE_MAP["Water"].get(water),
        "Shopping": CHOICE_MAP["Shopping"].get(shopping),
    }

    total_annual_emissions = 0
    total_green_score = 0
    count_green_score = 0
    breakdown = {}

    for label, (activity, option) in user_inputs.items():
        row = emissions_df[
            (emissions_df["Activity"] == activity) &
            (emissions_df["Option"] == option)
        ]
        if not row.empty:
            try:
                co2 = int(float(row["CO2_kg_per_year"].values[0]))
            except Exception as e:
                print(f"⚠️ Could not convert CO₂ for {activity}-{option}: {e}")
                co2 = 0

            try:
                green = int(float(row["Green_Score"].values[0]))
                total_green_score += green
                count_green_score += 1
            except Exception as e:
                print(f"⚠️ Could not convert Green Score for {activity}-{option}: {e}")
        else:
            print(f"⚠️ No match found for {activity} - {option}")
            co2 = 0

        total_annual_emissions += co2
        breakdown[label] = co2

    # ✅ Average Green Score
    green_score = total_green_score // count_green_score if count_green_score else 0

    yearly_projection = {
        2035: total_annual_emissions * 10,
        2050: total_annual_emissions * 25,
        2075: total_annual_emissions * 50,
    }

    return {
        "total_emissions": total_annual_emissions,
        "green_score": green_score,
        "breakdown": breakdown,
        "projection": yearly_projection
    }