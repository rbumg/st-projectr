from django.contrib import admin

from app.models import City, Project


class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "state")
    search_fields = ("name", "state")
    list_filter = ("cost_type",)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("set", "idx", "name", "start_date", "end_date", "get_city")
    search_fields = ("name",)
    list_filter = ("city",)
    ordering = ("set", "idx")

    def get_city(self, obj):
        # Append the cost type to the city name
        return obj.city.name + f" ({obj.city.get_cost_type_display()})"

    get_city.short_description = "City (Cost Type)"


admin.site.register(City, CityAdmin)
admin.site.register(Project, ProjectAdmin)
