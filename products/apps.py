from django.apps import AppConfig


class ProductsConfig(AppConfig): #Configures the products app
    default_auto_field = 'django.db.models.BigAutoField' #Sets the default auto field to BigAutoField
    name = 'products' #Sets the name of the app
