import plotly.graph_objs as go
from plotly.offline import plot

def create_chart():
    fig = go.Figure()
    scatter = go.Scatter(x=[0, 1, 2, 3], y=[0, 1, 2, 3], mode='lines', name='test')
    fig.add_trace(scatter)
    plot_div = plot(fig, output_type='div')
    return plot_div
