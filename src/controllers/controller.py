import time
import datetime
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import pandas as pd
import numpy as np


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.battery_level = 100
        self.running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulate)

        self.start_time = None

    def show_main_view(self):
        self.view.show()

    def on_tab_change(self, index):
        if index == 1:
            self.load_joint_data_csv()

    def load_joint_data_csv(self):
        file_path = '' # Import CSV file
        self.model.load_joint_data(file_path)
        self.plot_joint_data()

    def plot_joint_data(self):
        df = self.model.get_joint_data()
        if df is not None:
            joint = self.view.joint_selector.currentText()
            sampling_interval = (df.index[1] - df.index[0])
            sample_rate = 1 / sampling_interval
            self.view.graphic_data_canvas.figure.clear()
            ax = self.view.graphic_data_canvas.figure.add_subplot(111)

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
            ax.set_xlim([0, 200])  # Set x-axis limit to 200 seconds
            ax.set_xticks(range(0, 201, 25))
            ax.set_xticklabels([str(i) for i in range(0, 201, 25)], fontsize=8)

            
            self.view.graphic_data_canvas.draw()

    def on_joint_selected(self):
        self.plot_joint_data()

    def start_simulation(self):
        self.running = True
        self.view.state_label.setText("Simulation State (시뮬레이션 상태) : Running")
        self.view.state_label.setStyleSheet("color: green;")
        self.view.state_label.setProperty("status", "running")
        self.view.state_label.style().polish(self.view.state_label)
        self.update_action("Walking")
        self.decrease_battery_level()
        self.start_timer()
        self.timer.start(1000)
        self.view.ani_main.event_source.start()

    def stop_simulation(self):
        self.running = False
        self.view.state_label.setText("Simulation State (시뮬레이션 상태) : Stopped")
        self.view.state_label.setStyleSheet("color: red;")
        self.view.state_label.setProperty("status", "stopped")
        self.view.state_label.style().polish(self.view.state_label)
        self.update_action("Stopped")
        self.timer.stop()
        self.view.ani_main.event_source.stop()

    def update_action(self, action):
        self.view.action_label.setText(f"Current Action: {action}")

    def simulate(self):
        if self.running:
            self.update_time()
            self.check_faults()
            self.update_simulation_details()

    def decrease_battery_level(self):
        if self.running and self.battery_level > 0:
            self.battery_level -= 1
            self.view.battery_bar.setValue(self.battery_level)
            self.update_battery_color()
            QTimer.singleShot(1000, self.decrease_battery_level)
        elif self.battery_level <= 0:
            self.view.fault_text.setStyleSheet("color: black;")
            QMessageBox.information(self.view, "Battery Level", "Battery is empty")
            self.stop_simulation()

    def update_battery_color(self):
        if self.battery_level > 50:
            self.view.battery_bar.setStyleSheet("QProgressBar::chunk { background-color: green; }")
        elif 10 < self.battery_level <= 50:
            self.view.battery_bar.setStyleSheet("QProgressBar::chunk { background-color: orange; }")
        else:
            self.view.battery_bar.setStyleSheet("QProgressBar::chunk { background-color: red; }")

    def start_timer(self):
        self.start_time = time.time()

    def update_time(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        self.view.time_label.setText(f"Simulation time: {str(datetime.timedelta(seconds=elapsed_time))}")

    def check_faults(self):
        leg_pos = np.array([0, 0])
        if np.abs(leg_pos).max() > 1.0:
            fault_time = str(datetime.timedelta(seconds=time.time() - self.start_time))
            fault_description = "Fault detected: Leg position exceeds limit."
            fault_explanation = f"At time {fault_time}, the position of one or more legs exceeded the allowed limit. Please check the leg movement parameters."
            self.view.fault_text.setTextColor(QColor("red"))
            self.view.fault_text.append(f"{fault_description}\n{fault_explanation}\n\n")
            self.stop_simulation()
        else:
            self.view.fault_text.setTextColor(QColor("green"))
            self.view.fault_text.append("No fault detected.")

    def update_simulation_details(self):
        self.view.fault_text.setStyleSheet("color: black;")
        self.view.fault_text.append(f"Simulation running: {str(datetime.timedelta(seconds=time.time() - self.start_time))}")

    def load_csv(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self.view, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            self.view.file_path_display.setText(file_name)
            df = pd.read_csv(file_name)
            self.view.display_graphs(df)

    def save_csv(self):
        csv_name = self.view.csv_name_input.text()
        if not csv_name:
            QMessageBox.warning(self.view, "Input Error", "Please enter a CSV name.")
            return

        data = {
            "Column1": np.random.randn(100),
            "Column2": np.random.randn(100)
        }
        df = pd.DataFrame(data)
        save_path = QFileDialog.getSaveFileName(self.view, "Save CSV", f"{csv_name}.csv", "CSV Files (*.csv);;All Files (*)")[0]
        if save_path:
            df.to_csv(save_path, index=False)
            QMessageBox.information(self.view, "Save Success", f"CSV file saved as {save_path}")

    def load_motion_csv(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self.view, "Open Motion CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            self.view.motion_file_path_display.setText(file_name)
            df = pd.read_csv(file_name)
            self.view.motion_plot_figure.clear()
            ax = self.view.motion_plot_figure.add_subplot(111)
            ax.plot(df.index, df.iloc[:, 0])
            ax.set_title('Motion CSV Data Plot')
            ax.set_xlabel('Position')
            ax.set_ylabel('Seconds')
            self.view.motion_canvas.draw()






    



