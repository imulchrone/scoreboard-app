import dash
from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc
from getscore import getScores
import traceback

# Consolidate function with multi-line name block
def consolidate_scores(g1, g2, g3, order):
    rows = []
    for spot in range(1, 10):
        g1_names = "; ".join(g1.get(spot, {}).get('name', []))
        g2_names = "; ".join(g2.get(spot, {}).get('name', []))
        g3_names = "; ".join(g3.get(spot, {}).get('name', []))
        names = f"G1: {g1_names}\nG2: {g2_names}\nG3: {g3_names}"
        s1 = g1.get(spot, {}).get('score', 0)
        s2 = g2.get(spot, {}).get('score', 0)
        s3 = g3.get(spot, {}).get('score', 0)
        total = s1 + s2 + s3
        rows.append({
            'spot': f"{spot}.",
            'member': order[spot-1],
            'names': names,
            'g1': s1,
            'g2': s2,
            'g3': s3,
            'total': total
        })
    return rows

def centered(font_size='1.1vw', textAlign = 'center', justifyContent = 'center'):
    return {
        'textAlign': textAlign,
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': justifyContent,
        'fontSize': font_size,
        'overflow': 'hidden',
        'textOverflow': 'ellipsis'
    }

def build_team_table(team_name, rows):
    def build_header():
        return dbc.Row([
            dbc.Col("", width=1, style=centered()),
            dbc.Col("Member", width=2, style={**centered(font_size='2.8vw')}),
            dbc.Col("Players", width=4, style=centered(font_size='2.8vw')),
            dbc.Col("G1", width=1, style={**centered(font_size='2.8vw')}),
            dbc.Col("G2", width=1, style={**centered(font_size='2.8vw', justifyContent='center'),'paddingLeft':'4px'}),
            dbc.Col("G3", width=1, style={**centered(font_size='2.8vw', justifyContent='left'),'paddingLeft':'2px'}),
            dbc.Col("Total", width=1, style={**centered(font_size='2.3vw'),'paddingLeft':'10px'}),
        ], style={
            'color': 'white',
            'fontWeight': 'bold',
            'borderBottom': '2px solid white',
            'fontFamily': 'monospace',
            'fontSize': '1.3vw',
            'marginBottom': '6px',
            'paddingRight':'2px'
        })

    def build_row(row):
        return dbc.Row([
            dbc.Col(row['spot'], width=1, style={**centered(font_size='2.8vw')}),
            dbc.Col(row['member'], width=2, style={**centered(font_size='2.8vw', justifyContent='left')}),
            dbc.Col(
                html.Div(
                    html.Pre(row['names'], style={
                        'margin': 0,
                        'whiteSpace': 'pre-wrap',
                        'overflow': 'hidden',
                        'fontSize': '2.0vw'
                    }),
                    style={'display': 'flex', 'alignItems': 'center', 'height': '100%'}
                ), width=4
            ),
            dbc.Col(str(row['g1']), width=1, style={**centered(font_size='2.8vw')}),
            dbc.Col(str(row['g2']), width=1, style={**centered(font_size='2.8vw')}),
            dbc.Col(str(row['g3']), width=1, style={**centered(font_size='2.8vw')}),
            dbc.Col(str(row['total']), width=1, style={**centered(font_size='2.8vw'), 'paddingRight':'2px'}),
        ], style={
            'fontFamily': 'monospace',
            'color': 'white',
            'minHeight': '45px',
            'lineHeight': '1.2',
            'margin': 0,
            'padding': '0px',
            'marginBottom':'4px'
        })


    return html.Div(
        dbc.Card([
            html.H4(team_name, style={
                'color': 'white',
                'textAlign': 'center',
                'fontFamily': 'monospace'
            }),
            build_header(),
            *[build_row(row) for row in rows]
        ], style={
            'backgroundColor': '#2E6B3C',
            'padding': '20px',
            'border': '1px solid white',
            'borderRadius': '10px',
            'minWidth': '325px'  # Ensure full table fits
        }),
        style={
            'width': '100%',
            'overflowX': 'auto',   # enables scroll if too small
            'margin': '0 auto 30px auto',
            'paddingLeft': '2%',
            'paddingRight': '2%',
        }
    )





# Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Interval(id='refresh', interval=30*1000, n_intervals=0),
    dcc.Store(id='cached-data'),
    html.Div(id='content')
], style={
    'backgroundColor': '#1E4D2B',
    'margin': '0',
    'paddingTop': '30px',
    'paddingBottom': '30px',
    'width': '100vw',
    'minHeight': '100vh',
    'overflowX': 'hidden'  # Optional: prevents horizontal scrollbar
})


@app.callback(
    Output('cached-data', 'data'),
    Input('refresh', 'n_intervals')
)
def fetch_data(_):
    try:
        testgame = 777023
        testgame2 = 777018
        testgame3 = 777025
        team_a_order = ['Friz', 'Rife', 'Brian', 'Price', 'Ben', 'Ian', 'Julia','','']
        team_b_order = ['Childs', 'Adrian', 'Rory', 'Dave', 'Nagel', 'Dreyer', 'Sean','','']

        # Primary game
        team_a_name, team_a_g1 = getScores(testgame, 'away')
        team_b_name, team_b_g1 = getScores(testgame, 'home')

        # Placeholder for future games
        team_a_g2 = getScores(testgame2, 'away')[1]
        team_a_g3 = getScores(testgame3, 'away')[1]
        team_b_g2 = getScores(testgame2, 'home')[1]
        team_b_g3 = getScores(testgame3, 'home')[1]

        # cubs_name, cubs_g1 = getScores(777017,'away')
        # cubs_g2 = getScores(776994,'away')[1]
        # cubs_g3 = getScores(776989,'away')[1]

        # whitesox_name, whitesox_g1 = getScores(777017,'home')
        # whitesox_g2 = getScores(776994,'home')[1]
        # whitesox_g3 = getScores(776989,'home')[1]

        return {
            'team_a_name': team_a_name,
            'team_b_name': team_b_name,
            'team_a_rows': consolidate_scores(team_a_g1, team_a_g2, team_a_g3, team_a_order),
            'team_b_rows': consolidate_scores(team_b_g1, team_b_g2, team_b_g3, team_b_order)
        }

    except Exception as e:
        return {'error': str(e), 'traceback': traceback.format_exc()}

@app.callback(
    Output('content', 'children'),
    Input('cached-data', 'data')
)
def render_layout(data):
    if not data:
        return html.Div("Loading...", style={'color': 'white'})

    if 'error' in data:
        return html.Div([
            html.H4("Error fetching data", style={'color': 'red'}),
            html.Pre(data['error']),
            html.Details([
                html.Summary("Traceback"),
                html.Pre(data['traceback'])
            ])
        ])

    team_a = build_team_table(data['team_a_name'], data['team_a_rows'])
    team_b = build_team_table(data['team_b_name'], data['team_b_rows'])

    return [team_a, team_b]



if __name__ == '__main__':
    app.run(debug=True)