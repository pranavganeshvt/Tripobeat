/*This file is meant to implement simulated search for a given
key paraphrase: 'Blacksburg'. On correct keyphrase, we will load the item page
and wrong keyphrase will display a friendly error page*/
$(document).ready(function () {
    const searchParams = new URLSearchParams(window.location.search);
    var input = searchParams.get('text-input').toLowerCase();

    const resultsContainer = $('#message');

    if (input === 'blacksburg') {
        // Simulated search results
        window.location.href = "category.html";
    } else {
        const resultMessage = '<h1> No Results Found </h1>' +
            '<p> We are working on adding new destinations everyday. Please check back later to see if your destination is available on our website. Thank you! </p>'
        resultsContainer.html(resultMessage)
    }
});