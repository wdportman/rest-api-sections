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

- Issues:
    - If having set both `text` and `html` field in MailGun request, the text is not shown.
    - Endpoint url may be compromised in the confirmation email, so anyone can send an arbitrary request to the endpoint to confirm registration without accessing the true email. Is it a problem?
    - Did not add any logic in user authentication (to test if the account is activated)
    - Should use a web page to indicate successful confirmation, now only returning a json message.