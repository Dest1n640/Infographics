from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

df = px.data.gapminder()

numeric_cols =['pop', 'lifeExp', 'gdpPercap']
available_countries = df['country'].unique()
years = df['year'].unique()

app = Dash(__name__)
server = app.server 

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'}, children=[
    html.H1("Расширенный дашборд Gapminder", style={'textAlign': 'center'}),
    
    # БЛОК 1: Линейный график (2 элемента управления: страны, мера Y)
    html.Div(style={'backgroundColor': '#f9f9f9', 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '20px'}, children=[
        html.H3("1. Сравнение динамики стран (Линейный график)"),
        html.Div([
            html.Div([
                html.Label("Элемент 1: Выберите страны (Multi-select)"),
                dcc.Dropdown(
                    options=[{'label': c, 
                   'value': c} for c in available_countries],
                    value=['Canada', 'United States', 'Mexico'], # Значения по умолчанию
                    multi=True
                )
            ], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([
                html.Label("Элемент 2: Выберите ось Y"),
                dcc.Dropdown(
                    id='line-y-dropdown',
                    options=[{'label': col, 'value': col} for col in numeric_cols],
                    value='gdpPercap'
                )
            ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),
        ]),
        dcc.Graph(id='line-chart')
    ]),

    # КРОСС-ФИЛЬТР: Слайдер выбора года для пунктов 3, 4 и 5
    html.Div(style={'backgroundColor': '#eef5ff', 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '20px'}, children=[
        html.H3("Элемент 3: Кросс-фильтр по годам (влияет на графики ниже)"),
        dcc.Slider(
            id='year-slider',
            min=years.min(),
            max=years.max(),
            step=None,
            marks={str(year): str(year) for year in years},
            value=years.max()
        )
    ]),
html.Div(style={'backgroundColor': '#f9f9f9', 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '20px'}, children=[
        html.H3("2. Пузырьковая диаграмма по странам"),
        html.Div([
            html.Div([
                html.Label("Элемент 4: Ось X"),
                dcc.Dropdown(id='bubble-x', options=[{'label': c, 'value': c} for c in numeric_cols], value='gdpPercap')
            ], style={'width': '32%', 'display': 'inline-block'}),
            html.Div([
                html.Label("Элемент 5: Ось Y"),
                dcc.Dropdown(id='bubble-y', options=[{'label': c, 'value': c} for c in numeric_cols], value='lifeExp')
            ], style={'width': '32%', 'display': 'inline-block', 'marginLeft': '2%'}),
            html.Div([
                html.Label("Элемент 6: Размер пузырька"),
                dcc.Dropdown(id='bubble-size', options=[{'label': c, 'value': c} for c in numeric_cols], value='pop')
            ], style={'width': '32%', 'display': 'inline-block', 'float': 'right'})
        ]),
        dcc.Graph(id='bubble-chart')
    ]),

    # БЛОК 3: Bar-chart (Топ-15) и Круговая диаграмма
    html.Div([
        html.Div(style={'width': '48%', 'display': 'inline-block', 'backgroundColor': '#f9f9f9', 'padding': '10px', 'borderRadius': '10px'}, children=[
            html.H3("3. Топ-15 стран по населению"),
            dcc.Graph(id='bar-chart')
        ]),
        html.Div(style={'width': '48%', 'display': 'inline-block', 'float': 'right', 'backgroundColor': '#f9f9f9', 'padding': '10px', 'borderRadius': '10px'}, children=[
            html.H3("4. Распределение населения по континентам"),
            dcc.Graph(id='pie-chart')
        ])
    ])
])


# Callback для линейного графика (Пункты 1 и 2)
@app.callback(
    Output('line-chart', 'figure'),[Input('country-dropdown', 'value'),
     Input('line-y-dropdown', 'value')]
)
def update_line_chart(selected_countries, y_axis):
    if not selected_countries:
        return px.line(title="Пожалуйста, выберите хотя бы одну страну")
    
    filtered_df = df[df['country'].isin(selected_countries)]
    fig = px.line(filtered_df, x='year', y=y_axis, color='country', markers=True, title=f"Динамика: {y_axis}")
    return fig

@app.callback([Output('bubble-chart', 'figure'),
     Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure')], [Input('year-slider', 'value'),
     Input('bubble-x', 'value'),
     Input('bubble-y', 'value'),
     Input('bubble-size', 'value')])
def update_year_based_charts(selected_year, bub_x, bub_y, bub_size):
    # Фильтруем данные по выбранному году из слайдера
    filtered_df = df[df['year'] == selected_year]

    # 1. Пузырьковая диаграмма
    fig_bubble = px.scatter(
        filtered_df, x=bub_x, y=bub_y, size=bub_size, color='continent',
        hover_name='country', size_max=60, title=f"Связь {bub_x} и {bub_y} ({selected_year} г.)"
    )

    # 2. Bar Chart (Топ-15 стран по популяции)
    top_15_df = filtered_df.sort_values('pop', ascending=False).head(15)
    fig_bar = px.bar(
        top_15_df, x='country', y='pop', color='continent',
        title=f"Топ-15 стран ({selected_year} г.)"
    )
    fig_bar.update_layout(xaxis_tickangle=-45)

    # 3. Круговая диаграмма (Популяция по континентам)
    fig_pie = px.pie(
        filtered_df, values='pop', names='continent', hole=0.3,
        title=f"Континенты ({selected_year} г.)"
    )

    return fig_bubble, fig_bar, fig_pie

if __name__ == '__main__':
    app.run(debug=True)
