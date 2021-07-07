from ldap3 import SUBTREE

from django_ldap.ldap import ldap_connection


def paged_query(base, filter, attr, generator=False):
    with ldap_connection() as conn:
        return conn.extend.standard.paged_search(
            search_base=base,
            search_filter=filter,
            search_scope=SUBTREE,
            attributes=attr,
            paged_size=500,
            generator=generator,
        )
