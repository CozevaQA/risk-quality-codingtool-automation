from plyer import notification

def notify_success(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=5
    )