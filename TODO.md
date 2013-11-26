Version 0.9
===========

- Add support for bands (at the moment service plans have a band
  leader, but no bands)
- When creating (but not when editing) service plans, allow selecting
  a band to auto-populate band leader/musicians
- Add support for deleting service plans (ensure song choices are
  cleaned up etc)
- Add support for ScheduledEvent series
- Rest of support for importing from Kaleo (#62)
  - Import scheduled events
  - Import bands
  - Import service plans
  - Import attachments (and ensure the Markdown parser finds them)
  - Import legacy paths (not just LegacyPathMapping, but common Kaleo
    paths that will have moved, such as podcasts)
- Add support for podcasts (#4), and track podcast downloads
- Think through who can see Service Planning links (just those in a
  band?)

Version 1.0
===========

- Add "Save and Continue Editing" option to all model forms
- Change external requirements to better equivalents
  - Switch to Pillow (might need newer version of sorl-thumbnail,
    which is back in active development - see
    https://github.com/mariocesar/sorl-thumbnail/).
  - Switch from django-compressor to django-pipeline, and ensure we're
    serving compressed assets (also, should we be including unminified
    assets in the distributed wheel?)
- Version check requirements in setup.py
  - tweepy (upgrade to 2.1)
    - Check Twitter integration still works
    - Write tests against mock Twitter
  - Whoosh (upgrade to 2.5.5)
  - django-haystack to 2.x
- Add South migrations
- Add support for users with user management permissions to create
  accounts based on a first name, last name and email address, and
  have relevant instructions emailed (e.g. how to log in, what
  permissions the user has, and how to use them)
- Figure out what should go on the management home page (#41)
- Allow customisable home page templates (#56)
- Stop distributing tests (otherwise we need to make all the tests
  settings-independent, which is more work)

Version 1.1
===========

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
