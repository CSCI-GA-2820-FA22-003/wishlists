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
                var name=row.insertCell(1);
                var category=row.insertCell(2);
                var price=row.insertCell(3);
                var description=row.insertCell(4);
                id.innerHTML = wishlist.id;
                name.innerHTML = wishlist.name;
                category.innerHTML = wishlist.category;
                price.innerHTML = wishlist.price;
                description.innerHTML = wishlist.description;
            }
            flash_message(JSON.stringify(res));
            flash_message("Success");
        });

        ajax.fail(function(res){
            clear_form_data();
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
                name.innerHTML = wishlist.name;
                user_id.innerHTML = wishlist.user_id;
                created_at.innerHTML = wishlist.created_at;
                last_updated.innerHTML = wishlist.last_updated;
                is_enabled.innerHTML = wishlist.is_enabled;
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