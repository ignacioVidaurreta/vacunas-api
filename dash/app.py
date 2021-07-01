import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

df = pd.read_csv("vacunas.csv")
geo = gpd.read_file("provincias_argentinas_polygon.geojson")
print(geo[:5])

# choropleth map
fig = px.choropleth(
    data_frame=df,
    geojson=geo,
    locations="jurisdiccion_codigo_indec",
    featureidkey="properties.c_indec",
    color="primera_dosis_cantidad",
    color_continuous_scale="Mint",
)
fig.update_geos(
    showcountries=False,
    showcoastlines=False,
    showland=False,
    fitbounds="locations",
    visible=False,
    lataxis_range=[0, 0],
    projection={"type": "natural earth"},
)
fig.update_layout(
    # margin={"r": 0, "t": 0, "l": 0, "b": 0},
    plot_bgcolor="rgba(0, 0, 0, 0)",
    paper_bgcolor="rgba(0, 0, 0, 0)",
    margin=dict(t=0, r=0, l=0),
    height=650,
    geo=dict(bgcolor="rgba(0,0,0,0)"),
)


# barchart porcentaje vacunas
vac = ["Sputkin", "Sino", "Astra", "CoviShield"]
porc = [50, 30, 20, 10]
df2 = pd.DataFrame({"x": vac, "y": porc})
fig2 = px.bar(
    df2,
    y="y",
    x="x",
    text="y",
    color="y",
    custom_data=["x", "y"],
)

fig2.update_traces(
    textposition="outside",
    hovertemplate="%{x} <br>Porcentaje: %{y}% </br> ",
    texttemplate="%{y}%",
    marker_color=["#FFF1E6", "#FAD2E1", "#BEE1E6", "#CDDAFD"],
)
fig2.update_layout(
    uniformtext_minsize=8,
    uniformtext_mode="hide",
    plot_bgcolor="rgba(0, 0, 0, 0)",
    paper_bgcolor="rgba(0, 0, 0, 0)",
    xaxis_title="",
    autosize=True,
    margin={"r": 0, "t": 10, "l": 0, "b": 0},
    width=450,
)
fig2.update_yaxes(visible=False, showticklabels=False)
fig2.update(layout_coloraxis_showscale=False)


# Horizontal Bar chart

top_labels = [
    "2 Dosis",
    "1 Dosis",
    "Nada",
]

colors = [
    "rgba(38, 24, 74, 0.8)",
    "rgba(71, 58, 131, 0.8)",
    "rgba(142, 140, 171, 0.8)",
]

x_data = [
    [10, 20, 70],
]

y_data = [
    "Vacunados",
]

fig3 = go.Figure()

for i in range(0, len(x_data[0])):
    for xd, yd in zip(x_data, y_data):
        fig3.add_trace(
            go.Bar(
                x=[xd[i]],
                y=[yd],
                orientation="h",
                marker=dict(
                    color=colors[i], line=dict(color="rgb(248, 248, 249)", width=0.5)
                ),
                hoverinfo="none",
            )
        )

fig3.update_layout(
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
        domain=[0.15, 1],
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
    ),
    barmode="stack",
    plot_bgcolor="rgba(0, 0, 0, 0)",
    paper_bgcolor="rgba(0, 0, 0, 0)",
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    showlegend=False,
    height=200,
)
fig3.update_traces(dict(hoverinfo="skip"))

annotations = []

for yd, xd in zip(y_data, x_data):
    # labeling the y-axis
    annotations.append(
        dict(
            xref="paper",
            yref="y",
            x=0.14,
            y=yd,
            xanchor="right",
            text=str(yd),
            font=dict(family="Arial", size=14, color="rgb(67, 67, 67)"),
            showarrow=False,
            align="right",
        )
    )
    # labeling the first percentage of each bar (x_axis)
    annotations.append(
        dict(
            xref="x",
            yref="y",
            x=xd[0] / 2,
            y=yd,
            text=str(xd[0]) + "%",
            font=dict(family="Arial", size=14, color="rgb(248, 248, 255)"),
            showarrow=False,
        )
    )
    # labeling the first Likert scale (on the top)
    if yd == y_data[-1]:
        annotations.append(
            dict(
                xref="x",
                yref="paper",
                x=xd[0] / 2,
                y=1.1,
                text=top_labels[0],
                font=dict(family="Arial", size=14, color="rgb(67, 67, 67)"),
                showarrow=False,
            )
        )
    space = xd[0]
    for i in range(1, len(xd)):
        # labeling the rest of percentages for each bar (x_axis)
        annotations.append(
            dict(
                xref="x",
                yref="y",
                x=space + (xd[i] / 2),
                y=yd,
                text=str(xd[i]) + "%",
                font=dict(family="Arial", size=14, color="rgb(248, 248, 255)"),
                showarrow=False,
            )
        )
        # labeling the Likert scale
        if yd == y_data[-1]:
            annotations.append(
                dict(
                    xref="x",
                    yref="paper",
                    x=space + (xd[i] / 2),
                    y=1.1,
                    text=top_labels[i],
                    font=dict(family="Arial", size=14, color="rgb(67, 67, 67)"),
                    showarrow=False,
                )
            )
        space += xd[i]

fig3.update_layout(annotations=annotations)


# line chart dates
data = {
    "Date": ["2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04"],
    "Total": [45, 65, 75, 73],
    "Sputnik": [10, 20, 30, 30],
    "Aztra": [10, 10, 15, 13],
    "Sino": [20, 20, 23, 25],
    "Shiel": [5, 15, 7, 10],
}

df = px.data.stocks()
df4 = pd.DataFrame(data)
print(df)
print(df4)
fig4 = px.line(
    df4,
    x="Date",
    y=df4.columns,
    hover_data={"Date": "|%B %d, %Y"},
    color_discrete_map={
        "Total": "grey",
        "Sino": "#FAD2E1",
        "Aztra": "#BEE1E6",
        "Shiel": "#CDDAFD",
        "Sputnik": "#FFF1E6",
    },
)
fig4.update_xaxes(dtick="M1", tickformat="%d %B %Y")
fig4.update_traces(mode="markers+lines", hovertemplate=None, line=dict(width=3))
fig4.update_layout(
    hovermode="x unified",
    plot_bgcolor="rgba(0, 0, 0, 0)",
    paper_bgcolor="rgba(0, 0, 0, 0)",
    margin=dict(t=0, r=0, l=0, b=0),
    xaxis_title="",
    yaxis_title="Cantidad",
)


# dashboard!
app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.P(children="💉", className="header-emoji"),
                html.H1(
                    children="Vacunación COVID-19 Argentina", className="header-title"
                ),
                html.P(
                    children="Final para la Materia Visualización de la Información - ITBA - Lautaro Pinilla, Nacho Vidaurreta y Micaela Banfi",
                    className="header-description",
                ),
            ],
            id="header",
            className="header row flex-display ",
            style={"marginBottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="choropleth", figure=fig)],
                    className="pretty_container four columns",
                    id="choropleth-map",
                ),
                html.Div(
                    [
                        html.Div(
                            html.Div(
                                html.P(
                                    children="Aplicaciónes por vacuna en el Pais",
                                ),
                                id="tittle",
                                className="row container-display",
                                style={
                                    "fontSize": "30px",
                                    "fontWeight": "bold",
                                    "textAlign": "center",
                                },
                            ),
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P(children="AstraZeneca", id="az"),
                                        html.P(
                                            children="122341",
                                            style={"textAlign": "center"},
                                        ),
                                    ],
                                    className="mini_container",
                                    style={"background": "#BEE1E6"},
                                ),
                                html.Div(
                                    [
                                        html.P(children="COVISHIELD"),
                                        html.P(
                                            children="1234565",
                                            style={"textAlign": "center"},
                                        ),
                                    ],
                                    className="mini_container",
                                    style={"background": "#CDDAFD"},
                                ),
                                html.Div(
                                    [
                                        html.P(children="Sinopharm"),
                                        html.P(
                                            children="12345567",
                                            style={"textAlign": "center"},
                                        ),
                                    ],
                                    className="mini_container",
                                    style={"background": "#FAD2E1"},
                                ),
                                html.Div(
                                    [
                                        html.P(children="Sputnik V"),
                                        html.P(
                                            children="12345567",
                                            id="sv",
                                            style={"textAlign": "center"},
                                        ),
                                    ],
                                    className="mini_container",
                                    style={"background": "#FFF1E6"},
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="barchart", figure=fig2)],
                            id="vaccines",
                            className="row container-display",
                        ),
                    ],
                    id="right-column",
                    className="pretty_container columns",
                    style={"width": "50%"},
                ),
            ],
            className="container-display ",
        ),
        html.Div(
            [
                html.Div(
                    html.P(
                        children="Cantidad vacunas aplicadas por dia",
                        style={"marginBottom": "0px"},
                    ),
                    style={
                        "fontSize": "30px",
                        "fontWeight": "bold",
                        "textAlign": "center",
                    },
                ),
                html.Div(
                    [dcc.Graph(id="line_chart", figure=fig4)],
                    id="line",
                    className="row container-display",
                ),
            ],
            className="pretty_container  columns",
            style={"width": "100%"},
        ),
        html.Div(
            [
                html.Div(
                    html.P(children="Dosis Aplicadas", style={"marginBottom": "0px"}),
                    style={
                        "fontSize": "30px",
                        "fontWeight": "bold",
                        "textAlign": "center",
                    },
                ),
                html.Div(
                    [dcc.Graph(id="stack_barchart", figure=fig3)],
                    id="stack",
                    className="row container-display",
                ),
            ],
            className="pretty_container  columns",
            style={"width": "50%"},
        ),
        html.Div(
            [
                html.Div(
                    html.P(
                        children="Final",
                        className="header-description",
                    ),
                    className="pretty_container seven columns",
                ),
                html.Div(
                    html.P(
                        children="Final",
                        className="header-description",
                    ),
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flexDirection": "column"},
)


app.run_server(debug=True)
