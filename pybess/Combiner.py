import pandas as pd
import datetime
import math 

class Combiner(object):
	def __init__(self, trading_price, p5min, predispatch):
		self._trading_price = trading_price
		self._p5min	= p5min
		self._predispatch = predispatch

	def combined_forecast(self, run_dt):
		# get position in trading interval
		
		if run_dt.minute == 0 or run_dt.minute == 30:
			elapsed_intervals = 0
		else:
			elapsed_intervals = (run_dt.minute % 30 / 5)

		elapsed_intervals = int(elapsed_intervals)

		# Average over elapsed 5 minute prices
		elapsed_prices = []
		pointer = run_dt
		for i in range(elapsed_intervals):
			price = self._p5min[(self._p5min.RUN_DATETIME == pointer) & (self._p5min.INTERVAL_DATETIME == pointer)]['RRP'].values[0]
			elapsed_prices.append(price)
			pointer -= datetime.timedelta(minutes=5)

		# Get remaining prices in trading interval
		future_prices = []
		pointer = run_dt + datetime.timedelta(minutes=5)
		for i in range(6 - elapsed_intervals):
			price = self._p5min[(self._p5min.RUN_DATETIME == run_dt) & (self._p5min.INTERVAL_DATETIME == pointer)]['RRP'].values[0] 
			future_prices.append(price)
			pointer += datetime.timedelta(minutes=5)

		# Get first available predispatch timestep
		last_pd_update = run_dt - datetime.timedelta(minutes=run_dt.minute % 30)
		predispatch_df = self._predispatch[self._predispatch.RUN_DATETIME == last_pd_update]
		first_timestep_pd = predispatch_df['INTERVAL_DATETIME'].min()

		# Get latest p5min timestep
		p5min_df = self._p5min[self._p5min.RUN_DATETIME == run_dt]
		latest_timestep_p5min = p5min_df['INTERVAL_DATETIME'].max()

		# Get latest timestep we will use p5min for
		cutoff_timestep = latest_timestep_p5min - datetime.timedelta(minutes = latest_timestep_p5min.minute % 30)
		p5min_df = p5min_df[(p5min_df.INTERVAL_DATETIME <= cutoff_timestep) & (p5min_df.INTERVAL_DATETIME > run_dt)]
		predispatch_df = predispatch_df[predispatch_df.INTERVAL_DATETIME > cutoff_timestep]

		
		combined = pd.concat([p5min_df, predispatch_df], ignore_index=True, sort=True)
		combined = combined[['INTERVAL_DATETIME', 'RRP', 'tstep_len']]
		combined = combined.set_index('INTERVAL_DATETIME')

		# Get last timestep in this trading interval (round up 30 mins)
		decision_pointer = run_dt + datetime.timedelta(minutes=5)
		last_trading_timestep = decision_pointer + (datetime.datetime.min - decision_pointer) % datetime.timedelta(minutes=30)

		# Get timesteps to be averaged
		current_interval = combined[combined.index <= last_trading_timestep]
		elapsed_prices += current_interval['RRP'].tolist()

		current_interval_avg = sum(elapsed_prices)/len(elapsed_prices)

		for t in current_interval.index:
			combined.loc[t,'RRP'] = current_interval_avg

		# Average second half hour if full 5 min pd exists
		next_interval =combined[(combined.index > last_trading_timestep) & (combined.tstep_len == 5)]
		if not next_interval.empty:
			if len(next_interval) != 6:
				print(f"Error in pd dispatch, expected 6 values for next trading interval but received {len(next_interval)}")
			else:
				next_interval_prices = next_interval['RRP'].tolist()
				next_interval_avg = sum(next_interval_prices)/len(next_interval_prices)
				for t in next_interval.index:
					combined.loc[t, 'RRP'] = next_interval_avg
		
		return combined


	def combined_forecast_beta(self, run_dt):

		predispatch_df = self._predispatch[self._predispatch.RUN_DATETIME == run_dt]
		predispatch_df = pd.concat([predispatch_df], ignore_index=True, sort=True)
		predispatch_df = predispatch_df[['INTERVAL_DATETIME', 'RRP', 'tstep_len']]
		
		return predispatch_df

	def combined_forecast_elapsed(self, run_dt):

		# Get last timestep in this trading interval (round up 30 mins)
		decision_pointer = run_dt + datetime.timedelta(minutes=5)
		last_trading_timestep = decision_pointer + (datetime.datetime.min - decision_pointer) % datetime.timedelta(minutes=30)

		# Get first available predispatch timestep
		last_pd_update = run_dt - datetime.timedelta(minutes=run_dt.minute % 30)
		predispatch_df = self._predispatch[self._predispatch.RUN_DATETIME == last_pd_update]
		predispatch_df = predispatch_df[predispatch_df.INTERVAL_DATETIME >= last_trading_timestep]
		predispatch_df = predispatch_df[['INTERVAL_DATETIME', 'RRP', 'tstep_len']]
		
		# get position in trading interval	
		if run_dt.minute == 0 or run_dt.minute == 30:
			elapsed_intervals = 0
		else:
			elapsed_intervals = (run_dt.minute % 30 / 5)

		elapsed_intervals = int(elapsed_intervals)

		# Average over elapsed 5 minute prices
		elapsed_prices = []
		pointer = run_dt
		for i in range(elapsed_intervals):
			price = self._p5min[(self._p5min.RUN_DATETIME == pointer) & (self._p5min.INTERVAL_DATETIME == pointer)]['RRP'].values[0]
			elapsed_prices.append(price)
			pointer -= datetime.timedelta(minutes=5)

		if len(elapsed_prices) > 0:
			average_price = sum(elapsed_prices) / len(elapsed_prices)

			# Get remaining prices in trading interval
			future_prices = []
			pointer = run_dt + datetime.timedelta(minutes=5)
			for i in range(6 - elapsed_intervals):
				predispatch_df = predispatch_df.append({'INTERVAL_DATETIME': pointer, 'RRP': average_price, 'tstep_len': 5}, ignore_index=True)			
				pointer += datetime.timedelta(minutes=5)

			predispatch_df = predispatch_df.sort_values(by=['INTERVAL_DATETIME'])

		return predispatch_df





