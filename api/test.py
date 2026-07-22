from api.models import User
User.objects.filter(username='qwer').values('is_staff', 'is_superuser')