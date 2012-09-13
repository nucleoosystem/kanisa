# Banners

* Fix issue where image doesn't load for some time (might be limited
  to the dev server).
* Ordering/prioritisation?

# Diary

* Add something like event categories (for children; for teenagers;
  for adults etc).
* Fix bug in management interface when scheduling subsequent events
  whilst another event schedule request is in progress - the spinner
  disappears as it's not part of the rendering process (possible
  solution is to block redrawing until the last request is done, or
  just re-render the single event, which is tricky).
* Add support for event contacts (probably an online contact form,
  rather than an e-mail address).
* Add support for event reminders directly from the public site
  (provided you're logged in).
* Allow multiple schedules for regular events, with different names
  (e.g. Football/Football Training).
* Check support for multi-day events.
* Add links for non-regular events from the Church diary table.

# Sermons

* Add transcript facility.
* Add support for podcasts.
* Allow multiple podcasts (select which sermons go where at the sermon
  series layer - allow series to go to multiple podcasts).
* Add support for future sermons - which won't have audio or
  transcripts, but will give an idea of where series are going.
* Add a sermon archive feature, which shows a short list of all past
  sermon series, and also has a list of all past sermons, most recent
  first.

# Pages

* Drag-and-drop page moving.
* Allow logged-in users to see unpublished pages.
* Allow pages to use multiple templates?

# Social Media

* Allow delayed posting to Twitter (and Facebook?).
* Incorporate Twitter feed/Facebook feed into site?
* Follow us on Twitter/Like us on Facebook buttons?
* Allow posting to Facebook.
* Disallow editing tweets which have been posted
* Add a management command for posting tweets which were scheduled in
  the past hour

# User Management

* Allow users to upload photos?
* Allow quick membership approval process.
* Fix O(n)-ness of user management views (queries for each user to get
  their permissions).
* Add views for password changing.
* Add views for registration.

# Members' Area

* Service Planning (including notification centre).
* Rotas

# Search

* Paginate search results
* Boost future events in search results over past events
* Make sure objects are removed from search indexes on deletion
* Add a public search facility.

# Tests

* Add tests for the sermon management views (there's currently auth
  tests only).
* Add tests for document management views (there's currently auth
  tests only).
* Add tests for the social management views (there's currently auth
  tests only).
* Check coverage of diary/banner CRUD views.
* Add tests for search views.
* Make sure search results for test runs are kept separately.
* Don't inherit from TestCase for tests which don't use the database
* Unit test views directly, rather than via URLs.

# Misc

* Documentation (developer friendly/end user friendly)
* Make it possible to attach documents to events (e.g. agendas,
  minutes).
* Allow redirecting arbitrary URLs as a fallback - to help map old
  URLs.
* Stop making EpicEditor look like it support rich text (try making
  text bold, or pasting in rich text).
* Make sure each page has a descriptive title (i.e. the <title> tag
  contains something other than just the name of the Church).
* Detect references to dates in text, and flag for cleanup around that
  date on the home page of the Kanisa management interface.

# Frontend

* Actually implement the frontend of the site
* Add favicons, and other assorted Apple bits (see Bootstrap templates
  for examples).
