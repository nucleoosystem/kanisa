# Banners

* Fix issue where image doesn't load for some time (might be limited
  to the dev server).
* Ordering/prioritisation?

# Diary

* Allow multiple schedules for regular events, with different names
  (e.g. Football/Football Training).
* Allow creating RegularEvents on timetables other than day x of week.

# Sermons

* Allow multiple podcasts (select which sermons go where at the sermon
  series layer - allow series to go to multiple podcasts).

# Pages

* Drag-and-drop page moving
* Quick page hierarchy creation tool

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

# Members' Area

* Service Planning (including notification centre).
* Rotas

# Search

* Paginate search results
* Boost future events in search results over past events
* Make sure objects are removed from search indexes on deletion

# Tests

* Add tests for the sermon management views (there's currently auth
  tests only)
* Add tests for document management views (there's currently auth
  tests only)
* Add tests for the social management views (there's currently auth
  tests only)
* Check coverage of diary/banner CRUD views.
* Add tests for search views
* Add tests for page management views (there's currently tests for
  page deletion, and that the page creation view basically returns a
  success status)

# Misc

* Documentation (developer friendly/end user friendly)
* Make it possible to attach documents to events (e.g. agendas,
  minutes).
* Allow redirecting arbitrary URLs as a fallback - to help map old
  URLs.

# Frontend

* Actually implement the frontend of the site
* Add favicons, and other assorted Apple bits (see Bootstrap templates
  for examples).
