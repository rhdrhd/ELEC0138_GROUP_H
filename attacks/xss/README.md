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
<p onclick="alert('HELLOOOOOOOO!');"> DON'T Click me!</p>
```

4. Click the review

## Mitigation

DOM-based XSS: This type of XSS attack occurs when data from an untrusted source is used to manipulate the Document Object Model (DOM) in an unsafe way. Vue.js might not automatically sanitize JavaScript code that manipulates the DOM directly, especially if you use v-html to insert raw HTML dynamically. Always ensure that any dynamic HTML is properly sanitized before insertion.

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
