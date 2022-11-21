Feature: Blood Preasure Calculator
  As a user, I want to check my blood preasure category.

  Scenario Outline: Calculate blood preasure category
    Given a blood preasure calculator

    When systolic is <systolic> and diastolic is <diastolic>
    And form is submitted

    Then blood preasure category is <bp_category>

    Examples:
      | systolic | diastolic | bp_category |
      | 100      | 80        | pre-high    |
      | 110      | 70        | ideal       |
      | 190      | 70        | high        |
      | 80       | 50        | low         |
