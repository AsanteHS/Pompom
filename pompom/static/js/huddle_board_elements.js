$(function () {
    preloadGlyphiconsFont();
});

function preloadGlyphiconsFont() {
    // If the offline message remains hidden until board is offline, browser never loads glyphicons font.
    // Show message for a moment so font is loaded at the beginning.
    $('#board-offline').removeClass('hidden').addClass('hidden');
}

function ElementRetriever(viewURL, element, timer, doAfterRetrieve) {
    doAfterRetrieve = defaultFor(doAfterRetrieve, function(data) {
        refreshElementOnScreen(element, data);
    });
    setInterval(retrieveElement, timer * 1000, viewURL, element, doAfterRetrieve);
}

function defaultFor(arg, val) {
    return typeof arg === 'undefined' ? val : arg;
}

function retrieveElement(viewURL, element, doAfterRetrieve) {
    var $offlineMessage = $('#board-offline');
    $.ajax({
        url : viewURL,
        success : function(data) {
            if(isExpectedElement(data, element)){
                $offlineMessage.addClass('hidden');
                doAfterRetrieve(data);
            } else {
                window.location.replace("/");
            }
        },
        error: function() {
            $offlineMessage.removeClass('hidden');
        }
    });
}

function isExpectedElement(data, element) {
    var $data = $(data);
    var expectedID = element + '-element';
    var retrievedID = $data.attr('id');
    $data.remove();
    console.log(expectedID, retrievedID);
    return expectedID === retrievedID;
}

function refreshElementOnScreen(element, data) {
    $("#" + element + "-container").html(data);
}

function CardsRetriever(viewURL, element, timer){
    var doAfterRetrieve = function(data) {
        preloadImages(
            getImagesFromHTML(data),
            function () {refreshElementOnScreen(element, data);}
        );
    };
    ElementRetriever(viewURL, element, timer, doAfterRetrieve);
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
        img.src = src;
    };

    for (i = 0; i < arrayLength; i++){
        loadImage(new Image(), arrayOfImages[i]);
    }
}

function getImagesFromHTML(data) {
    var $data = $(data);
    var imageArray = $('img', $data).map(function() { return this.src; });
    $data.remove();
    return imageArray;
}

function QRRetriever(viewURL, element, timer){
    var doAfterRetrieve = function(data) {
        if (qrCodeHasChanged(data)) {
            refreshElementOnScreen(element, data);
            displayQRCode();
        }
    };
    ElementRetriever(viewURL, element, timer, doAfterRetrieve);
}

function qrCodeHasChanged(data) {
    var qrTextOnPage = document.getElementById("qr-code").getAttribute("data-qr-text");
    var qrTextReceived = getQRLinkFromHTML(data);
    return (qrTextReceived !== qrTextOnPage);
}

function getQRLinkFromHTML(data) {
    var $data = $(data);
    var qrLink = $('#qr-code', $data).data('qr-text');
    $data.remove();
    return qrLink;

}

function displayQRCode() {
    var qrElement = document.getElementById("qr-code");
    var qrText = qrElement.getAttribute("data-qr-text");
    new QRCode(qrElement, qrText);
}
