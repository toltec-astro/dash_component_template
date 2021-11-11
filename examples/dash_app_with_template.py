#!/usr/bin/env python


from dash_component_template import ComponentTemplate
import dash_bootstrap_components as dbc
import pandas as pd
import dash
import plotly.express as px
from dash import html, dcc


# This class defines the section with have a title, subtitle, and graph for
# a data frame
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


# now create the app and set the bootstrap css
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

page = MyPage()
page.setup_layout(app)
app.layout = page.layout

if __name__ == '__main__':
    app.run_server(debug=True)
