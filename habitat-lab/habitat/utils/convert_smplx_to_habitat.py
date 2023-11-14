import glob
import os
from os import path as osp
from typing import List, Optional

import magnum as mn
import numpy as np
import pybullet as p
import pickle as pkl

from fairmotion_utils import AmassHelper, MotionData


class Motions:
    """
    The Motions class is collection of stats that will hold the different movement motions
    for the character to use when following a path. The character is left-footed so that
    is our reference for with step the motions assume first.
    """

    def __init__(self, amass_path, body_model_path):
        self.amass_path = amass_path
        self.body_model_path = body_model_path

        # logger.info("Loading Motion data...")

        # TODO: add more diversity here
        motion_files = {
            #"walk": f"{amass_path}/CMU/10/10_04_stageii.npz",  # [0] cycle walk
            "walk": f"{amass_path}/10_04_stageii.npz",
        }

        kwargs = {
            'model_type': "smplx"
        }
        motion_data = {
            key: AmassHelper.load_amass_file(value, bm_path=body_model_path, **kwargs)
            for key, value in motion_files.items()
        }

        # Standing pose that must be converted (amass -> habitat joint positions)
        self.standing_pose = motion_data["walk"].poses[0]


        

class AmassHumanConverterSMPLX:
    """
    Human Controller, converts high level actions such as walk, or reach into joints that control
    to control a URDF object.
    """

    def __init__(
        self,
        urdf_path,
        amass_path,
        body_model_path,
        motion_path=None,
        output_path="motion_mdm",
    ):
        self.motions = Motions(amass_path, body_model_path)
        skeleton = self.motions.standing_pose.skel

        self.pc_id = p.connect(p.DIRECT)
        self.human_bullet_id = p.loadURDF(urdf_path)

        self.link_ids = list(range(p.getNumJoints(self.human_bullet_id)))
        self.joint_info = [
            p.getJointInfo(self.human_bullet_id, index)
            for index in self.link_ids
        ]

        # Data used to grab
        # self.use_ik_grab = False
        
        content_motion = np.load(motion_path, allow_pickle=True)
        
        pose_info = {
            "trans": content_motion["trans"],
            "root_orient": content_motion["poses"][:,:3],
            "pose": content_motion["poses"][:, 3:66]
        }
        num_poses = content_motion["poses"].shape[0]
        transform_array = []
        joints_array = []
        for index in range(num_poses):
            # breakpoint()
            pose = MotionData.obtain_pose(
                skeleton, pose_info, index
            )

            pose_quat, root_trans, root_rot = AmassHelper.convert_CMUamass_single_pose(
                pose, self.joint_info, raw=False
            )
            transform_as_mat = np.array(
                mn.Matrix4.from_(root_rot.to_matrix(), root_trans)
            )
            transform_array.append(transform_as_mat[None, :])
            joints_array.append(np.array(pose_quat)[None, :])

        transform_array = np.concatenate(transform_array)
        joints_array = np.concatenate(joints_array)
        # breakpoint()
        walk_motion = {
            "joints_array": joints_array,
            "transform_array": transform_array,
            "displacement": None,
            "fps": 1
        }
        content_motion = {
            "pose_motion": walk_motion,
        }
        with open(f"{output_path}.pkl", 'wb+') as ff:
            pkl.dump(content_motion, ff)



if __name__ == '__main__':
    # Converts a npz motion file into a pkl file that can be processed in habitat. Note that the 
    # resulting pkl file will have the same format as the ones used to move the character in 
    # Humanoid RearrangeController
    # The npz file should contain:
    # trans: N x 3, specifying the root translation on each of the N poses
    # poses: N x (J*3 + 1) * 3: containing the root rotation, as well as the rotation for each
    # of the 21 joints 
    motion_file = "path_to_npz_files" # motion_to_convert (npz)
    files = glob.glob(motion_file)
    for in_path in files:
        AmassHumanConverterSMPLX(
            urdf_path="data/humanoids/humanoid_data/female2_0.urdf",
            amass_path="data/smplx/",
            motion_path=in_path,
            output_path=in_path.replace(".npz", ""),
            body_model_path="data/smplx/model/female/model.npz"
        )