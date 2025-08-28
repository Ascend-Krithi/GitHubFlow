package pomPages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;


public class Login{
	WebDriver driver;
	WebDriverWait wait;
	
	@FindBy(xpath="//div[@class='position-relative HeaderMenu-link-wrap d-lg-inline-block']//a")
	WebElement signInLink;
	@FindBy(xpath="//input[@id='login_field']")
	WebElement emailField;
	@FindBy(xpath="//input[@id='password']")
	WebElement passwordField;
	@FindBy(xpath="//input[@value='Sign in']")
	WebElement signInButton;
	
	public Login(WebDriver driver) {
		this.driver = driver;
		this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        PageFactory.initElements(driver, this);
	}
	
	public void clickLoginLink() {
		signInLink.click();
	}
	//email validation
    public boolean verifyEmailVisibility() {
    	wait.until(ExpectedConditions.visibilityOf(emailField));
    	return emailField.isDisplayed();
    }
    public boolean verifyEmailClickability() {
    	wait.until(ExpectedConditions.elementToBeClickable(emailField));
    	return emailField.isEnabled();
    }
    
    public void enterEmail(String email) {
    	emailField.sendKeys(email);
    }
    
    public boolean verifyPasswordVisibility() {
    	wait.until(ExpectedConditions.visibilityOf(passwordField));
    	return emailField.isDisplayed();
    }
    public boolean verifyPasswordClickability() {
    	wait.until(ExpectedConditions.elementToBeClickable(passwordField));
    	return emailField.isEnabled();
    }
    
    public void enterPassword(String password) {
    	passwordField.sendKeys(password);
    }
    
    public void clickSignInButton() {
    	wait.until(ExpectedConditions.elementToBeClickable(signInButton));
    	signInButton.click();
    }
    
    public String homePageTitleCheck() {
    	System.out.println( driver.getTitle());
        return driver.getTitle();
    }
}