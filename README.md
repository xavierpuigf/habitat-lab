# Code to reproduce Habitat 3.0 Submission

This anonymous repository contains the code to reproduce experiments in Habitat 3.0. 
Note that the full set of experiments in the paper are done in the HSSD scenes. To ease reproduction, we are providing example configs to run our trained policies in ReplicaCAD, a smaller dataset of indoor scenes. Upon acceptance, we will be releasing the full dataset. 


## Setup

1. **Preparing conda env**

   Assuming you have [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) installed, let's prepare a conda env:
   ```bash
   # We require python>=3.9 and cmake>=3.14
   conda create -n habitat_30_submission python=3.9 cmake=3.14.0
   conda activate habitat_30_submission
   ```

1. **conda install habitat-sim**
   
   To install habitat-sim with bullet physics
      ```
      conda install habitat-sim withbullet headless -c conda-forge -c aihabitat-nightly
      ```
      

1. **pip install habitat-lab stable version**.

      ```bash
      cd habitat-lab
      pip install -e habitat-lab  # install habitat_lab
      ```
1. **Install habitat-baselines**.

    The command above will install only core of Habitat-Lab. To include habitat_baselines along with all additional requirements, use the command below after installing habitat-lab:

      ```bash
      pip install -e habitat-baselines  # install habitat_baselines
      ```

1. **Download necessary data**.
      ```
      python -m habitat_sim.utils.datasets_download --uids rearrange_dataset_v1 --data-path data/
      python -m habitat_sim.utils.datasets_download --uids replica_cad_dataset --data-path data/
      python -m habitat_sim.utils.datasets_download --uids ycb --data-path data/
      python -m habitat_sim.utils.datasets_download --uids hab_spot_arm --data-path data/

      ```


You may need to run these scripts more than once. If you see an git-lfs related error, try installing git-lfs. In the end you should have the following folders in your habitat-lab/ folder:
```
data/objects/ycb
data/datasets/replica_cad
data/replica_cad
data/robots/hab_spot_arm
```

## Training
Here is the code to train the different social rearrangement baselines:

```
## Learn-Single
python habitat-baselines/habitat_baselines/run.py \
-m --config-name experiments_hab3/pop_play_kinematic_oracle_humanoid_spot_fp.yaml \
habitat_baselines.evaluate=False \
habitat_baselines.eval.should_load_ckpt=False \
habitat_baselines.rl.agent.num_pool_agents_per_type=[1,1]

## Plan-pop
# plan id can be 1 to 4
export plan_id=1 
export plan_id_agent=$((-(5 - plan_id)))
python habitat-baselines/habitat_baselines/run.py \
-m --config-name experiments_hab3/pop_play_kinematic_oracle_humanoid_spot_fp.yaml \
habitat_baselines.evaluate=False \
habitat_baselines.eval.should_load_ckpt=False \
habitat_baselines/rl/policy@habitat_baselines.rl.policy.agent_1=hab3_planner \
habitat_baselines.rl.policy.agent_1.hierarchical_policy.high_level_policy.plan_idx="${plan_id_agent}" 

## Learn-pop
python habitat-baselines/habitat_baselines/run.py \
-m --config-name experiments_hab3/pop_play_kinematic_oracle_humanoid_spot_fp.yaml \
habitat_baselines.evaluate=False \
habitat_baselines.eval.should_load_ckpt=False \
habitat_baselines.rl.agent.num_pool_agents_per_type=[1,8]
```

## Evaluation

Below is the code to run the different baselines. For each baselines, we generate 5 episodes. A video will be saved for each episode in the video specified by video_dir. 

```
# PUT HERE THE DIR OF YOUR CHECKPOINTS
export base_dir=/path/to/checkpoint 
```


```
## Learn-Single
python habitat-baselines/habitat_baselines/run.py \
-m --config-name experiments_hab3/pop_play_kinematic_oracle_humanoid_spot_fp.yaml \
habitat_baselines.eval_ckpt_path_dir="${base_dir}/learn_single.pth" \
habitat_baselines.test_episode_count=5 \
habitat_baselines.video_dir="video_learn_single_hbao"

## Plan-Pop
# plan id can be 1 to 4
export plan_id=1 
export plan_id_agent=$((-(5 - plan_id)))
python habitat-baselines/habitat_baselines/run.py \
-m --config-name experiments_hab3/pop_play_kinematic_oracle_humanoid_spot_fp.yaml \
habitat_baselines.eval_ckpt_path_dir="${base_dir}/plan_pop_${plan_id}.pth" \
habitat_baselines.test_episode_count=5 \
habitat_baselines/rl/policy@habitat_baselines.rl.policy.agent_1=hab3_planner \
habitat_baselines.rl.policy.agent_1.hierarchical_policy.high_level_policy.plan_idx="${plan_id_agent}" \
habitat_baselines.video_dir="video_learn_plan"

## Learn-Pop
export ckpt_pth=$base_dir"/learn_single.pth"
python habitat-baselines/habitat_baselines/run.py \
-m --config-name experiments_hab3/pop_play_kinematic_oracle_humanoid_spot_fp.yaml \
habitat_baselines.eval_ckpt_path_dir="${base_dir}/learn_pop.pth" \
habitat_baselines.test_episode_count=5 \
habitat_baselines.video_dir="video_learn_pop"
```

## HITL
For instructions on how to run the Human-In-The-Loop (HITL) tool, please checkout the folder: `hitl/`.

To download this repository, you can use a resource like [this](https://github.com/fedebotu/clone-anonymous-github). 

