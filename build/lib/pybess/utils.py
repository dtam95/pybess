import datetime
import plotly.graph_objs as go
from plotly.offline import plot, iplot
from pybess.Arbitrage import Arbitrage

def plot(arb):
	df = arb.results().head(n=336)

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
	df = arb.results().head(n=336)

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

	#fig = dict(data=data, layout=layout)
	fig = go.Figure(data=data, layout=layout)
	return fig

def heat_map(arb):
	df = arb.results()

	TSTEPS_PER_DAY = 48
	power_dispatch = df['dispatch'].tolist()
	dataset =[[power_dispatch[i]] for i in range(0, TSTEPS_PER_DAY)]


	i = 0
	while i < len(power_dispatch)-TSTEPS_PER_DAY-1:
		day = power_dispatch[i:i+TSTEPS_PER_DAY]
		for j in range(0, TSTEPS_PER_DAY):
			dataset[j].append(day[j])
		i += TSTEPS_PER_DAY



	hours = []
	i = 0
	while i < 24:
		j = 0
		while j < 60:
			hours.append(datetime.time(i, j))
			j += 30
		i += 1

	data = [
		go.Heatmap(
			z=dataset,
			colorscale=[[0.0, 'rgb(165,0,38)'], [0.1111111111111111, 'rgb(215,48,39)'], [0.2222222222222222, 'rgb(244,109,67)'],
			[0.3333333333333333, 'rgb(253,174,97)'], [0.4444444444444444, 'rgb(254,224,144)'], [0.5555555555555556, 'rgb(224,243,248)'],
			[0.6666666666666666, 'rgb(171,217,233)'],[0.7777777777777778, 'rgb(116,173,209)'], [0.8888888888888888, 'rgb(69,117,180)'],
			[1.0, 'rgb(49,54,149)']],
			colorbar = dict(
				#title = 'Surface Heat',
				titleside = 'top',
				tickmode = 'array',
				tickvals = [-25,25],
				ticktext = ['Charging','Discharging'],
				ticks = 'outside'
			),
			y=hours,
			zsmooth='best',
			xaxis='x1',
			yaxis='y1'
		)
	]

	layout = go.Layout(
		title='Optimal Charge/Discharge Schedule',
		xaxis=dict(title="Day of Year")
	)
	fig = go.Figure(data=data, layout=layout)

	return fig