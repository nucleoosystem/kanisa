# Banners

* Fix issue where image doesn't load for some time (might be limited
  to the dev server).
* Ordering/prioritisation?

# Diary

* Allow multiple schedules for regular events, with different names
  (e.g. Football/Football Training).
* Make it possible to create a RegularEvent from a ScheduledEvent (for
  when you've created an event once, and then realise it'll happen
  regularly).
* Allow creating RegularEvents on timetables other than day x of week.

# Sermons

* Allow multiple podcasts (select which sermons go where at the sermon
  series layer - allow series to go to multiple podcasts).

# Pages

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
* Allow admin staff to quickly give permissions (not too granular -
  based on content types rather than individual create/edit/delete for
  each).
* Allow quick membership approval process.

# Members' Area

* Service Planning
* Rotas

# Search

* Paginate search results
* Limit number of words in details bit
* Boost future events in search results over past events
* Make sure objects are removed from search indexes on deletion

# Tests

* Add tests for the sermon views (there's currently no coverage here at all)
* Add tests for document management views (there's currently auth tests only)
* Add tests for the social management views (there's currently no coverage
  here at all)
* Add tests for XHR views (there's currently no coverage here at all)
* Check coverage of diary/banner CRUD views.

# Misc

* Documentation (developer friendly/end user friendly)
* Make it possible to attach documents to events (e.g. agendas,
  minutes).
* Allow redirecting arbitrary URLs as a fallback - to help map old
  URLs.
* Cache queries for the management sidebar

# Frontend

* Actually implement the frontend of the site
