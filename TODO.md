Version 1.0
===========

- Figure out what should go on the management home page (#41)
- Improve navbar
  - Ensure *some* links show in the nav on smaller screens - perhaps
    just home and account bar?
  - Ensure the root links (e.g. About Us), can be navigated to - at
    the moment they just expand the nav submenu
- Upgrade to latest Bootstrap
  - Fix thumbnail displays in the management interface
    - Sermon speakers
    - Inline images
    - Banners
  - Check for usage of img-polaroid
- Remove all inline styles
- Improve scheduled event sidebar (it shows *all* regular events, with
  contact information below - it should probably just show related
  events, like the regular event pages do, though this won't work for
  one-offs)
- Improve flow of editing scheduled instances of regular events - at
  present it may prompt you for an event title, if one is not set. It
  should just fill that in automatically

Version 1.1
===========

- Replace banners with fixed call-out content, perhaps defaulting to
  diary if no content is available (call-outs can still be
  time-limited)
- Figure out how to run jslint as part of the minification process
- Members' directory?
  - Add a setting for allowing email addresses to be shared with other
    members (off by default)
- Figure out how to have "Save & Continue" for model creation forms
  (this probably involves being more consistent about model editing
  URLs, and having better tests).
- Improve pagination of document attachment widget
- Allow customisable home page templates (#56)
- Version check requirements in setup.py
  - Pillow (upgrade to 2.3.0 - might need newer version of
    sorl-thumbnail, which is back in active development - see
    https://github.com/mariocesar/sorl-thumbnail/)
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
