Feature: Blood Preasure Calculator Feedback
  As a user, I want to get feedback when an error occurs.

  Scenario Outline: Input incorrect values into the calculator
    Given a blood preasure calculator

    When systolic is <systolic> and diastolic is <diastolic>
    And form is submitted

    Then error should list "<error>"

    Examples:
      | systolic | diastolic | error                                                    |
      | 80       | 100       | Systolic preasure must be higher than diastolic preasure |
      | 200      | 80        | Systolic value must be between 70 and 190                |
      | 140      | 30        | Diastolic value must be between 40 and 100               |
      | ''       | ''        | Valid values must be entered                             |
      | 100      | string    | Valid values must be entered                             |