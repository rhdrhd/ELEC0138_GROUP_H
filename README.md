# ELEC0138_GROUP_H

## Contents

- [Prerequisites](#Prerequisites)
- [Environment Setup](#Environment-Setup)
    - [Frontend](#Frontend)
    - [Backend](#Backend)
    - [Database](#Database)
- [Debugging](#Debugging)

## Prerequisites

* [Node.js 20.11.1](https://nodejs.org/en)
* [Anaconda](https://www.anaconda.com/) / [Miniconda](https://docs.anaconda.com/free/miniconda/index.html) for python 3.8

## Environment Setup

We offer two versions of our ticket sales website.
One is the original version (v1) which may have some security risks and vulnerabilities,
and the other is a newer version (v2) that incorporates numerous mechanisms to safeguard the system.

To access each version of the website, you'll need to navigate to the respective directory first.

```bash
$ cd v1
# or
$ cd v2
```

### Frontend

We are using [Vue.js](https://vuejs.org/guide/quick-start) to create our frontend website.

Open a new terminal and run:

```bash
# cd v1 or v2
$ cd frontend
$ npm install
$ npm run dev
```

And then you can visit our ticket selling website through `http://localhost:5173`.

### Backend

We are using [Flask](https://flask.palletsprojects.com/en/3.0.x/) to create our backend server.

Open a new terminal and run:

```bash
# cd v1 or v2
$ make create-env
# or
$ conda env create -f environment.yml
```

Activate your conda environment:

```bash
$ conda activate security
```

To run the website:

```bash
# cd v1 or v2
$ cd backend
$ python app.py
```

The backend server's URL is `http://127.0.0.1:5000`.

### Database

We are using sqlite as our database.

By default:

* `username: elec0138`
* `password: 8964`

### Debugging

* [Debugging guide](docs/dev/debugging.md)

### TODOs

* [ ] Attacks
    * [ ] Phishing (liuqiyuan)
    * [ ] Brute-force (liuqiyuan)
    * [ ] csrf
    * [ ] mitm
    * [ ] sql_injection
    * [ ] credential_stuffing
    * [ ] dos (luzhaoyan)
    * [ ] xss
* [ ] Website
    * [ ] backend
        * [ ] ticket (wangzirui)
        * [ ] cart (yangyiwen)
        * [ ] comments(optional)
    * [ ] frontend
        * [ ] ticket (wangzirui)
        * [ ] cart (yangyiwen)
        * [ ] comments(optional)
