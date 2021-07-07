from collections import defaultdict

from ldap3 import ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, SUBTREE

from django_ldap.ldap import ldap_connection


def get_paged_result(base, filter, attr, key, raw=False):
    results = defaultdict()

    with ldap_connection() as connection:

        entry_list = connection.extend.standard.paged_search(
            search_base=base,
            search_filter=filter,
            search_scope=SUBTREE,
            attributes=attr,
            paged_size=500,
            generator=False,
        )

        for entry in entry_list:
            try:
                name = entry["attributes"][key]
                if attr == [ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES] or raw == True:
                    results[name] = entry["attributes"]
                else:
                    results[name] = {a: entry["attributes"][a] for a in attr}
            except:
                pass
    return results
