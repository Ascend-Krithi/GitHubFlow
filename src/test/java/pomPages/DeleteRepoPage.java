package pomPages;

import java.time.Duration;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class DeleteRepoPage{
	WebDriver driver;
	WebDriverWait wait;
	
	@FindBy(xpath="//div[@class='AppHeader-localBar']//li[9]//a")
	WebElement settingsLink;
	
	@FindBy(xpath="//button[@id='dialog-show-repo-delete-menu-dialog']")
	WebElement deleteBtn;
	
	@FindBy(xpath="//button[@id='repo-delete-proceed-button']")
	WebElement deleteProceedBtn;
	
	@FindBy(xpath="//div[@id='repo-delete-proceed-button-container']//label")
	WebElement labelElement;
	
	@FindBy(xpath="//div[@id='repo-delete-proceed-button-container']//input")
	WebElement inputField;
	
	
	public DeleteRepoPage(WebDriver driver) {
		this.driver = driver;
		this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        PageFactory.initElements(driver, this);
	}
	
	
	public void clickSettings() {
		wait.until(ExpectedConditions.elementToBeClickable(settingsLink));
		settingsLink.click();
	}
	public void clickDelete() {
		wait.until(ExpectedConditions.elementToBeClickable(deleteBtn));
		deleteBtn.click();
	}
	public void clickProceedDelete() {
		wait.until(ExpectedConditions.elementToBeClickable(deleteProceedBtn));
		deleteProceedBtn.click();
	}
	
	public void clickRead() {
		wait.until(ExpectedConditions.elementToBeClickable(deleteProceedBtn));
		deleteProceedBtn.click();
	}
	
	public void typeRepoName() {
		String labelText = labelElement.getText();
		
		String repoName = labelText.split("\"")[1];
		
		inputField.sendKeys(repoName);
		
		wait.until(ExpectedConditions.elementToBeClickable(deleteProceedBtn));
		deleteProceedBtn.click();
	}
	
}

