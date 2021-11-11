=======================
dash_component_template
=======================


.. image:: https://img.shields.io/pypi/v/dash_component_template.svg
        :target: https://pypi.python.org/pypi/dash_component_template

.. image:: https://img.shields.io/badge/gh--pages-doc-brightgreen
        :target: https://toltec-astro.github.io/dash_component_template

.. image:: https://github.com/toltec-astro/dash_component_template/actions/workflows/ci_tests.yml/badge.svg
        :target: https://github.com/toltec-astro/dash_component_template/actions/workflows/ci_tests.yml

.. image:: https://codecov.io/gh/toltec-astro/dash_component_template/branch/main/graph/badge.svg?token=4Z2P2IPL1U
      :target: https://codecov.io/gh/toltec-astro/dash_component_template


A framework to create reusable Dash layout.


* Free software: BSD license
* Documentation: https://toltec-astro.github.io/dash_component_template


Features
--------

This package provides a new API for creating Dash layout and callbacks.

* The id and children are managed automatically. No deeply nested dicts
  and lists any more; unique ids of components are automatically created.

* A re-usable template can be defined by sub-classing
  ``dash_component_template.ComponentTemplate``. Instances of the template
  have children with unique ids and can be used anywhere in anyway inside
  a larger Dash app layout tree.

Get Started
-----------

Suppose we have the following Dash app (from Dash tutorial site):

.. code::

    # Run this app with `python app.py` and
    # visit http://127.0.0.1:8050/ in your web browser.

    import dash
    from dash import dcc, html
    import plotly.express as px
    import pandas as pd

    app = dash.Dash(__name__)

    # assume you have a "long-form" data frame
    # see https://plotly.com/python/px-arguments/ for more options
    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for your data.
        '''),

        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ])

    if __name__ == '__main__':
        app.run_server(debug=True)

Let's build a new app which have two columns of the same layout.

.. code::

    from dash_component_template import ComponentTemplate
    import dash_bootstrap_components as dbc
    import pandas as pd
    import dash
    import plotly.express as px
    from dash import html, dcc


    # This class defines a template that resembles the Dash example,
    # with a title, subtitle, and graph for visualizing a data frame
    class MyTableGraph(ComponentTemplate):

        class Meta:
            component_cls = dbc.Container

        def __init__(self, title_text, subtitle_text, df, parent=None):
            super().__init__(parent=parent)
            self._title_text = title_text
            self._subtitle_text = subtitle_text
            self._df = df

        def setup_layout(self, app):
            container = self
            container.child(html.Div, self._title_text)
            container.child(html.Div, self._subtitle_text)
            container.child(dcc.Graph, figure=self._make_fig())
            super().setup_layout(app)

        def _make_fig(self):
            return px.bar(
                self._df, x="Fruit", y="Amount", color="City", barmode="group")


    # This class defines the app layout which have two columns each column
    # contains an instance of the template defined above.

    class MyPage(ComponentTemplate):

        class Meta:
            component_cls = dbc.Container

        # define some data
        df1 = pd.DataFrame({
            "Fruit": [
                "Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
            "Amount": [4, 1, 2, 2, 4, 5],
            "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
        })

        df2 = pd.DataFrame({
            "Fruit": [
                "Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
            "Amount": [5, 6, 7, 8, 4, 5],
            "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
        })

        def setup_layout(self, app):
            col1, col2 = self.grid(nrows=1, ncols=2, squeeze=True)
            col1.child(MyTableGraph(
                df=self.df1,
                title_text='Hello Dash (left)',
                subtitle_text='Re-usable template instance 1'
                ))
            col2.child(MyTableGraph(
                df=self.df2,
                title_text='Hello Dash (right)',
                subtitle_text='Re-usable template instance 2'
                ))
            # this line is important which triggers children's setup_layout
            super().setup_layout(app)


    # Now create the app and set the bootstrap css
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    # Instantiant the page tempalte, and call the setup layout function
    # This only "declare" the structure of the Dash components. No actual
    # Dash components are created yet.
    page = MyPage()
    page.setup_layout(app)
    # Create and assign the app layout. The actual creation of Dash components
    # are done here.
    app.layout = page.layout

    if __name__ == '__main__':
        app.run_server(debug=True)


Live Examples
-------------

Live examples can be found in the `TolTEC DR site <http://toltecdr.astro.umass.edu>`_.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
