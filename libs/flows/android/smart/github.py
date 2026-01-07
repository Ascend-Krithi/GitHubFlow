from MobileApps.libs.flows.android.smart.flow_container import FlowContainer

class GithubFlow(object):
    def __init__(self, driver):
        self.driver = driver

    def enter_username(self, username):
        """
        Enter username in login field
        """
        self.driver.wait_for_object("login_username_field")
        self.driver.send_keys("login_username_field", username)

    def enter_password(self, password):
        """
        Enter password in login field
        """
        self.driver.wait_for_object("login_password_field")
        self.driver.send_keys("login_password_field", password)

    def click_sign_in(self):
        """
        Click Sign In button
        """
        self.driver.wait_for_object("login_sign_in_button")
        self.driver.click("login_sign_in_button")

    def click_profile_avatar(self):
        """
        Click profile avatar on home page
        """
        self.driver.wait_for_object("home_profile_avatar")
        self.driver.click("home_profile_avatar")

    def click_sign_out(self):
        """
        Click Sign Out button from profile dropdown
        """
        self.driver.wait_for_object("home_sign_out_button")
        self.driver.click("home_sign_out_button")

    def click_new_repo(self):
        """
        Click New Repository button
        """
        self.driver.wait_for_object("repo_new_repo_button")
        self.driver.click("repo_new_repo_button")

    def enter_repo_name(self, repo_name):
        """
        Enter repository name
        """
        self.driver.wait_for_object("repo_name_field")
        self.driver.send_keys("repo_name_field", repo_name)

    def click_create_repo(self):
        """
        Click Create Repository button
        """
        self.driver.wait_for_object("repo_create_repo_button")
        self.driver.click("repo_create_repo_button")

    def click_settings_tab(self):
        """
        Click Settings tab in repository
        """
        self.driver.wait_for_object("settings_tab")
        self.driver.click("settings_tab")

    def click_delete_repo(self):
        """
        Click Delete this repository button in Danger Zone
        """
        self.driver.wait_for_object("settings_delete_repo_button")
        self.driver.click("settings_delete_repo_button")

    def enter_confirm_repo_name(self, repo_name):
        """
        Enter repository name for delete confirmation
        """
        self.driver.wait_for_object("settings_confirm_repo_name_field")
        self.driver.send_keys("settings_confirm_repo_name_field", repo_name)

    def click_confirm_delete(self):
        """
        Click confirm delete button
        """
        self.driver.wait_for_object("settings_confirm_delete_button")
        self.driver.click("settings_confirm_delete_button")
