Version 1.0
===========

Features
--------

- Add a handler for Google maps in `main_input_widget`
- Add handlers for links, bold and italics in `main_input_widget`

Deployment
----------

- Add a way to set up cron jobs
- Ensure media, whoosh_index are chowned appropriately with every
  deploy

Other
-----

Unknown - I'll fill this out based on feedback from pilot users.

Version 1.1
===========

Deployment
----------

- Remove all inline styles
- Split up kanisa.css somehow
- Version check requirements in setup.py
  - Pillow (upgrade to 2.3.0 - might need newer version of
    sorl-thumbnail, which is back in active development - see
    https://github.com/mariocesar/sorl-thumbnail/)
  - tweepy (upgrade to 2.1)
    - Check Twitter integration still works
    - Write tests against mock Twitter
  - Whoosh (upgrade to 2.5.5)
  - django-haystack to 2.x
- Ensure branding changes create images with cache-busting URLs
  (i.e. include a hash of the file contents in the name)
- Add `unicode_literals`, `print_function`, `absolute_import` and
  `division` imports from `__future__` to all files (plus a way of
  checking they're everywhere)
- Fix proliferation of `kanisa.*.css` and `kanisa.*.js` (since the
  filenames are modified with each CSS/JS change, and old files don't
  get cleaned up)

Mobile
------

- Fix navbar breakpoint - currently at certain screen sizes the navbar
  flows over two rows
- Replace banners with fixed call-out content, perhaps defaulting to
  diary if no content is available (call-outs can still be
  time-limited)
- Make inline images responsive (don't send full versions to mobiles)
  (#47)
- Check layout on mobile
- Improve usability of management views on mobile

Features
--------

- Add support for a simple blog.
- Allow customisable home page templates (#56)
- Add Facebook integration
  - Support for delayed posting
  - Facility for adding Like/Share buttons on individual pages
  - Showing recent posts?
- Add logs of actions taken in the management console
- Add a way to permanently remove inactive users (e.g. spam
  registrations)

Bug fixes
---------

- What happens if no series are active on the sermons home page?
- Ensure search form is visible even if no logo is set up
- Fix bug in rendering of event table when scheduling multiple events
  (#13)
- Fix weird layout of user editing page

Version 1.2
===========

Deployment
----------

- Python 3 support
- Figure out how to run jslint as part of the minification process
- Improve deployment process (can we deploy without the site 500ing
  whilst the virtualenv is in flux? perhaps enter maintenance mode?)
- Improve test coverage (#33)

Features
--------

- Add facility for more full-fledged service planning (i.e. not just
  songs), with updated plans emailed to service leaders (perhaps as
  printable PDFs)
- Members' directory?
  - Add a setting for allowing email addresses to be shared with other
    members (off by default)
- Find references to media, and ensure media can't be deleted if there
  are existing references to them (#54)
- Add a navigation checker (#44)
- Detect references to dates in text (#37)
- Allow pages to use multiple templates (#20)
- Add support for rota management (#28)
- Add support for multiple podcasts (perhaps grouped by service?)
- Support for multiple schedules in a single RegularEvent (for events
  which are logically connected but have different components) (#15)
- Add weekly notice sheet feature - ability to add notices far in
  advance
- Remove `kanisa_from_kaleo` and `kanisa_guess_schedule`, both of
  which were created to facilitate the move from Kaleo to Kanisa
