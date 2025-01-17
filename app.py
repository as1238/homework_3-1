import dash
import html as html
import plotly.graph_objects as go
import dash_loading_spinners as dls
from dash_bootstrap_components._components.Container import Container
import dash_bootstrap_components as dbc
import time
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from ibapi.contract import Contract
from fintech_ibkr import *
import pandas as pd

# Make a Dash app!
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
server = app.server
# Define the layout.
MY_LOGO = "https://cdn-icons.flaticon.com/png/512/3594/premium/3594288.png?token=exp=1647974831~hmac=03c2daf16b6b2e58cb9d380766048d61"
#MY_LOGO = "https://cdn-icons.flaticon.com/png/512/4486/premiu…=1647974831~hmac=e13c6d501748ec4c8a17902f15278640"
app.layout = html.Div([
    #Message Alert
    html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader(
                        dbc.ModalTitle("Error Message"), close_button=False
                    ),
                    dbc.ModalBody(
                        "This should be an error but i couldn't connect it to the timeout."
                    ),
                    dbc.ModalFooter(dbc.Button("Close", id="close-dismiss")),
                ],
                id="modal-dismiss",
                keyboard=False,
                backdrop="static",
            ),
        ],
    ),
    #Navigation Bar
    dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=MY_LOGO, height="45px")),
                        dbc.Col(dbc.NavbarBrand("Fxtronata", className="ms-2")),
                    ],
                    align="right",
                    className="g-0",
                ),
                href="https://fxtronata.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                #search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
),

    # Section title
    html.H2("Section 1: Fetch & Display exchange rate historical data"),
    html.Br(),
    html.H6("Select value for whatToShow:"),
    html.Div(
        dcc.Dropdown(
            ["TRADES", "MIDPOINT", "BID", "ASK", "BID_ASK", "ADJUSTED_LAST",
             "HISTORICAL_VOLATILITY", "OPTION_IMPLIED_VOLATILITY", 'REBATE_RATE',
             'FEE_RATE', "YIELD_BID", "YIELD_ASK", 'YIELD_BID_ASK', 'YIELD_LAST',
             "SCHEDULE"],
            "MIDPOINT",
            id='what-to-show'
        ),
        style={'width': '365px'}
    ),
    html.Br(),
    # useRTH, Whether (1) or not (0) to retrieve data generated only within
    # Regular Trading Hours (RTH)
    html.H6("Select value for Regular Trading Hours (RTH):"),
    html.Div(
        dcc.RadioItems(id='user-RTH', options=[
            {'label': 'True', 'value': True},
            {'label': 'False', 'value': False}
        ],
                       value=True),

    ),
    html.Br(),
    html.H6("Select value for endDateTime:"),
    html.Div(
        children=[
            html.P("You may select a specific endDateTime for the call to" + \
            "fetch_historical_data. If any of the below is left empty, " + \
                   "the current present moment will be used.")
        ],
        style={'width': '565px'}
    ),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Label('Date:'),
                    dcc.DatePickerSingle(id='edt-date')
                ],
                style={
                    'display': 'inline-block',
                    'margin-right': '20px',
                }
            ),
            html.Div(
                children=[
                    html.Label('Hour:'),
                    dcc.Dropdown(list(range(24)), id='edt-hour'),
                ],
                style={
                    'display': 'inline-block',
                    'padding-right': '5px'
                }
            ),
            html.Div(
                children=[
                    html.Label('Minute:'),
                    dcc.Dropdown(list(range(60)), id='edt-minute'),
                ],
                style={
                    'display': 'inline-block',
                    'padding-right': '5px'
                }
            ),
            html.Div(
                children=[
                    html.Label('Second:'),
                    dcc.Dropdown(list(range(60)), id='edt-second'),
                ],
                style={'display': 'inline-block'}
            )
        ]
    ),
    html.Br(),
    html.H6("Select value for Bar size of the candle :"),
    html.Div(
        dcc.Dropdown(
            ["1 secs", "5 secs", "10 secs", "15 secs", "30 secs",
             "1 min", "2 mins", "3 mins", "5 mins", "10 mins", "15 mins", "20 mins",
             "30 mins", "1 hour", "2 hours", "3 hours", "4 hours", "8 hours",
             "1 day", "1 week", "1 month"], "1 hour",
            id='bar-size'
        ),
        style={'width': '100px'}
    ),
    html.Br(),
    html.H6("Select value for Duration of the plot (D=day, W=Week, M=Month, Y=Year) :"),
    html.Div(
        dcc.Dropdown(
            ["10 D", "20 D", "30 D", "1 W", "2 W",
             "3 W", "1 M", "3 M", "6 M", "1 Y", "5 Y"], "30 D",
            id='duration-str'
        ),
        style={'width': '100px'}
    ),
    html.Br(),
    html.H6("Enter a currency pair:"),
    html.P(
        children=[
            "See the various currency pairs here: ",
            html.A(
                "currency pairs",
                href='https://www.interactivebrokers.com/en/index.php?f=2222&exch=ibfxpro&showcategories=FX'
            )
        ]
    ),
    # Currency pair text input, within its own div.
    html.Div(
        # The input object itself
        ["Input Currency: ", dcc.Input(
            id='currency-input', value='USD.JPY', type='text'
        )],
        # Style it so that the submit button appears beside the input.
        style={'display': 'inline-block', 'padding-top': '5px'}
    ),
    # Submit button
    dbc.Button('Submit', id='submit-button',outline=True, color="success", className="me-1", n_clicks=0),
    # Line break
    html.Br(),
    # Div to hold the initial instructions and the updated info once submit is pressed
    html.Div(id='currency-output', children='Enter a currency code and press submit'),
    # Div to hold the candlestick graph
    dbc.Row(dbc.Col(dbc.Spinner([dcc.Graph(id='candlestick-graph')],
             #color="#435278",
            color="success",
            size=100,
            fullscreen=False,))
                    ),

    # html.Div([dcc.Graph(id='candlestick-graph')]),
    # Another line break
    html.Br(),
    # Section title
    html.H6("Make a Trade"),
    # Div to confirm what trade was made
    html.Div(id='trade-output'),
    # Radio items to select buy or sell
    dcc.RadioItems(
        id='buy-or-sell',
        options=[
            {'label': 'BUY', 'value': 'BUY'},
            {'label': 'SELL', 'value': 'SELL'}
        ],
        value='BUY'
    ),
    # Text input for the currency pair to be traded
    dcc.Input(id='trade-currency', value='AUDCAD', type='text'),
    # Numeric input for the trade amount
    dcc.Input(id='trade-amt', value='20000', type='number'),
    # Submit button for the trade
    html.Button('Trade', id='trade-button', n_clicks=0)

])


# Callback for what to do when submit-button is pressed
@app.callback(
    [  # there's more than one output here, so you have to use square brackets to pass it in as an array.
        Output(component_id='currency-output', component_property='children'),
        Output(component_id='candlestick-graph', component_property='figure'),
        #Output(component_id='confirm-danger', component_property='alert')
    ],
    [Input('submit-button', 'n_clicks'),

     ],
    # The callback function will
    # fire when the submit button's n_clicks changes
    # The currency input's value is passed in as a "State" because if the user is typing and the value changes, then
    #   the callback function won't run. But the callback does run because the submit button was pressed, then the value
    #   of 'currency-input' at the time the button was pressed DOES get passed in.
    [State('currency-input', 'value'), State('what-to-show', 'value'),
     State('edt-date', 'date'), State('edt-hour', 'value'),
     State('edt-minute', 'value'), State('edt-second', 'value'),
     State('user-RTH', 'value'), State('bar-size', 'value'), State('duration-str', 'value')]

)
def update_candlestick_graph(n_clicks, currency_string, what_to_show,
                             edt_date, edt_hour, edt_minute, edt_second, user_RTH, bar_size, duration_str):
    # print(currency_string)
    #try:
        time.sleep(3)
        # n_clicks doesn't
        # get used, we only include it for the dependency.

        if any([i is None for i in [edt_date, edt_hour, edt_minute, edt_second]]):
            endDateTime = ''
        else:
            print(edt_date, edt_hour, edt_minute, edt_second)

        # First things first -- what currency pair history do you want to fetch?
        # Define it as a contract object!
        contract = Contract()
        contract.symbol = currency_string.split(".")[0]
        contract.secType = 'CASH'
        contract.exchange = 'IDEALPRO'  # 'IDEALPRO' is the currency exchange.
        contract.currency = currency_string.split(".")[1]

        ############################################################################
        ############################################################################
        # This block is the one you'll need to work on. UN-comment the code in this
        #   section and alter it to fetch & display your currency data!
        # Make the historical data request.
        # Where indicated below, you need to make a REACTIVE INPUT for each one of
        #   the required inputs for req_historical_data().
        # This resource should help a lot: https://dash.plotly.com/dash-core-components

        # Some default values are provided below to help with your testing.
        # Don't forget -- you'll need to update the signature in this callback
        #   function to include your new vars!
        cph = fetch_historical_data(
            contract=contract,
            endDateTime='',
            durationStr=duration_str,  # <-- make a reactive input
            barSizeSetting=bar_size,  # <-- make a reactive input
            whatToShow=what_to_show,
            useRTH=user_RTH,
            # formatDate = 1, keepUpToDate = False, chartOptions = []
        )
        # # # Make the candlestick figure
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=cph['date'],
                    open=cph['open'],
                    high=cph['high'],
                    low=cph['low'],
                    close=cph['close']
                )
            ]
        )
        # # # Give the candlestick figure a title
        fig.update_layout(title=('Exchange Rate: ' + currency_string))
        ############################################################################
        ############################################################################

        ############################################################################
        ############################################################################
        # This block returns a candlestick plot of apple stock prices. You'll need
        # to delete or comment out this block and use your currency prices instead.
        # df = pd.read_csv(
        #     'https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv'
        # )
        # df = cph
        # fig = go.Figure(
        #     data=[
        #         go.Candlestick(
        #             x=df['date'],
        #             open=df['open'],
        #             high=df['high'],
        #             low=df['low'],
        #             close=df['close']
        #         )
        #     ]
        # )

        # currency_string = 'default Apple price data fetch'
        ############################################################################
        ############################################################################
        #if len(fetch_contract_details(contract)) == 0:
         #   return "Alert!!!"
        #else:
            # Return your updated text to currency-output, and the figure to candlestick-graph outputs
        return ('Submitted query for ' + currency_string), fig
    #except:

#Callback for the Navigation Bar
@app.callback(
    Output("modal-dismiss", "is_open"),
    [Input("submit-button", "n_clicks"), Input("close-dismiss", "n_clicks")],
    [State("modal-dismiss", "is_open")],
)
def toggle_modal(n_open, n_close, is_open):
    if n_open or n_close:
        return not is_open
    return is_open

# Callback for what to do when trade-button is pressed
@app.callback(
    # We're going to output the result to trade-output
    Output(component_id='trade-output', component_property='children'),
    # We only want to run this callback function when the trade-button is pressed
    Input('trade-button', 'n_clicks'),
    # We DON'T want to run this function whenever buy-or-sell, trade-currency, or trade-amt is updated, so we pass those
    #   in as States, not Inputs:
    [State('buy-or-sell', 'value'), State('trade-currency', 'value'), State('trade-amt', 'value')],
    # We DON'T want to start executing trades just because n_clicks was initialized to 0!!!
    prevent_initial_call=True
)
def trade(n_clicks, action, trade_currency, trade_amt):  # Still don't use n_clicks, but we need the dependency

    # Make the message that we want to send back to trade-output
    msg = action + ' ' + trade_amt + ' ' + trade_currency

    # Make our trade_order object -- a DICTIONARY.
    trade_order = {
        "action": action,
        "trade_currency": trade_currency,
        "trade_amt": trade_amt
    }

    # Return the message, which goes to the trade-output div's "children" attribute.
    return msg


# Run it!
if __name__ == '__main__':
    app.run_server(host='localhost', port=3001, debug=True)
