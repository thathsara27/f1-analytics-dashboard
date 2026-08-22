def get_fastest_lap_telemetry(session, driver):
    """Get telemetry data from a driver's fastest lap."""

    # Get all laps for the selected driver
    driver_laps = session.laps.pick_drivers(driver)

    # Find the fastest lap
    fastest_lap = driver_laps.pick_fastest()

    # Check whether a fastest lap was found
    if fastest_lap is None:
        return None

    # Get telemetry data
    telemetry = fastest_lap.get_car_data().add_distance()

    # Keep only the columns we need
    telemetry = telemetry[
        ["Distance", "Speed", "Throttle", "Brake"]
    ]

    return telemetry