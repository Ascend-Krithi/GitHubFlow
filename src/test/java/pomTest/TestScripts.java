package pomTest;

import org.testng.annotations.AfterClass;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

import org.testng.Assert;
import org.testng.AssertJUnit;
import java.time.Duration;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.testng.annotations.Test;

import pomPages.*;
public class TestScripts{
	WebDriver driver;
	@BeforeClass
	public void setup() {
		driver = new ChromeDriver();
		 
        driver.manage().window().maximize();
		driver.get("https://www.github.com");
		System.out.println("Navigating to url");
		
	}
	
	@Test(priority=1)
	public void loginPositive() throws Exception {
		Login login = new Login(driver);
		login.clickLoginLink();
		
		login.verifyEmailVisibility();
		login.verifyEmailClickability();
		login.enterEmail("gkiruthika1505@gmail.com");
		
		login.verifyPasswordVisibility();
		login.verifyPasswordClickability();
		login.enterPassword("Ascendion@123");
		
		login.clickSignInButton();
		Thread.sleep(3000);
		System.out.println("Account signed in");
		String actualTitle = login.homePageTitleCheck();
		Assert.assertTrue(actualTitle.contains("GitHub"), "Homepage title does not match!");
		
		HomePage home = new HomePage(driver);
		home.clickCreateRepo();
	}
	@Test(priority=2)
	public void RepoCreation() throws Exception {
		CreateRepoPage create = new CreateRepoPage(driver);
		create.enterRepoName("Ascendion");
		create.createRepoBtnClick();
		System.out.println("Repository created");
	}
	
	@Test(priority=3)
	public void DeleteRepo() throws Exception {
		DeleteRepoPage delete = new DeleteRepoPage(driver);
		delete.clickSettings();
		delete.clickDelete();
		delete.clickProceedDelete();
		delete.clickRead();
		Thread.sleep(2000);
		delete.typeRepoName();
		System.out.println("Repository deleted");
		
	}
	
	@Test(priority=4)
	public void SignOut() {
		SignOut signout = new SignOut(driver);
		signout.clickProfile();
		signout.clickSignOut();
		System.out.println("Account signed out");
	}
	
	@AfterClass
	public void tearDown() {
		if (driver != null) {
            driver.quit();
            System.out.println("Browser closed.");
        }
	}
}