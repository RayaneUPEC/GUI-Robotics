import sys
from PyQt5.QtWidgets import QApplication
from models.model import Model
from views.view import OpeningWindow, MainView
from controllers.controller import Controller

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("#css#", "r") as f:
        css = f.read()
        app.setStyleSheet(css)

    # Indicate that the CSS has been loaded
    print("CSS loaded successfully.")

    # Create model
    model = Model()
    print("Model OK.")

    # Create controller first with no view
    controller = Controller(model, None)
    print("Controller created without view.")

    # Create main view with controller reference
    main_view = MainView(controller)
    print("Main view OK.")

    # Update controller's view reference
    controller.view = main_view
    print("Controller's view reference updated.")

    # Update view's controller reference
    main_view.controller = controller
    print("Main view's controller reference updated.")

    # Create and show the opening view
    opening_view = OpeningWindow(controller)
    opening_view.show()
    print("Opening view shown.")

    # Execute the application
    sys.exit(app.exec_())
    print("Application exited.")


