import pandas as pd
import datetime
from pybess.Battery import Battery
from pybess.Arbitrage import Arbitrage
from pybess.utils import *


battery = Battery.Battery(cap_power=30, cap_store=119, charge_eff=0.9, dcharge_factor=1/0.9, cap_init=0)


start_date = datetime.datetime(2018, 1, 1)
end_date = datetime.datetime(2019, 1, 1)
state="SA1"


arb = Arbitrage.Arbitrage(battery, start_date, end_date, state)

arb.solve()

print(arb.results())

plot(arb)


