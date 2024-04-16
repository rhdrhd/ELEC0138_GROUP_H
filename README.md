# ELEC0138_GROUP_H

In this project, a ticket sales website is created. The website is designed to sell tickets for various events. The website has two versions: a safe version and an unsafe version. The safe version is designed to be secure and protect the user's data, while the unsafe version is designed to have vulnerabilities that can be exploited by attackers. The website has various features, including ticket sales, shopping cart, and user reviews. The website is built using Flask for the backend and Vue.js for the frontend. The website uses SQLite as the database.

## Contents

- [ELEC0138\_GROUP\_H](#elec0138_group_h)
  - [Contents](#contents)
  - [Prerequisites](#prerequisites)
  - [Environment Setup](#environment-setup)
    - [Backend](#backend)
    - [Frontend](#frontend)
    - [Database](#database)
    - [Debugging](#debugging)
    - [TODOs](#todos)
  - [Features](#features)
    - [Attacks](#attacks)
    - [Defense](#defense)

## Prerequisites

* [Node.js 20.11.1](https://nodejs.org/en)
* [Anaconda](https://www.anaconda.com/) / [Miniconda](https://docs.anaconda.com/free/miniconda/index.html) for python 3.8

## Environment Setup

We offer two versions of our ticket sales website.

One is the unsafe mode which may have some security risks and vulnerabilities,
and the other is a safe mode that incorporates numerous mechanisms to safeguard the system.

You can change the website's mode using different options.

### Backend

We are using [Flask](https://flask.palletsprojects.com/en/3.0.x/) to create our backend server.

Open a new terminal and run:

```bash
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
$ cd v1/backend
# Safe mode (default)
$ python app.py
# Unsafe mode
$ MODE=unsafe python app.py
```

The backend server's URL is `http://127.0.0.1:5000`.

### Frontend

We are using [Vue.js](https://vuejs.org/guide/quick-start) to create our frontend website.

Open a new terminal and run:

```bash
$ cd v1/frontend

# Install all dependencies needed
$ npm install

# Choose your website mode
# Safe mode (default)
$ cat v1/frontend/.env.development
...
VITE_APP_MODE=safe
# Unsafe mode
$ cat v1/frontend/.env.development
...
VITE_APP_MODE=unsafe

# Launch your website
$ npm run dev
```

And then you can visit our ticket selling website through `http://localhost:5173`.

### Database

We are using sqlite as our database.

By default::

* `username: elec0138`
* `password: 8964`

### Debugging

* [Debugging guide](docs/dev/debugging.md)

### TODOs

* [x] Attacks
    * [x] Phishing (liuqiyuan)
    * [x] Brute-force (liuqiyuan)
    * [x] CSRF (liuqiyuan)
    * [x] sql_injection (yangyiwen)
    * [ ] credential_stuffing
    * [x] dos (luzhaoyan)
    * [x] xss (luzhaoyan)
* [x] Defense
    * [x] reCAPTCHA (wangzirui)
    * [x] Two-factor (liuqiyuan)
    * [x] DoS (luzhaoyan)
    * [x] JWT (luzhaoyan)
    * [x] xss (luzhaoyan)
* [x] Website
    * [x] backend
        * [x] unsafe and safe modes (luzhaoyan)
        * [X] ticket (wangzirui)
        * [X] cart (wangzirui)
        * [x] reviews (luzhaoyan)
    * [x] frontend
        * [X] ticket (wangzirui)
        * [X] cart (wangzirui)
        * [x] reviews (luzhaoyan)

## Features

### Attacks

| Attack Type               | Description                                                                                       |
|---------------------------|---------------------------------------------------------------------------------------------------|
| **Phishing**              | Examine vulnerabilities that could be exploited by phishing attacks to educate and build awareness. |
| **Brute-force**           | Simulate brute-force attacks to test the strength of password policies and authentication methods. |
| **CSRF (Cross-Site Request Forgery)** | Demonstrate how CSRF attacks can manipulate users into performing actions without their knowledge.  |
| **SQL Injection**         | Assess the robustness of database systems against unauthorized data manipulation or access.       |
| **Credential Stuffing**   | Highlight the risks of reused credentials and the importance of unique password policies.         |
| **DoS (Denial of Service)** | Showcase methods attackers use to disrupt service availability.                                  |
| **XSS (Cross-Site Scripting)** | Explore how malicious scripts can be injected into web pages and compromise user interactions.   |

### Defense

| Defense Type              | Description                                                                                       |
|---------------------------|---------------------------------------------------------------------------------------------------|
| **reCAPTCHA**             | Enhances security by ensuring interactions are human-driven, preventing automated software attacks. |
| **Two-factor Authentication** | Strengthens login security by requiring two forms of user verification, dramatically reducing the risk of unauthorized access. |
| **DoS Defense**           | Implements advanced measures to protect against service disruptions caused by Denial of Service attacks. |
| **JWT (JSON Web Tokens)** | Ensures secure user session management through robust token-based authentication.                  |
| **XSS Protection**        | Provides safeguards against Cross-Site Scripting to maintain the integrity and security of user data. |
| **Parameterized Queries**             | Protects against SQL injection attacks by separating SQL code from data inputs, ensuring that user inputs cannot alter the structure of SQL queries. |

