from src.analysis.lap_analysis import load_race_session
from src.analysis.telemetry_analysis import get_fastest_lap_telemetry


# Load the race session
session = load_race_session(
    2024,
    "Italian Grand Prix",
    "R"
)

# Get telemetry for Leclerc's fastest lap
telemetry = get_fastest_lap_telemetry(
    session,
    "LEC"
)

# Check the result
if telemetry is not None:
    print("Telemetry loaded successfully!\n")

    print("Available columns:")
    print(telemetry.columns.tolist())

    print("\nFirst 5 telemetry records:")
    print(telemetry.head())
else:
    print("No telemetry data found.")