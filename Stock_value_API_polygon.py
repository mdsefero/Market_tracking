import pandas as pd
import plotly.graph_objects as go
import pickle, os 
import requests



# Polygon API configuration
def get_api(): 
    with open ('API.txt', r) as f: 
        return f.read()

api_key = get_api()
base_url = "https://api.polygon.io/v2"
ticker = 'MSFT'
#ticker = 'I:SPX'
#ticker = 'I:DJI'


#attempts to use already downloaded data if it exists, if not, downloads and saves
def get_data(ticker):
    file_path = 'SP500_data.pkl'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            df = pickle.load(f)
    else:
        # Define the API endpoint and parameters - essentiallu building URL
        endpoint = f"/aggs/ticker/{ticker}/range/1/day/1981-07-03/2023-05-22"  # set date range here
        params = {
            "apiKey": api_key,
            "unadjusted": "false"
        }
        # Make the API request
        response = requests.get(base_url + endpoint, params=params) 
        # Extract data from the response
        data = response.json()#["results"]
        results = data["results"]
        # Create a DataFrame from the historical data
        df = pd.DataFrame(results)
        df = df.rename(columns={"t": "timestamp", "c": "close"})
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df = df.set_index("timestamp")
        
        with open(file_path, 'wb') as f:  #saves data for next time
            pickle.dump(df, f)
    return df


def shade_days(fig, column, color):
    for i in df[df[column]].index:
        fig.add_shape(
            dict(
                type="rect",
                xref="x",
                yref="paper",
                x0=i,
                y0=0,
                x1=i + pd.Timedelta(days=1),
                y1=1,
                fillcolor=color,
                opacity=0.5,
                layer="below",
                line_width=0,
            )
        )
    return fig


# MAIN CODE
df = get_data(ticker)

df['run_max'] = df['close'].cummax()
df['90_percent_of_run_max'] = df['run_max'] * 0.9
df['Correction'] = df['close'] < df['90_percent_of_run_max']
df['80_percent_of_run_max'] = df['run_max'] * 0.8
df['Bear'] = df['close'] < df['80_percent_of_run_max']

# Create the figure
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['close'], name='S&P Historical'))
fig.update_layout(xaxis_title='Date', yaxis_title='Index/Price')

fig = shade_days(fig, 'Correction', 'orange')
fig = shade_days(fig, 'Bear', 'red')

fig.update_layout(showlegend=True)
fig.show()

# You can print the result
df.to_csv('SP500_data.csv')