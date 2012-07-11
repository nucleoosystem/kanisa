from __future__ import absolute_import
from .bible_constants import (BOOKS_OF_THE_BIBLE,
                              SINGLE_CHAPTER_BOOKS,
                              CHAPTERS_IN_THE_BOOKS,
                              VERSES_IN_THE_CHAPTERS,
                              BOOK_PSEUDONYMS)
import re


class InvalidPassage(Exception):
    pass


class BookBoundsError(InvalidPassage):
    pass


class ChapterBoundsError(InvalidPassage):
    pass

chapter_segment = r'\s*([0-9]+)\s*'
verse_segment = r'\s*([0-9]+)\s*'
chapter_prefix = r'\s*(ch|chapter)?\s*'
verse_prefix = r'\s*(:|v|verse|verses)\s*'

chapter = re.compile(r'^%s(?P<chapter>%s)$'
                     % (chapter_prefix, chapter_segment))
chapter_range = re.compile(r'^%s(?P<begin_chapter>%s)-(?P<end_chapter>%s)$'
                           % (chapter_prefix,
                              chapter_segment,
                              chapter_segment))
chapter_verse = re.compile(r'^%s(?P<chapter>%s)%s(?P<verse>%s)$'
                           % (chapter_prefix,
                              chapter_segment,
                              verse_prefix,
                              verse_segment))
chapter_verse_range = re.compile((r'^%s(?P<chapter>%s)%s(?P<begin_verse>%s)'
                                  '-(%s)?(?P<end_verse>%s)$')
                                 % (chapter_prefix,
                                    chapter_segment,
                                    verse_prefix,
                                    verse_segment,
                                    verse_prefix,
                                    verse_segment))
full_range = re.compile((r'^%s(?P<begin_chapter>%s)%s(?P<begin_verse>%s)'
                         '-%s(?P<end_chapter>%s)%s(?P<end_verse>%s)$')
                        % (chapter_prefix,
                           chapter_segment,
                           verse_prefix,
                           verse_segment,
                           chapter_prefix,
                           chapter_segment,
                           verse_prefix,
                           verse_segment))


def _parse_remnant(inputstring):
    if len(inputstring) == 0:
        return (None, None, None, None)

    co = chapter.match(inputstring)
    if co:
        parts = co.groupdict()
        return ((int)(parts['chapter']), None, None, None)

    cro = chapter_range.match(inputstring)
    if cro:
        parts = cro.groupdict()
        return ((int)(parts['begin_chapter']),
                None,
                (int)(parts['end_chapter']),
                None)

    candv = chapter_verse.match(inputstring)
    if candv:
        parts = candv.groupdict()
        return ((int)(parts['chapter']),
                (int)(parts['verse']),
                None,
                None)

    candvr = chapter_verse_range.match(inputstring)
    if candvr:
        parts = candvr.groupdict()
        return ((int)(parts['chapter']),
                (int)(parts['begin_verse']),
                None,
                (int)(parts['end_verse']))

    fullr = full_range.match(inputstring)
    if fullr:
        parts = fullr.groupdict()
        return ((int)(parts['begin_chapter']),
                (int)(parts['begin_verse']),
                (int)(parts['end_chapter']),
                (int)(parts['end_verse']))

    raise InvalidPassage


def get_verses(book_index, chapter):
    return VERSES_IN_THE_CHAPTERS[book_index][chapter - 1]


def normalise_book(book_str):
    if book_str == 'Psalm':
        return 'Psalms'
    return book_str


def to_passage(inputstring):
    """
    Takes passages of the form:

    1 Thessalonians
    1 Thessalonians 3
    1 Thessalonians 3-4
    1 Thessalonians 3:4-8
    1 Thessalonians 3:4-4:5
    1 thessalonians 3:4 - 4:5
    and translates it to a BiblePassage object
    """

    if not isinstance(inputstring, str):
        if not isinstance(inputstring, unicode):
            raise InvalidPassage

    input = inputstring.strip().lower()

    try:
        i = [b.lower() for b in BOOKS_OF_THE_BIBLE].index(input)
        return BiblePassage(BOOKS_OF_THE_BIBLE[i])
    except ValueError:
        pass

    for b in BOOKS_OF_THE_BIBLE:
        if b.lower() + ' ' == input[0:len(b) + 1]:
            book = b
            remainder = input[len(b) + 1:]
            (sc, sv, ec, ev) = _parse_remnant(remainder)
            return BiblePassage(book, sc, sv, ec, ev)

    for (key, value) in BOOK_PSEUDONYMS.items():
        if key + ' ' == input[:len(key) + 1] or key == input:
            book = value
            remainder = input[len(key) + 1:]
            (sc, sv, ec, ev) = _parse_remnant(remainder)
            return BiblePassage(book,
                                sc,
                                sv,
                                ec,
                                ev)

    raise InvalidPassage


class BiblePassage(object):
    def __init__(self,
                 book,
                 start_chapter=None,
                 start_verse=None,
                 end_chapter=None,
                 end_verse=None):
        # Check types of input make sense
        if not isinstance(book, str):
            raise InvalidPassage('Book \'%s\' is not textual.' % book)

        book = book.strip()

        try:
            book_index = BOOKS_OF_THE_BIBLE.index(book)
        except ValueError:
            raise InvalidPassage('%s is not a known book of the Bible.' % book)

        if start_chapter and not isinstance(start_chapter, int):
            raise InvalidPassage("Start Chapter '%s' is not a whole number."
                                 % start_chapter)
        if end_chapter and not isinstance(end_chapter, int):
            raise InvalidPassage("End Chapter '%s' is not a whole number."
                                 % end_chapter)
        if start_verse and not isinstance(start_verse, int):
            raise InvalidPassage("Start Verse '%s' is not a whole number."
                                 % start_verse)
        if end_verse and not isinstance(end_verse, int):
            raise InvalidPassage("End Verse '%s' is not a whole number."
                                 % end_verse)

        if start_verse and not start_chapter:
            raise InvalidPassage("You must provide a starting chapter if "
                                 "providing a starting verse.")
        if end_chapter and not start_chapter:
            raise InvalidPassage("You must provide a starting chapter if "
                                 "providing an ending chapter.")
        if end_verse and not start_verse:
            raise InvalidPassage("You must provide a starting verse if "
                                 "providing an ending verse.")
        if start_verse and end_chapter and not end_verse:
            raise InvalidPassage("You must provide an ending verse if "
                                 "providing a starting chapter and verse.")

        self.book = book

        if end_verse and not end_chapter:
            end_chapter = start_chapter

        if start_chapter and end_chapter:
            if start_chapter > end_chapter:
                raise InvalidPassage('The passage must end after it begins!')
            if start_chapter == end_chapter:
                if end_verse and start_verse:
                    if end_verse < start_verse:
                        msg = 'The passage must end after it begins!'
                        raise InvalidPassage(msg)

        if book in SINGLE_CHAPTER_BOOKS:
            if not start_verse and not end_verse:
                if start_chapter:
                    start_verse = start_chapter
                    start_chapter = 1
                if end_chapter:
                    end_verse = end_chapter
                    end_chapter = 1

        legal_chapters = CHAPTERS_IN_THE_BOOKS[book_index]

        if start_chapter > legal_chapters or end_chapter > legal_chapters:
            if legal_chapters == 1:
                raise BookBoundsError('There is only 1 chapter in %s.'
                                      % (normalise_book(book)))
            else:
                raise BookBoundsError('There are only %i chapters in %s.'
                                      % (legal_chapters, normalise_book(book)))

        if start_chapter and start_verse:
            if start_verse > get_verses(book_index, start_chapter):
                raise ChapterBoundsError('There are only %i verses in %s %i.'
                                         % (get_verses(book_index,
                                                       start_chapter),
                                            book,
                                            start_chapter))
        if end_chapter and end_verse:
            if end_verse > get_verses(book_index, end_chapter):
                raise ChapterBoundsError('There are only %i verses in %s %i.'
                                         % (get_verses(book_index,
                                                       end_chapter),
                                            book,
                                            end_chapter))

        self.start_chapter = start_chapter
        self.start_verse = start_verse
        self.end_chapter = end_chapter
        self.end_verse = end_verse

    def __unicode__(self):
        if not self.start_chapter:
            return normalise_book(self.book)

        if self.start_chapter == 1 and self.book in SINGLE_CHAPTER_BOOKS:
            if not self.end_verse:
                return '%s %s' % (self.book, self.start_verse)

            return '%s %s-%s' % (self.book, self.start_verse, self.end_verse)

        if not self.start_verse and self.end_chapter:
            if self.start_chapter == self.end_chapter:
                return '%s %s' % (self.book,
                                  self.start_chapter)
            else:
                return '%s %s-%s' % (self.book,
                                     self.start_chapter,
                                     self.end_chapter)

        if not self.start_verse:
            return '%s %s' % (self.book, self.start_chapter)

        if not self.end_chapter:
            return '%s %s:%s' % (self.book,
                                 self.start_chapter,
                                 self.start_verse)

        if self.start_chapter == self.end_chapter:
            return '%s %s:%s-%s' % (self.book,
                                    self.start_chapter,
                                    self.start_verse,
                                    self.end_verse)

        return '%s %s:%s-%s:%s' % (self.book,
                                   self.start_chapter,
                                   self.start_verse,
                                   self.end_chapter,
                                   self.end_verse)

    def __len__(self):
        return len(unicode(self))


def normalise_passage(input):
    return unicode(to_passage(input))
