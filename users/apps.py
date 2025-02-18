from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Configuration for the 'users' app in Django.

    This class defines the configuration for the 'users' app, including the default field type for primary keys
    and the initialization of app signals. It is automatically used when the app is started by Django.

    Attributes:
        default_auto_field (str): The default field type for auto-generated primary keys. Set to 'BigAutoField' for large-scale applications.
        name (str): The name of the app, in this case, 'users'.

    Methods:
        ready(self): Called when the app is ready. It imports the signals module to ensure signals are connected.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        """
        Initializes the signals for the 'users' app when the app is ready.

        This method ensures that the signals defined in the `users.signals` module are connected when the app starts up.
        It is typically called during the app startup to hook into the Django signal system.

        Returns:
            None: This method does not return any value, but ensures signals are properly imported and connected.
        """
        import users.signals  # Import signals on app startup
