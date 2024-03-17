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
3. send login request to phishing backend. Always return login successful to user and save user attempts into user_credentials.csv under attacks/phishing/phishing_website/backend

## Phishing website
Just use the same one as the real website in our project. Only login function is reimplemented.

## Mitigation Method
Using 2-factor authentication. Only the password stolen is not enough.

On the user side, we provide a simple Multi-layer perceptron model to detect if a url is phishing url

The training data and feature extractor is taken from https://github.com/vaibhavbichave/Phishing-URL-Detection/tree/master

To run the url test:
```
cd attacks/phishing
pip install -r requirements.txt
python url_detection.py
```
