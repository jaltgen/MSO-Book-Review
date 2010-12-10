# -*- coding: utf-8 -*-
import ldap

from django.contrib.auth.models import User

import settings

class LDAPBackend():
    def authenticate(self, username=None, password=None):
        # Benutzer gegen die Datenbank authentifizieren, wenn das gut geht existiert er und das Passwort stimmt
        ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, settings.BASE_PATH + '/cacert.pem')
        conn = ldap.initialize(settings.LDAP_URI)
        try:
            conn.simple_bind_s("uid=" + username + "," + settings.LDAP_USER_BASE, password)
        except ldap.INVALID_CREDENTIALS:
            return None

        # Sämtliche Benutzerdaten aus der LDAP sammeln
        ldap_data = conn.search_s(settings.LDAP_USER_BASE, ldap.SCOPE_SUBTREE, "(uid=" + username + ")")

        # Jetzt das entsprechende User Objekt aus der Django DB rauskramen oder anlegen
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(username=username, password="")
            user.set_unusable_password()
            user.first_name = ldap_data[0][1]['givenName'][0]
            user.last_name = ldap_data[0][1]['sn'][0]
            user.save()

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
