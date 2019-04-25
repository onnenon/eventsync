def register_blueprints(app):
    from eventsync.Blueprints.auth import auth
    from eventsync.Blueprints.events import events
    from eventsync.Blueprints.users import users
    from eventsync.Blueprints.invites import invites

    app.register_blueprint(auth)
    app.register_blueprint(events)
    app.register_blueprint(users)
    app.register_blueprint(invites)
