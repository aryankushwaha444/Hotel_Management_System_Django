
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class web {
	public static void main ( String[] args) {
		
		//use chrome driver from selenium
		WebDriver driver = new ChromeDriver();
		
		try {
			
		//Navigate to desired website
			driver.get("http://127.0.0.1:8000/hotel/register/");
			
			//get and print the page title
			String pageTitle= driver.getTitle();
			System.out.println("Page Title:" + pageTitle);
			
			
			//pass values to required feilds
			driver.findElement(By.name("username")).sendKeys("lll1");
			driver.findElement(By.name("email")).sendKeys("lll@test.com");
			driver.findElement(By.name("first_name")).sendKeys("lll");
			driver.findElement(By.name("last_name")).sendKeys("fbej");
			driver.findElement(By.name("phone_number")).sendKeys("8763826373");

			driver.findElement(By.name("password1")).sendKeys("Llllll1@");
			driver.findElement(By.name("password1")).sendKeys("Llllll1@");

			driver.findElement(By.name("register")).click();
			
			//wait for few sec for demonstration purpose
			Thread.sleep(5000);
			
		}
		catch(InterruptedException e) {
			e.printStackTrace();
		}
		finally {
			driver.quit();
		}
	}
	
}



// login_test

// public class web {
// 	public static void main ( String[] args) {
		
// 		//use chrome driver from selenium
// 		WebDriver driver = new ChromeDriver();
		
// 		try {
			
// 		//Navigate to desired website
// 			driver.get("http://127.0.0.1:8000/accounts/login/");
			
// 			//get and print the page title
// 			String pageTitle= driver.getTitle();
// 			System.out.println("Page Title:" + pageTitle);
			
			
// 			//pass values to required feilds
// 			driver.findElement(By.name("username")).sendKeys("qqq1");
// 			driver.findElement(By.name("password")).sendKeys("Qqqqqq1@");
// 			driver.findElement(By.name("login")).click();
			
// 			//wait for few sec for demonstration purpose
// 			Thread.sleep(8000);
			
// 		}
// 		catch(InterruptedException e) {
// 			e.printStackTrace();
// 		}
// 		finally {
// 			driver.quit();
// 		}
// 	}
	
// }