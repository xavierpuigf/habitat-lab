# HITL Tool


# Overview
This is a 3D interactive GUI app for evaluating Habitat 3.0 rearrangemnt along with real humans.

# Example commands
### GUI-controlled humanoid and learned-policy-controlled Spot

* To launch GUI-controlled humanoid and random-policy-controlled (initialized with random weights) Spot, in HSSD run:
```
HABITAT_SIM_LOG=warning MAGNUM_LOG=warning \
python hitl/sandbox_app.py \
--disable-inverse-kinematics \
--never-end \
--gui-controlled-agent-index 1 \
--cfg experiments_hab3/pop_play_kinematic_oracle_humanoid_spot_fp.yaml \
--cfg-opts \
habitat_baselines.evaluate=True \
habitat_baselines.num_environments=1 \
habitat_baselines.eval.should_load_ckpt=False \
~habitat.task.measurements.agent_blame_measure
```


To use **trained**-policy-controlled agent(s) instead of random-policy-controlled:

Run two above commands with the following `--cfg-opts`:
```
--cfg-opts \
habitat_baselines.evaluate=True \
habitat_baselines.num_environments=1 \
habitat_baselines.eval.should_load_ckpt=True \
habitat_baselines.eval_ckpt_path_dir=path/to/checkpoint.pth
```
Where the checkpoint path can be `plan_pop_${plan_id}.pth`, `learn_single.pth`, `learn_pop.pth`


# Controls
* See on-screen help text for common keyboard and mouse controls
* `N` to toggle navmesh visualization in the debug third-person view (`--debug-third-person-width`)
* For `--first-person-mode`, you can toggle mouse-look by left-clicking anywhere



# Command-line Options



## Saving episode data
Use `--save-filepath-base my_session`. When the user presses `M` to reset the env, the first episode will be saved as `my_session.0.json.gz` and `my_session.0.pkl.gz`. These files contain mostly-identical data; we save both so that developers have two choices for how to consume the data later. After pressing `M` again, the second episode will be saved as `my_session.1.json.gz`, etc. For an example of consuming this data, see `test_episode_save_files.py` .


## GUI-controlled agents and free camera mode
Add `--gui-controlled-agent-index` followed by the agent's index you want to control via GUI (for example, `--gui-controlled-agent-index 0` to control the first agent).

If not set, it is assumed that scene is empty or all agents are policy-controlled. App switches to free camera mode in this case. User-controlled free camera lets the user observe the scene (instead of controlling one of the agents). For instance, one use case is to (eventually) observe policy-controlled agents.

**Note:** Currently, only Spot and Humanoid agents can be policy-controlled (PDDL planner + oracle skills). If you want to test the free camera mode, omit `--gui-controlled-agent-index` argument.

## First-person and third-person mode for GUI-controlled humanoid
Include `--first-person-mode`, or omit it to use third-person mode. With first-person mode, use  `--max-look-up-angle` and `--min-look-down-angle` arguments to limit humanoid's look up/down angle. For example, `--max-look-up-angle 0 --min-look-down-angle -45` to let the humanoid look down -45 degrees.


## Human-in-the-loop tutorial sequence
The sandbox tool can show a tutorial sequence at the start of every episode to introduce the user to the scene and goals in a human-in-the-loop context. To enable this, use the `--show-tutorial` command-line argument.
