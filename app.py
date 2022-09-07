import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import pandas as pd

########### Define your variables ######

tabtitle = 'Pokedex'
sourceurl = 'https://www.kaggle.com/datasets/abcsds/pokemon'
githublink = 'https://github.com/mlee111/306-agriculture-exports-dropdown'
# here's the list of possible columns to choose from.


########## Set up the chart
df = pd.read_csv('assets/Pokemon.csv')
list_of_columns = df['Type 1'].unique()

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout

app.layout = html.Div(children=[
    html.H1('Pokemon Data'),
    html.Div([
        html.Div([
            dcc.Tabs(id='tabs', value='tab1', children=[
                dcc.Tab(label='Analysis 1', value='tab1'),
                dcc.Tab(label='Analysis 2', value='tab2'),
                dcc.Tab(label='Analysis 3', value='tab3')
            ]),
            html.Div(id='tab_content'),
    ]),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ])
]
)


# make a function that can intake any varname and produce a map.
@app.callback(Output('figure-1', 'figure'),
             [Input('options-drop', 'value')])
def make_figure(varname):
    mygraphtitle = f'Pokemon grouped by generation'
    mycolorbartitle = "Num Pokemon"
    
    colors_dict = {'Grass':'#7deb34', 'Fire':'#eb4f3b', 'Water':'#2983e3', 'Bug':'#3b8c3f', 'Normal':'#d9d3a7', 'Poison':'#b348d4', 'Electric':'#feffb8', 'Ground':'#7a4917','Fairy':'#f7b7e9', 'Fighting':'#4d6ec9', 'Psychic':'#e3a3d6', 'Rock':'#6e6b6d', 'Ghost':'#311559', 'Ice':'#8af1ff', 'Dragon':'#9e233e', 'Dark':'#242323', 'Steel':'#5e5e5e', 'Flying':'#7a93ff'}

    subset = df[df['Type 1'] == varname]
    grouped_data = subset.groupby('Generation')
    df2 = pd.DataFrame(grouped_data.count()['Type 1'])
    
    barchart = go.Bar(
        x=df2.index,
        y=df2['Type 1'],
        name=varname,
        marker=dict(color=colors_dict[varname])
    )
    
    chart_layout = go.Layout(
        title = 'Pokemon by type',
        xaxis = dict(title = 'Generation'), # x-axis label
        yaxis = dict(title = '# of pokemon'), # y-axis label
    )
    fig = go.Figure(data=barchart, layout=chart_layout)
    return fig

@app.callback(Output('tab_content', 'children'),
              [Input('tabs', 'value')])
def render_tabs(tab):
    if tab == 'tab1':
        return html.Div([
            html.H6('Select a variable for analysis:'),
            dcc.Dropdown(
                id='options-drop',
                options=[{'label': i, 'value': i} for i in list_of_columns],
                value='Water'
            ),
            html.Div([dcc.Graph(id='figure-1')]),
         ])
    elif tab == 'tab2':
        scatter1 = go.Scatter(
            x = df[df['Generation'] < 4]['Attack'],
            y = df[df['Generation'] < 4]['Defense'],
            mode='markers',
            text=df.Name,
            marker=dict(
                color=df['Generation'],
            ),
            hoverinfo='text',
        )
        layout = go.Layout(
            title='Pokemon Atk vs Def [Gen 1-3]',
            xaxis_title='Attack',
            yaxis_title='Defense',

        )
        
        first_gen_scatter = go.Figure(data=scatter1, layout=layout);
        
        scatter2 = go.Scatter(
            x = df[df['Generation'] >= 4]['Attack'],
            y = df[df['Generation'] >= 4]['Defense'],
            mode='markers',
            text=df.Name,
            marker=dict(
                color=df['Generation'],
            ),
            hoverinfo='text',
        )
        layout2 = go.Layout(
            title='Pokemon Atk vs Def [Gen 4-6]',
            xaxis_title='Attack',
            yaxis_title='Defense',

        )
        last_gen_scatter = go.Figure(data=scatter2, layout=layout2);
        return html.Div([
            html.H4('Attack and Defense stats (hover to view Pokemon name)'),
            html.H6('Attack + Defense Stats Gen 1-3'),
            html.Div([dcc.Graph(id='figure-2', figure=first_gen_scatter)]),
            html.H6('Attack + Defense Stats Gen 4-6'),
            html.Div([dcc.Graph(id='figure-3', figure=last_gen_scatter)]),
        ])
    elif tab == 'tab3':
        legendaries = df[df['Legendary'] == True]
        grouped_data = legendaries.groupby('Generation')
        totals = pd.DataFrame(grouped_data.mean()['Attack'])

        barchart = go.Bar(
            x = totals.index,
            y = totals['Attack']
        )

        fig3 = go.Figure(data=barchart)
        return html.Div([
            html.H4('Average Attack of Legendaries by generation'),
            html.Div([dcc.Graph(id='figure-3', figure=fig3)]),
        ])
        
    

############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
