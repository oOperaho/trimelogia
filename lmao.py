from numpy import arange
import plotly.graph_objects as go
from dash import dcc, html, Input, Output, State, Dash
import dash_bootstrap_components as dbc

valoresX = arange(0, 10.1, .1)
valores = {"Qualitativa": 0, "Atividades": 0, "Parcial": 0, "Simulado": 0, "Conclusiva": 0}

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.FLATLY], meta_tags=[{'name':'viewport', 'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}])
server = app.server

def sety(valoresX, Qualitativa, Parcial, Atividades):
    z = []
    for x in range(0, len(valoresX)):
        y = (8 - 0.3 * Qualitativa - 0.21 * Parcial - 0.14 * Atividades - 0.175 * valoresX[x]) / 0.175
        if y < 0:
            z.append(0)
        elif y > 10:
            z.append(None)
        else:
            z.append(y)
    return z
def pegarvalor(textosR):
    textos = []
    textostatus = None
    valores2 = {"Qualitativa": True, "Atividades": True, "Parcial": True, "Simulado": True, "Conclusiva": True}
    for x in range(0, len(textosR)):
        textos.append(textosR[x])
        try:
            textos[x] = float(textos[x])
        except:
            if textos[x] == "" or textos[x] == None:
                textos[x] = 0
                valores2[list(valores2.keys())[x]] = False
        if textos[x] > 10 or textos[x] < 0:
            textostatus = "Valor inválido!"
            valores2[list(valores2.keys())[x]] = False
            textos[x] = 0
        valores[list(valores.keys())[x]] = textos[x]
    return [textostatus, valores, valores2]
def atualizarstatus(textostatus, valores, valores2):
    operadores = [(0.3 * valores["Qualitativa"]), (0.14 * valores["Atividades"]), (0.21 * valores["Parcial"]),
                  (0.175 * valores["Simulado"]), (0.175 * valores["Conclusiva"])]
    ordens = [(1, 2, 3, 4, 0.3), (0, 2, 3, 4, 0.14), (0, 1, 3, 4, 0.21), (0, 1, 2, 4, 0.175), (0, 1, 2, 3, 0.175),
              (0, 1, 2, 3, 4)]
    y = 0
    for x in range(0, 5):
        if list(valores2.values())[x] != False:
            y += 1
    if y < 4:
        textosituacao = "[Incerta]"
        textomedia = "?"
        textostatus = "Não é possível calcular uma nota \ncom os dados disponíveis."
    if y == 4:
        trollge = list(valores2.values()).index(False)
        notarestante = (8 - operadores[ordens[trollge][0]] - operadores[ordens[trollge][1]] - operadores[ordens[trollge][2]] - operadores[ordens[trollge][3]]) / ordens[trollge][4]
        if notarestante > 10.0:
            textosituacao = "[Reprovado]"
            textomedia = "<8"
            textostatus = "Os pontos que você tirou não \nsão suficientes pra passar, nem \nse tirar 10 na outra nota. :("
        elif notarestante <= 0.0:
            textosituacao = "[Aprovado]"
            textomedia = ">8"
            textostatus = "Os pontos que você tirou são \nsuficientes pra passar. :)"
        elif notarestante < 10.0:
            textosituacao = "[Incerto]"
            textomedia = "?"
            textostatus = f"Precisa-se de {notarestante:.2f} \nno(a) {list(valores.keys())[trollge]}."
    if y == 5:
        soma = (operadores[ordens[5][0]] + operadores[ordens[5][1]] + operadores[ordens[5][2]] + operadores[ordens[5][3]] + operadores[ordens[5][4]])
        textosituacao = f"[{'Reprovado' if soma < 8 else 'Aprovado'}]"
        textomedia = f"{soma:.3f}"
        textostatus = None
    return textosituacao, textomedia, textostatus

#grafico
fig = go.Figure()
fig.add_trace(go.Scatter(x=valoresX, y=sety(valoresX, valores["Qualitativa"], valores["Parcial"], valores["Atividades"])))

fig.update_xaxes(title_text="Conclusiva", range=[-1, 11])
fig.update_yaxes(title_text="Simulado", range=[-1, 11])
fig.update_layout(margin=dict(b=50, t=50, l=50, r=50))
fig.update_layout(title={"text": "Gráfico da nota necessária",})

########sliders
def slidergen(nomelmao):
    return html.Div(
        dcc.Slider(
        min=0,
        max=10,
        step=0.1,
        value=0,
        marks={0: "0", 10: "10"},
        tooltip={"placement": "right", "always_visible": True},
        id=f"{nomelmao.upper()}SLIDER"
        )
    )

sliders = []
for x in ["Qualitativa", "Atividades", "Parcial"]:
    sliders.append(slidergen(x))

graficosliders = [
    dbc.Col([
        dbc.Row(html.Div(dcc.Graph(figure=fig, id="GRAFICO"))),
        dbc.Row([
            dbc.Col(sliders[0], width=10),
            dbc.Col(html.Label("Qualitativa"), width=2)
        ]),
        dbc.Row([
            dbc.Col(sliders[1], width=10),
            dbc.Col(html.Label("Atividades"), width=2)
        ]),
        dbc.Row([
            dbc.Col(sliders[2], width=10),
            dbc.Col(html.Label("Parcial"), width=2)
        ]),
    ], style={"margin-left":"5%"})
]

########inputs
opsie=6
def linhavalor(nome):
    return dbc.Row(
        [
            dbc.Col(
                [
                    html.Label(f"{nome}")
                ],
                width=opsie,
                style={"background-color": "", "font-size":"150%", "text-align":"right", "padding-right":"1%"}
            ),
            dbc.Col(
                [
                    dbc.Input(type="number", min=0, max=10, step=0.1, id=f"{nome.upper()}INPUT"),
                ],
                width=opsie,
            )
        ],
        className="g-0",
        style={"margin-top":"1%"}
    )

inputs = []
for key, value in valores.items():
    inputs.append(linhavalor(key))

##########botão-output
textosbotao = dbc.Col([
    dbc.Row([
        dbc.Button("Calcular", style={"font-weight":"bold"}, id="BOTAOSUPREMO")
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row(html.Label("Situação")),
            dbc.Row(html.Label("Média"))
        ]),
        dbc.Col([
            dbc.Row(html.Label("?", id="NOTALMAO")),
            dbc.Row(html.Label("[Incerto]", id="SITUACAO"))
        ]),
    ], style={"background-color":"lightblue", "margin-top":"3%", "font-size":"120%", "text-align":"center"}),
    dbc.Row(html.Label("[Status]", id="STATUS"), style={"margin-top":"5%", "font-size":"120%", "text-align":"center"})
], width=opsie*2, style={"margin-top":"1%", "margin-bottom":"20%"})

#######display
grid = html.Div(
    [
        dbc.Row(html.H1("Trimelogia")),
        dbc.Row(html.A('Dúvidas e contato', href='https://docs.google.com/document/d/17-Gh2lBkhPswoL8pFfpeZZjfrT01U0Vz_l8IIQo6tqc/edit?usp=sharing')),
        dbc.Row([
            dbc.Col([
                dbc.Row(inputs),
                dbc.Row(textosbotao)
            ], xs=12, sm=12, md=6, lg=6, xl=6),
            dbc.Col(graficosliders, xs=12, sm=12, md=6, lg=6, xl=6),
        ]),
    ],
    style={"padding-left":"2%", "padding-right":"2%", "margin-top":"2%"}
)

@app.callback(
    Output(component_id="GRAFICO", component_property="figure"),
    Input(component_id="QUALITATIVASLIDER", component_property="value"),
    Input(component_id="ATIVIDADESSLIDER", component_property="value"),
    Input(component_id="PARCIALSLIDER", component_property="value"),
    prevent_initial_call=True
)
def update(aqlS, atvS, parS):
    fig.update_traces(y=sety(valoresX, aqlS, parS, atvS))
    return fig

@app.callback(
    [Output(component_id="NOTALMAO", component_property="children"),
    Output(component_id="SITUACAO", component_property="children"),
    Output(component_id="STATUS", component_property="children"),
    Output(component_id="QUALITATIVASLIDER", component_property="value"),
    Output(component_id="ATIVIDADESSLIDER", component_property="value"),
    Output(component_id="PARCIALSLIDER", component_property="value")],

    [Input(component_id="BOTAOSUPREMO", component_property="n_clicks")],

    [State(component_id="QUALITATIVAINPUT", component_property="value"),
     State(component_id="ATIVIDADESINPUT", component_property="value"),
     State(component_id="PARCIALINPUT", component_property="value"),
     State(component_id="SIMULADOINPUT", component_property="value"),
     State(component_id="CONCLUSIVAINPUT", component_property="value"),
     State(component_id="QUALITATIVASLIDER", component_property="value"),
     State(component_id="ATIVIDADESSLIDER", component_property="value"),
     State(component_id="PARCIALSLIDER", component_property="value")
     ],
    prevent_initial_call=True
)
def update(botao, aqlI, atvI, parI, simI, conI, AqlS, AtvS, ParS):
    textosR = [aqlI, atvI, parI, simI, conI]
    AqlS = aqlI
    AtvS = atvI
    ParS = parI
    return *atualizarstatus(pegarvalor(textosR)[0], pegarvalor(textosR)[1], pegarvalor(textosR)[2]), AqlS, AtvS, ParS

#######run
app.layout = html.Div([dbc.Container([grid], fluid=True)])
if __name__ == "__main__":
    app.run_server(debug=False)