from probo.marketdata import MarketData
from probo.payoff import VanillaPayoff, call_payoff, put_payoff
from probo.engine import MonteCarloEngine, AsianControlVariatePricerCall, NaiveAsianCall
from probo.facade import OptionFacade


## Set up the market data
spot = 100.0
rate = 0.06
volatility = 0.2
dividend = 0.03
thedata = MarketData(rate, spot, volatility, dividend)

## Set up the option
expiry = 1.0
strike = 100.0
thecall = VanillaPayoff(expiry, strike, call_payoff)

## Set up Asian Control Variate Pricer
nreps = 10000
steps = 10
pricercontvar = AsianControlVariatePricerCall
enginecontvar = MonteCarloEngine(nreps, steps, pricercontvar)

## Set up Naive Asian Pricer (nreps and nsteps are the same)

pricernaive = NaiveAsianCall
enginenaive = MonteCarloEngine(nreps, steps, pricernaive)


## Calculate the price
option1 = OptionFacade(thecall, enginecontvar, thedata)
price1,se1 = option1.price()

option2 = OptionFacade(thecall, enginenaive, thedata)
price2, se2 = option2.price()




print("The Asian Control Variate Call  is   {0:.3f}".format(price1)," The SE is{0:.6f}".format(se1))
