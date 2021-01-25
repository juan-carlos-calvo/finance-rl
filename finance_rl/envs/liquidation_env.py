import gym
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding

from .models import EnvParams, Transactions


class LiquidationEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, env_params: EnvParams = EnvParams()):
        self.info = env_params.info
        self.state = env_params.state
        self.alm_params = env_params.alm_params
        self.fin_params = env_params.fin_params
        self.transactions = Transactions()

    def step(self, action):
        pass

    def reset(self, env_params: EnvParams = EnvParams()):
        self.__init__(env_params)
        self.state.initial_state = np.array(
            list(self.state.logReturns)
            + [
                self.state.timeHorizon / self.alm_params.num_n,
                self.state.shares_remaining / self.alm_params.total_shares,
            ]
        )
        self.transactions.prevPrice = self.alm_params.startingPrice
        self.transactions.prevUtility = self.compute_AC_utility(
            self.alm_params.total_shares
        )

    def render(self, mode='human', close=False):
        pass

    def get_AC_variance(self, sharesToSell: int) -> float:
        ft = 0.5 * (self.alm_params.singleStepVariance) * (sharesToSell ** 2)
        nst = self.alm_params.tau * np.sinh(
            self.alm_params.kappa * self.alm_params.liquidation_time
        ) * np.cosh(
            self.alm_params.kappa
            * (self.alm_params.liquidation_time - self.alm_params.tau)
        ) - self.alm_params.liquidation_time * np.sinh(
            self.alm_params.kappa * self.alm_params.tau
        )
        dst = (
            np.sinh(self.alm_params.kappa * self.alm_params.liquidation_time) ** 2
        ) * np.sinh(self.alm_params.kappa * self.alm_params.tau)
        st = nst / dst
        return ft * st

    def get_AC_expected_shortfall(self, sharesToSell: int) -> float:
        ft = 0.5 * self.alm_params.gamma * (sharesToSell ** 2)
        st = self.alm_params.epsilon * sharesToSell
        tt = self.alm_params.eta_hat * (sharesToSell ** 2)
        nft = np.tanh(0.5 * self.alm_params.kappa * self.alm_params.tau) * (
            self.alm_params.tau
            * np.sinh(2 * self.alm_params.kappa * self.alm_params.liquidation_time)
            + 2
            * self.alm_params.liquidation_time
            * np.sinh(self.alm_params.kappa * self.alm_params.tau)
        )
        dft = (
            2
            * (self.alm_params.tau ** 2)
            * (np.sinh(self.alm_params.kappa * self.alm_params.liquidation_time) ** 2)
        )
        fot = nft / dft
        return ft + st + (tt * fot)

    def compute_AC_utility(self, sharesToSell: int) -> float:
        # Calculate the AC Utility according to pg. 13 of the AC paper
        if self.alm_params.liquidation_time == 0:
            return 0
        E = self.get_AC_expected_shortfall(sharesToSell)
        V = self.get_AC_variance(sharesToSell)
        return E + self.alm_params.llambda * V
