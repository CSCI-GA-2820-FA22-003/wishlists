$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#wishlist_id").val(res.id);
        $("#wishlist_name").val(res.name);
        if (res.is_enabled == true) {
            $("#wishlist_enabled").val("true");
        } else {
            $("#wishlist_enabled").val("false");
        }
        $("#wishlist_uid").val(res.user_id);
    }

    function update_item_form_data(res){
        $("#item_id").val(res.id);
        $("#item_name").val(res.name);
        $("#item_category").val(res.category);
        $("#item_description").val(res.description);
        $("#item_price").val(res.price);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#wishlist_id").val("");
        $("#wishlist_name").val("");
        $("#wishlist_enabled").val("");
        $("#wishlist_uid").val("");
        document.getElementById("wishlist_items").style.display="none";
        document.getElementById("items_title").style.display="none";
        document.getElementById("wishlist_results").style.display="none";
        document.getElementById("wishlists_title").style.display="none";
    }

    /// Clears all item form fields
    function clear_item_form_data() {
        $("#item_id").val("");
        $("#item_name").val("");
        $("#item_category").val("");
        $("#item_price").val("");
        $("#item_description").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Wishlist
    // ****************************************

    $("#create-btn").click(function () {
        let name = $("#wishlist_name").val();
        let user_id = $("#wishlist_uid").val();
        let is_enabled = $("#wishlist_enabled").val() === 'true';

        let data = {
            name,
            user_id,
            items: [],
            is_enabled
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "POST",
            url: "/wishlists",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            console.log(res)
            flash_message((res.responseJSON && res.responseJSON.message) || res.statusText)
        });
    });



    // ****************************************
    // Create an Item
    // ****************************************

    $("#create-item-btn").click(function () {
        if($("#items_title")[0].style.display == 'none'){
            flash_message("No Wishlist retrieved");
            return;
        }
        let wishlist_id = $("#items_title")[0].innerHTML;
        wishlist_id = wishlist_id.slice(wishlist_id.lastIndexOf(' ')+1);
        let id = $("#item_id").val();
        let name = $("#item_name").val();
        let category = $("#item_category").val();
        let price = $("#item_price").val();
        let description = $("#item_description").val();

        let data = {
            id,
	        wishlist_id: wishlist_id, 
            name,
            category,
            price: parseInt(price),
            description
        };
        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "POST",
            url: `/wishlists/${wishlist_id}/items`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            clear_item_form_data()
            $("#retrieve-btn").click();
            flash_message("Success")
        });

        ajax.fail(function (res) {
            console.log(res)
            flash_message((res.responseJSON && res.responseJSON.message) || res.statusText)
        });
    });


    // ****************************************
    // Delete an Item
    // ****************************************

    $("#delete-item-btn").click(function () {
        if($("#items_title")[0].style.display == 'none'){
            flash_message("No Wishlist retrieved");
            return;
        }
        let wishlist_id = $("#items_title")[0].innerHTML;
        wishlist_id = wishlist_id.slice(wishlist_id.lastIndexOf(' ')+1);
        let id = $("#item_id").val();
        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/wishlists/${wishlist_id}/items/${id}`,
            contentType: "application/json",
            data: '',
        });

        ajax.done(function(res){
            clear_item_form_data()
            $("#retrieve-btn").click();
            flash_message("Success");
        });

        ajax.fail(function (res) {
            console.log(res)
            flash_message((res.responseJSON && res.responseJSON.message) || res.statusText)
        });
    });


    // ****************************************
    // Update a Wishlist
    // ****************************************

    $("#update-btn").click(function () {
        
        let wishlist_id = $("#wishlist_id").val();
        let name = $("#wishlist_name").val();
        let user_id = $("#wishlist_uid").val();
        let is_enabled = $("#wishlist_enabled").val() === 'true';        

        let data = {
            wishlist_id,
            name,
            user_id,
            items: [],
            is_enabled
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/wishlists/${wishlist_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Wishlist
    // ****************************************

    $("#retrieve-btn").click(function () {

        var id = $("#wishlist_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/wishlists/${id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res);
            document.getElementById("wishlist_items").style.display="table";
            document.getElementById("items_title").style.display="block";
            document.getElementById("items_title").innerHTML=`Items in Wishlist ${res.id}`;
            var table = document.getElementById("wishlist_items_body");
            table.innerHTML = "";
            for(let i = 0; i < res.items.length; i++) {
                let wishlist = res.items[i];
                var row = table.insertRow(-1);
                var id=row.insertCell(0);
                id.id = "item_entry-"+(i+1)+"-id";
                var name=row.insertCell(1);
                name.id = "item_entry-"+(i+1)+"-name";
                var category=row.insertCell(2);
                category.id = "item_entry-"+(i+1)+"-category";
                var price=row.insertCell(3);
                price.id = "item_entry-"+(i+1)+"-price";
                var description=row.insertCell(4);
                description.id = "item_entry-"+(i+1)+"-description";
                id.innerHTML = wishlist.id;
                name.innerHTML = wishlist.name;
                category.innerHTML = wishlist.category;
                price.innerHTML = wishlist.price;
                description.innerHTML = wishlist.description;
            }
            flash_message("Success");
        });

        ajax.fail(function(res){
            clear_form_data();
            flash_message(res.responseJSON.message);
        });

    });


    // ****************************************
    // Retrieve an Item
    // ****************************************

    $("#retrieve-item-btn").click(function () {
        if($("#items_title")[0].style.display == 'none'){
            flash_message("No Wishlist retrieved");
            return;
        }
        let wishlist_id = $("#items_title")[0].innerHTML;
        wishlist_id = wishlist_id.slice(wishlist_id.lastIndexOf(' ')+1);
        let id = $("#item_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/wishlists/${wishlist_id}/items/${id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_item_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function(res){
            clear_item_form_data();
            flash_message(res.responseJSON.message);
        });

    });

    // ****************************************
    // Delete a Wishlist
    // ****************************************

    $("#delete-btn").click(function () {

        let wishlist_id = $("#wishlist_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/wishlists/${wishlist_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Wishlist has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#wishlist_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Clear the Item form
    // ****************************************

    $("#clear-item-btn").click(function () {
        $("#item_id").val("");
        $("#flash_message").empty();
        clear_item_form_data()
    });

    // ****************************************
    // Search for a Wishlist
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#wishlist_name").val();
        let user_id = $("#wishlist_uid").val();
        let is_enabled = $("#wishlist_enabled").val() == "true";

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (user_id) {
            if (queryString.length > 0) {
                queryString += '&user_id=' + user_id
            } else {
                queryString += 'user_id=' + user_id
            }
        }
        if (is_enabled) {
            if (queryString.length > 0) {
                queryString += '&available=' + is_enabled
            } else {
                queryString += 'available=' + is_enabled
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/wishlists?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            document.getElementById("wishlist_results").style.display="table";
            document.getElementById("wishlists_title").style.display="block";
            var table = document.getElementById("wishlist_results_body");
            table.innerHTML = "";
            let firstWishlist = "";
            for(let i = 0; i < res.length; i++) {
                let wishlist = res[i];
                var row = table.insertRow(-1);
                var id=row.insertCell(0);
                var name=row.insertCell(1);
                var user_id=row.insertCell(2);
                var created_at=row.insertCell(3);
                var last_updated=row.insertCell(4);
                var is_enabled=row.insertCell(5);
                id.innerHTML = wishlist.id;
                id.id = "wishlist_entry-"+(i+1)+"-id";
                name.innerHTML = wishlist.name;
                name.id = "wishlist_entry-"+(i+1)+"-name";
                user_id.innerHTML = wishlist.user_id;
                user_id.id = "wishlist_entry-"+(i+1)+"-user_id";
                created_at.innerHTML = wishlist.created_at;
                created_at.id = "wishlist_entry-"+(i+1)+"-created_at";
                last_updated.innerHTML = wishlist.last_updated;
                last_updated.id = "wishlist_entry-"+(i+1)+"-last_updated";
                is_enabled.innerHTML = wishlist.is_enabled;
                is_enabled.id = "wishlist_entry-"+(i+1)+"-is_enabled";
                if (i == 0) {
                    firstWishlist = wishlist;
                }
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})