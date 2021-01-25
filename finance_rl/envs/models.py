import collections
from typing import Iterable

import numpy as np
from pydantic import BaseModel, root_validator, validator
from pydantic.dataclasses import dataclass


class Info(BaseModel):
    done: bool = False
    implementation_shortfall: float = None
    expected_shortfall: float = None
    expected_variance: float = None
    utility: float = None
    price: float = None
    share_to_sell_now: int = None
    currentPermanentImpact: float = None
    currentTemporaryImpact: float = None
    exec_price: float = None


ANNUAL_VOLAT = 0.12  # Annual volatility in stock price
BID_ASK_SP = 1 / 8  # Bid-ask spread
DAILY_TRADE_VOL = 5e6  # Average Daily trading volume
TRAD_DAYS = 250  # Number of trading days in a year
DAILY_VOLAT = ANNUAL_VOLAT / np.sqrt(TRAD_DAYS)  # Daily volatility in stock price


class FinantialParams(BaseModel):
    anv: float = ANNUAL_VOLAT
    basp: float = BID_ASK_SP
    dtv: int = DAILY_TRADE_VOL
    dpv: float = DAILY_VOLAT


TOTAL_SHARES = 1000000  # Total number of shares to sell
STARTING_PRICE = 50  # Starting price per share
LLAMBDA = 1e-6  # Trader's risk aversion
LIQUIDATION_TIME = 60  # How many days to sell all the shares.
NUM_N = 60  # Number of trades
EPSILON = BID_ASK_SP / 2  # Fixed Cost of Selling.
SINGLE_STEP_VARIANCE = (
    DAILY_VOLAT * STARTING_PRICE
) ** 2  # Calculate single step variance
ETA = BID_ASK_SP / (
    0.01 * DAILY_TRADE_VOL
)  # Price Impact for Each 1% of Daily Volume Traded
GAMMA = BID_ASK_SP / (0.1 * DAILY_TRADE_VOL)  # Permanent Impact Constant


@dataclass
class AlmgrenChrissParams:
    liquidation_time: int = LIQUIDATION_TIME
    num_n: int = NUM_N
    eta: float = ETA
    gamma: float = GAMMA
    llambda: float = LLAMBDA
    singleStepVariance: float = SINGLE_STEP_VARIANCE
    total_shares: int = TOTAL_SHARES
    startingPrice: int = STARTING_PRICE
    epsilon: float = EPSILON
    tau: float = None
    eta_hat: float = None
    kappa_hat: float = None
    kappa: float = None

    def __post_init_post_parse__(self):
        self.tau = self.liquidation_time / self.num_n
        self.eta_hat = self.eta - (0.5 * self.gamma * self.tau)
        self.kappa_hat = np.sqrt(
            (self.llambda * self.singleStepVariance) / self.eta_hat
        )
        self.kappa = (
            np.arccosh((((self.kappa_hat ** 2) * (self.tau ** 2)) / 2) + 1) / self.tau
            if self.tau > 0
            else 1
        )


class State(BaseModel):
    shares_remaining: int = TOTAL_SHARES
    timeHorizon: int = NUM_N
    logReturns: Iterable = collections.deque(np.zeros(6))
    prevImpactedPrice: int = STARTING_PRICE
    transacting: bool = False
    trade_number: int = 0
    initial_state: Iterable = None


class EnvParams(BaseModel):
    info: Info = Info()
    state: State = State()
    alm_params: AlmgrenChrissParams = AlmgrenChrissParams()
    fin_params: FinantialParams = FinantialParams()

    @root_validator(pre=True)
    def parse_init(cls, params):
        st = {'timeHorizon': params.get('num_n', NUM_N)}
        kwargs = {}
        kwargs['alm_params'] = params
        kwargs['state'] = st
        return kwargs


class Transactions(BaseModel):
    tolerance: int = 1
    totalCapture: int = 0
    prevPrice: int = None
    totalSSSQ: int = 0
    totalSRSQ: int = 0
    prevUtility: int = None

    # # Set the variables for the initial state
    # self.shares_remaining = self.total_shares
    # self.timeHorizon = self.num_n
    # self.logReturns = collections.deque(np.zeros(6))

    # # Set the initial impacted price to the starting price
    # self.prevImpactedPrice = self.startingPrice

    # # Set the initial transaction state to False
    # self.transacting = False

    # # Set a variable to keep trak of the trade number
    # self.k = 0
