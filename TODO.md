Version 1.0
===========

- Figure out what should go on the management home page (#41)
- Upgrade to latest Bootstrap
  - Fix thumbnail displays in the management interface
    - Banners (once the banners page has been ported we can probably
      remove the thumbnail-caption styles in kanisa.css)
- Improve scheduled event sidebar (it shows *all* regular events, with
  contact information below - it should probably just show related
  events, like the regular event pages do, though this won't work for
  one-offs)

Version 1.1
===========

- Fix navbar breakpoint - currently at certain screen sizes the navbar
  flows over two rows
- Add facility for more full-fledged service planning (i.e. not just
  songs), with updated plans emailed to service leaders (perhaps as
  printable PDFs)
- Ensure search form is visible even if no logo is set up
- Remove all inline styles
- Split up kanisa.css somehow
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
