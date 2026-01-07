import pytest
from MobileApps.libs.flows.android.smart.flow_container import FlowContainer

@pytest.mark.usefixtures("class_setup_fixture_ota_regression")
class Test_Suite_01_Github:
    @pytest.fixture(scope="class", autouse=True)
    def class_setup(cls, session_setup):
        cls.driver = session_setup
        cls.fc = FlowContainer(cls.driver)
        cls.github = cls.fc.fd["github"]

    @pytest.mark.regression
    def test_01_login_success_TC01(self):
        """
        TC01 - Verify successful login to Github
        Steps:
        1. Navigate to Github login page
        2. Enter valid username
        3. Enter valid password
        4. Click on Sign in button
        """
        self.github.enter_username("<valid_username>")
        self.github.enter_password("<valid_password>")
        self.github.click_sign_in()

    @pytest.mark.regression
    def test_02_create_repository_TC02(self):
        """
        TC02 - Verify repository creation
        Steps:
        1. Login to Github
        2. Click on New repository button
        3. Enter repository name
        4. Click on Create repository button
        """
        self.github.enter_username("<valid_username>")
        self.github.enter_password("<valid_password>")
        self.github.click_sign_in()
        self.github.click_new_repo()
        self.github.enter_repo_name("<repo_name>")
        self.github.click_create_repo()

    @pytest.mark.regression
    def test_03_delete_repository_TC03(self):
        """
        TC03 - Verify repository deletion
        Steps:
        1. Login to Github
        2. Navigate to the repository settings
        3. Scroll to Danger Zone and click Delete this repository
        4. Confirm repository name and click I understand the consequences, delete this repository
        """
        self.github.enter_username("<valid_username>")
        self.github.enter_password("<valid_password>")
        self.github.click_sign_in()
        self.github.click_settings_tab()
        self.github.click_delete_repo()
        self.github.enter_confirm_repo_name("<repo_name>")
        self.github.click_confirm_delete()

    @pytest.mark.regression
    def test_04_logout_TC04(self):
        """
        TC04 - Verify logout functionality
        Steps:
        1. Login to Github
        2. Click on profile avatar
        3. Click on Sign out
        """
        self.github.enter_username("<valid_username>")
        self.github.enter_password("<valid_password>")
        self.github.click_sign_in()
        self.github.click_profile_avatar()
        self.github.click_sign_out()
