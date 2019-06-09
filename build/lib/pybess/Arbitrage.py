import pandas as pd
from pybess.HistoricalOpt import HistoricalOpt
from pybess.Battery import Battery
from pybess.Importer import NEMOSISImporter

class Arbitrage(object):
	def __init__(self, battery, start_date, end_date, state, thruput=False):
		self._state = state
		self._start_date = start_date
		self._end_date = end_date
		self._battery = battery

		importer = NEMOSISImporter(start_date, end_date, state)
		self._opt = HistoricalOpt(battery, state, importer, thruput)


	def solve(self):
		print(f"Running optimisation for \n STATE: {self._opt._state}, \n BATTERY: {self._battery}, \n FROM: {self._start_date}, \n TO: {self._end_date}")
		self._opt.solve()

	def results(self):
		if self._opt.simulation_results is None:
			raise NameError("Please run simulation using Arbitrage.solve() before fetching results")
		else:
			return self._opt.simulation_results

