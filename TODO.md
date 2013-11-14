Version 0.8
===========

- Version check requirements in setup.py
  - Upgrade django-password-reset to 0.5.1 (which now supports
    custom users)
  - tweepy (upgrade to 2.1)
  - Whoosh (upgrade to 2.5.5)
- Add support for user photos, ensuring they can be set by users with
  user management permissions (#25)

Version 0.9
===========

- Add support for ScheduledEvent series
- Support importing from Kaleo (#62)
  - Import scheduled events
  - Import users
  - Import groups
  - Import permissions
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
  - Switch to Pillow
  - Switch from django-compressor to django-pipeline, and ensure we're
    serving compressed assets (also, should we be including unminified
    assets in the distributed wheel?)
- Add South migrations
- Check Twitter integration still works
- Figure out what should go on the management home page (#41)
- Allow customisable home page templates (#56)
- Fix O(n)ness of user-management views (#26)

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
- Upgrade django-haystack to 2.x
