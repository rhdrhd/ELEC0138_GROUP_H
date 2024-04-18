# Brute-force Attack

## Attack

To run brute force attack with 
1. 1000 most common passwords
2. all possible passwords less than 6 digits

```
cd attacks/brute_force
python brute_force.py
```

In password-top1000.txt line 100, the correct password 8964 is added to save debugging time.

## Mitigation

1. recaptcha to prevent malicious script
2. Enable Flask-limiter to control the number of requests