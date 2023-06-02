from handler import handler_app_factory
from frontend import frontend_app_factory
from feeding_calc import feeding_calc_app_factory


# ChatGPT said to do this, but it clearly just runs one app at a time
# looks like computers aren't coming for my job after all.
if __name__ == "__main__":
    handler_app = handler_app_factory()
    with handler_app.app_context():
        handler_app.run(port=55001, host="0.0.0.0")

    feeding_calc_app = feeding_calc_app_factory()
    with feeding_calc_app.app_context():
        feeding_calc_app.run(port=55003, host="0.0.0.0")

    frontend_app = frontend_app_factory()
    with frontend_app.app_context():
        frontend_app.run(port=55005, host="0.0.0.0")
