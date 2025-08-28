package pomPages;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;

public class CreateRepoPage{
	WebDriver driver;
	WebDriverWait wait;
	
	@FindBy(xpath="//input[@id='repository-name-input']")
	WebElement repoName;
	
	@FindBy(xpath="//button[@class='prc-Button-ButtonBase-c50BI mt-4']")
	WebElement createRepoBtn;
	
	public CreateRepoPage(WebDriver driver) {
		this.driver=driver;
		this.wait=new WebDriverWait(driver, Duration.ofSeconds(10));
		PageFactory.initElements(driver, this);
	}
	
	public void enterRepoName(String name) {
		wait.until(ExpectedConditions.visibilityOf(repoName));
		repoName.sendKeys(name);
	}
	
	public void createRepoBtnClick() throws Exception {
		((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView(true);", createRepoBtn);
		Thread.sleep(2000);
		wait.until(ExpectedConditions.elementToBeClickable(createRepoBtn));
		createRepoBtn.click();
	}
}