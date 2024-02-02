$(document).ready(function () {

    /* Here, after entering date in date box, if the date is invalid, the add to cart button is disabled, and turns
       red (modifying existing element) and Invalid date entered text is displayed (adding new element) using DOM Traversal */
    $('.cart-addition').on('change', '.date-box', function () {
        var selectedDate = $(this).val();
        var cartButton = $(this).closest('.cart-addition').find('#addtoCart');
        var Placeholder = $(this).closest('.cart-addition').find('#placeholderaddSuccess');

        if (isValidDate(selectedDate)) {
            cartButton.prop('disabled', false);
            cartButton.css('cursor', 'pointer');
            cartButton.css('background-color', '#1e4722');
            $(cartButton).on('click', function () {
                Placeholder.empty();
                Placeholder.append('<p>Added to Cart Succesfully</p>');
                setTimeout(function () {
                    Placeholder.empty();
                    cartButton.css('background-color', '#72491e');
                }, 1000);
            })

        }
        else {
            cartButton.prop('disabled', true);
            cartButton.css('cursor', 'auto');
            cartButton.css('background-color', 'red');
            Placeholder.append('<p>Invalid Date Entered</p>');
            setTimeout(function () {
                cartButton.css('background-color', '#72491e');
                Placeholder.empty();
            }, 2000);
        }
    });

    function isValidDate(dateString) {
        var parts = dateString.split('/');
        var month = parseInt(parts[0], 10);
        var day = parseInt(parts[1], 10);
        var year = parseInt(parts[2], 10);
        if (year < 2023 || year > 2035 || month == 0 || month > 12) return false;
        if ((month == 4 || month == 6 || month == 9 || month == 11) && day > 30) return false;
        if (day > 31) return false;
        var selectedDate = new Date(year, month - 1, day);
        var currentDate = new Date();
        if (selectedDate <= currentDate) {
            return false;
        }
        return true;
    }

    /* Here we are toggling the lists, which shows list description of list using
    Event Delegation. Existing lists appearance is modified (modifying existing element)
    and new list content (adding new element) is shown on clicking on the dropdown. */
    $(".dropdown-container").on("click", ".dropdown-toggle", function () {
        $(this).next(".lists").toggle();
    });


     $("#leave-review-button").click(function () {
        $("#review-form").show();
    });

    $("#review-form").submit(function (e) {
    e.preventDefault();
    console.log("Submitting Review")
    var title = $(this).find("input[name='title']").val();
    var description = $(this).find("textarea[name='description']").val();
    var itineraryId = $(this).find("input[name='itinerary-id']").val();

    console.log("itineraryId:", itineraryId);
    $.ajax({
        type: "POST",
        url: `/itineraries/${itineraryId}/`,
        data: $(this).serialize(),
        success: function (response) {
            $("body").html(response);
        }
    });
});

        $('#load-other-blogs').on('click', function() {
           $(this).hide();
            console.log("Loading..")
        $.ajax({
            url: '/get_other_blogs/',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                console.log(data);
                var otherBlogsContainer = $('.other-blogs-container');
                otherBlogsContainer.empty();

                $.each(data.blogs, function(index, blog) {
                    var blogHtml = `
                        <div class="background">
                            <a href="blog.html">
                                <h3 class="text-background">${blog.title}</h3>
                                <p class="text-background">${blog.description}</p>
                            </a>
                        </div>
                    `;
                    otherBlogsContainer.append(blogHtml);
                });

                otherBlogsContainer.show();
            },
        });
    });

        $(".delete-review").on("click", function() {
            var $clickedElement = $(this);
        console.log("Checking..")
        var reviewId = $(this).data("review-id");
        var itineraryId = $(this).data("itinerary-id");
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            url: "/itineraries/" + itineraryId + "/delete_review/" + reviewId + '/',
            method: "POST",
            data: {
                review_id: reviewId,
                itinerary_id: itineraryId
            },
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function(response) {
                if (response.success) {
                    $clickedElement.closest('.ind-review-new').remove();
                    location.reload();
                }
            },
        });
    });
});
