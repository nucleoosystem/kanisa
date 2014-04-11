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

from .views.test_auth import (
    PasswordResetViewTest
)
from .views.test_banners import (
    BannerManagementViewTest,
    BannerPublicViewTest
)
from .views.test_diary import (
    DiaryManagementViewTest,
    DiaryPublicViewTest
)
from .views.test_documents import DocumentManagementViewTest
from .views.test_management import ManagementViewTest
from .views.test_navigation import NavigationManagementViewTest
from .views.test_pages import (
    PageManagementViewTest,
    PagePublicViewTest
)
from .views.test_public import PublicViewTest
from .views.test_sermons import (
    SermonManagementViewTest,
    SermonPublicViewTest
)
from .views.test_services import ServiceMembersViewTest
from .views.test_social import SocialViewTest
from .views.test_user import UserManagementViewTest
from .views.test_xhr import (
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
