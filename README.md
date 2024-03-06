# ELEC0138_GROUP_H

## Prerequisites

* [Node.js 20.11.1](https://nodejs.org/en)
* [Anaconda](https://www.anaconda.com/) / [Miniconda](https://docs.anaconda.com/free/miniconda/index.html) for python 3.8

## Environment Setup

### Frontend

We are using [Vue.js](https://vuejs.org/guide/quick-start) to create our frontend website.

Open a new terminal and run:

```bash
$ cd frontend
$ npm install
$ npm run dev
```

And then you can visit our ticket selling website through `http://localhost:5173`.

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
$ cd backend
$ python app.py
```

Then go to 
The backend server's URL is `http://127.0.0.1:5000/login`.

### Database

We are using sqlite as our database.

By default:

* `username: elec0138`
* `password: 8964`
