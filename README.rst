=====================
GroupMe Score Tracker
=====================

.. image:: https://travis-ci.org/cheeseypi/GroupMeScoreTracker.svg?branch=master
   :alt: Travis Build Badge
   :target: https://travis-ci.org/cheeseypi/GroupMeScoreTracker

Tracks scores for GroupMe, allowing for friendly competition.

Evironment Variables:

=====================  ===============================================================  =========
Variable               Description                                                      Required?
=====================  ===============================================================  =========
``BOT_ID``             Bot ID cooresponding to group, generated on `dev.groupme.com`__  YES
``SCORETRACKER_PORT``  Port to run bot on                                               NO
=====================  ===============================================================  =========

.. _groupme: http://dev.groupme.com

__ groupme_

To start, run ``python -m scoretracker.start_server``. By default runs on port 6660.

Future:

- ``SCORETRACKER_PORT`` environment variable
- Case-insensitivity in person names/categories
- Double-space handling in commands from groupme
