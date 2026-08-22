from src.analysis.lap_analysis import (
    load_race_session,
    get_driver_laps
)

from src.visualization.lap_charts import (
    create_lap_time_chart
)

from src.dashboard import main


if __name__ == "__main__":
    main()

# Load session
session = load_race_session(
    2024,
    "Monza",
    "R"
)

# Drivers
driver_1 = "LEC"
driver_2 = "PIA"

# Get lap data
laps_1 = get_driver_laps(session, driver_1)
laps_2 = get_driver_laps(session, driver_2)

# Create chart
driver_data = {
    driver_1: laps_1,
    driver_2: laps_2
}

fig = create_lap_time_chart(driver_data)

# Save chart
fig.write_html("lap_time_comparison.html")

print("Chart created successfully!")