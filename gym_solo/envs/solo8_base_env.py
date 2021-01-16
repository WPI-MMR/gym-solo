import abc
import gym
import pybullet as p
import pybullet_data as pbd
import pybullet_utils.bullet_client as bc

from gym_solo.core import termination as terms
from gym_solo.core import configs
from gym_solo.core import obs
from gym_solo.core import rewards


class Solo8BaseEnv(gym.Env, abc.ABC):
  """Solo 8 abstract base environment."""
  def __init__(self, config: configs.Solo8BaseConfig, use_gui: bool, 
               realtime: bool):
    """Create a solo8 env.

    Args:
      config (configs.Solo8BaseConfig): The SoloConfig. Defaults to None.
      use_gui (bool): Whether or not to show the pybullet GUI. Defaults to 
        False.
      realtime (bool): Whether or not to run the simulation in real time. 
        Defaults to False.
    """
    self._realtime = realtime
    self._config = config

    self.client = bc.BulletClient(
      connection_mode=p.GUI if use_gui else p.DIRECT)
    self.client.setAdditionalSearchPath(pbd.getDataPath())
    self.client.setGravity(*self._config.gravity)
    self.client.setPhysicsEngineParameter(fixedTimeStep=self._config.dt, 
                                          numSubSteps=1)

    self.plane = self.client.loadURDF('plane.urdf')
    self.load_bodies()

    self.obs_factory = obs.ObservationFactory(self.client)
    self.reward_factory = rewards.RewardFactory(self.client)
    self.termination_factory = terms.TerminationFactory()

    self.reset(init_call=True)