from kivy.app import App
from kivy.uix.widget import Widget
from kivy.base import EventLoop

from IPython.lib.inputhook import stdin_ready, InputHookManager

class TestApp(App):
    def build(self):
        return Widget()

def get_app_kivy(*args, **kwargs):
    """Create a new wx app or return an exiting one."""
    app = TestApp()
    return app

def is_event_loop_running_kivy(app=None):
    """Is the wx event loop running."""
    if app is None:
        app = get_app_kivy()
    if hasattr(app, '_in_event_loop'):
        return app._in_event_loop
    else:
        from kivy.base import EventLoop
        if EventLoop is not None and EventLoop.status == "started":
            return True
        else:
            return False

def start_event_loop_kivy(app=None):
    """Start the kivy event loop in a consistent manner."""
    if app is None:
        app = get_app_kivy()
    if not is_event_loop_running_kivy(app):
        app._in_event_loop = True
        app.run()
        app._in_event_loop = False
    else:
        app._in_event_loop = True

def create_inputhook_kivy(app=None):
    if app is None:
        app = App.get_running_app()
        if app is None:
            app = get_app_kivy()

    def inputhook_kivy(self = None):
        try:
            while not stdin_ready() and not EventLoop.quit:
                EventLoop.window._mainloop()

        except KeyboardInterrupt:
            print("???")

        return 0

    return app, inputhook_kivy

def enable_kivy():
    app, inputhook = create_inputhook_kivy()
    inputhook_manager = InputHookManager()
    inputhook_manager.set_inputhook(inputhook)
    app.run(True)
    return app
