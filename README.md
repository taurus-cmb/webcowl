# WebCowl

Web-based user interfaces for monitoring and commanding balloon payloads. These
are roughly based on two programs created for BLAST, Spider, and SuperBIT:

 * cow: (Command Operations Window). Select and send commands.
 * owl: (Overview Window L?). Information-dense status dashboard.

## Under development

These tools are in early development.

## Setup

To re-create the Python environment, for use as a development
server, follow the steps here. The file `setup.txt` documents the original
creation of these environments, but should not be followed.

```
python -m venv venv
venv/bin/pip install -r requirements.txt
```

However, the pygetdata dependency does not play nice with pip. Need to install
that manually. TBD: more info.

Running things
==============

```
source venv/bin/activate
QUART_APP=webcowl:app quart run
```
