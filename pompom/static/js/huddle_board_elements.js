function CardsRetriever(viewURL){
    var seconds = 15;
    setInterval(retrieveCards, seconds * 1000, viewURL);
}

function retrieveCards(viewURL){
    $.ajax({
        url : viewURL,
        type : "GET",
        success : function(data) {
            preloadImages(
                getImagesFromHTML(data),
                function(){refreshCardsOnScreen(data);}
            );
        }
    });
}

function preloadImages(arrayOfImages, callback) {
    var i;
    var arrayLength = arrayOfImages.length;
    var loaded = 0;

    var loadImage = function (img, src) {
        img.onload = function () {
            if (++loaded === arrayLength && callback) {
                callback();
            }
        };
        img.onerror = function () {};
        img.onabort = function () {};
        img.src = src;
    };

    for (i = 0; i < arrayLength; i++){
        loadImage(new Image(), arrayOfImages[i]);
    }
}

function getImagesFromHTML(data) {
    var dummy = $('<div></div>');
    dummy.html(data);
    return $('img', dummy).map(function() { return this.src; });
}

function refreshCardsOnScreen(data) {
    $('#cards-container').html(data);
}
