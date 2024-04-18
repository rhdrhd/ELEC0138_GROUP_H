# Cross Site Request Forgery (CSRF)

## Process
1. User login to the website and keep active
2. The browser saves the cookie for this session
3. The user visit a malicious website
4. The script in this website sends a request to the server with this cookie for authentication

## Example

1. Login to the ticket selling website in unsafe mode using "elec0138" account
2. Open malicious.html and a request modifying the email address of this user will be sent.

```
{
  "data": {
    "email": "attacker@example.com", 
    "username": "elec0138"
  }, 
  "msg": "Profile updated successfully.", 
  "status": "success"
}
```
3. In the database, this email address will be changed to

    (1, 'elec0138', '8964', 'attacker@example.com')

## Mitigation

1. Save JWT in local storage instead of cookie
2. Set SameSite cookie attribute to 'Strict' or 'Lax'

Other good mitigation method have not been implemented yet.

...