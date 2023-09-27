# Code to reproduce Habitat 3.0 Submission


## Setup

1. **Preparing conda env**

   Assuming you have [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) installed, let's prepare a conda env:
   ```bash
   # We require python>=3.9 and cmake>=3.14
   conda create -n habitat_30_submission python=3.9 cmake=3.14.0
   conda activate habitat_30_submission
   ```

1. **conda install habitat-sim**
   - To install habitat-sim with bullet physics
      ```
      conda install habitat-sim withbullet headless -c conda-forge -c aihabitat-nightly
      ```
      

1. **pip install habitat-lab stable version**.

      ```bash
      git clone --branch stable https://github.com/facebookresearch/habitat-lab.git
      cd habitat-lab
      pip install -e habitat-lab  # install habitat_lab
      ```
1. **Install habitat-baselines**.

    The command above will install only core of Habitat-Lab. To include habitat_baselines along with all additional requirements, use the command below after installing habitat-lab:

      ```bash
      pip install -e habitat-baselines  # install habitat_baselines
      ```

1. **Download necessary data**.

## Testing

1. Let's download some 3D assets using Habitat-Sim's python data download utility:
   - Download (testing) 3D scenes:
      ```bash
      python -m habitat_sim.utils.datasets_download --uids habitat_test_scenes --data-path data/
      ```
      Note that these testing scenes do not provide semantic annotations.

   - Download point-goal navigation episodes for the test scenes:
      ```bash
      python -m habitat_sim.utils.datasets_download --uids habitat_test_pointnav_dataset --data-path data/
      ```

1. **Non-interactive testing**: Test the Pick task: Run the example pick task script
    <!--- Please, update `examples/example.py` if you update example. -->
    ```bash
    python examples/example.py
    ```

    which uses [`habitat-lab/habitat/config/benchmark/rearrange/pick.yaml`](habitat-lab/habitat/config/benchmark/rearrange/pick.yaml) for configuration of task and agent. The script roughly does this:

    ```python
    import gym
    import habitat.gym

    # Load embodied AI task (RearrangePick) and a pre-specified virtual robot
    env = gym.make("HabitatRenderPick-v0")
    observations = env.reset()

    terminal = False

    # Step through environment with random actions
    while not terminal:
        observations, reward, terminal, info = env.step(env.action_space.sample())
    ```

    To modify some of the configurations of the environment, you can also use the `habitat.gym.make_gym_from_config` method that allows you to create a habitat environment using a configuration.

    ```python
    config = habitat.get_config(
      "benchmark/rearrange/pick.yaml",
      overrides=["habitat.environment.max_episode_steps=20"]
    )
    env = habitat.gym.make_gym_from_config(config)
    ```

    If you want to know more about what the different configuration keys overrides do, you can use [this reference](habitat-lab/habitat/config/CONFIG_KEYS.md).

    See [`examples/register_new_sensors_and_measures.py`](examples/register_new_sensors_and_measures.py) for an example of how to extend habitat-lab from _outside_ the source code.



1. **Interactive testing**: Using you keyboard and mouse to control a Fetch robot in a ReplicaCAD environment:
    ```bash
    # Pygame for interactive visualization, pybullet for inverse kinematics
    pip install pygame==2.0.1 pybullet==3.0.4

    # Interactive play script
    python examples/interactive_play.py --never-end
    ```

   Use I/J/K/L keys to move the robot base forward/left/backward/right and W/A/S/D to move the arm end-effector forward/left/backward/right and E/Q to move the arm up/down. The arm can be difficult to control via end-effector control. More details in documentation. Try to move the base and the arm to touch the red bowl on the table. Have fun!

   Note: Interactive testing currently fails on Ubuntu 20.04 with an error: `X Error of failed request:  BadAccess (attempt to access private resource denied)`. We are working on fixing this, and will update instructions once we have a fix. The script works without errors on MacOS.

## Debugging an environment issue

Our vectorized environments are very fast, but they are not very verbose. When using `VectorEnv` some errors may be silenced, resulting in process hanging or multiprocessing errors that are hard to interpret. We recommend setting the environment variable `HABITAT_ENV_DEBUG` to 1 when debugging (`export HABITAT_ENV_DEBUG=1`) as this will use the slower, but more verbose `ThreadedVectorEnv` class. Do not forget to reset `HABITAT_ENV_DEBUG` (`unset HABITAT_ENV_DEBUG`) when you are done debugging since `VectorEnv` is much faster than `ThreadedVectorEnv`.

## Documentation

Browse the online [Habitat-Lab documentation](https://aihabitat.org/docs/habitat-lab/index.html) and the extensive [tutorial on how to train your agents with Habitat](https://aihabitat.org/tutorial/2020/). For Habitat 2.0, use this [quickstart guide](https://aihabitat.org/docs/habitat2/).


## Docker Setup
We provide docker containers for Habitat, updated approximately once per year for the [Habitat Challenge](https://github.com/facebookresearch/habitat-challenge). This works on machines with an NVIDIA GPU and requires users to install [nvidia-docker](https://github.com/NVIDIA/nvidia-docker). To setup the habitat stack using docker follow the below steps:

1. Pull the habitat docker image: `docker pull fairembodied/habitat-challenge:testing_2022_habitat_base_docker`

1. Start an interactive bash session inside the habitat docker: `docker run --runtime=nvidia -it fairembodied/habitat-challenge:testing_2022_habitat_base_docker`

1. Activate the habitat conda environment: `conda init; source ~/.bashrc; source activate habitat`

1. Run the testing scripts as above: `cd habitat-lab; python examples/example.py`. This should print out an output like:
    ```bash
    Agent acting inside environment.
    Episode finished after 200 steps.
    ```

### Questions?
Can't find the answer to your question? Try asking the developers and community on our [Discussions forum](https://github.com/facebookresearch/habitat-lab/discussions).

## Datasets

[Common task and episode datasets used with Habitat-Lab](DATASETS.md).

## Baselines
Habitat-Lab includes reinforcement learning (via PPO) baselines. For running PPO training on sample data and more details refer [habitat_baselines/README.md](habitat-baselines/habitat_baselines/README.md).

## ROS-X-Habitat
ROS-X-Habitat (https://github.com/ericchen321/ros_x_habitat) is a framework that bridges the AI Habitat platform (Habitat Lab + Habitat Sim) with other robotics resources via ROS. Compared with Habitat-PyRobot, ROS-X-Habitat places emphasis on 1) leveraging Habitat Sim v2's physics-based simulation capability and 2) allowing roboticists to access simulation assets from ROS. The work has also been made public as a [paper](https://arxiv.org/abs/2109.07703).

Note that ROS-X-Habitat was developed, and is maintained by the Lab for Computational Intelligence at UBC; it has not yet been officially supported by the Habitat Lab team. Please refer to the framework's repository for docs and discussions.


## License
Habitat-Lab is MIT licensed. See the [LICENSE file](/LICENSE) for details.

The trained models and the task datasets are considered data derived from the correspondent scene datasets.

- Matterport3D based task datasets and trained models are distributed with [Matterport3D Terms of Use](http://kaldir.vc.in.tum.de/matterport/MP_TOS.pdf) and under [CC BY-NC-SA 3.0 US license](https://creativecommons.org/licenses/by-nc-sa/3.0/us/).
- Gibson based task datasets, the code for generating such datasets, and trained models are distributed with [Gibson Terms of Use](https://storage.googleapis.com/gibson_material/Agreement%20GDS%2006-04-18.pdf) and under [CC BY-NC-SA 3.0 US license](https://creativecommons.org/licenses/by-nc-sa/3.0/us/).
