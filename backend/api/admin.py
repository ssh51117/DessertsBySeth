from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.MailingListSubscriber)
admin.site.register(models.GuineaPig)
admin.site.register(models.GuineaPigDrop)
admin.site.register(models.GuineaPigClaim)
admin.site.register(models.Product)
admin.site.register(models.PreorderWindow)
admin.site.register(models.PreorderListing)
admin.site.register(models.Preorder)
admin.site.register(models.PreorderItem)
admin.site.register(models.CustomOrderRequest)