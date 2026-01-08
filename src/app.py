import dash
from dash import dcc, html, callback, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from data_loader import load_trial, list_all_trials
from metrics import extract_trial_metrics

app = dash.Dash(__name__)
server = app.server
all_trials = list_all_trials()

app.layout = html.Div([
    html.H1("Free Throw Performance Dashboard"),
    
    html.Div([
        html.Label("Select Trial:"),
        dcc.Dropdown(
            id='trial-dropdown',
            options=[{'label': t, 'value': t} for t in all_trials],
            value=all_trials[0]
        )
    ], style={'margin': '20px'}),
    
    html.Div(id='shot-info', style={'margin': '20px', 'fontSize': '18px'}),
    
    html.Div([
        dcc.Graph(id='angles-graph'),
        dcc.Graph(id='ball-trajectory-graph')
    ])
])

@callback(
    Output('shot-info', 'children'),
    Input('trial-dropdown', 'value')
)
def update_info(selected_trial):
    trial = load_trial(selected_trial)
    result = trial['result'].upper()
    entry_angle = trial['entry_angle']
    landing = f"({trial['landing_x']}, {trial['landing_y']})"
    
    return html.Div([
        html.P(f"Result: {result}", style={'color': 'green' if result == 'MADE' else 'red'}),
        html.P(f"Entry Angle: {entry_angle}°"),
        html.P(f"Landing Position: {landing}")
    ])

@callback(
    [Output('angles-graph', 'figure'),
     Output('ball-trajectory-graph', 'figure')],
    Input('trial-dropdown', 'value')
)
def update_graphs(selected_trial):
    trial = load_trial(selected_trial)
    metrics = extract_trial_metrics(trial)
    df = pd.DataFrame(metrics)
    
    # Angles graph
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df['frame'], y=df['r_elbow_angle'],
        mode='lines', name='Right Elbow'
    ))
    fig1.add_trace(go.Scatter(
        x=df['frame'], y=df['l_elbow_angle'],
        mode='lines', name='Left Elbow'
    ))
    fig1.add_trace(go.Scatter(
        x=df['frame'], y=df['r_knee_angle'],
        mode='lines', name='Right Knee'
    ))
    fig1.update_layout(
        title=f"Joint Angles - {selected_trial}",
        xaxis_title="Frame",
        yaxis_title="Angle (degrees)"
    )
    
    # Ball trajectory
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter3d(
        x=df['ball_x'], y=df['ball_y'], z=df['ball_z'],
        mode='lines', name='Ball Path'
    ))
    fig2.update_layout(title="Ball Trajectory (3D)")
    
    return fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)