from pathlib import Path

framework_dir = Path("data/framework")
steps_dir = framework_dir / "src" / "test" / "java" / "com" / "company" / "automation" / "steps"

print("🔧 Creating files with matching names...")

# Create loginsteps.java (lowercase to match **/*steps*.java)
login_content = '''package com.company.automation.steps;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;

public class loginsteps {
    
    @Given("I am on the login page")
    public void i_am_on_the_login_page() {
        System.out.println("Navigating to login page");
    }
    
    @Given("I am on the authentication screen")
    public void i_am_on_the_authentication_screen() {
        System.out.println("Opening authentication screen");
    }
    
    @When("I enter valid credentials")
    public void i_enter_valid_credentials() {
        System.out.println("Entering valid credentials");
    }
    
    @When("I click the login button")
    public void i_click_the_login_button() {
        System.out.println("Clicking login button");
    }
    
    @Then("I should be logged in successfully")
    public void i_should_be_logged_in_successfully() {
        System.out.println("Verifying successful login");
    }
    
    @Then("I should be redirected to the dashboard")
    public void i_should_be_redirected_to_the_dashboard() {
        System.out.println("Verifying dashboard redirect");
    }
}'''

# Create searchsteps.java
search_content = '''package com.company.automation.steps;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;

public class searchsteps {
    
    @Given("I am on the home page")
    public void i_am_on_the_home_page() {
        System.out.println("Navigating to home page");
    }
    
    @When("I search for {string}")
    public void i_search_for(String searchTerm) {
        System.out.println("Searching for: " + searchTerm);
    }
    
    @When("I click the search button")
    public void i_click_the_search_button() {
        System.out.println("Clicking search button");
    }
    
    @Then("I should see search results")
    public void i_should_see_search_results() {
        System.out.println("Verifying search results");
    }
    
    @Then("the results should contain {string}")
    public void the_results_should_contain(String expectedText) {
        System.out.println("Verifying results contain: " + expectedText);
    }
}'''

# Write files with lowercase names
with open(steps_dir / "loginsteps.java", 'w') as f:
    f.write(login_content)

with open(steps_dir / "searchsteps.java", 'w') as f:
    f.write(search_content)

print("✅ Created loginsteps.java")
print("✅ Created searchsteps.java")

# Test pattern matching
print("\n🔍 Testing pattern matching:")
for pattern in ["**/*steps*.java", "**/*step*.java"]:
    files = list(framework_dir.glob(pattern))
    print(f"   {pattern}: {len(files)} files")
    for f in files:
        print(f"      - {f}")