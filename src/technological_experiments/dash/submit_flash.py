import flask
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Form([
    dcc.Input(name='name'),
    html.Button('Submit', type='submit')
], action='/post', method='post')


@app.server.route('/post', methods=['POST'])
def on_post():
    data = flask.request.form
    print(data)
    return flask.redirect('/')


if __name__ == '__main__':
    app.run_server(debug=True, port=7779)