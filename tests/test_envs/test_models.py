import hypothesis.strategies as st
import numpy as np
from hypothesis import given

from finance_rl.envs import AlmgrenChrissParams


@given(
    lt=st.integers(1, 360),
    nt=st.integers(1, 10000),
    etap=st.floats(1e-5, 0.01, exclude_min=True),
    gamma=st.floats(1e-5, 0.01, exclude_min=True),
    llambda=st.floats(0, 1e-5, exclude_min=True),
    ssv=st.floats(1, 1000),
    xs=st.lists(
        st.floats(min_value=0, exclude_min=True, max_value=1e6), min_size=0, max_size=7
    ),
)
def test_info(lt, nt, etap, gamma, llambda, ssv, xs):
    etah = 0.5 * gamma * lt / nt + etap
    params = AlmgrenChrissParams(lt, nt, etah, gamma, llambda, ssv, *xs)
    assert params.tau == params.liquidation_time / params.num_n
    assert params.eta_hat == params.eta - (0.5 * params.gamma * params.tau)
    assert params.kappa_hat == np.sqrt(
        (params.llambda * params.singleStepVariance) / params.eta_hat
    )
    assert params.kappa == (
        np.arccosh((((params.kappa_hat ** 2) * (params.tau ** 2)) / 2) + 1) / params.tau
    )
