Version 0.9.5
=============

The changes in this version should be sufficient to move all sites
using Kaleo to Kanisa (though until we've got support for automating
adding cron jobs, and started using Whitenoise for static assets, we
probably don't want to deploy this too widely).

- Add support for a simple blog
  - Public display
    - Add tests
    - Add ability to view unpublished posts for users with privs
      (including clear links to where the posts will be published)
    - Paginate the blog home page
  - Make blog posts searchable
  - Ability to post from the management interface (needs a separate
    permission)
  - RSS feeds
  - Update edit post links to go to the management interface, rather
    than the admin
  - Add support for importing posts from tinyblog, which is what
    sites running Kaleo use for blogging
- Add speaker profiles

Version 0.9.6
=============

The changes in this version are intended to make deployment easier,
and to find performance problems earlier.

- Add speedbar (https://pypi.python.org/pypi/django-speedbar)
  - Probably warrants a way of importing required settings or
    something
  - Waiting for https://github.com/theospears/django-speedbar/pull/9
    to be merged to add Django 1.6 support
- Look at using Whitenoise for serving static assets
  - http://whitenoise.evans.io/en/latest/django.html
- Add a way of searching for an individual song/composer to the Song
  Finder
- Add a way to set up cron jobs
  - For posting scheduled tweets
  - For rebuilding the search index

Version 1.0
===========

Features
--------

- Add a hint on the management home page that series with no sermons
  in `x` weeks should be marked complete
- Add handlers for links, bold and italics in `main_input_widget`
- Remove `kanisa_from_kaleo` which was created to facilitate the move
  from Kaleo to Kanisa

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

- Make the sermon archive more sensible - instead of just a giant list
  of all sermons - split it up by year/passage etc
- Add a handler for Google maps in `main_input_widget`
- Add support for multiple Bible passages in the sermon/sermon series
  models
- Allow customisable home page templates (#56)
- Add Facebook integration
  - Support for delayed posting
  - Facility for adding Like/Share buttons on individual pages
  - Showing recent posts on the home page
- Add logs of actions taken in the management console
- Add a permission for branding management
- Add a good way of finding a particular user in the user management
  interface (which doesn't involve paging through all the pages)
- Add a good way of finding a particular document in the document
  management interface (which doesn't involve paging through all the
  pages)
- Add support for merging duplicate songs/composers

Bug fixes
---------

- What happens if no series are active on the sermons home page?
- Ensure search form is visible even if no logo is set up
- Fix bug in rendering of event table when scheduling multiple events
  (#13)
- Fix weird layout of user editing page
- Fix bulk-editing events handling invalid dates (currently we don't
  save the date if it's invalid, but we don't notify the user)

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
  - Mostly for adding support for two-column pages
- Add support for rota management (#28)
- Add support for multiple podcasts (perhaps grouped by service?)
- Support for multiple schedules in a single RegularEvent (for events
  which are logically connected but have different components) (#15)
- Add weekly notice sheet feature - ability to add notices far in
  advance
