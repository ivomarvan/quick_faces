#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Test for GUI
'''

import base64
import os
import re
import sys

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '', '..', '..'))
sys.path.append(PROJECT_ROOT)
STATIC_FILES_DIR = os.path.join(PROJECT_ROOT, 'src', 'gui', 'static_files')


class ImgProcessorsGui:
    WHITE_CHARS = re.compile(r'[\s\.]+')

    def __init__(self):
        pass

    def _get_proc_categories(self) -> []:
        '''
        Returs hieararchical description of processors.
        @todo Will be generated, it is static for experimemts window
        '''
        return [
            {
                'name': 'source',
                'params': {
                    'collapseable': False
                },
                'items': [
                    {'name': 'Camera'},
                    {'name': 'Directory'},
                    {'name': 'Video file'},
                ]
            },
            {
                'name': 'faces',
                'items': [
                    {
                        'name': 'face_detector',
                        'items': [
                            {'name': 'jedna'},
                            {'name': 'dva'},
                            {'name': 'tři'},
                        ]
                    },
                    {
                        'name': 'landmarks_detector',
                        'items': [
                            {'name': 'jedna'},
                            {'name': 'dva'},
                            {'name': 'tři'},
                        ]
                    },
                    {
                        'name': 'marker',
                        'items': [
                            {'name': 'jedna'},
                            {'name': 'dva'},
                            {'name': 'tři'},
                        ]
                    },
                ]
            },
            {
                'name': 'storage',
                'params': {
                    'collapseable': False
                },
                'items': [
                    {'name': 'Camera'},
                    {'name': 'Directory'},
                    {'name': 'Video file'},
                ]
            }
        ]

    def _get_nav_bar(self):
        image_filename = os.path.join(STATIC_FILES_DIR, 'cv32.png')
        encoded_image = base64.b64encode(open(image_filename, 'rb').read())

        return dbc.Navbar([
            html.Span(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))),
                        dbc.Col(dbc.NavbarBrand("Image processors", className="ml-1")),
                    ],
                    align="center",
                    no_gutters=True,
                )
            ),
        ],
            dark=False,
            # color='warning'
        )

    def _get_html_for_category(self, category: dict, namespace: str = ''):
        def get(key, default=None):
            try:
                return category[key]
            except KeyError:
                return default

        name = get('name')
        good_name = self.WHITE_CHARS.sub('-', name.lower())
        if namespace:
            id = namespace + '-' + good_name
        else:
            id = good_name
        print(id)

        if 'items' in category:
            card_body = dbc.Collapse(
                dbc.CardBody(
                    self._get_html_for_categories(categories=get('items'), namespace=id)
                )
            )
        else:
            card_body = dbc.CardBody(f"This is the content of group {id}..."),

        return dbc.Card(
            [
                dbc.CardHeader(
                    html.Div(
                        dbc.Button(
                            f'{name}',
                            color="link",
                            id=f"group-{id}-toggle",
                        )
                    )
                ),
                dbc.Collapse(
                    card_body,
                    id=f"collapse-{id}",
                )
            ]
        )

    def _get_html_for_categories(self, categories: list, namespace: str = ''):
        ret_list = []
        for category in categories:
            ret_list.append(self._get_html_for_category(category=category, namespace=namespace))
        return ret_list

    def _get_layout(self):
        categories = self._get_proc_categories()
        return html.Div(
            [
                self._get_nav_bar(),
                dbc.Row(
                    [
                        dbc.Col(self._get_html_for_categories(categories), width=4),
                        dbc.Col([html.Div("One of three columns")]),
                    ]
                ),

            ]
        )

    def _get_app(self, title: str = 'Image processors'):
        app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], title=title)
        app.layout = self._get_layout()
        return app

    def run(self, debug=True, threaded=True, port=10451):
        self._get_app().run_server(debug=debug, threaded=threaded, port=port)


if __name__ == '__main__':
    gui = ImgProcessorsGui()
    gui.run(debug=True, threaded=True, port=10450)
