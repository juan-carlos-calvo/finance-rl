import gym
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding

from .models import EnvParams


class LiquidationEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, env_params: EnvParams = EnvParams()):
        self.info = env_params.info
        self.state = env_params.state
        self.alm_params = env_params.alm_params
        self.fin_params = env_params.fin_params

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

    def render(self, mode='human', close=False):
        pass
