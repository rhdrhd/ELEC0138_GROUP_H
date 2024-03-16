# Phishing Attack
## Process
1. send a phishing email to all victims in victim_list.csv (requires a gmail account and corresponding app password) (not tested yet)
```
cd attacks/phishing
python email_sending.py
```
2. start a phishing website
```
cd attacks/phishing/phishing_website/backend
python app.py
```
3. send login request to phishing backend. The phishing website will send the same request to real website. If login successful, the user account will be stolen.

## Phishing website
Just use the same one as the real website in our project. Only login function is reimplemented.

## Mitigation Method
Using 2-factor authentication. Only the password stolen is not enough.
