from kanisa.models.bible import bible
from django.test import TestCase


class BiblePassageBadInput(TestCase):
    def testInvalidArguments(self):
        self.assertRaises(bible.InvalidPassage, bible.BiblePassage,
                          'foo')
        self.assertRaises(bible.InvalidPassage, bible.BiblePassage,
                          '1 Peter', None, 3)
        self.assertRaises(bible.InvalidPassage, bible.BiblePassage,
                          '1 Peter', 2, 3, 1, 3)
        self.assertRaises(bible.InvalidPassage, bible.BiblePassage,
                          '1 Peter', 2, 4, 2, 3)
        self.assertRaises(bible.InvalidPassage, bible.BiblePassage,
                          '1 Peters')
        self.assertRaises(bible.InvalidPassage, bible.BiblePassage, 3)
        self.assertRaises(bible.InvalidPassage, bible.BiblePassage,
                          '1 Peter', 'foo')
        self.assertRaises(bible.InvalidPassage, bible.BiblePassage,
                          '1 Peter', 3, 'bar')
        self.assertRaises(bible.InvalidPassage, bible.BiblePassage,
                          '1 Peter', 3, 4, 'bar', 5)
        self.assertRaises(bible.InvalidPassage, bible.BiblePassage,
                          '1 Peter', 3, 4, 4, 'baz')
        self.assertRaises(bible.InvalidPassage, bible.BiblePassage,
                          '1 Peter', 3, None, 4, 3)
        self.assertRaises(bible.InvalidPassage, bible.BiblePassage,
                          '1 Peter', 3, 1, 4, None)
        self.assertRaises(bible.InvalidPassage, bible.BiblePassage,
                          '1 Peter', None, 4, None, None)
        self.assertRaises(bible.InvalidPassage, bible.BiblePassage,
                          '1 Peter', None, 1, 2, None)
        self.assertRaises(bible.InvalidPassage, bible.BiblePassage,
                          '1 Peter', None, 1, None, 2)
        self.assertRaises(bible.InvalidPassage, bible.BiblePassage,
                          '1 Peter', None, 1, 2, 3)
        self.assertRaises(bible.InvalidPassage, bible.BiblePassage,
                          '1 Peter', None, None, 4, None)
        self.assertRaises(bible.InvalidPassage, bible.BiblePassage,
                          '1 Peter', None, None, None, 4)

    def testOutOfRange(self):
        self.assertRaises(bible.BookBoundsError, bible.BiblePassage,
                          'Matthew', 29)
        self.assertRaises(bible.BookBoundsError, bible.BiblePassage,
                          'Psalm', 151)
        self.assertRaises(bible.BookBoundsError, bible.to_passage,
                          'Revelation 1-23')
        self.assertRaises(bible.BookBoundsError, bible.to_passage,
                          'Revelation 23-24')
        self.assertRaises(bible.ChapterBoundsError, bible.BiblePassage,
                          'Revelation', 22, 22)
        self.assertRaises(bible.ChapterBoundsError, bible.to_passage,
                          'Revelation 22:20-22')


class BiblePassage(TestCase):
    def testToString(self):
        self.assertEqual(unicode(bible.to_passage('1 thessalonians')),
                         '1 Thessalonians')
        self.assertEqual(unicode(bible.to_passage('1 thessalonians  3')),
                         '1 Thessalonians 3')
        self.assertEqual(unicode(bible.to_passage('1 thessalonians 3 v 8')),
                         '1 Thessalonians 3:8')
        bit_too_long = unicode(bible.to_passage('1 thessalonians 3 v 8 - 4:1'))
        self.assertEqual(bit_too_long,
                         '1 Thessalonians 3:8-4:1')
        self.assertEqual(unicode(bible.to_passage('1 th 3 v 8 - 3:9')),
                         '1 Thessalonians 3:8-9')
        self.assertEqual(unicode(bible.to_passage('1 cor')),
                         '1 Corinthians')
        self.assertEqual(unicode(bible.to_passage('1 cor 2')),
                         '1 Corinthians 2')
        self.assertEqual(unicode(bible.to_passage('1 cor 2:3-7')),
                         '1 Corinthians 2:3-7')
        self.assertEqual(unicode(bible.to_passage('1 cor 2-3')),
                         '1 Corinthians 2-3')

    def testLength(self):
        self.assertEqual(len(bible.to_passage('1 cor 2 v 3 - 7')),
                         len('1 Corinthians 2:3-7'))
        self.assertEqual(len(bible.to_passage('1 cor 2-3')),
                         len('1 Corinthians 2-3'))


class ToPassageBadInput(TestCase):
    def testNonString(self):
        self.assertRaises(bible.InvalidPassage, bible.to_passage, 4000)

    def testNonBook(self):
        self.assertRaises(bible.InvalidPassage, bible.to_passage, 'foo')

    def testInvalidRange(self):
        self.assertRaises(bible.InvalidPassage, bible.to_passage,
                          '1 Thessalonians 2:1 - 1v2')
        self.assertRaises(bible.InvalidPassage, bible.to_passage,
                          '1 Thessalonians 2-1')
        self.assertRaises(bible.InvalidPassage, bible.to_passage,
                          '1 Thessalonians 2:2-2:1')

    def testGoodBookStupidRange(self):
        self.assertRaises(bible.InvalidPassage, bible.to_passage,
                          '1 Thessalonians Fish')


class ToPassageGoodInput(TestCase):
    def testBooksOnly(self):
        for b in bible.BOOKS_OF_THE_BIBLE:
            passage = bible.to_passage(b)
            self.assertEqual(passage.book, b)
            self.assertEqual(passage.book, b)
            self.assertEqual(passage.start_chapter, None)
            self.assertEqual(passage.start_verse, None)
            self.assertEqual(passage.end_chapter, None)
            self.assertEqual(passage.end_verse, None)

    def testUppercaseBooksOnly(self):
        for b in bible.BOOKS_OF_THE_BIBLE:
            passage = bible.to_passage(b.upper())
            self.assertEqual(passage.book, b)
            self.assertEqual(passage.start_chapter, None)
            self.assertEqual(passage.start_verse, None)
            self.assertEqual(passage.end_chapter, None)
            self.assertEqual(passage.end_verse, None)

    def testLowerCaseFullPassage(self):
        passage = bible.to_passage('1 thessalonians 3:1-4:5')
        self.assertEqual(passage.book, '1 Thessalonians')
        self.assertEqual(passage.start_chapter, 3)
        self.assertEqual(passage.start_verse, 1)
        self.assertEqual(passage.end_chapter, 4)
        self.assertEqual(passage.end_verse, 5)

    def testBooksWithChapter1(self):
        for b in bible.MULTI_CHAPTER_BOOKS:
            passage = bible.to_passage(b + ' 1')
            self.assertEqual(passage.book, b)
            self.assertEqual(passage.book, b)
            self.assertEqual(passage.start_chapter, 1)
            self.assertEqual(passage.start_verse, None)
            self.assertEqual(passage.end_chapter, None)
            self.assertEqual(passage.end_verse, None)

    def testBooksWithChapter1To2(self):
        for b in bible.MULTI_CHAPTER_BOOKS:
            passage = bible.to_passage(b + ' 1 - 2')
            self.assertEqual(passage.book, b)
            self.assertEqual(passage.book, b)
            self.assertEqual(passage.start_chapter, 1)
            self.assertEqual(passage.start_verse, None)
            self.assertEqual(passage.end_chapter, 2)
            self.assertEqual(passage.end_verse, None)

    def testBooksWithChapter1Verse1(self):
        for b in bible.BOOKS_OF_THE_BIBLE:
            passage = bible.to_passage(b + ' 1:2')
            self.assertEqual(passage.book, b)
            self.assertEqual(passage.start_chapter, 1)
            self.assertEqual(passage.start_verse, 2)
            self.assertEqual(passage.end_chapter, None)
            self.assertEqual(passage.end_verse, None)

            passage2 = bible.to_passage(b + ' 1 v 2')
            self.assertEqual(passage2.book, b)
            self.assertEqual(passage2.start_chapter, 1)
            self.assertEqual(passage2.start_verse, 2)
            self.assertEqual(passage2.end_chapter, None)
            self.assertEqual(passage2.end_verse, None)

    def testBooksWithChapterAndVerseRange(self):
        for b in bible.BOOKS_OF_THE_BIBLE:
            passage = bible.to_passage(b + ' 1:1-2')
            self.assertEqual(passage.book, b)
            self.assertEqual(passage.start_chapter, 1)
            self.assertEqual(passage.start_verse, 1)
            self.assertEqual(passage.end_chapter, 1)
            self.assertEqual(passage.end_verse, 2)

            passage2 = bible.to_passage(b + ' 1 v 1 - 2')
            self.assertEqual(passage2.book, b)
            self.assertEqual(passage2.start_chapter, 1)
            self.assertEqual(passage2.start_verse, 1)
            self.assertEqual(passage2.end_chapter, 1)
            self.assertEqual(passage2.end_verse, 2)

    def testBooksWithFullRange(self):
        for b in bible.MULTI_CHAPTER_BOOKS:
            passage = bible.to_passage(b + ' 1:3-2:4')
            self.assertEqual(passage.book, b)
            self.assertEqual(passage.start_chapter, 1)
            self.assertEqual(passage.start_verse, 3)
            self.assertEqual(passage.end_chapter, 2)
            self.assertEqual(passage.end_verse, 4)

            passage2 = bible.to_passage(b + ' 1 v 3 - 2 v 4')
            self.assertEqual(passage2.book, b)
            self.assertEqual(passage2.start_chapter, 1)
            self.assertEqual(passage2.start_verse, 3)
            self.assertEqual(passage2.end_chapter, 2)
            self.assertEqual(passage2.end_verse, 4)

    def testBookPseudonyms(self):
        self.assertEqual(bible.normalise_passage('Psalms 23:1-6'),
                         'Psalm 23:1-6')
        self.assertEqual(bible.normalise_passage('1 Jn 4:1-5'),
                         '1 John 4:1-5')
        self.assertEqual(bible.normalise_passage('Song of Songs 4:2'),
                         'Song of Solomon 4:2')
        self.assertEqual(bible.normalise_passage('Sos 4:2'),
                         'Song of Solomon 4:2')
        self.assertEqual(bible.normalise_passage('Eph 4:2'),
                         'Ephesians 4:2')
        self.assertEqual(bible.normalise_passage('1 Jo 3:2'),
                         '1 John 3:2')
        self.assertEqual(bible.normalise_passage('1 Jo 1:1-5:5'),
                         '1 John 1:1-5:5')

    def testAmbiguousNames(self):
        self.assertRaises(bible.InvalidPassage, bible.to_passage, 'J 3:16')
        self.assertRaises(bible.InvalidPassage, bible.to_passage, 'Ez 3:16')

    def testOverlyLongNames(self):
        self.assertRaises(bible.InvalidPassage, bible.to_passage, 'Johns 3:16')

    def testLessLikelyInputs(self):
        passage = bible.to_passage('1 John ch 2 v 3-5')
        self.assertEqual(unicode(passage), '1 John 2:3-5')

        passage = bible.to_passage('1 John chapter 2 v 3-5')
        self.assertEqual(unicode(passage), '1 John 2:3-5')

        passage = bible.to_passage('1 John chapter 2 verse 3 - v5')
        self.assertEqual(unicode(passage), '1 John 2:3-5')

        passage = bible.to_passage('1 John ch 2 v 3 - ch 4:5')
        self.assertEqual(unicode(passage), '1 John 2:3-4:5')

    def testSingleChapterBooks(self):
        passage = bible.to_passage('Jude 1:2-3')
        self.assertEqual(passage.book, 'Jude')
        self.assertEqual(passage.start_chapter, 1)
        self.assertEqual(passage.end_chapter, 1)
        self.assertEqual(passage.start_verse, 2)
        self.assertEqual(passage.end_verse, 3)
        self.assertEqual(unicode(passage), 'Jude 2-3')

        passage = bible.to_passage('Obadiah 1:2-1:3')
        self.assertEqual(passage.book, 'Obadiah')
        self.assertEqual(passage.start_chapter, 1)
        self.assertEqual(passage.end_chapter, 1)
        self.assertEqual(passage.start_verse, 2)
        self.assertEqual(passage.end_verse, 3)
        self.assertEqual(unicode(passage), 'Obadiah 2-3')

        passage = bible.to_passage('Philemon 2-3')
        self.assertEqual(passage.book, 'Philemon')
        self.assertEqual(passage.start_chapter, 1)
        self.assertEqual(passage.end_chapter, 1)
        self.assertEqual(passage.start_verse, 2)
        self.assertEqual(passage.end_verse, 3)
        self.assertEqual(unicode(passage), 'Philemon 2-3')

        passage = bible.to_passage('2 Jo 1')
        self.assertEqual(passage.book, '2 John')
        self.assertEqual(passage.start_chapter, 1)
        self.assertEqual(passage.end_chapter, None)
        self.assertEqual(passage.start_verse, 1)
        self.assertEqual(passage.end_verse, None)
        self.assertEqual(unicode(passage), '2 John 1')

        self.assertRaises(bible.ChapterBoundsError, bible.to_passage,
                          '2 John 1-14')
        self.assertRaises(bible.ChapterBoundsError, bible.to_passage,
                          '2 John 14')
        self.assertRaises(bible.ChapterBoundsError, bible.to_passage,
                          '2 John 14-15')
        self.assertRaises(bible.BookBoundsError, bible.to_passage,
                          '2 John 1:1-2:1')
        self.assertRaises(bible.BookBoundsError, bible.to_passage,
                          '2 John 2:1-2')
        self.assertRaises(bible.BookBoundsError, bible.to_passage,
                          '2 John 2:1-2:2')
