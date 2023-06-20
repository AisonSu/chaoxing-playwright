import re
from typing import List, NewType, TypedDict
from playwright.sync_api import Page, Locator, FrameLocator
from utils import attachBrowser


class TaskInfo(TypedDict):
    type: str
    frame: FrameLocator
    task_locator: Locator


Tasks = NewType("Tasks", List[TaskInfo])


def getTasks(page: Page) -> Tasks:
    tasks: Tasks = Tasks([])
    frameLocator = page.locator("#iframe")
    frameUrl = frameLocator.get_attribute("src")
    frame = page.frame(url=frameUrl)
    taskLocators = frame.locator(
        "div.ans-attach-ct", has=frame.locator(".ans-job-icon")
    ).all()
    for task_locator in taskLocators:
        if re.search("ans-job-finished", task_locator.get_attribute("class")):
            continue
        taskframe_locator = task_locator.locator("iframe")
        taskframeUrl = taskframe_locator.get_attribute("src")
        taskframeClassName = taskframe_locator.get_attribute("class")
        # 目前采用classname识别，可以采用url识别
        module = re.search(r".*+modules/(w+)/.*", taskframeUrl)
        task_framelocator = task_locator.frame_locator("iframe")
        if taskframeClassName is not None:
            # video
            result = re.search(r"ans-insertvideo-online", taskframeClassName)
            if result is not None:
                tasks.append(
                    {
                        "type": "video",
                        "frame": task_framelocator,
                        "task_locator": task_locator,
                    }
                )
            # pdf
            result = re.search(r"insertdoc-online", taskframeClassName)
            if result is not None:
                tasks.append(
                    {
                        "type": "pdf",
                        "frame": task_framelocator,
                        "frameLocator": taskframe_locator,
                    }
                )
        else:
            # click
            jobidText = taskframe_locator.get_attribute("jobid")
            if jobidText is not None:
                result = re.search("read", jobidText)
                if result is not None:
                    tasks.append(
                        {
                            "type": "click",
                            "frame": task_framelocator,
                            "frameLocator": taskframe_locator,
                        }
                    )
    return tasks


if __name__ == "__main__":
    page = attachBrowser()
    getTasks(page)
