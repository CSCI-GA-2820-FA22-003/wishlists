Feature: The store service back-end
    As a Store Owner
    I need a RESTful wishlist service
    So that I can keep track of all my wishlists

Background:
    Given the server is started
    And the following wishlists
        | id      | user_id  | name                    | created_at                         | last_updated                     |
        | 1       | 12       | Christmas Wishlist      | 2022-10-19 02:32:08.442973+00:00   | 2022-10-19 02:32:08.442973+00:00 |
        | 2       | 5        | Birthday Wishlist       | 2022-10-19 02:32:08.442973+00:00   | 2022-10-19 02:32:08.442973+00:00 |
        | 4       | 12       | Secondary Wishlist      | 2022-10-19 02:32:08.442973+00:00   | 2022-10-19 02:32:08.442973+00:00 |
    And the following items
        | id      | wishlist_id  | name                    | category        | price         | description                     |
        | 1       | 1            | XBOX 360                | gaming          | 350           | Gaming console released in 2012 |
        | 2       | 4            | XBOX One X              | gaming          | 550           | Gaming console released in 2019 |

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

Scenario: Clear a Wishlist
    When I visit the "Home Page"
    And I set "Name" to "Wishlist 5"
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
    And I should see "Wishlist 5" in the "Name" field
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Clear-Wishlist" button
    Then I should see the message "Success"

Scenario: Query a Wishlist
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see wishlist "1" with "Christmas Wishlist" in the "Name" field
    And I should see wishlist "2" with "Birthday Wishlist" in the "Name" field
    And I should see wishlist "3" with "Secondary Wishlist" in the "Name" field
    When I press the "Clear" button
    And I set "Name" to "Birthday"
    And I press the "Search" button
    Then I should see wishlist "1" with "Birthday Wishlist" in the "Name" field

Scenario: Retrieve a Wishlist
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the first "Id" entry in "wishlist" table
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Christmas Wishlist" in the "Name" field
    And I should see item "1" with "XBOX 360" in the "Name" field
    And I should see item "2" with "XBOX One X" in the "Name" field

Scenario: Add Item to Wishlist
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the first "Id" entry in "wishlist" table
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    When I set the item "Id" to "3"
    And I set the item "Name" to "New Item"
    And I set the item "Category" to "Gaming"
    And I set the item "Price" to "300"
    And I set the item "Description" to "New Item description"
    And I press the "create-item" button
    Then I should see the message "Success"
    And I should see item "3" with "New Item" in the "Name" field
    And I should see item "3" with "Gaming" in the "Category" field
    And I should see item "3" with "300" in the "Price" field
    And I should see item "3" with "New Item description" in the "Description" field

Scenario: Delete Item from Wishlist
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the first "Id" entry in "wishlist" table
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see item "1" with "XBOX 360" in the "Name" field
    When I copy the first "Id" entry in "item" table
    And I paste the item "id" field
    And I press the "delete-item" button
    Then I should see the message "Success"
    And I should see item "1" with "XBOX One X" in the "Name" field

Scenario: Retrieve Item from Wishlist
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the first "Id" entry in "wishlist" table
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    When I copy the first "Id" entry in "item" table
    And I paste the item "id" field
    And I press the "retrieve-item" button
    Then I should see "XBOX 360" in the "name" item field
    And I should see "gaming" in the "category" item field
    And I should see "350" in the "price" item field
    And I should see "Gaming console released in 2012" in the "description" item field

Scenario: Update Item from Wishlist
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the first "Id" entry in "wishlist" table
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    When I copy the first "Id" entry in "item" table
    And I paste the item "id" field
    And I press the "retrieve-item" button
    Then I should see the message "Success"
    When I set the item "Name" to "XBOX 3600"
    And I set the item "Category" to "GamingUpdated"
    And I set the item "Price" to "300"
    And I set the item "Description" to "Updated Gaming console released in 2012"
    And I press the "update-item" button
    Then I should see the message "Success"
    And I should see item "1" with "XBOX 3600" in the "Name" field
    And I should see item "1" with "GamingUpdated" in the "Category" field
    And I should see item "1" with "300" in the "Price" field
    And I should see item "1" with "Updated Gaming console released in 2012" in the "Description" field
    