Changelog
=========

2.6.4 (2021-02-26)
-----------------
* Change warning for Romania
  [dianaboiangiu]

2.6.3 (2020-10-26)
-----------------
* Disable download factsheets for period 2013
  [dianaboiangiu]

2.6.2 (2020-10-20)
-----------------
* Insert audit trails for 2013 period
* Add methodolgy and guideline/add note for period 2013
  [dianaboiangiu]

2.6.1 (2020-09-29)
-----------------
* Fix progress page links to summary
  [dianaboiangiu]

2.6.0(2020-09-03)
-----------------
* Prepared for period 2013-2018
  [dianaboiangiu]

2.5.5(2019-06-09)
----------------------
* Fixed security issues
* Fixed tests
* Added newer docker-compose installation
  [dianaboiangiu]

2.5.4(2019-06-09)
----------------------
* Fix tests
* Use Eionet password reset link
  [dianaboiangiu]

2.5.3(2019-06-26)
----------------------
* Add missing template
  [dianaboiangiu]

2.5.2(2019-06-26)
----------------------
* Remove Eionet header and footer
* Handle LDAP authentication in application
  [dianaboiangiu]

2.5.1(2019-09-13)
----------------------
* Center align application
  [dianaboiangiu]

2.5.0(2019-09-12)
----------------------
* Add collect static
* Switch application to new plone header and footer
  [dianaboiangiu]

2.4.8(2018-09-17)
----------------------
* Disable factsheets download for non-native species which have a native version
  [dianaboiangiu]

2.4.7(2018-09-14)
----------------------
* Download factsheets from external source
  [dianaboiangiu]

2.4.6 (2018-09-12)
----------------------
* Simulate collect static in docker entrypoint
  [dianaboiangiu]

2.4.5 (2018-09-05)
----------------------
* Remove period 2012bis from progress page
  [dianaboiangiu]

2.4.4 (2018-08-28)
----------------------
* Set new wordings
  [dianaboiangiu]

2.4.3 (2018-08-06)
----------------------
* Fix ajax links
 [dianaboiangiu]
 
2.4.2 (2018-07-30)
----------------------
* Use new mysqlclient package
 [dianaboiangiu]
 
2.4.1 (2018-07-26)
----------------------
* Refactor import greece script for production environment
 [dianaboiangiu]

2.4.0 (2018-05-29)
----------------------
* Refactor import greece script
 [dianaboiangiu]

2.3.5 (2018-03-13)
----------------------
* Add filter on reports page
 [dianaboiangiu]

2.3.4 (2018-03-12)
----------------------
* Keep subject options selected on period change
 [dianaboiangiu]

2.3.3 (2018-03-12)
----------------------
* Improve period filter
 [dianaboiangiu]

2.3.2 (2018-03-12)
----------------------
* Rename database
 [nico4]

2.3.1 (2018-03-12)
----------------------
* Docker follow redirect on linux package download
 [nico4]

2.3 (2018-02-23)
-----------------------
* Prepare Greece import
 [dianaboiangiu]

2.2 (2017-06-08)
-----------------------
* Rename database
 [nico4]

2.1 (2017-05-11)
-----------------------
* Missing factsheets in dockerized article 17 si article 12
  - installed wkhtmltopdf
  - used mysql 5.6 - DO NOT upgrade to 5.7 since MySQL 5.7.5+ changed the way
    GROUP BY behaved in order to be SQL99 compliant
    (where in previous versions it was not).
  - created volumes for maps and factsheets
  [chiridra refs #84975]

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
