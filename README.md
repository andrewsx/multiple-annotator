# AnnoMultiply

## Description 
The goal of this project is to make the process for data annotation with entities more efficient, transparent, and centralized for a team of collaborators.  

## Motivation
We wanted to provide a way to streamline the process of annotation by allowing multiple clients to connect to one machine. This increases transparency as other collaborators can examine the annotations and discuss or resolve any misunderstandings regarding certain entity definitions. This project will also eliminate costs for the school by obviating the need to pay for a subscription. 


## Features
* Centralize all annotations on one machine
* Multiple annotators can connect simultaneously 
* Create and delete datasets
* See the annotations inside any dataset
* List current information about datasets such as author, time of creation, description, number of annotations
* Resume annotating with any existing dataset


## Technologies
* Python 3
* Flask/Jinja
* Prodigy
* Gunicorn

## Setup
Make sure to modify the config.py to include the name of the users, a Flask key, and open ports for allocation to a user

For example: 
```python
users = [
    'thomas',
    'jeffrey',
    'elaina',
]

coder_list = [{"name": "thomas", "port": 2111},
            {"name": "jeffrey", "port": 1415},
            {"name": "elaina", "port": 7217}]
```

After configuration, fire up the terminal with this command!
```
gunicorn --bind <ip>:<port> --workers 4 main:app
```
