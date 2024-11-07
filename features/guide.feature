Feature: Guide
  This feature describes the functionalities implemented in the Gherkin Guide application.
  
  # Funcionalidad de Importación de Archivos `.feature`
  Scenario: Import a feature file
    Given I have opened the Gherkin Guide application
    When I click on the "Features" menu
    And I select the "Import" option
    Then I should see a form to load a feature file
    When I click on the "Load File" button
    And I select a `.feature` file from the system dialog
    Then I should see the path and name of the selected file
    And I should see two buttons: "Accept" and "Cancel"

  Scenario: Cancel file selection
    Given I have selected a `.feature` file
    When I click on the "Cancel" button
    Then the file path and name should be cleared
    And the file should not be loaded

  Scenario: Accept file selection and start import process
    Given I have selected a `.feature` file
    When I click on the "Accept" button
    Then the file should be loaded
    And the feature, scenarios, and steps should be processed and stored in the database

  # Funcionalidad de Búsqueda Predictiva
  Scenario: Perform predictive search
    Given I have opened the Gherkin Guide application
    When I enter a query in the search field
    Then I should see matching features, scenarios, and steps from the database

  # Funcionalidad de Cambio de Idioma
  Scenario: Change application language to Spanish
    Given I have opened the Gherkin Guide application
    When I click on the "Configuración" menu
    And I select the "ES" option with the Spain flag
    Then the application language should change to Spanish
    And I should see all texts in Spanish

  Scenario: Change application language to English
    Given I have opened the Gherkin Guide application
    When I click on the "Configuración" menu
    And I select the "US" option with the US flag
    Then the application language should change to English
    And I should see all texts in English

  # Funcionalidad de About
  Scenario: View About section
    Given I have opened the Gherkin Guide application
    When I click on the "About" menu
    Then I should see the application logo
    And I should see the version, creator, and last updated date

  # Funcionalidad de Menú Desplegable
  Scenario: View features dropdown menu
    Given I have opened the Gherkin Guide application
    When I click on the "Features" menu
    Then I should see options "Create", "Consult", and "Import"
