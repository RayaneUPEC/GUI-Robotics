import sys
import time
from PyQt5.QtWidgets import QApplication
from views.view import OpeningWindow, MainView
from controllers.controller import Controller

def measure_performance():
    app = QApplication(sys.argv)

    # Measure the OpeningWindow initialization time
    start_time = time.time()
    controller = Controller()
    splash = OpeningWindow(controller)
    end_time = time.time()
    opening_window_time = end_time - start_time
    print(f"OpeningWindow initialization time: {opening_window_time:.4f} seconds")

    # Measure the MainView initialization time
    start_time = time.time()
    main_view = MainView(controller)
    end_time = time.time()
    main_view_time = end_time - start_time
    print(f"MainView initialization time: {main_view_time:.4f} seconds")

    # Load the CSS file
    css_path = "" # Insert the CSS file path
    start_time = time.time()
    with open(css_path, "r") as f:
        css = f.read()
        app.setStyleSheet(css)
    end_time = time.time()
    css_load_time = end_time - start_time
    print(f"CSS file load time: {css_load_time:.4f} seconds")

    # Show the OpeningWindow
    splash.show()

    # Run the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    measure_performance()

