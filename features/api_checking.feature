# language: en
Feature: Hong Kong Observatory API Testing
  As a test engineer
  I want to test the Hong Kong Observatory weather API
  So that I can verify the API response and extract weather data

  Scenario: Check API response and extract relative humidity for the day after tomorrow
    When I get API of 9-day forcast from Hong Kong Observatory
    Then I send request to the API
    And I check response status is successful
    And I extract the relative humidity for the day after tommorrow
    And I display API response summary