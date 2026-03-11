import dash
from dash import dcc, html, dash_table, Input, Output
import pandas as pd
import plotly.express as px

# 1. Carga y limpieza de datos
df_detalle = pd.read_csv('/Users/leonmiguelramoscorchado/Documents/GitHub/ISIC_Big-Data/Unidad_2/003_Dashboard/dashboard_inventarios_utiles_detalle.csv')
df_resumen = pd.read_csv('/Users/leonmiguelramoscorchado/Documents/GitHub/ISIC_Big-Data/Unidad_2/003_Dashboard/dashboard_inventarios_utiles_resumen.csv')

# Asegurar formato de fecha
df_detalle['Fecha'] = pd.to_datetime(df_detalle['Fecha'])

# Inicializar la App
app = dash.Dash(__name__)

# 2. Diseño de la Interfaz (Layout)
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'}, children=[
    html.H1("Dashboard de Inventarios y Útiles Escolares", style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    html.Div([
        html.Label("Filtrar por Marca:"),
        dcc.Dropdown(
            id='marca-filter',
            options=[{'label': i, 'value': i} for i in df_detalle['Marca'].unique()],
            value=df_detalle['Marca'].unique()[0],
            clearable=False
        ),
    ], style={'width': '30%', 'marginBottom': '20px'}),

    html.Div([
        # Gráfico de Ventas por Nivel
        html.Div([
            dcc.Graph(id='ventas-nivel-graph')
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        # Gráfico de Tendencia Semanal
        html.Div([
            dcc.Graph(id='tendencia-semanal-graph')
        ], style={'width': '48%', 'display': 'inline-block'}),
    ]),

    html.Hr(),

    html.H3("Detalle de Inventarios Actuales"),
    dash_table.DataTable(
        id='table-detalle',
        columns=[{"name": i, "id": i} for i in df_detalle.columns],
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '10px'},
        style_header={'backgroundColor': '#34495e', 'color': 'white', 'fontWeight': 'bold'}
    )
])

# 3. Lógica Dinámica (Callbacks)
@app.callback(
    [Output('ventas-nivel-graph', 'figure'),
     Output('tendencia-semanal-graph', 'figure'),
     Output('table-detalle', 'data')],
    [Input('marca-filter', 'value')]
)
def update_dashboard(marca_seleccionada):
    # Filtrar detalle por marca
    filtered_df = df_detalle[df_detalle['Marca'] == marca_seleccionada]
    
    # Gráfico 1: Ventas totales por Nivel Escolar
    fig_ventas = px.bar(
        filtered_df.groupby('Nivel_Escolar')['Ventas'].sum().reset_index(),
        x='Nivel_Escolar', y='Ventas',
        title=f"Ventas Totales por Nivel - {marca_seleccionada}",
        color_discrete_sequence=['#3498db']
    )

    # Gráfico 2: Evolución de Inventario Final (del resumen general)
    fig_tendencia = px.line(
        df_resumen, 
        x='Semana', y='Inventario_Final', color='Nivel_Escolar',
        title="Tendencia de Inventario Final por Semana (General)",
        markers=True
    )

    return fig_ventas, fig_tendencia, filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run(debug=True)