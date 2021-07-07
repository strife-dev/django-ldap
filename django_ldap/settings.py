"""
Settings for LDAP framework are all namespaced in the DJANGO_LDAP setting.
For example, in your settings.py:
DJANGO_LDAP = {
    'LDAP_HOST': "ldap://localhost:389",
    'LDAP_TLS': True
    'LDAP_SET_LDAP3_ARGS': {
        'SOCKET_SIZE': 4096,
        'RESTARTABLE_TRIES': 30
    },
}
This module exposes an `ldap_setting` object used across this framework, user options set in the DJANGO_LDAP settings
option are taken preference over the defaults set in this file.

Implementation derived from Django Rest Framework code, https://github.com/encode/django-rest-framework/blob/master/rest_framework/settings.py
"""
import logging
import ssl

from django.conf import settings
from django.test.signals import setting_changed
from django.utils.module_loading import import_string

logger = logging.getLogger("django_ldap")

DEFAULTS = {
    "LDAP_DRIVER": "ldap3",  # currently only supports ldap3, eventually python-ldap
    "LDAP_HOST": "ldap://localhost:389",
    "LDAP_TLS": False,
    "LDAP_TLS_VALIDATE": ssl.CERT_OPTIONAL,
    "LDAP_TLS_VERSION": ssl.PROTOCOL_TLSv1,
    "LDAP_BIND_USER_DN": None,
    "LDAP_BIND_PASS": None,
    "LDAP_PAGE_SIZE": "500",
    "LDAP_SEARCH_ROOT": "dc=example,dc=com",
    "LDAP_ENABLE_REF_CACHE": True,
    "LDAP_SET_LDAP3_ARGS": {},
    "LDAP_AUTH_MODE": None,
}

# List of settings that may be in string import notation.
IMPORT_STRINGS = []

# List of settings that have been removed
REMOVED_SETTINGS = []


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        return import_string(val)
    except ImportError as e:
        msg = "Could not import '%s' for LDAP setting '%s'. %s: %s." % (
            val,
            setting_name,
            e.__class__.__name__,
            e,
        )
        raise ImportError(msg)


class LDAPSettings:
    """
    A settings object that allows REST Framework settings to be accessed as
    properties. For example:
        from django_ldap.settings import ldap_settings
        print(ldap_settings.LDAP_HOST)
    Any setting with string import paths will be automatically resolved
    and return the class, rather than the string literal.
    Note:
    This is an internal class that is only compatible with settings namespaced
    under the DJANGO_LDAP name.
    """

    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, "DJANGO_LDAP", {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        SETTINGS_DOC = "https://github.com/strife-dev/django-ldap/blob/master/documentation/settings.md"
        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(
                    "The '%s' setting has been removed. Please refer to '%s' for available settings."
                    % (setting, SETTINGS_DOC)
                )
        return user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")


ldap_settings = LDAPSettings(None, DEFAULTS, IMPORT_STRINGS)


def reload_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == "DJANGO_LDAP":
        ldap_settings.reload()


setting_changed.connect(reload_settings)
