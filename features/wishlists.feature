Feature: The store service back-end
    As a Store Owner
    I need a RESTful wishlist service
    So that I can keep track of all my wishlists

Background:
    Given the server is started

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Wishlist REST API Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Wishlist
    When I visit the "home page"
    And I set "Name" to "Wishlist 1"
    And I set "uid" to "123"
    And I select "True" in the "Enabled" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    And I should not see "404 Not Found"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "uid" field should be empty
    And the "Enabled" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Wishlist 1" in the "Name" field
    And I should see "123" in the "uid" field
    And I should see "True" in the "Enabled" dropdown

Scenario: Get a Wishlist
    When I visit the "Home Page"
    And I set "Name" to "Wishlist 2"
    And I set "uid" to "123"
    And I select "True" in the "Enabled" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "uid" field should be empty
    And the "Enabled" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Wishlist 2" in the "Name" field
    And I should see "123" in the "uid" field
    And I should see "True" in the "Enabled" dropdown

Scenario: Delete a Wishlist
    When I visit the "Home Page"
    And I set "Name" to "Wishlist 3"
    And I set "uid" to "123"
    And I select "True" in the "Enabled" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "uid" field should be empty
    And the "Enabled" field should be empty
    When I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Wishlist has been Deleted!"

Scenario: Update a Wishlist
    When I visit the "Home Page"
    And I set "Name" to "Wishlist 4"
    And I set "uid" to "123"
    And I select "True" in the "Enabled" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "uid" field should be empty
    And the "Enabled" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Wishlist 4" in the "Name" field
    When I change "Name" to "Wishlist 4 Updated"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Wishlist 4 Updated" in the "Name" field