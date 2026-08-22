import plotly.graph_objects as go

def create_lap_time_chart(driver_data):
    """Create an interactive lap-time comparison chart."""

    fig = go.Figure()

    for driver, laps in driver_data.items():

        fig.add_trace(
            go.Scatter(
                x=laps["LapNumber"],
                y=laps["LapTimeSeconds"],
                mode="lines+markers",
                name=driver,
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