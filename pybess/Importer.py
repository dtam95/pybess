import pandas as pd 
import datetime
from abc import ABC, abstractmethod
from nemosis import data_fetch_methods

class Importer(object):
  def __init__(self):
    pass

  @abstractmethod
  def trading_price(self):
    pass

  @property
  @abstractmethod
  def start_date(self):
    pass
  
  @property
  @abstractmethod
  def end_date(self):
    pass
  
    
class NEMOSISImporter(Importer):
  """
    Import historical NEM price data using the open source NEMOSIS tool developed by Nick Gorman 
    URL: https://github.com/UNSW-CEEM/NEMOSIS/wiki
  """
  def __init__(self, start_date, end_date, state):
    Importer.__init__(self)
    self._start_date = start_date
    self._end_date = end_date
    self._state = state

  @property
  def start_date(self):
    return self._start_date
  
  @property
  def end_date(self):
    return self._end_date

  @property
  def state(self):
    return self._state
  
  def trading_price(self):
    table = 'TRADINGPRICE'
    raw_data_cache = './cache'

    trading_price = data_fetch_methods.dynamic_data_compiler(
      self._start_date.strftime("%Y/%m/%d 00:00:00"), 
      self._end_date.strftime("%Y/%m/%d 00:00:00"), 
      table, 
      raw_data_cache
    )

    trading_price = trading_price.loc[trading_price['REGIONID'] == self._state]
    trading_price['SETTLEMENTDATE'] = pd.to_datetime(trading_price['SETTLEMENTDATE'], format='%d/%m/%Y %H:%M') 
    trading_price = trading_price.sort_values(by=['SETTLEMENTDATE'])
    trading_price = trading_price.reset_index(drop=True)    
    trading_price['tstep_len'] = [30]*len(trading_price.index)

    columns = ['RRP', 'RAISE6SECRRP', 'RAISE60SECRRP', 'RAISE5MINRRP', 'RAISEREGRRP', 'LOWER6SECRRP', 'LOWER60SECRRP', 'LOWERREGRRP']
    trading_price[columns] = trading_price[columns].astype(float)

    return trading_price
