# WebCowl

Web-based user interfaces for monitoring and commanding balloon payloads. These
are roughly based on two programs created for BLAST, Spider, and SuperBIT:

 * cow: (Command Operations Window). Select and send commands.
 * owl: (Overview Window L?). Information-dense status dashboard.

## Under development

These tools are in early development, not yet ready for mission critical
applications.

## Components

The project currently consists of three parts:

 * client: the client application written in TypeScript and using React. Most
 of the code lives here.
 * api: the API backend server, written in Python and using Flask.
 * data_faker.py: small test script to generate fake data during development

## Setup

To re-create the Python and TypeScript environments, for use as a development
server, follow the steps here. The file `setup.txt` documents the original
creation of these environments, but should not be followed.

### API server environment

```
cd api
python -m venv venv
venv/bin/pip install -r requirements.txt
```

However, the pygetdata dependency does not play nice with pip. Need to install
that manually. TBD: more info.

### client environment

```
cd client
npm install
```

Running things
==============

```
python ./fake_data.py
cd client
npm run dev
npm run api
```
