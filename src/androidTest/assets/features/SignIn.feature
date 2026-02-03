Feature: Sign In

  Scenario: Validate the user is able to sign in from sign in or sign up screen
    Given Launch DSG Application
    Then user should see user is on Dicks Sporting Goods application landing screen
    When user tap on sign in button in DSG application
    Then user should be navigated to sign in page in DSG application
    When user made a successful sign in after enter a valid username and password in DS
    And user tap on signIn button in Sign In screen in DSG application
    And user should see the location services screen in DSG application
    And user tap on next button and allow location in DSG application
    And user should see the notification services screen in DSG application
    And user tap on next button in notification screen in DSG application
    Then user should be navigated to home screen in DSG application
    And user is able to see sign in user home screen in DSG application
