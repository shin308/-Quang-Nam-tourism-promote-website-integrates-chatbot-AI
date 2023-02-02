from django.contrib import admin
from .models import Destination
from .models import Detailed_desc
from .models import NetBanking
from .models import Cards
# from .models import User
from .models import Transactions
from .models import pessanger_detail
# Register your models here.

# admin.site.register(User)
admin.site.register(Cards)
admin.site.register(NetBanking)
admin.site.register(Destination)
admin.site.register(Detailed_desc)
admin.site.register(Transactions)
admin.site.register(pessanger_detail)

