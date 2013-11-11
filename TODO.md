Version 0.9
===========

- Add support for ScheduledEvent series
- Create default image for event contacts
- Create default image for sermon series
- Support importing from Kaleo
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
- Add support for podcasts
- Add support for user photos
- Think through who can see Service Planning links (just those in a
  band?)

Version 1.0
===========

- Make inline images responsive (don't send full versions to mobiles)
- Add support for rota management
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

Version 1.1
===========

- Improve test coverage
- Improve usability of management views on mobile
- Allow customisable home page templates
- Find references to media, and ensure media can't be deleted if there
  are existing references to them
- Add a navigation checker
- Detect references to dates in text
- Fix O(n)ness of user-management views
- Allow pages to use multiple templates
- Fix bug in rendering of event table when scheduling multiple events
- Python 3 support
