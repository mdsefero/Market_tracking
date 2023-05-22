import pandas as pd
import plotly.graph_objects as go


def get_data():
    file_path = 'historical_SPdata.csv'
    df = pd.read_csv(file_path, parse_dates=True, index_col='date')
    for col in df.columns:
        df[col] = df[col].str.replace(',', '').astype(float)
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

# Obtain historical data (saved as csv) 
df = get_data()
start_date = pd.to_datetime('1981-07-03')
df = df[df.index >= start_date]
df = df.sort_index(ascending=True)

# Calculate the trailing average to plot
trailing_average = df['close'].rolling(window='21D').mean()

df['run_max'] = df['close'].cummax()
df['90_percent_of_run_max'] = df['run_max'] * 0.9
df['Correction'] = df['close'] < df['90_percent_of_run_max']
df['80_percent_of_run_max'] = df['run_max'] * 0.8
df['Bear'] = df['close'] < df['80_percent_of_run_max']
df['200D_average'] = df['close'].rolling(window='200D').mean()
df['Bull'] = df['close'] > df['200D_average']

# Create the figure
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['close'], name='S&P500'))
fig.add_trace(go.Scatter(x=trailing_average.index, y=trailing_average, name='21d Trailing Average'))
fig.update_layout(xaxis_title='Date', yaxis_title='Index')

fig = shade_days(fig, 'Correction', 'orange')
fig = shade_days(fig, 'Bear', 'red')
fig = shade_days(fig, 'Bull', 'green')

fig.update_layout(showlegend=True)
fig.show()

#Save processed data
df.to_csv('SP500_data.csv')