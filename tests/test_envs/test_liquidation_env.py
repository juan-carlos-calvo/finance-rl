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
        env.transactions.prevPrice == env.alm_params.startingPrice
    ), 'prev price not correctly initialized'
    if env.alm_params.kappa > 0:
        breakpoint()
        assert env.transactions.prevUtility == env.compute_AC_utility(
            env.alm_params.total_shares
        ), 'prev utility not correctly initialized'


def test_AC_variance():
    actual = 204.3095586503
    env = gym.make(ENV_ID)
    result = env.get_AC_variance(30)
    np.testing.assert_almost_equal(actual, result)


def test_AC_expected_shortfall():
    actual = 1.87537369133
    env = gym.make(ENV_ID)
    result = env.get_AC_expected_shortfall(30)
    np.testing.assert_almost_equal(actual, result)


def test_AC_utility():
    actual = 1.87557800
    env = gym.make(ENV_ID)
    result = env.compute_AC_utility(30)
    np.testing.assert_almost_equal(actual, result)
    env_params = EnvParams(liquidation_time=0)
    env.reset(env_params=env_params)
    assert env.compute_AC_utility(0) == 0
