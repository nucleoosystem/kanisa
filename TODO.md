Version 0.9
===========

- Add support for ScheduledEvent series
- Create default image for sermon series
- Add support for user photos, ensuring they can be set by users with
  user management permissions (#25)
- Support importing from Kaleo (#62)
  - Import scheduled events
  - Import users
  - Import groups
  - Import permissions
  - Import bands
  - Import service plans
  - Import attachments (and ensure the Markdown parser finds them)
  - Import sermons and sermon series
  - Import legacy paths (not just LegacyPathMapping, but common Kaleo
    paths that will have moved, such as podcasts)
- Add support for podcasts (#4)
- Think through who can see Service Planning links (just those in a
  band?)
- Remove {% load url from future %}, since it's not needed by Django
  1.5 or higher

Version 1.0
===========

- Make inline images responsive (don't send full versions to mobiles)
  (#47)
- Add support for rota management (#28)
- Check layout on mobile
- Check Twitter integration still works
- Add Facebook integration
  - Support for delayed posting
  - Facility for adding Like/Share buttons on individual pages
  - Showing recent posts?
- Consider adding Twilio integration
- Switch to Pillow
- Version check requirements in setup.py
- See if any dependencies can be removed (e.g. django-compressor,
  django-password-reset?)
- Figure out what should go on the management home page (#41)

Version 1.1
===========

- Improve test coverage (#33)
- Improve usability of management views on mobile
- Allow customisable home page templates (#56)
- Find references to media, and ensure media can't be deleted if there
  are existing references to them (#54)
- Add a navigation checker (#44)
- Detect references to dates in text (#37)
- Fix O(n)ness of user-management views (#26)
- Allow pages to use multiple templates (#20)
- Fix bug in rendering of event table when scheduling multiple events
  (#13)
- Python 3 support
- Support for multiple schedules in a single RegularEvent (for events
  which are logically connected but have different componentes) (#15)
