# Phishing Attack
## Process
1. send a phishing email to all victims in victim_list.csv (requires a gmail account and corresponding app password) (not tested yet)
```
cd attacks/phishing
python email_sending.py
```
2. start a phishing website

Open a terminal and run
```
cd attacks/phishing/phishing_website/frontend
npm install
npm run dev
```
Open another terminal and run
```
cd attacks/phishing/phishing_website/backend
python app.py
```
The frontend will run in port 4001 and backend in 8001

3. send login request to phishing backend. Always return login successful to user and save user attempts into user_credentials.csv under attacks/phishing/phishing_website/backend. Saved usernames and passwords can be tried to login in the real website later.

## Phishing website
A website similar to the real one for demonstration purpose.


## Mitigation
Using 2-factor authentication. Only the password stolen is not enough.

On the user side, we provide a simple Multi Layer Perceptron (MLP) model demo in url_detection.py to detect if a url is phishing url

The training data and feature extractor is taken from https://github.com/vaibhavbichave/Phishing-URL-Detection/tree/master. The model is retrained.

To run the url test:
```
cd attacks/phishing
pip install -r requirements.txt
python url_detection.py
```

Example:

Enter the URL: http://localhost:4001/

The probability of the URL being a phishing URL is:  0.999981000754567
