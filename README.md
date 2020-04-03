# Playing Card Platform

## Overview

This is the backend to support a platform that allows users to set up any game using a standard deck of playing cards (in future custom cards as well) as well as other tabletop game paraphenalia such as chips, dice and counters

## Dependencies

- [Git](https://git-scm.com/)
- [Python 3.6+](https://www.python.org/)
- [Poetry](https://python-poetry.org/)

## Quickstart

- Clone this repo
    ```bash
    git clone https://github.com/marlanperumal/playing-card-platform.git
    ```
- Enter the cloned folder
    ```bash
    cd playing-card-platform
    ```
- Setup up poetry virtual environment and install libraries
    ```bash
    poetry install
    ```
- Create a copy of the `.env` file from the template. This will load necessary environment variables
  ```bash
  cp template.env .env
  ``` 
- Modify the `.env` file with appropriate values for connection to a database of your choice
  - Choices for `DB_TYPE` are `postgresql` and `mysql`
  - If `DB_TYPE` is left blank then playing-card-platform will use an ephemeral in-memory sqlite database
- Create the database you're going to be using if necessary
- Run the migrations to create all required database entities
    ```bash
    poetry run flask db migrate
    ```
- Start the server (doesn't do anything yet)
    ```bash
    poetry run flask run
    ```

## Development
- Run tests (pytest)
    ```bash
    poetry run pytest -v tests
    ```
- Run linter (flake8)
    ```bash
    poetry run flake8 .
    ```
- Run autoformatter (black)
    ```bash
    poetry run black .
    ```
