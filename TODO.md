Version 0.8
===========

- Modify user edit form to allow managing permissions
- Modify user edit form to allow creating superusers (sets `is_staff` and
  `is_superuser`, only available to superusers)
- Ensure first name, last name and email are required fields at all
  points during the registration and account management process
- Add support for user photos, ensuring they can be set by users with
  user management permissions (#25)
- Ensure users with user management permissions are emailed on new
  user registration
- Fix O(n)ness of user-management views (#26) - can be fixed by just
  removing the checkboxes once permissions can be managed from the
  user edit form
- A bit more support for importing from Kaleo (#62)
  - Import users
  - Import groups
  - Import permissions

Version 0.9
===========

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
  which are logically connected but have different componentes) (#15)
- Consider adding Twilio integration
- Add support for rota management (#28)
- Add Facebook integration
  - Support for delayed posting
  - Facility for adding Like/Share buttons on individual pages
  - Showing recent posts?
