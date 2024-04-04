# This file is typically the entry page to a multipage app using Dash Page -- https://dash.plotly.com/urls#dash-pages
# More multipage app examples by Ann Marie: https://github.com/AnnMarieW/dash-multi-page-app-demos
# Here is some code to get started:
import dash
from dash import Dash, html, dcc
from flask_login import LoginManager, UserMixin, login_user, login_required

app = Dash(__name__, use_pages=True,suppress_callback_exceptions=True)
server = app.server

login_manager = LoginManager()
login_manager.init_app(server)

class User(UserMixin):
    def __init__(self,id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)



app.layout = html.Div([
    html.H1('Response Reporting Platform -- VOST Europe'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)
