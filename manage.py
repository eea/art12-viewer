#!/usr/bin/env python

import logging
from art12.app import create_app, create_manager

app, collect = create_app()


def main():
    logging.basicConfig(loglevel=logging.DEBUG)
    logging.getLogger("werkzeug").setLevel(logging.INFO)
    logging.getLogger("alembic").setLevel(logging.INFO)
    if app.config.get("DEBUG_SQL"):
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    manager = create_manager(app, collect)
    manager.run()


if __name__ == "__main__":
    main()
