# Importing the required modules

# The admin module is used to create the admin site for the application
from django.contrib import admin

# The models module is used to import the models from the models.py file
from .models import Candidate, Position


# The admin.site.register() method is used to register the models to the admin site
@admin.register(Position)

# The PositionAdmin class is used to create the admin site for the Position model
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Candidate)

# The CandidateAdmin class is used to create the admin site for the Candidate model
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name','position')
    list_filter = ('position',)
    search_fields = ('name','position')
    readonly_fields = ('total_vote',)
