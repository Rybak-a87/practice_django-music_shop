from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'musicshop.main'   # TODO разобраться как сделать чтобы работало без <musicshop.>
