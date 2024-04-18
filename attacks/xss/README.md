# Cross-Site Scripting (XSS)

## Attack

1. Start the server with unsafe mode

```bash
# backend
$ cd path/to/this/repo
$ cd v1/backend
$ MODE=unsafe python app.py

# frontend
$ cd path/to/this/repo
$ cd v1/frontend
$ vim .env.development
...
# set VITE_APP_MODE=unsafe
$ npm run dev
```

2. Open `http://localhost:5173/details/1`
3. Post a new review with the following content:

```
<p onclick="alert('WARNING: You are running a malicious script!!!!!');"> DON'T Click me!</p>
```

4. Click the review

## Mitigation

### Stored XSS

Stored XSS occurs when a web application stores user input that is later embedded in output delivered to other users. The malicious script is stored on the server (e.g., in a database, message forum, visitor log, comment field).
When other users access the stored information, the malicious script executes within their browsers. This makes stored XSS particularly dangerous, as it can affect multiple users and persists over time until the malicious data is removed.

Therefore, we must replace

```html
<p class="review-text" v-html="review.review_text"></p>
```

with

```html
<p class="review-text"> {{ review.review_text }}</p>
```

by using safe mode:

```bash
# backend
$ cd path/to/this/repo
$ cd v1/backend
$ python app.py

# frontend
$ cd path/to/this/repo
$ cd v1/frontend
$ vim .env.development
...
# set VITE_APP_MODE=safe
$ npm run dev
```
