from django.contrib import admin

# Register your models here.
from .models import Data
from .models import MapData
from .models import AgentKeys
from .models import AgentData

admin.site.register(Data)
admin.site.register(MapData)
admin.site.register(AgentKeys)
admin.site.register(AgentData)
