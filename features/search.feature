Feature: Browse and Filter Features and Scenarios

  Scenario Outline: Search Features and Scenarios
    Given I am on the features and scenarios page
    When I enter "<feature_filter>" in the feature search box
    And I enter "<scenario_filter>" in the scenario search box
    Then I should see only features and scenarios matching the filters
    Examples:
      | feature_filter | scenario_filter  |
      | ""             | ""               | 
      | Login          | ""               | 
      | ""             | Login Successful |  
      | Login          | Login Successful |

  Scenario: Browse Features and Scenarios
    Given I am on the features and scenarios page
    Then I should see a list of features
    And I should see a list of scenarios for each feature
    And I should see the steps for each scenario

  Scenario: Paginate Features and Scenarios
    Given I am on the features and scenarios page
    And there are more features and scenarios than fit on one page
    Then I should see pagination buttons (Previous/Next)
    When I click the "Next" button
    Then I should see the next page of features and scenarios
    And I should see the "Previous" button enabled