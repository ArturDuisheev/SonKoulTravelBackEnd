from django.contrib import admin

from .models import (
    TourDates,
    TourProgram,
    Tips,
    Price,
    Photo,
    TourAdd,
    BookingGroupTour,
    BookingPrivateTour
)

admin.site.register(TourAdd)
admin.site.register(TourProgram)
admin.site.register(Price)
admin.site.register(Tips)
admin.site.register(Photo)
admin.site.register(TourDates)
admin.site.register(BookingGroupTour)
admin.site.register(BookingPrivateTour)
