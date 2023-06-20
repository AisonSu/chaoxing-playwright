from typing import Annotated, Callable, Dict, NewType, Tuple
from playwright.sync_api import Page, Locator
from getSubjects import SubjectBtn, SubjectDict

LessonBtnCal = Annotated[Callable[[], Locator], "LessonBtnCal"]
LessonDict = NewType("LessonDict", Dict[str, LessonBtnCal])


def getLessons(page: Page, subjectBtn: SubjectBtn) -> Tuple[LessonDict, Page]:
    lessonDict: LessonDict = LessonDict({})
    with page.expect_popup() as newpage_info:
        subjectBtn.click()
    newpage = newpage_info.value
    # 切换新版
    newpage.get_by_text("体验新版").click()
    newpage.get_by_text("章节").click()
    newpage.wait_for_timeout(2500)
    newframe = newpage.frame(name="frame_content-zj")
    if newframe is not None:
        # 没有has条件将导致识别到一些作为大标题而不是课程标题的页面元素
        lessonLocators = newframe.locator(
            "div.catalog_title",
            has_not=newframe.locator("div.icon_yiwanc"),
            has=newframe.locator("span.catalog_points_yi"),
        ).all()

        # 进入任务页面再切换回课程全览将导致定位元素失效，所以需要将按钮延时计算
        def getLessonBtn(title: str):
            def realtimeBtn():
                page.wait_for_timeout(1500)
                currentframe = newpage.frame(name="frame_content-zj")
                lessonLocator = currentframe.locator(
                    "li div.catalog_name", has_text=title
                )
                return lessonLocator

            return realtimeBtn

        for lessonLocator in lessonLocators:
            titleLocator = lessonLocator.locator("div.catalog_name")
            titleText = titleLocator.inner_text()
            lessonDict[titleText] = getLessonBtn(titleText)

    return (lessonDict, newpage)
