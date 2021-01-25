import gym
import hypothesis.strategies as st
import numpy as np
from hypothesis import assume, given

from finance_rl.envs import EnvParams
from finance_rl.envs.models import ETA, GAMMA


ENV_ID = 'liquidation-v0'


@given(
    liquidation_time=st.integers(1, 1000),
    num_n=st.integers(1, 1000),
    llambda=st.floats(0, 1e-5, exclude_min=True),
)
def test_reset(liquidation_time, num_n, llambda):
    assume(liquidation_time / num_n < 2 * ETA / GAMMA)
    env_params = EnvParams(
        liquidation_time=liquidation_time, num_n=num_n, llambda=llambda
    )
    env = gym.make(ENV_ID)
    env.reset(env_params=env_params)
    np.testing.assert_allclose(
        env.state.initial_state,
        np.array(
            list(env.state.logReturns)
            + [
                env.state.timeHorizon / env.alm_params.num_n,
                env.state.shares_remaining / env.alm_params.total_shares,
            ]
        ),
    )
    assert (
        env.transations.prevPrice == env.alm_params.startingPrice
    ), 'prev price not correctly initialized'
