Feature: Site Navigation
  As a user, I want to navigate the site.

  Scenario: Navigate to home page
    Given a blood preasure calculator

    When Navigation button "Home" exists
    And Navigation button is clicked

    Then url should be "/"