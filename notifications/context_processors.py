from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        return {
            'notifications': Notification.objects.filter(user=request.user)[:5],
            'notif_count': Notification.objects.filter(user=request.user, is_read=False).count(),
        }
    return {'notifications': [], 'notif_count': 0}

