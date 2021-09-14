import os
import platform
from typing import List
from drongo_types import Section
from contextlib import closing
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def create_dir_if_not_exists(driver: webdriver.Chrome, directory_name_to_create: str):
    try:
        driver.find_element_by_link_text(directory_name_to_create)
    except NoSuchElementException:
        create_folder_link = driver.find_element_by_id("MainPlaceHolder_FileBrowserControl_SelectCreateFolderButton")
        create_folder_link.click()

        folder_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "MainPlaceHolder_FileBrowserControl_NewFolder")))
        folder_name_input.send_keys(directory_name_to_create)

        create_button = driver.find_element_by_id("MainPlaceHolder_FileBrowserControl_CreateFolderButton")
        create_button.click()


def login(driver: webdriver.Chrome, username: str, password: str):
    driver.get("https://new.drongo.org.uk/Users/Login.aspx")
    username_input = driver.find_element_by_id("MainPlaceHolder_UsernameText")
    username_input.send_keys(username)
    password_input = driver.find_element_by_id("MainPlaceHolder_PasswordText")
    password_input.send_keys(password)

    login_button = driver.find_element_by_id("MainPlaceHolder_LogInButton")
    login_button.click()


def upload_photos(driver: webdriver.Chrome, year: int, processed_photo_dir: str, photo_upload_dir_name: str):
    year_str = str(year)
    photo_filenames = sorted(os.listdir(processed_photo_dir))

    driver.get("https://new.drongo.org.uk/Admin/ManageFiles.aspx")

    web_images_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'MainPlaceHolder_SelectFolderList_3')))
    web_images_button.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'MainPlaceHolder_FileBrowserControl_SelectCreateFolderButton')))

    create_dir_if_not_exists(driver, year_str)
    dir_2021 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, year_str)))
    dir_2021.click()

    create_dir_if_not_exists(driver, photo_upload_dir_name)
    dir_test_folder = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, photo_upload_dir_name)))
    dir_test_folder.click()

    for photo_filename in photo_filenames:
        file_chooser = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'MainPlaceHolder_FileBrowserControl_UploadFile')))
        file_chooser.send_keys(os.path.join(processed_photo_dir, photo_filename))

        overwrite_if_exists_checkbox = driver.find_element_by_id("MainPlaceHolder_FileBrowserControl_OverwriteCheck")
        if not overwrite_if_exists_checkbox.is_selected():
            overwrite_if_exists_checkbox.click()

        upload_button = driver.find_element_by_id("MainPlaceHolder_FileBrowserControl_UploadFileButton")
        upload_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, photo_filename)))


def upload_report(driver: webdriver.Chrome, report_title: str, report_content: List[Section]):
    driver.get("https://new.drongo.org.uk/Admin/EditNews.aspx")

    elements = driver.find_elements_by_xpath(f"//*[contains(text(), '{report_title}')]")

    if len(elements) == 0:
        add_news_item_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "MainPlaceHolder_AddButton")))
        add_news_item_button.click()
    else:
        parent_element = elements[0].find_element_by_xpath('..')
        edit_button = parent_element.find_element_by_link_text("Edit")
        edit_button.click()

    title_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "MainPlaceHolder_TitleText")))
    title_input.clear()
    title_input.send_keys(report_title)

    i = 0
    while True:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "MainPlaceHolder_SectionsView_DeleteSectionButton_0")))
        try:
            delete_section_button = driver.find_element_by_id("MainPlaceHolder_SectionsView_DeleteSectionButton_1")
            delete_section_button.click()
            obj = driver.switch_to.alert
            obj.accept()
        except Exception:
            # When delete section 1 button no longer found, stop deleting sections
            break
        i += 1

    for i, section in enumerate(report_content):
        print(f"Section {i}")
        if i > 0:
            add_section_button = driver.find_element_by_id("MainPlaceHolder_AddSectionButton")
            add_section_button.click()

        section_title_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, f"MainPlaceHolder_SectionsView_SubtitleText_{i}")))
        if section.title is not None:
            section_title_input.clear()
            section_title_input.send_keys(section.title)
        else:
            section_title_input.clear()

        content_input = driver.find_element_by_id(f"MainPlaceHolder_SectionsView_ContentText_{i}")
        content_input.clear()
        content_input.send_keys(section.content)

    save_button = driver.find_element_by_id("MainPlaceHolder_SaveButton")
    save_button.click()


def upload_to_website(year: int, processed_photo_dir: str, photo_upload_dir_name: str,
                      username: str, password: str, report_title: str, report_content: List[Section]):
    chromedriver_name = "chromedriver.exe" if platform.system() == "Windows" else "chromedriver"
    with closing(webdriver.Chrome(chromedriver_name)) as driver:
        login(driver, username, password)

        upload_photos(driver, year, processed_photo_dir, photo_upload_dir_name)
        time.sleep(5)

        upload_report(driver, report_title, report_content)
        time.sleep(5)
