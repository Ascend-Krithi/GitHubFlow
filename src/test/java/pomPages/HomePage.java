package pomPages;

import java.time.Duration;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class HomePage{
	WebDriver driver;
	WebDriverWait wait;
	
	@FindBy(xpath="//div[@class='js-repos-container']//a")
	WebElement createRepoBtn;
	
	public HomePage(WebDriver driver) {
		this.driver = driver;
		this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        PageFactory.initElements(driver, this);
	}
	
	public void clickCreateRepo() {
		wait.until(ExpectedConditions.elementToBeClickable(createRepoBtn));
		createRepoBtn.click();
	}
}