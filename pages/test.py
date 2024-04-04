from flask import Flask, render_template
import dash
from dash import dcc
from dash import html

app = Flask(__name__)
dash_app = dash.Dash(__name__, server=app)

# Routes Flask
@app.route('/')
def home():
    return "Bienvenue sur la page d'accueil Flask !"

# Route Dash
dash_app.layout = html.Div([
    html.H1("Tableau de bord Dash"),
    dcc.Graph(id='example-graph', figure={'data': [{'y': [1, 2, 3]}]})
])

if __name__ == '__main__':
    app.run(debug=True)