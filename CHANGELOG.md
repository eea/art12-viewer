Changelog
=========

2.1.dev0 - (unreleased)
-----------------------

2.0 - (2017-05-08)
------------------
* Dockerise Article 12 consultation tool
  - discarded waitress and supervisor and used gunicorn
  - loaded settings from environment
  - major changes to Docker file: added docker-entrypoint script for
    running the app
  - added docker compose files version 2 for production and devel
    environments
  - added CHANGELOG.md file for tracking changes and keeping versions
  [chiridra refs #81736]

1.0 - (2013-01-01)
------------------
* Initial release
