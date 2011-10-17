# import the User object
from django.contrib.auth.models import User

# import the IMAP library
from imaplib import IMAP4

# import time - this is used to create Django's internal username
import time
import settings

mail_server = settings.IMAP_SERVER
use_full_mail = settings.USE_FULL_MAIL

# Name my backend 'MyCustomBackend'
class ImapBackend(object):

    supports_inactive_user = False
    supports_object_permissions = False
    supports_anonymous_user = False

    # Create an authentication method
    # This is called by the standard Django login procedure
    def authenticate(self, username=None, password=None):
        try:
            # Check if this user is valid on the mail server
            c = IMAP4(mail_server)
            c.login(username, password)
            c.logout()
        except:
            return None

	if use_full_mail:
	        try:
        	    # Check if the user exists in Django's local database
	            user = User.objects.get(email=username)
        	except User.DoesNotExist:
	            # Create a user in Django's local database
        	    user = User.objects.create_user(time.time(), username, 'internalpw')
	else:
		user, created = User.objects.get_or_create(username=username)

        return user

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
