from django.contrib.auth.backends import ModelBackend


class LDAPBackend(ModelBackend):
    """
    LDAP Backend
    """

    def authenticate(self, *args, **kwargs):
        """
        LDAP authenticate implementation from ModelBackend
        :return UserModel object
        """
        raise NotImplementedError
