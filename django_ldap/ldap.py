from contextlib import contextmanager

from ldap3 import Server, Tls, Connection

from django_ldap.settings import logger, ldap_settings


@contextmanager
def ldap_connection(*args, **kwargs):
    logger.info("Creating LDAP connection")

    tls_configuration = (
        Tls(
            validate=ldap_settings.LDAP_TLS_VALIDATE,
            version=ldap_settings.LDAP_TLS_VERSION,
        )
        if ldap_settings.LDAP_TLS
        else None
    )

    server = Server(
        ldap_settings.LDAP_HOST,
        use_ssl=ldap_settings.LDAP_TLS,
        tls=tls_configuration,
    )

    with Connection(
        server,
        user=ldap_settings.LDAP_BIND_USER_DN,
        password=ldap_settings.LDAP_BIND_PASS,
        auto_bind=True,
        authentication=ldap_settings.LDAP_AUTH_MODE,
    ) as conn:
        logger.info(f"Connection: {conn}")

        yield conn
