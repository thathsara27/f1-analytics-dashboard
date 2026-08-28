import streamlit as st
from src.analysis.telemetry_analysis import get_fastest_lap_telemetry
from src.visualization.telemetry_charts import create_speed_comparison

from src.analysis.lap_analysis import (
    load_race_session,
    get_driver_laps,
    get_race_summary,
    get_driver_performance,
    format_lap_time,
    get_tire_strategy
)

from src.visualization.lap_charts import (
    create_lap_time_chart
)

def main():

    st.set_page_config(
        page_title="F1 Analytics",
        page_icon="🏎️",
        layout="wide"
    )

    st.title("🏎️ F1 Analytics")
    st.caption("Formula 1 Telemetry & Strategy Dashboard")

    st.sidebar.header("Race Selection")

    year = st.sidebar.selectbox(
        "Season",
        [2024]
    )

    grand_prix = st.sidebar.selectbox(
        "Grand Prix",
        ["Monza"]
    )

    session_name = st.sidebar.selectbox(
        "Session",
        ["Race"]
    )

    session = load_race_session(
        year,
        grand_prix,
        session_name
    )

    summary = get_race_summary(session)

    # Get driver abbreviations from the lap data
    driver_info = (
        session.laps[["Driver", "DriverNumber"]]
        .drop_duplicates()
        .sort_values("Driver")
    )

    driver_codes = driver_info["Driver"].tolist()

    driver_1 = st.sidebar.selectbox(
        "Driver 1",
        driver_codes,
        index=driver_codes.index("LEC")
    )

    driver_2 = st.sidebar.selectbox(
        "Driver 2",
        driver_codes,
        index=driver_codes.index("PIA")
    )

    telemetry_1 = get_fastest_lap_telemetry(
        session,
        driver_1
    )

    telemetry_2 = get_fastest_lap_telemetry(
        session,
        driver_2
    )

    st.header(
        f"{session.event.EventName} — {session.name}"
    )

    st.write(
        f"Season: {year} | "
        f"Date: {session.date.strftime('%d %B %Y')}"
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🏆 Race Winner",
            value=summary["winner"]
        )

    with col2:
        fastest_time = summary["fastest_time"]

        if fastest_time is not None:
            fastest_time_text = str(fastest_time).split(" days ")[-1]
            fastest_time_text = fastest_time_text[:12]
        else:
            fastest_time_text = "N/A"

        st.metric(
            label="⚡ Fastest Lap",
            value=fastest_time_text,
            delta=summary["fastest_driver"]
        )

    with col3:
        st.metric(
            label="🏁 Total Laps",
            value=summary["total_laps"]
        )

    with col4:
        st.metric(
            label="👥 Drivers",
            value=summary["driver_count"]
        )

    st.divider()

    laps_1 = get_driver_laps(
        session,
        driver_1
    )

    laps_2 = get_driver_laps(
        session,
        driver_2
    )

    performance_1 = get_driver_performance(laps_1)
    performance_2 = get_driver_performance(laps_2)

    strategy_1 = get_tire_strategy(
        session.laps,
        driver_1
    )

    strategy_2 = get_tire_strategy(
        session.laps,
        driver_2
    )

    st.divider()

    st.subheader("🛞 Tire Strategy")

    col1, col2 = st.columns(2)


    def display_strategy(driver, strategy):

        st.markdown(f"### 🏎️ {driver}")

        if not strategy:
            st.info("No tire strategy data available.")
            return

        for stint in strategy:

            compound = stint["compound"]

            st.markdown(
                f"""
                **Stint {stint["stint"]} — {compound}**

                Lap {stint["start_lap"]} → Lap {stint["end_lap"]}

                **{stint["laps"]} laps**
                """
            )

            progress_value = min(
                stint["laps"] / 50,
                1.0
            )

            st.progress(progress_value)

    with col1:
        display_strategy(
            driver_1,
            strategy_1
        )

    with col2:
        display_strategy(
            driver_2,
            strategy_2
        )

    driver_data = {
        driver_1: laps_1,
        driver_2: laps_2
    }

    fig = create_lap_time_chart(
        driver_data,
        session
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    st.subheader("📊 Driver Performance")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(f"### 🏎️ {driver_1}")

        if performance_1:

            st.metric(
                "Best Lap",
                format_lap_time(
                    performance_1["best_lap"]
                )
            )

            st.metric(
                "Average Lap",
                format_lap_time(
                    performance_1["average_lap"]
                )
            )

            st.metric(
                "Best Sector 1",
                format_lap_time(
                    performance_1["best_sector_1"]
                )
            )

            st.metric(
                "Best Sector 2",
                format_lap_time(
                    performance_1["best_sector_2"]
                )
            )

            st.metric(
                "Best Sector 3",
                format_lap_time(
                    performance_1["best_sector_3"]
                )
            )

            st.metric(
                "Lap Consistency",
                f"{performance_1['lap_consistency']:.3f} s"
            )


    with col2:

        st.markdown(f"### 🏎️ {driver_2}")

        if performance_2:

            st.metric(
                "Best Lap",
                format_lap_time(
                    performance_2["best_lap"]
                )
            )

            st.metric(
                "Average Lap",
                format_lap_time(
                    performance_2["average_lap"]
                )
            )

            st.metric(
                "Best Sector 1",
                format_lap_time(
                    performance_2["best_sector_1"]
                )
            )

            st.metric(
                "Best Sector 2",
                format_lap_time(
                    performance_2["best_sector_2"]
                )
            )

            st.metric(
                "Best Sector 3",
                format_lap_time(
                    performance_2["best_sector_3"]
                )
            )

            st.metric(
                "Lap Consistency",
                f"{performance_2['lap_consistency']:.3f} s"
            )

    st.divider()

    st.header("📡 Telemetry Analysis")

    st.subheader("⚡ Speed Comparison")

    if telemetry_1 is not None and telemetry_2 is not None:

        speed_chart = create_speed_comparison(
            telemetry_1,
            telemetry_2,
            driver_1,
            driver_2
        )

        st.plotly_chart(
            speed_chart,
            width="stretch"
        )

    else:
        st.warning("Telemetry data is not available for one or both drivers.")