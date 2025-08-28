package pomPages;

import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;

public class SignOut{
	WebDriver driver;
	WebDriverWait wait;
	
	@FindBy(xpath="//div[@class='AppHeader-user']//button")
	WebElement profileIcon;
	
	@FindBy(xpath="//div[@class='prc-Dialog-Body-LCvER']//li[24]//a")
	WebElement signOutBtn;
	
	public SignOut(WebDriver driver) {
		this.driver = driver;
		this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        PageFactory.initElements(driver, this);
	}
	
	public void clickProfile() {
		wait.until(ExpectedConditions.elementToBeClickable(profileIcon));
		profileIcon.click();
		
	}
	
	public void clickSignOut() {
		wait.until(ExpectedConditions.elementToBeClickable(signOutBtn));
		signOutBtn.click();
	}
	public String checkPageTitle() {
		return driver.getTitle();
	}
}