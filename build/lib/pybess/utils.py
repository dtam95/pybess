import plotly as py
import plotly.graph_objs as go
from pybess.Arbitrage import Arbitrage

def plot(arb):
	df = arb.results()

	trace_battery= go.Bar(
	    x=df['timestamp'],
	    y=df['dispatch'],
	    name = "Battery Dispatch (MW)",
	    marker = dict(color = '#17BECF'),
	    opacity = 0.4,
	    yaxis='y2')

	trace_price = go.Scatter(
	    x=df['timestamp'],
	    y=df['RRP'],
	    name = "Spot Price ($/MWh)",
	    line = dict(color = '#7F7F7F'),
	    opacity = 0.8)

	data = [trace_battery, trace_price]

	layout = dict(
	    title='Spot Price & Battery Dispatch',
	    xaxis=dict(
	        rangeselector=dict(
	            buttons=list([
	                dict(count=1,
	                     label='1m',
	                     step='month',
	                     stepmode='backward'),
	                dict(count=6,
	                     label='6m',
	                     step='month',
	                     stepmode='backward'),
	                dict(step='all')
	            ])
	        ),
	        rangeslider=dict(
	            visible = True
	        ),
	        type='date'
	    ),
	    yaxis=dict(
	    	title="Spot Price ($/MWh)"
	    ),
	    yaxis2=dict(
	    	overlaying='y',
	    	side='right',
	    	title="Battery Dispatch (MW)"
	    )
	)

	fig = dict(data=data, layout=layout)
	py.offline.plot(fig, filename = "battery_dispatch.html")

def nbplot(arb):
	df = arb.results()

	trace_battery= go.Bar(
	    x=df['timestamp'],
	    y=df['dispatch'],
	    name = "Battery Dispatch (MW)",
	    marker = dict(color = '#17BECF'),
	    opacity = 0.4,
	    yaxis='y2')

	trace_price = go.Scatter(
	    x=df['timestamp'],
	    y=df['RRP'],
	    name = "Spot Price ($/MWh)",
	    line = dict(color = '#7F7F7F'),
	    opacity = 0.8)

	data = [trace_battery, trace_price]

	layout = dict(
	    title='Spot Price & Battery Dispatch',
	    xaxis=dict(
	        rangeselector=dict(
	            buttons=list([
	                dict(count=1,
	                     label='1m',
	                     step='month',
	                     stepmode='backward'),
	                dict(count=6,
	                     label='6m',
	                     step='month',
	                     stepmode='backward'),
	                dict(step='all')
	            ])
	        ),
	        rangeslider=dict(
	            visible = True
	        ),
	        type='date'
	    ),
	    yaxis=dict(
	    	title="Spot Price ($/MWh)"
	    ),
	    yaxis2=dict(
	    	overlaying='y',
	    	side='right',
	    	title="Battery Dispatch (MW)"
	    )
	)

	fig = dict(data=data, layout=layout)
	return py.plotly.iplot(fig, filename = "battery_dispatch.html")