    function confirmDelete(itineraryId) {
        if (confirm("Are you sure you want to delete this item?")) {
            document.querySelector(`form[action*="${itineraryId}"]`).submit();
        }
    }
    function addform() {
        const showForm = document.querySelector('#add-form');
        showForm.classList.toggle("hidden");
    }

    function sortCategoriesByTitle() {
        var categoriesContainer = $('.items-grid');
        var categories = categoriesContainer.find('.categories');

        categories.sort(function(a, b) {
            var placeNameA = $(a).data('title').toUpperCase();
            var placeNameB = $(b).data('title').toUpperCase();
            return placeNameA.localeCompare(placeNameB);
        });

        categoriesContainer.empty().append(categories);
    }