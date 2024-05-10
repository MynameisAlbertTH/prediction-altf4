import streamlit as st
from datetime import date
import yfinance as yf 
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objects as go
import plotly.graph_objs as go
import streamlit.components.v1 as components
from prophet.plot import plot_plotly
import numpy as np






# เปลี่ยนแปลงพอร์ตเซิร์ฟเวอร์เมื่อมีการรัน Streamlit app
port = 8502
START = "2019-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title("Stock Prediction App")

stocks = ("ADVANC.BK", "AOT.BK", "AWC.BK", "BANPU.BK", "BBL.BK", "BDMS.BK", "BEM.BK", "BGRIM.BK", "BH.BK", "BTS.BK",
    "CBG.BK", "CENTEL.BK", "COM7.BK", "CPALL.BK", "CPF.BK", "CPN.BK", "CRC.BK", "DELTA.BK", "EA.BK", "EGCO.BK",
    "GLOBAL.BK", "GPSC.BK", "GULF.BK", "HMPRO.BK", "INTUCH.BK", "IVL.BK", "KBANK.BK", "KCE.BK", "KTB.BK", "KTC.BK",
    "LH.BK", "MINT.BK", "MTC.BK", "OR.BK", "OSP.BK", "PTT.BK", "PTTEP.BK", "PTTGC.BK", "RATCH.BK", "SAWAD.BK",
    "SCB.BK", "SCC.BK", "SCGP.BK", "TISCO.BK", "TOP.BK", "TTB.BK", "TU.BK", "WHA.BK")

selected_stocks = st.selectbox("Select Symbol for prediction",stocks)

n_years = st.slider("Year of Prediction",1,4)
period = n_years * 365 

@st.cache_data
def load_data(ticker):
    data = yf.download(ticker,START,TODAY,progress=False)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text("Load data....")
data = load_data(selected_stocks)
data_load_state.text("Loading data...done")


def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Open'],name='stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Close'],name='stock_close'))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

#Forecasting
df_train = data[['Date','Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.subheader('Forecast data')
st.write(forecast.tail())

fig1 = plot_plotly(m, forecast)
components.html(fig1.to_html(full_html=False), height=600, )

fig2 = m.plot_components(forecast)
st.pyplot(fig2)

y_true = forecast.set_index('ds')['m'].values
y_pred = forecast.set_index('ds')['yhat'].values

# Calculate the Mean Squared Error (MSE)
mse = np.mean((y_true - y_pred) ** 2)

# Display the MSE
st.write(f"Mean Squared Error (MSE): {mse:.2f}")
