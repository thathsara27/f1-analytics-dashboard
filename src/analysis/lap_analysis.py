import fastf1
import streamlit as st

@st.cache_resource

def load_race_session(year, grand_pix, session_name):
    """Load an F1 session using FastF1."""
    session = fastf1.get_session(year, grand_pix, session_name)
    session.load()

    return session

def get_driver_laps(session, driver):
    """Return clean lap data for a specific driver."""

    laps = session.laps.pick_drivers(driver).copy()

    # Remove laps without a valid laptime
    laps = laps.dropna(subset=["LapTime"])

    # Convert lap time to seconds
    laps["LapTimeSeconds"] = laps["LapTime"].dt.total_seconds()

    return laps

def get_race_summary(session):
    """Calculate basic race summary statistics."""

    laps = session.laps.copy()

    # Remove laps without lap numbers
    valid_laps = laps.dropna(subset=["LapNumber"])

    # Total race laps
    total_laps = int(valid_laps["LapNumber"].max())

    # Number of drivers
    driver_count = valid_laps["Driver"].nunique()

    # Fastest valid lap
    fastest_lap = valid_laps.dropna(subset=["LapTime"]).nsmallest(
        1,
        "LapTime"
    )

    if not fastest_lap.empty:
        fastest_driver = fastest_lap.iloc[0]["Driver"]
        fastest_time = fastest_lap.iloc[0]["LapTime"]
    else:
        fastest_driver = "N/A"
        fastest_time = None

    # Race winner
    # The final recorded position of each driver is used.
    final_positions = (
        valid_laps
        .dropna(subset=["Position"])
        .sort_values("LapNumber")
        .groupby("Driver")
        .tail(1)
    )

    winner = "N/A"

    if not final_positions.empty:
        winner_row = final_positions.sort_values("Position").iloc[0]
        winner = winner_row["Driver"]

    return {
        "winner": winner,
        "fastest_driver": fastest_driver,
        "fastest_time": fastest_time,
        "total_laps": total_laps,
        "driver_count": driver_count
    }

def get_driver_performance(laps):
    """Calculate performance statistics for a driver."""

    # Keep only accurate laps
    valid_laps = laps[
        laps["IsAccurate"] == True
    ].copy()

    if valid_laps.empty:
        return None

    # Lap time in seconds
    lap_times = valid_laps["LapTimeSeconds"]

    # Sector times in seconds
    sector_1 = valid_laps["Sector1Time"].dt.total_seconds()
    sector_2 = valid_laps["Sector2Time"].dt.total_seconds()
    sector_3 = valid_laps["Sector3Time"].dt.total_seconds()

    return {
        "best_lap": lap_times.min(),
        "average_lap": lap_times.mean(),
        "best_sector_1": sector_1.min(),
        "best_sector_2": sector_2.min(),
        "best_sector_3": sector_3.min(),
        "lap_consistency": lap_times.std()
    }

def format_lap_time(seconds):
    """Convert seconds into M:SS.mmm format."""

    if seconds is None:
        return "N/A"

    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60

    return f"{minutes}:{remaining_seconds:06.3f}"

def get_tire_strategy(laps, driver):
    """Return tire stints for a driver."""

    driver_laps = laps[laps["Driver"] == driver].copy()

    driver_laps = driver_laps.dropna(
        subset=["Compound", "Stint"]
    )

    if driver_laps.empty:
        return []

    stints = []

    for stint_number, stint_data in driver_laps.groupby("Stint"):

        compound = stint_data["Compound"].iloc[0]

        start_lap = int(stint_data["LapNumber"].min())
        end_lap = int(stint_data["LapNumber"].max())

        stint_length = end_lap - start_lap + 1

        stints.append({
            "stint": int(stint_number),
            "compound": compound,
            "start_lap": start_lap,
            "end_lap": end_lap,
            "laps": stint_length
        })

    return stints