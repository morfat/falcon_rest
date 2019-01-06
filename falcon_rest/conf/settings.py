"""
Settings and configuration for Falcon Rest 

Read values from the module specified by the FALCON_REST_SETTINGS_MODULE environment
variable, and then from django.conf.global_settings; see the global_settings.py
for a list of all possible variables.
"""

import os
import importlib
from falcon_rest.conf import global_settings


ENVIRONMENT_VARIABLE = "FALCON_REST_SETTINGS_MODULE"

class Settings:
    def __init__(self):
        # update this dict from global settings (but only for ALL_CAPS settings)
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))

        # store the settings module in case someone later cares
        self.SETTINGS_MODULE =  os.environ.get(ENVIRONMENT_VARIABLE)

        mod = importlib.import_module(self.SETTINGS_MODULE)

        tuple_settings = (
            "INSTALLED_APPS",
        )
        self._explicit_settings = set()
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)

                if (setting in tuple_settings and
                        not isinstance(setting_value, (list, tuple))):
                    raise ImproperlyConfigured("The %s setting must be a list or a tuple. " % setting)
                setattr(self, setting, setting_value)
                self._explicit_settings.add(setting)

        #if not self.SECRET_KEY:
        #    raise ImproperlyConfigured("The SECRET_KEY setting must not be empty.")

    def __repr__(self):
        return '<%(cls)s "%(settings_module)s">' % {
            'cls': self.__class__.__name__,
            'settings_module': self.SETTINGS_MODULE,
        }


settings = Settings()
