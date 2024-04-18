# ELEC0138_GROUP_H: Security System for Online Ticket Sales Website

This is Group H's final assignment for the module ELEC0138: Security and Privacy 23/24.

In this project, a ticket sales website is created.
The website is designed to sell tickets for various events.

The website has two versions:

* The unsafe version has vulnerabilities that can be exploited by attackers,
* while the safe version is designed to be secure and protect the user's data.

The website has various features, including ticket sales, shopping cart, and user reviews.
The website is built using `Flask` for the backend and `Vue.js` for the frontend.
The website uses `SQLite` as the database.

## Group Member

* Qiyuan Liu `23075647`
* Yiwen Yang `23143115`
* Zhaoyan Lu `23049710`
* Zirui Wang `23039407`

## Contents

- [ELEC0138\_GROUP\_H](#elec0138_group_h)
  - [Group Members](#group-member)
  - [Contents](#contents)
  - [Features](#features)
    - [Attacks](#attacks)
    - [Mitigations](#mitigations)
  - [Prerequisites](#prerequisites)
  - [Environment Setup](#environment-setup)
    - [Backend](#backend)
    - [Frontend](#frontend)
    - [Database](#database)
    - [Debugging](#debugging)

## Features

### Attacks

| Attack Type                           | Description                                                                                         |
|:-------------------------------------:|:---------------------------------------------------------------------------------------------------:|
| **Phishing**                          | Examine vulnerabilities that could be exploited by phishing attacks to educate and build awareness. |
| **Brute-force**                       | Simulate brute-force attacks to test the strength of password policies and authentication methods.  |
| **CSRF (Cross-Site Request Forgery)** | Demonstrate how CSRF attacks can manipulate users into performing actions without their knowledge.  |
| **SQL Injection**                     | Assess the robustness of database systems against unauthorized data manipulation or access.         |
| **Credential Stuffing**               | Highlight the risks of reused credentials and the importance of unique password policies.           |
| **DoS (Denial of Service)**           | Showcase methods attackers use to disrupt service availability.                                     |
| **XSS (Cross-Site Scripting)**        | Explore how malicious scripts can be injected into web pages and compromise user interactions.      |

### Mitigations

| Attack Type                           | Description                                                                                         |
|:-------------------------------------:|:---------------------------------------------------------------------------------------------------:|
| **Phishing**                          | Examine vulnerabilities that could be exploited by phishing attacks to educate and build awareness. |
| **Brute-force**                       | Simulate brute-force attacks to test the strength of password policies and authentication methods.  |
| **CSRF (Cross-Site Request Forgery)** | Demonstrate how CSRF attacks can manipulate users into performing actions without their knowledge.  |
| **SQL Injection**                     | Assess the robustness of database systems against unauthorized data manipulation or access.         |
| **Credential Stuffing**               | Highlight the risks of reused credentials and the importance of unique password policies.           |
| **DoS (Denial of Service)**           | Showcase methods attackers use to disrupt service availability.                                     |
| **XSS (Cross-Site Scripting)**        | Explore how malicious scripts can be injected into web pages and compromise user interactions.      |


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
