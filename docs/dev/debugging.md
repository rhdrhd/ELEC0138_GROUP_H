# Debugging

## backend API

You need to create the "security" conda environment first.

```bash
$ cd backend
$ conda activate security
$ python app.py
```

* `/login`

```bash
# Use curl to send a post request to the /login API with user data and get its response
$ curl -X POST http://127.0.0.1:5000/login -d '{ "username":"elec0138","password":"8964"}' -H 'Content-Type: application/json'
{
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsImV4cCI6MTcwOTY5NzA2MX0.ZeWnRWUFEnXz11_eqcGVl3SZbIXr8B8KRRMpOw2I4oA",
    "user": {
      "id": "1",
      "username": "elec0138"
    }
  },
  "msg": "User logged in successfully.",
  "status": "SUCCESS"
}
```

* `/dashboard`
```bash
# Use curl to send a POST request to the /dashboard API with the token you get from the /login API (remember the token will expire after a few minutes)
$ curl -X POST http://127.0.0.1:5000/dashboard -d '{ "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsImV4cCI6MTcwOTY5NzA2MX0.ZeWnRWUFEnXz11_eqcGVl3SZbIXr8B8KRRMpOw2I4oA"}' -H 'Content-Type: application/json'
# if the token has not expired
{
  "data": {
    "user": {
      "id": "1",
      "username": "elec0138"
    }
  },
  "msg": "Dashboard",
  "status": "SUCCESS"
}
# expired
{
  "msg": "Your session has expired. Please log in again.",
  "status": "FAILED"
}
```
