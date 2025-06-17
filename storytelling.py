import cohere
import os
from typing import Dict

# === Load API Key from Environment Variable ===
cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise EnvironmentError("❌ COHERE_API_KEY not set in environment variables.")

co = cohere.Client(cohere_api_key)

def generate_story(sim_result: Dict) -> str:
    """
    Generate a fictional climate impact story based on simulation results.

    Args:
        sim_result (Dict): Dictionary with total_emissions, breakdown, projection, green_score

    Returns:
        str: Generated narrative story from Cohere
    """
    total = sim_result["total_emissions"]
    breakdown = sim_result["breakdown"]
    projection = sim_result["projection"]

    prompt = f"""
    You are an AI climate storyteller. Write a compelling, fictional narrative describing the environmental impact of a person
    whose annual CO₂ emissions are {total} kg/year.

    Break down their carbon footprint as follows:
    - Meat: {breakdown.get('Eat Meat Daily', 0)} kg
    - Commute: {breakdown.get('Commute', 0)} kg
    - Plastic: {breakdown.get('Plastic Use', 0)} kg
    - Energy: {breakdown.get('Energy', 0)} kg

    Project their emissions into the future:
    - 2035 = {projection.get(2035, 0)} kg
    - 2050 = {projection.get(2050, 0)} kg
    - 2075 = {projection.get(2075, 0)} kg

    Describe what the world might look like then. Include fictional news headlines and tell a human story behind these emissions.
    """

    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=500,
        temperature=0.8
    )

    return response.generations[0].text.strip()