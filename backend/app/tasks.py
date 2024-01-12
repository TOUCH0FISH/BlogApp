from .celery_worker import celery

@celery.task(name='app.tasks.send_notification')
def send_notification(user_id, message):
    from . import create_app
    app = create_app()

    with app.app_context():
        from .models.models import Notification
        from . import db

        notification = Notification(message=message, user_id=user_id)
        db.session.add(notification)
        db.session.commit()
