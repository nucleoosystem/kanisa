# flake8: noqa

from __future__ import absolute_import
from .test_banners import BannerTest
from .test_bible_passages import (
    BiblePassageBadInput,
    BiblePassage,
    ToPassageBadInput,
    ToPassageGoodInput,
    BiblePassageModelField
)
from .test_diary import (
    DiaryTest,
    DiaryGetWeekBoundsTest,
    DiaryGetScheduleTest,
    DiaryScheduledEventTest
)
from .test_kanisa_markup import KanisaMarkupTest
from .test_media import InlineImageTest
from .test_navigation import NavigationElementTest
from .test_pages import (
    PageTest,
    GetPageFromPathTest,
    PageTemplatesTest
)
from .test_sermons import SermonTest

from .views.auth import (
    PasswordResetViewTest
)
from .views.banners import (
    BannerManagementViewTest,
    BannerPublicViewTest
)
from .views.diary import (
    DiaryManagementViewTest,
    DiaryPublicViewTest
)
from .views.documents import DocumentManagementViewTest
from .views.management import ManagementViewTest
from .views.navigation import NavigationManagementViewTest
from .views.pages import (
    PageManagementViewTest,
    PagePublicViewTest
)
from .views.public import PublicViewTest
from .views.sermons import (
    SermonManagementViewTest,
    SermonPublicViewTest
)
from .views.services import ServiceMembersViewTest
from .views.social import SocialViewTest
from .views.user import UserManagementViewTest
from .views.xhr import (
    XHRBiblePassageViewTest,
    XHRCreatePageViewTest,
    XHRListPagesViewTest,
    XHRMarkSermonSeriesComplete,
    XHRScheduleRegularEventViewTest,
    XHRFetchScheduleViewTest,
    XHRListNavigationViewTest,
    XHRMoveNavigationUpViewTest,
    XHRMoveNavigationDownViewTest,
    XHRBandInformationViewTestCase,
    XHREventInformationViewTestCase,
)
