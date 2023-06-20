import re
from finishTask import finishTask
from getLessons import getLessons
from getSubjects import getSubjects
from getTasks import getTasks
from utils import attachBrowser

if __name__ == "__main__":
    page = attachBrowser()
    # 登录
    page.goto("http://i.chaoxing.com/")
    if page.title() == "用户登录":
        page.get_by_placeholder("手机号/超星号").fill("17620692447")
        page.get_by_placeholder("学习通密码").fill("hQkqtdegtubXd9HE")
        page.get_by_role("button", name="登录").click()

    # 读取科目
    page.wait_for_timeout(3000)  # 等待科目加载
    subjects = getSubjects(page)
    for index, info in subjects.items():
        # 进度识别
        if info["progress"] == " 100.0% ":
            # 有些课程，表面上任务点满了，但进度没满，点进去还有任务点，因此根据进度判断
            continue

        # 获取课程
        (lessonDict, lessonPage) = getLessons(page, info["btn"])
        for title, btn in lessonDict.items():
            btn().click()
            page.wait_for_timeout(1000)
            backBtn = lessonPage.locator("a.subBack")
            sectionLocators = lessonPage.locator("ul.prev_ul li").all()
            # 判断单页面与多页面
            # 单页面
            if len(sectionLocators) == 1:
                tasks = getTasks(lessonPage)
                for task in tasks:
                    finishTask(lessonPage, task)
            # 多页面
            else:
                for sectionLocator in sectionLocators:
                    # 页面切换
                    sectionLocator.click()
                    page.wait_for_timeout(1500)
                    # 单页面任务完成
                    tasks = getTasks(lessonPage)  # 获取当前页面任务点
                    for task in tasks:
                        finishTask(lessonPage, task)
            backBtn.click()  # 返回课程列表
        lessonPage.close()
