# SQL injection

Vulnerable code for injection:
```
cur.execute(f"SELECT * FROM users WHERE username = '{username}'")
```

SQL injection examples
1. username = ' OR '1'='1' --
```
SELECT * FROM users WHERE username = '' OR '1'='1'
{
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IicgT1IgJzEnPScxJyAtLSIsInBhc3N3b3JkIjoicGJrZGYyOnNoYTI1NjoyNjAwMDAkOUNFaERmbm1VdUNqUlhGayQ2MzliNTcwOTZlODRiMGQzOGEwYTU3OTg4YjYxZTg0NWNjZWQ1ZDlkYmY5YmUzN2JjNzAxN2ZiZjNhNGQ4MmNlIiwiZXhwIjoxNzEwNjI2OTg5fQ.oOYUXDTt5c8t98esazE_fVG35I-FMzDnA0DxT5QNcoU",
    "user": {
      "username": "' OR '1'='1' --"
    }
  },
  "msg": "User logged in successfully.",
  "status": "SUCCESS"
}
```




Safe code:

```
cur.execute("SELECT * FROM users WHERE username = ?", (username,))
```