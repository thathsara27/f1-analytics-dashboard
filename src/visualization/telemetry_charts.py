import plotly.graph_objects as go


def create_speed_comparison(
    telemetry_1,
    telemetry_2,
    driver_1,
    driver_2
):
    """Create a speed comparison chart for two drivers."""

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=telemetry_1["Distance"],
            y=telemetry_1["Speed"],
            mode="lines",
            name=driver_1
        )
    )

    fig.add_trace(
        go.Scatter(
            x=telemetry_2["Distance"],
            y=telemetry_2["Speed"],
            mode="lines",
            name=driver_2
        )
    )

    fig.update_layout(
        title="Speed Comparison",
        xaxis_title="Distance Around Track (m)",
        yaxis_title="Speed (km/h)",
        template="plotly_dark",
        hovermode="x unified"
    )

    return fig