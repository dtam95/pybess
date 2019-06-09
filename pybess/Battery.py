class Battery(object):
  def __init__(self, cap_power, cap_store, charge_eff, dcharge_factor, cap_init, thruput=None):
    self._capacity_power = cap_power
    self._capacity_store = cap_store
    self._charge_eff = charge_eff
    self._dcharge_factor = dcharge_factor
    self._capacity_init = cap_init
    self._thruput = thruput
    self._stored_energy = cap_init

  @property
  def capacity_power(self):
    return self._capacity_power

  @property
  def capacity_store(self):
    return self._capacity_store

  @property
  def charge_eff(self):
    return self._charge_eff 

  @property
  def dcharge_factor(self):
    return self._dcharge_factor

  @property
  def capacity_init(self):
    return self._capacity_init

  @property
  def thruput(self):
    return self._thruput

  @property
  def stored_energy(self):
    return self._stored_energy

  @stored_energy.setter
  def stored_energy(self, value):
    self._stored_energy = value

  def charge(self, tstep_len, power):
    MINS_PER_HR = 60
    self._stored_energy = self._stored_energy + (power * self.charge_eff * tstep_len / MINS_PER_HR)
  
  def discharge(self, tstep_len, power):
    MINS_PER_HR = 60
    self._stored_energy = self._stored_energy - (power * self.dcharge_factor * tstep_len / MINS_PER_HR )
  

  def __str__(self):
    return(f"{self._capacity_power}MW/{self._capacity_store}MWh Battery.")