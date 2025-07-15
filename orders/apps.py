from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' #Sets the default auto field for the app
    name = 'orders' #Sets the name of the app