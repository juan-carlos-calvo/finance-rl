from gym.envs.registration import register
from pkg_resources import DistributionNotFound, get_distribution


try:
    __version__ = get_distribution('finance-rl').version
except DistributionNotFound:
    __version__ = '(local)'


register(
    id='liquidation-v0',
    entry_point='finance_rl.envs:LiquidationEnv',
)
