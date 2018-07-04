from import_export import resources
from .models import Party

class PartyResource(resources.ModelResource):
    class Meta:
        model = Party