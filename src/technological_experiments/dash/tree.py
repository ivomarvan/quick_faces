import dash
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Details(
            [
                html.Summary(
                    html.A(id='outer-link', children=['Outer Link']),
                ),
                html.Div(
                    [
                        html.Details(
                            html.Summary(
                                html.A(id='inner-link', children=['Inner Link'])
                            )
                        )
                    ],
                    style={'text-indent':'2em'}
                )
            ]
        ),
        html.Div(id='outer-count'),
        html.Div(id='inner-count'),
        html.Div(id='last-clicked')
    ]
)

@app.callback(
    [
        Output('outer-count', 'children'),
        Output('inner-count', 'children'),
        Output('last-clicked', 'children')
    ],
    [
        Input('outer-link', 'n_clicks'),
        Input('outer-link', 'n_clicks_timestamp'),
        Input('inner-link', 'n_clicks'),
        Input('inner-link', 'n_clicks_timestamp')
    ],
)
def divclick(outer_link_clicks, outer_link_time, inner_link_clicks, inner_link_time):
    if outer_link_time is None:
        outer_link_time = 0
    if inner_link_time is None:
        inner_link_time = 0

    timestamps = {
        'None':1,
        'Outer Link': outer_link_time,
        'Inner Link': inner_link_time
    }

    last_clicked = max(timestamps, key=timestamps.get)

    return(
        'Outer link clicks: ' + str(outer_link_clicks),
        'Inner link clicks: ' + str(inner_link_clicks),
        'Last clicked: ' + last_clicked
    )

if __name__ == '__main__':
    app.run_server()