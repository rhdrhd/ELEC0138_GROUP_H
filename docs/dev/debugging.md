# Debugging

## Backend APIs

You need to create the "security" conda environment first.

```bash
$ cd v1/backend
$ conda activate security
$ python app.py
```

### v1 APIs

> Tips: If you don't want to use `curl` to send requests, you can try [postman](https://www.postman.com/).

* `/api/v1/login`

```bash
# Use curl to send a post request to the /api/v1/login API with user data and get its response
$ curl -X POST http://127.0.0.1:5000/api/v1/login -d '{ "username":"elec0138","password":"8964"}' -H 'Content-Type: application/json'
{
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImVsZWMwMTM4IiwicGFzc3dvcmQiOiJwYmtkZjI6c2hhMjU2OjI2MDAwMCQ5Q0VoRGZubVV1Q2pSWEZrJDYzOWI1NzA5NmU4NGIwZDM4YTBhNTc5ODhiNjFlODQ1Y2NlZDVkOWRiZjliZTM3YmM3MDE3ZmJmM2E0ZDgyY2UiLCJleHAiOjE3MDk5MzQ5NTd9.wPrmZDGGTXfiIr2vUNuhGSbxeUErLpshhFzkh_DkdRA",
    "user": {
      "username": "elec0138"
    }
  },
  "msg": "User logged in successfully.",
  "status": "SUCCESS"
}
```

* `/api/v1/dashboard`
```bash
# Use curl to send a POST request to the /api/v1/dashboard API with the token you get from the /api/v1/login API (remember the token will expire after a few minutes)
# Notice: Authorization token format: `Bearer <YOUR_TOKEN>`.
# More details: https://swagger.io/docs/specification/authentication/bearer-authentication/
$ curl -X POST http://127.0.0.1:5000/api/v1/dashboard -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImVsZWMwMTM4IiwicGFzc3dvcmQiOiJwYmtkZjI6c2hhMjU2OjI2MDAwMCQ5Q0VoRGZubVV1Q2pSWEZrJDYzOWI1NzA5NmU4NGIwZDM4YTBhNTc5ODhiNjFlODQ1Y2NlZDVkOWRiZjliZTM3YmM3MDE3ZmJmM2E0ZDgyY2UiLCJleHAiOjE3MDk5MzQ5NTd9.wPrmZDGGTXfiIr2vUNuhGSbxeUErLpshhFzkh_DkdRA' -H 'Content-Type: application/json'
# if the token has not expired
{
  "data": {
    "user": {
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
