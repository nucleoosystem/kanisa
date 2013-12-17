Version 1.0
===========

- Remove "Save & Continue" on "Update account" form
- Add support for users with user management permissions to create
  accounts based on a first name, last name and email address, and
  have relevant instructions emailed (e.g. how to log in, what
  permissions the user has, and how to use them)
- Figure out what should go on the management home page (#41)
- Figure out what should go on the members' home page
- Change external requirements to better equivalents
  - Switch to Pillow (might need newer version of sorl-thumbnail,
    which is back in active development - see
    https://github.com/mariocesar/sorl-thumbnail/).
  - Switch from django-compressor to django-pipeline, and ensure we're
    serving compressed assets (also, should we be including unminified
    assets in the distributed wheel?)
- Add South migrations
- Replace banners with fixed call-out content, perhaps defaulting to
  diary if no content is available (call-outs can still be
  time-limited)
- Ensure *some* links show in the nav on smaller screens - perhaps
  just home and account bar?

Version 1.1
===========

- Figure out how to have "Save & Continue" for model creation forms
  (this probably involves being more consistent about model editing
  URLs, and having better tests).
- Improve pagination of document attachment widget
- Allow customisable home page templates (#56)
- Version check requirements in setup.py
  - tweepy (upgrade to 2.1)
    - Check Twitter integration still works
    - Write tests against mock Twitter
  - Whoosh (upgrade to 2.5.5)
  - django-haystack to 2.x
- Make inline images responsive (don't send full versions to mobiles)
  (#47)
- Check layout on mobile
- Improve test coverage (#33)
- Improve usability of management views on mobile
- Find references to media, and ensure media can't be deleted if there
  are existing references to them (#54)
- Add a navigation checker (#44)
- Detect references to dates in text (#37)
- Allow pages to use multiple templates (#20)
- Fix bug in rendering of event table when scheduling multiple events
  (#13)
- Python 3 support
- Support for multiple schedules in a single RegularEvent (for events
  which are logically connected but have different components) (#15)
- Consider adding Twilio integration
- Add support for rota management (#28)
- Add Facebook integration
  - Support for delayed posting
  - Facility for adding Like/Share buttons on individual pages
  - Showing recent posts?
- Add support for multiple podcasts (perhaps grouped by service?)
- Improve deployment process (can we deploy without the site 500ing
  whilst the virtualenv is in flux? perhaps enter maintenance mode?)
- Add logs of actions taken in the management console
