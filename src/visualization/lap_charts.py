import plotly.graph_objects as go
import fastf1.plotting

def _lighten_color(hex_color, amount=0.4):
    """Blend a hex color toward white by the given amount (0-1)."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    r = int(r + (255 - r) * amount)
    g = int(g + (255 - g) * amount)
    b = int(b + (255 - b) * amount)
    return f"#{r:02x}{g:02x}{b:02x}"

def create_lap_time_chart(driver_data, session):
    """Create an interactive lap-time comparison chart."""

    fig = go.Figure()
    used_colors = []

    for driver, laps in driver_data.items():

        driver_color = fastf1.plotting.get_driver_color(driver, session)

        if driver_color in used_colors:
            driver_color = _lighten_color(driver_color, 0.45)
            marker_symbol = "diamond"
            line_dash = "dash"
        else:
            marker_symbol = "circle"
            line_dash = "solid"

        used_colors.append(fastf1.plotting.get_driver_color(driver, session))

        fig.add_trace(
            go.Scatter(
                x=laps["LapNumber"],
                y=laps["LapTimeSeconds"],
                mode="lines+markers",
                name=driver,
                line=dict(color=driver_color, dash=line_dash),
                marker=dict(color=driver_color, symbol=marker_symbol, size=7),
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