# language: en
Feature: My Observatory App Automation Tests
  As a user
  I want to use the My Observatory app to check weather information
  So that I can know the current and future weather conditions

  Background:
    Given I have opened the My Observatory app
    And I am on the main page

  Scenario Outline: Check weather information for different cities
    When I search for the city "<city_name>"
    And I select the city "<city_name>"
    Then I should see the current temperature information
    And I should see the weather description
    And I should see the humidity information
    And I should see the wind speed information

    Examples:
      | city_name |
      | Beijing   |
      | Shanghai  |
      | Guangzhou |

  Scenario: Get current location weather using the location feature
    When I click the location button
    Then I should see the current temperature information
    And I should see the weather description
    And I should see the humidity information
    And I should see the wind speed information

  Scenario: View detailed weather information
    Given I use the city "beijing" from the test data
    When I search for the city "Beijing"
    And I select the city "Beijing"
    Then I should see the current temperature information
    And I should see the weather description
    And I should see the humidity information
    And I should see the wind speed information
    And the temperature should be within a reasonable range
    And the humidity should be within a reasonable range

  Scenario: Access application settings
    When I click the menu button
    And I click the settings button
    Then the settings page should be displayed

  Scenario: Change temperature unit setting
    Given I click the menu button
    And I click the settings button
    When I toggle the temperature unit
    Then the settings page should be displayed

  Scenario: Change notification settings
    Given I click the menu button
    And I click the settings button
    When I toggle the notification settings
    Then the settings page should be displayed

  Scenario: Search functionality test
    When I click the search button
    Then the search page should be displayed
    When I search for the city "Beijing"
    And I select the city "Beijing"
    Then the city "Beijing" should be selected
    And I should see the current temperature information 