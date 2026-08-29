import plotly.graph_objects as go
import fastf1.plotting


def create_lap_time_chart(driver_data, session):
    """Create an interactive lap-time comparison chart."""

    fig = go.Figure()

    for driver, laps in driver_data.items():

        driver_color = fastf1.plotting.get_driver_color(driver, session)

        fig.add_trace(
            go.Scatter(
                x=laps["LapNumber"],
                y=laps["LapTimeSeconds"],
                mode="lines+markers",
                name=driver,
                line=dict(color=driver_color),
                marker=dict(color=driver_color),
                hovertemplate=(
                    "<b>%{fullData.name}</b><br>"
                    "Lap: %{x}<br>"
                    "Lap Time: %{y:.3f} s"
                    "<extra></extra>"
                )
            )
        )

    fig.update_layout(
        title="Driver Lap-Time Comparison",
        xaxis_title="Lap Number",
        yaxis_title="Lap Time (seconds)",
        template="plotly_dark",
        hovermode="x unified",
        legend_title="Driver"
    )

    return fig