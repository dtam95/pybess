from pulp import *
import pandas as pd
import datetime
from pybess.Battery import Battery

MINS_PER_HR = 60
CYCLES_PA = 350

class HistoricalOpt(object):

	def __init__(self, battery, state, importer, thruput=False):
		self._battery = battery
		self._state = state
		self._importer = importer

		trading_price = importer.trading_price()

		self._rrp = trading_price['RRP'].tolist()
		self._timesteps = trading_price['SETTLEMENTDATE'].tolist()
		self._tstep_len = trading_price['tstep_len'].tolist()
		self._thruput = thruput # False if unlimited
		self._duration = (importer.end_date - importer.start_date).total_seconds() / (365*24*60*60) # in years

		# Store simulation results
		self._simulation_results = None

	def solve(self):
		print("Defining optimisation problem...")
		tsteps = self._timesteps

		prob = LpProblem("Arbitrage", LpMaximize)

		store_vars = LpVariable.dicts("CapacityStore", tsteps, 0, self._battery.capacity_store)
		charge_vars = LpVariable.dicts("ChargePower", tsteps, -self._battery.capacity_power, 0)
		dcharge_vars = LpVariable.dicts("DchargePower", tsteps, 0, self._battery.capacity_power)

		# Maximisation function
		prob += lpSum(self._rrp[i] * (dcharge_vars[tsteps[i]] + charge_vars[tsteps[i]]) * self._tstep_len[i] / MINS_PER_HR 
		  for i in range(0,len(tsteps)))

		# Initial capacity constraint
		prob += store_vars[tsteps[0]] == self._battery.capacity_init - (dcharge_vars[tsteps[0]] 
		  * self._battery.dcharge_factor + charge_vars[tsteps[0]] * self._battery.charge_eff) * self._tstep_len[0] / MINS_PER_HR

		# Temporal storage links constraint
		for j in range(1, len(tsteps)):
			prob += ( store_vars[tsteps[j-1]] - (
			  	dcharge_vars[tsteps[j]] * self._battery.dcharge_factor + charge_vars[tsteps[j]] * self._battery._charge_eff
			  ) * self._tstep_len[j] / MINS_PER_HR
			) == store_vars[tsteps[j]]

		# Throughput Limitations
		if self._thruput is not False:
			prob += lpSum(dcharge_vars[tsteps[t]] * self._tstep_len[t] / MINS_PER_HR for t in range(0, len(tsteps))) <= self._thruput
		
		print("Solving optimisation problem...")
		prob.solve()
		self.write_results(charge_vars, dcharge_vars, store_vars)
		print("...Solved!")


	def write_results(self, charge_vars, dcharge_vars, store_vars):
		results_df = pd.DataFrame()
		discharge_list  = []
		charge_list  = []
		store_list = []
		for t in self._timesteps:
			discharge_list.append(dcharge_vars[t].varValue)
			charge_list.append(charge_vars[t].varValue)
			store_list.append(store_vars[t].varValue)

		results_df['timestamp'] = self._timesteps
		results_df['discharge'] = discharge_list
		results_df['charge'] = charge_list
		results_df['dispatch'] = results_df['discharge'] + results_df['charge']
		results_df['stored_energy'] = store_list
		results_df['RRP'] = self._rrp

		self._simulation_results = results_df

	@property
	def simulation_results(self):
		return self._simulation_results
