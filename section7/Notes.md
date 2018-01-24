- Modified `UserModel`:
    - added `email` field with unique constraint.
    - added unique constraint to `username` field to make class method `find_by_username()` more consistent.
    - added `activated` field to indicate if the user has confirmed via email
    - set default value of `activated` to `False`, consider introducing default values for parameters here.
    - added class method `delete_from_db()` to roll back when sending confirmation email fails
    - added `json()` method for testing purpose (to show the `activated` field before/after user confirmation)

- Registration work flow:
    - user submits credentials
    - create a `UserModel` instance with field `activated=False` and call `save_to_db()`
    - send a confirmation email to user's registered email
    - after user click the link in the email, a GET request is send to the `/user_confirm/<int:_id>` endpoint, which sets the user's `activated` field to `True`

- Miscellaneous:
    - Used `os.environ` to retrieve MailGun domain and API key, since it will be consistent with our pattern in previous sections on deploying to Heroku and DigitalOcean.
    - Raised an `EnvironmentError` with some message when failed to load MailGun config from `os.environ`, and raised an `Exception` when failed to deliver confirmation email via MailGun. When registering a new user, try to catch these exceptions via `except Exception as e` and return the error message in `e`.

- Issues:
    - If having set both `text` and `html` field in MailGun request, the text is not shown.
    - Endpoint url may be compromised in the confirmation email, so anyone can send an arbitrary request to the endpoint to confirm registration without accessing the true email. Is it a problem?
    - Did not add any logic in user authentication (to test if the account is activated)
    - Should use a web page to indicate successful confirmation, now only returning a json message.
    - Consider introducing domain names, since we may have to need one for MailGun. The auto-genrated MailGun domain may not be able to function fully (I can use it to send to my Gmail but not Yahoo mail, and it ask me to do some more configurations).
