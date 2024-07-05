import sys
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QProgressBar, QTextEdit, QTabWidget, QGroupBox, QScrollArea, QGridLayout, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d import art3d
from matplotlib.animation import FuncAnimation
import datetime

class OpeningWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Opening GUI Interface (GUI 인터페이스 열기)")
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()

        image_path = "" # Insert image path
        pixmap = QPixmap(image_path).scaled(500, 300, Qt.KeepAspectRatio)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        layout.addWidget(image_label)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        open_button = QPushButton("Open(열려 있는)")
        open_button.setObjectName("open_button")
        open_button.clicked.connect(self.open_main_gui)
        button_layout.addWidget(open_button)

        close_button = QPushButton("Close(닫다)")
        close_button.clicked.connect(self.close_app)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def open_main_gui(self):
        self.close()
        self.controller.show_main_view()

    def close_app(self):
        self.close()

class MainView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(' GUI (Graphical User Interface / 그래픽 사용자 인터페이스)')
        self.setGeometry(100, 100, 1400, 900)

        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.simulation_tab = QWidget()
        self.graphic_data_tab = QWidget()

        self.tabs.addTab(self.simulation_tab, "Simulation (시뮬레이션)")
        self.tabs.addTab(self.graphic_data_tab, "Data (데이터)")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.create_simulation_ui()
        self.create_graphic_data_tab_ui()
        self.init_3d_visualization()

    def create_simulation_ui(self):
        sim_layout = QVBoxLayout()

        main_pane = QHBoxLayout()
        left_pane = QVBoxLayout()
        right_pane = QVBoxLayout()

        viz_frame = QGroupBox("3D/2D Visualization")
        viz_layout = QVBoxLayout()

        self.fig = plt.figure(figsize=(12, 10))
        self.canvas = FigureCanvas(self.fig)
        viz_layout.addWidget(self.canvas)
        viz_frame.setLayout(viz_layout)
        left_pane.addWidget(viz_frame)

        scroll_widget = QGroupBox()
        self.joint_values_layout = QGridLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth(500)
        scroll_widget.setLayout(self.joint_values_layout)
        scroll_area.setWidget(scroll_widget)

        joint_values_groupbox = QGroupBox("Joint Values")
        joint_values_layout = QVBoxLayout()
        joint_values_layout.addWidget(scroll_area)
        joint_values_groupbox.setLayout(joint_values_layout)

        right_pane.addWidget(joint_values_groupbox)

        fault_group = QGroupBox("Fault Detection (결함 감지)")
        fault_group.setStyleSheet("background-color: white;")
        fault_layout = QVBoxLayout()
        self.time_label = QLabel("Simulation time: 00:00:00")
        fault_layout.addWidget(self.time_label)
        self.fault_text = QTextEdit()
        self.fault_text.setStyleSheet("background-color: #e0e0e0;")
        fault_layout.addWidget(self.fault_text)
        fault_group.setLayout(fault_layout)
        right_pane.addWidget(fault_group)

        main_pane.addLayout(left_pane, 2)
        main_pane.addLayout(right_pane, 1)
        sim_layout.addLayout(main_pane)

        battery_state_layout = QHBoxLayout()
        self.battery_bar = QProgressBar()
        self.battery_bar.setValue(100)
        self.battery_bar.setFormat("Battery Level: %p%")
        self.battery_bar.setStyleSheet("QProgressBar {color: black;}")
        battery_state_layout.addWidget(self.battery_bar)

        self.state_label = QLabel("Simulation State (시뮬레이션 상태): Stopped")
        self.state_label.setStyleSheet("color: red;")
        battery_state_layout.addWidget(self.state_label)

        sim_layout.addLayout(battery_state_layout)

        action_frame = QGroupBox("Action (행동)")
        action_frame.setStyleSheet("background-color: #e0e0e0;")
        action_layout = QVBoxLayout()
        self.action_label = QLabel("None")
        action_layout.addWidget(self.action_label)
        action_frame.setLayout(action_layout)
        sim_layout.addWidget(action_frame)

        control_layout = QHBoxLayout()
        start_button = QPushButton("Start Simulation (시뮬레이션 시작)")
        start_button.clicked.connect(self.controller.start_simulation)
        control_layout.addWidget(start_button)
        stop_button = QPushButton("Stop Simulation (시뮬레이션 중지)")
        stop_button.clicked.connect(self.controller.stop_simulation)
        control_layout.addWidget(stop_button)
        sim_layout.addLayout(control_layout)

        bottom_layout = QHBoxLayout()
        exit_button = QPushButton("Exit (출구)")
        exit_button.clicked.connect(self.close)
        bottom_layout.addWidget(exit_button)
        sim_layout.addLayout(bottom_layout)

        self.simulation_tab.setLayout(sim_layout)

    def create_graphic_data_tab_ui(self):
        graphic_data_layout = QVBoxLayout()

        combo_layout = QHBoxLayout()
        self.joint_selector = QComboBox()
        self.joint_selector.addItems([
            'left_foot', 'left_knee', 'left_hip', 'left_upper_hip',
            'right_foot', 'right_knee', 'right_hip'
        ])
        self.joint_selector.currentTextChanged.connect(self.controller.on_joint_selected)
        combo_layout.addWidget(self.joint_selector)
        graphic_data_layout.addLayout(combo_layout)

        self.graphic_data_canvas = FigureCanvas(Figure(figsize=(12, 8)))
        graphic_data_layout.addWidget(self.graphic_data_canvas)

        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        graphic_data_layout.addWidget(exit_button)

        self.graphic_data_tab.setLayout(graphic_data_layout)

    def init_3d_visualization(self):
        gait_swing_left_joint_position = pd.read_csv('') # Insert file path

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

        for positions in self.joint_positions_dict:
            com = np.mean(np.array(list(positions.values())), axis=0)
            positions['CoM'] = com

        def adjust_coordinates(joint_positions):
            translation_vector = joint_positions['left_foot']
            for joint in joint_positions:
                joint_positions[joint] -= translation_vector
                joint_positions[joint] = np.array([joint_positions[joint][0], -joint_positions[joint][2], joint_positions[joint][1]])
            return joint_positions

        self.joint_positions_dict = [adjust_coordinates(positions) for positions in self.joint_positions_dict]

        self.ax_main = self.fig.add_subplot(121, projection='3d')
        self.ax_2d = self.fig.add_subplot(122)

        self.ax_main.set_xlim(-0.5, 0.5)
        self.ax_main.set_ylim(-0.5, 0.5)
        self.ax_main.set_zlim(0, 1.5)

        self.ax_2d.set_xlim(-0.5, 0.5)
        self.ax_2d.set_ylim(-0.5, 1.5)

        self.lines_main = []
        self.points_main = []
        for _ in range(len(self.connections)):
            line, = self.ax_main.plot([], [], [], 'o-', lw=2, color='black')
            self.lines_main.append(line)
        for _ in range(len(self.joint_names)):
            point, = self.ax_main.plot([], [], [], 'o', color='blue')
            self.points_main.append(point)

        self.lines_2d = []
        self.points_2d = []
        for _ in range(len(self.connections)):
            line, = self.ax_2d.plot([], [], 'o-', lw=2, color='black')
            self.lines_2d.append(line)
        for _ in range(len(self.joint_names)):
            point, = self.ax_2d.plot([], [], 'o', color='blue')
            self.points_2d.append(point)

        def add_foot_patch(ax, x, y, z):
            p = Rectangle((x - 0.05, y - 0.05), 0.1, 0.1, color='gray', alpha=0.5)
            ax.add_patch(p)
            art3d.pathpatch_2d_to_3d(p, z=z, zdir="z")
            return p

        self.left_foot_patch_main = add_foot_patch(self.ax_main, self.joint_positions_dict[0]['left_foot'][0], self.joint_positions_dict[0]['left_foot'][1], self.joint_positions_dict[0]['left_foot'][2])
        self.right_foot_patch_main = add_foot_patch(self.ax_main, self.joint_positions_dict[0]['right_foot'][0], self.joint_positions_dict[0]['right_foot'][1], self.joint_positions_dict[0]['right_foot'][2])

        def init():
            for line in self.lines_main:
                line.set_data([], [])
                line.set_3d_properties([])
            for point in self.points_main:
                point.set_data([], [])
                point.set_3d_properties([])
            for line in self.lines_2d:
                line.set_data([], [])
            for point in self.points_2d:
                point.set_data([], [])
            return self.lines_main + self.points_main + self.lines_2d + self.points_2d

        def update(frame):
            for i, (start_joint, end_joint) in enumerate(self.connections):
                line_data = np.array([frame[start_joint], frame[end_joint]]).T
                self.lines_main[i].set_data(line_data[:2, :])
                self.lines_main[i].set_3d_properties(line_data[2, :])
                self.lines_2d[i].set_data(line_data[0, :], line_data[2, :])
            for i, joint in enumerate(self.joint_names):
                self.points_main[i].set_data([frame[joint][0]], [frame[joint][1]])
                self.points_main[i].set_3d_properties([frame[joint][2]])
                self.points_2d[i].set_data([frame[joint][0]], [frame[joint][2]])
            self.update_joint_display(frame)
            return self.lines_main + self.points_main + self.lines_2d + self.points_2d

        self.ani_main = FuncAnimation(self.fig, update, frames=self.joint_positions_dict, init_func=init, blit=False, interval=100)
        self.ani_main.event_source.stop()
        self.canvas.draw()

    def update_joint_display(self, joint_positions):
        for i in reversed(range(self.joint_values_layout.count())):
            widget = self.joint_values_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        row = 0
        for joint_name, coords in joint_positions.items():
            joint_group = QGroupBox(joint_name)
            joint_layout = QVBoxLayout()
            joint_group.setLayout(joint_layout)

            x_label = QLabel(f"X: {coords[0]:.2f}")
            y_label = QLabel(f"Y: {coords[1]:.2f}")
            z_label = QLabel(f"Z: {coords[2]:.2f}")

            font = x_label.font()
            font.setPointSize(14)
            x_label.setFont(font)
            y_label.setFont(font)
            z_label.setFont(font)

            joint_layout.addWidget(x_label)
            joint_layout.addWidget(y_label)
            joint_layout.addWidget(z_label)

            self.joint_values_layout.addWidget(joint_group, row // 2, row % 2)
            row += 1

    def plot_joint_data(self, df, joint, sample_rate):
        fig = self.graphic_data_canvas.figure
        fig.clear()

        ax = fig.add_subplot(111)
        time_vector = df.index / sample_rate

        ax.plot(time_vector, df[f'{joint}_X'], label=f'{joint.capitalize()} X', color='r', linewidth=0.7)
        ax.plot(time_vector, df[f'{joint}_Y'], label=f'{joint.capitalize()} Y', color='g', linewidth=0.7)
        ax.plot(time_vector, df[f'{joint}_Z'], label=f'{joint.capitalize()} Z', color='b', linewidth=0.7)
        ax.set_ylabel('Position', fontsize=8)
        ax.set_xlabel('Seconds (s)', fontsize=8)
        ax.set_title(f'{joint.capitalize()} Position in X, Y, Z Axes', fontsize=10)
        ax.legend(loc='upper right', fontsize='x-small')
        ax.grid(True, linestyle='--', linewidth=0.5)
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.set_xlim([0, 200])
        ax.set_xticks(range(0, 201, 25))
        ax.set_xticklabels([str(i) for i in range(0, 201, 25)], fontsize=8)

        fig.tight_layout()
        self.graphic_data_canvas.draw()

    def update_battery_level(self, level):
        self.battery_bar.setValue(level)
        if level > 50:
            self.battery_bar.setStyleSheet("QProgressBar::chunk { background-color: green; }")
        elif 10 < level <= 50:
            self.battery_bar.setStyleSheet("QProgressBar::chunk { background-color: orange; }")
        else:
            self.battery_bar.setStyleSheet("QProgressBar::chunk { background-color: red; }")

    def update_action(self, action):
        self.action_label.setText(f"Current Action: {action}")


