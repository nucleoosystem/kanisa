# flake8: noqa

from __future__ import absolute_import
from .banners import BannerTest
from .bible_passages import (BiblePassageBadInput,
                             BiblePassage,
                             ToPassageBadInput,
                             ToPassageGoodInput,
                             BiblePassageModelField)
from .diary import (DiaryTest,
                    DiaryGetWeekBoundsTest,
                    DiaryGetScheduleTest,
                    DiaryScheduledEventTest)
from .kanisa_markup import KanisaMarkupTest
from .media import InlineImageTest
from .navigation import NavigationElementTest
from .pages import (PageTest,
                    GetPageFromPathTest,
                    PageTemplatesTest)
from .sermons import SermonTest

from .views.banners import (BannerManagementViewTest,
                            BannerPublicViewTest)
from .views.diary import (DiaryManagementViewTest,
                          DiaryPublicViewTest)
from .views.documents import DocumentManagementViewTest
from .views.management import ManagementViewTest
from .views.navigation import NavigationManagementViewTest
from .views.pages import (PageManagementViewTest,
                          PagePublicViewTest)
from .views.public import PublicViewTest
from .views.sermons import (SermonManagementViewTest,
                            SermonPublicViewTest)
from .views.social import SocialViewTest
from .views.user import UserManagementViewTest
from .views.xhr import (XHRBiblePassageViewTest,
                        XHRUserPermissionViewTest,
                        XHRCreatePageViewTest,
                        XHRListPagesViewTest,
                        XHRMarkSermonSeriesComplete,
                        XHRScheduleRegularEventViewTest,
                        XHRFetchScheduleViewTest,
                        XHRListNavigationViewTest,
                        XHRMoveNavigationUpViewTest,
                        XHRMoveNavigationDownViewTest)
