import pandas as pd
import numpy as np
import time
import datetime

class Model:
    def __init__(self):
        self.battery_level = 100
        self.running = False
        self.start_time = 0
        self.joint_positions_dict = []
        self.joint_names = []
        self.connections = []
        self.joint_data = None

    def load_joint_data(self, file_path):
        gait_swing_left_joint_position = pd.read_csv(file_path)
        gait_swing_left_joint_position_np = gait_swing_left_joint_position.iloc[1:].to_numpy()

        self.joint_names = ['left_foot', 'left_knee', 'left_hip', 'left_upper_hip', 'left_upper_knee', 'left_lower_knee', 'left_ankle',
                            'right_ankle', 'right_lower_knee', 'right_upper_knee', 'right_upper_hip', 'right_hip',
                            'right_knee', 'right_low_knee', 'right_foot']

        self.connections = [
            ('left_foot', 'left_knee'),
            ('left_knee', 'left_hip'),
            ('left_hip', 'left_upper_hip'),
            ('left_upper_hip', 'left_upper_knee'),
            ('left_upper_knee', 'left_lower_knee'),
            ('left_lower_knee', 'left_ankle'),
            ('left_ankle', 'right_ankle'),
            ('right_ankle', 'right_lower_knee'),
            ('right_lower_knee', 'right_upper_knee'),
            ('right_upper_knee', 'right_upper_hip'),
            ('right_upper_hip', 'right_hip'),
            ('right_hip', 'right_knee'),
            ('right_knee', 'right_low_knee'),
            ('right_knee', 'right_foot')
        ]

        time_steps = gait_swing_left_joint_position_np.shape[0]
        self.joint_positions_dict = []
        for step in range(time_steps):
            positions = {}
            for i, joint in enumerate(self.joint_names):
                x = float(gait_swing_left_joint_position_np[step, 1 + i * 3])
                y = float(gait_swing_left_joint_position_np[step, 2 + i * 3])
                z = float(gait_swing_left_joint_position_np[step, 3 + i * 3])
                positions[joint] = np.array([x, y, z])
            self.joint_positions_dict.append(positions)

        try:
            self.joint_data = pd.read_csv(file_path, index_col=0, parse_dates=True)
        except Exception as e:
            print(f"Error loading joint data: {e}")

    def get_joint_data(self):
        return self.joint_data

    def decrease_battery_level(self):
        if self.running and self.battery_level > 0:
            self.battery_level -= 1
            return self.battery_level

    def update_time(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        return str(datetime.timedelta(seconds=elapsed_time))

    def check_faults(self):
        leg_pos = np.array([0, 0])

        if np.abs(leg_pos).max() > 1.0:
            fault_time = str(datetime.timedelta(seconds=time.time() - self.start_time))
            fault_description = "Fault detected: Leg position exceeds limit."
            fault_explanation = f"At time {fault_time}, the position of one or more legs exceeded the allowed limit. Please check the leg movement parameters."
            return fault_description, fault_explanation
        else:
            return None, None


