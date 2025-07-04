# language: en
Feature: My Observatory App Automation Tests
  As a user
  I want to use the My Observatory app to check weather information
  So that I can know the current and future weather conditions

  Background:
    Given I have opened the My Observatory app
    And I am on the main page

  Scenario Outline: Check 9-Day Forecast

  Scenario: View 9-Day Forecast weather information
    Given I have opened the My Observatory app
    When I click the "9-Day Forecast" tab
    Then I should see the 9-day forecast section displayed
    And I should see weather information for 9 days
    And each day should display temperature range
    And each day should display humidity range
