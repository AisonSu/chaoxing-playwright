import re
from playwright.sync_api import Page
from getTasks import TaskInfo


def finishTask(page: Page, task: TaskInfo):
    frame = task["frame"]
    task_locator = task["task_locator"]
    match task["type"]:
        case "video":
            btn = frame.locator("body")
            btn.click()
            finish = False
            while True:
                # 激活显示进度条
                btn.hover()
                control = frame.get_by_label("进度小节")
                control.wait_for(state="visible")
                # 等待进度条浮现
                page.wait_for_timeout(470)
                # 点击进度末端
                moveMouseProperty = control.bounding_box()
                # 计算末端位置
                if moveMouseProperty is not None:
                    x = moveMouseProperty["x"] + (
                        moveMouseProperty["width"] - (moveMouseProperty["width"] / 700)
                    )
                    y = moveMouseProperty["y"] + moveMouseProperty["height"] / 2
                    # 点击末端
                    page.mouse.move(x, y)
                    page.mouse.down()
                    page.mouse.up()
                    # 11秒等待，超时重新判断
                    for x in range(12):
                        className = task_locator.get_attribute("class")
                        result = re.search("ans-job-finished", className)
                        if result is not None:
                            finish = True
                            break
                        else:
                            page.wait_for_timeout(1000)
                            continue
                    if finish == True:
                        break
                    else:
                        continue

        case "pdf":
            # 鼠标移动至PDF中心
            pdf_container = frame.locator("#docContainer")
            moveMouseProperty = pdf_container.bounding_box()
            if moveMouseProperty is not None:
                x = moveMouseProperty["x"] + moveMouseProperty["width"] / 2
                y = moveMouseProperty["y"] + moveMouseProperty["height"] / 2
                page.mouse.move(x, y)
                # 获取滚动长度
                element = pdf_container.frame_locator("iframe").locator("div.fileBox")
                length = element.evaluate("(element) => element.scrollHeight")
                page.mouse.wheel(0, length)
                # 等待任务点完成
                page.wait_for_timeout(3000)
        case "click":
            with page.expect_popup() as newpage_info:
                frame.frame_locator("#frame_content").get_by_text(
                    "去阅读", exact=True
                ).click()
                newpage_info.value.close()
