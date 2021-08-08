from dash_html_components.A import A
import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objs as go
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport",
        "content": "width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,"
        },
    ]
)
app.title = "NTU exchange stats"
server = app.server

MAIN_COLOR = '#256ae5'
DEFAULT_GRAPH_STYLE = {
                       'height': '100%',
                       'width': '100%',
                       'max-height': '250px',
                       'max-width': '600px'
                      }
DEFAULT_GRAPH_MARGIN = dict(l=20, r=20, t=35, b=10)
DEFAULT_GRAPH_TITLE_POSITION = dict(x=0.5, y=0.95)

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("./data/ntu_exchange_eng.csv")
df = df.dropna()
# df["school_year"] = df["school_year"].map(lambda x: int(x[:-2]))
years = df["school_year"].sort_values(ascending=False).unique()

departments = df["department"].unique()
departments_option = [{"label": dept, "value": dept} for dept in departments]

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(
    className="page",
    children= [
        html.H1("NTU Outbound Exchange", style={'text-align': 'center'}),
        html.Div(
            className="range-slider",
            children=[
                dcc.RangeSlider(id="slct_year",
                                min=years[-1],
                                max=years[0],
                                step=1,
                                marks={str(year): str(year) for year in years if year%2==0},
                                value=[years[-1], years[0]]
                                )
            ],
        ),
        html.Div(
            className="department-dropdown",
            children=[
                dcc.Dropdown(id="slct_department",
                            options=departments_option,
                            multi=False,
                            # value="Department of Economics",
                            placeholder="Select a department",
                            optionHeight=50
                            )
            ],
        ),
        html.Div(
            className="pane-grid",
            children=[
                html.Div(
                    className="pane stats-grid",
                    children=[
                        html.Div(
                            className="stats-card",
                            children=[
                                html.H2(id='num_students'),
                                html.P("attended exchange")
                            ]
                        ),
                        html.Div(
                            className="stats-card",
                            children=[
                                html.H2(id='one_sem_pct'),
                                html.P("% attended 1-semester program")
                            ]
                        ),
                        html.Div(
                            className="stats-card",
                            children=[
                                html.H2(id='num_countries'),
                                html.P("Top Destination Countries")
                            ]
                        ),
                        html.Div(
                            className="stats-card",
                            children=[
                                html.H2(id='num_schools'),
                                html.P("Destination Universities")
                            ]
                        ),
                    ]
                ),
                # html.Div(
                #     className="pane pane-table",
                #     children=dash_table.DataTable(
                #                             id="table_school",
                #                             page_size=400,
                #                             columns=[
                #                                 {'id': 'university', 'name': 'Top Destination Universities'},
                #                                 {'id': 'count', 'name': 'Count'},
                #                             ],
                #                             style_header={
                #                                 'textAlign': 'center',
                #                                 'fontWeight': 'bold',
                #                             },
                #                             style_cell={
                #                                 'textAlign': 'center',
                #                                 'fontFamily': 'Verdana',
                #                                 'paddingRight': '0.5rem',
                #                             },
                #                             style_cell_conditional=[{
                #                                 'if': {'column_id': 'count'},
                #                                 'textAlign': 'right'
                #                             }],
                #                             style_data={
                #                                 'whiteSpace': 'normal',
                #                                 'height': 'auto',
                #                             },
                #                             style_data_conditional=[{
                #                                 "if": {"state": "selected"},
                #                                 "backgroundColor": "inherit !important",
                #                                 "border": "inherit !important",
                #                             }],
                #                             style_table={
                #                                 'padding-top': '.4rem',
                #                                 'padding-left': '0rem',
                #                                 'padding-right': '.4rem',
                #                                 'height': '250',
                #                                 'width': '600',
                #                             }
                #                         ),
                # ),
                html.Div(
                    className="pane",
                    children=dcc.Graph(
                                    style=DEFAULT_GRAPH_STYLE,
                                    id='hist_year',
                                    figure={},
                                    responsive=True,
                                    config={'displayModeBar': False}
                                )
                ),
                html.Div(
                    className="pane",
                    children=dcc.Graph(
                                    style=DEFAULT_GRAPH_STYLE,
                                    id='hist_country',
                                    figure={},
                                    responsive=True,
                                    config={'displayModeBar': False}
                                )
                ),
                html.Div(
                    className="pane",
                    children=dcc.Graph(
                                    style=DEFAULT_GRAPH_STYLE,
                                    id='hist_school',
                                    figure={},
                                    responsive=True,
                                    config={'displayModeBar': False}
                                )
                ),
            ]
        ),
        html.Footer(
            children=[
                html.Span(
                    "Project Link: "
                ),
                html.A(
                    className='footer-item',
                    href='https://github.com/grceliu/ntu-exchange-analysis-eng',
                    target='_blank',
                    children=[
                        html.Img(
                            src='assets/GitHub-Mark-120px-plus.png',
                            height='15',
                            width='15',
                        ),
                    ]
                ),
                html.Span(
                    "    | © 2021 Grace Liu",
                ),
            ]
        )
])
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='one_sem_pct', component_property='children'),
     Output(component_id='num_students', component_property='children'),
     Output(component_id='num_countries', component_property='children'),
     Output(component_id='num_schools', component_property='children'),
     Output(component_id='hist_year', component_property='figure'),
     Output(component_id='hist_country', component_property='figure'),
     Output(component_id='hist_school', component_property='figure'),
     # Output(component_id='table_school', component_property='data'),
     ],
    [Input(component_id='slct_year', component_property='value'),
     Input(component_id='slct_department', component_property='value')]
)
def update_graph(slct_year, slct_department):
    # dataframe
    dff = df.copy()
    if not slct_department:
        slct_department = ''
        dff = dff[(dff["school_year"]>=slct_year[0]) & (dff["school_year"]<=slct_year[1])]
    else:
        dff = dff[(dff["school_year"]>=slct_year[0]) & (dff["school_year"]<=slct_year[1]) & (dff["department"]==slct_department)]

    if len(dff) > 0:
        one_sem_pct = int(round((len(dff[dff["num_of_sems"]==1]) / len(dff))*100))
    else:
        one_sem_pct = 0

    num_students = len(dff)
    num_countries = dff["country"].nunique()
    num_schools = dff['university'].nunique()

    fig_year = px.histogram(dff, x="school_year", title="Number of Exchange Students".format(slct_department), color_discrete_sequence=[MAIN_COLOR], nbins=len(years))
    fig_year.update_layout(bargap=0.2, title=DEFAULT_GRAPH_TITLE_POSITION, margin=DEFAULT_GRAPH_MARGIN)
    fig_year.update_xaxes(fixedrange=True)
    fig_year.update_yaxes(fixedrange=True)

    country_dff = dff.groupby('country').count().sort_values('university').iloc[-10:,1].reset_index()
    country_dff.columns = ['country', 'count']
    fig_country = px.bar(country_dff, x='count', y='country', orientation='h', title="Top 10 Destination Countries".format(slct_department), color_discrete_sequence=[MAIN_COLOR])
    fig_country.update_traces(
        textposition='inside',
        hovertemplate = "country=%{y}<br>count=%{x}"
    )
    fig_country.update_layout(title=DEFAULT_GRAPH_TITLE_POSITION, margin=DEFAULT_GRAPH_MARGIN)
    fig_country.update_yaxes(tickfont=dict(size=10, family='Verdana'), fixedrange=True)
    fig_country.update_xaxes(fixedrange=True)

    school_dff = dff.groupby('university').count().sort_values('country').iloc[-10:,1].reset_index()
    school_dff.columns = ['university', 'count']
    fig_school = px.bar(school_dff, x='count', y='university', orientation='h', title="Top 10 Destination Universities".format(slct_department), color_discrete_sequence=[MAIN_COLOR])
    fig_school.update_traces(
        textposition='inside',
        hovertemplate = "university=%{y}<br>count=%{x}"
    )
    fig_school.update_layout(title=DEFAULT_GRAPH_TITLE_POSITION, margin=DEFAULT_GRAPH_MARGIN)
    fig_school.update_yaxes(tickfont=dict(size=10, family='Verdana'), fixedrange=True)
    fig_school.update_xaxes(fixedrange=True)

    return one_sem_pct, num_students, num_countries, num_schools, fig_year, fig_country, fig_school#, school_df

if __name__ == '__main__':
    app.run_server(debug=True)
