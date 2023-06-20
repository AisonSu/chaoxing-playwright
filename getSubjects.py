from typing import Dict, NewType, TypedDict
from playwright.sync_api import Page, Locator

SubjectBtn = NewType("SubjectBtn", Locator)


class SubjectInfo(TypedDict):
    progress: str
    btn: SubjectBtn


SubjectDict = NewType("SubjectDict", Dict[str, SubjectInfo])


def getSubjects(page: Page) -> SubjectDict:
    frame = page.frame_locator("#frame_content")
    subjectLocators = frame.locator("dl", has_text="进入学习").all()
    subjectDict: SubjectDict = SubjectDict({})
    for subjectLocator in subjectLocators:
        title = subjectLocator.locator("h3 a").inner_text()
        progress = subjectLocator.locator("div.percent").inner_text()
        btn = subjectLocator.get_by_text("进入学习")
        subjectDict[title] = {"progress": progress, "btn": SubjectBtn(btn)}
    return subjectDict
