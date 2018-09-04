Version 1.0
===========

* Change emails sent for account approval to have everyone in "to"
  list, and include name of approver/spammer
* Start storing records of all emails sent by the website, for
  tracking purposes;
* Get rid of banners/site wide notices (consolidate into a single
  site wide notice thing which we'll use for previewing major
  things - the sorts of things we create timed banners for right
  now);
* Redesign the sermon area layout;
* Redesign the home page;
* Start sending out monthly (thoughts on frequency of these welcome)
  emails to event owners to confirm pages are adequately up to date;
* Ground up mobile redesign;
* Get a new look for the seasonal (Christmas/Easter) page.

Version 1.1
===========

Service Management
------------------

- Change alphabetic sort to ignore case (and potentially ignore
  spaces) - possible in Django 1.8 using
  `django.db.models.functions.Lower`;
- Add support for merging duplicate songs;
- Add support for merging duplicate composers;
- Add a way to edit composers;
- Add a way of searching for an individual song/composer to the Song
  Finder.

Sermon Archives
---------------

- Make the sermon archive more sensible - instead of just a giant
  list of all sermons - split it up by year/passage etc;
- Remove the concept of sermon series being "complete";
- What happens if no series are active on the sermons home page?

Miscellaneous
-------------

- Rename management JS to members JS.

Version 1.2
===========

Deployment
----------

- Remove all inline styles
- Split up kanisa.css somehow
- Add `unicode_literals`, `print_function`, `absolute_import` and
  `division` imports from `__future__` to all files (plus a way of
  checking they're everywhere)

Mobile
------

- Fix navbar breakpoint - currently at certain screen sizes the navbar
  flows over two rows
- Replace banners with fixed call-out content, perhaps defaulting to
  diary if no content is available (call-outs can still be
  time-limited)
- Make inline images responsive (don't send full versions to mobiles)
  (#47) - see https://github.com/scottjehl/picturefill

Features
--------

- Add handlers for links, bold and italics in `main_input_widget`
- Add a handler for Google maps in `main_input_widget`
- Add support for multiple Bible passages in the sermon/sermon series
  models
- Add logs of actions taken in the management console

Bug fixes
---------

- Fix bug in rendering of event table when scheduling multiple events
  (#13)
- Fix weird layout of user editing page
- Fix bulk-editing events handling invalid dates (currently we don't
  save the date if it's invalid, but we don't notify the user)

Version 1.1
===========

Deployment
----------

- Python 3 support
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
  - Mostly for adding support for two-column pages
- Add support for rota management (#28)
- Support for multiple schedules in a single RegularEvent (for events
  which are logically connected but have different components) (#15)
