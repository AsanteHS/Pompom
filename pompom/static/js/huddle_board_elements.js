function ElementRetriever(viewURL, element, timer) {
    var apply = function(data) {
        refreshElementOnScreen(element, data);
    };
    setInterval(retrieveElement, timer * 1000, viewURL, apply);
}

function retrieveElement(viewURL, apply) {
    $.ajax({
        url : viewURL,
        success : function(data) {
            apply(data);
        }
    });
}

function refreshElementOnScreen(element, data) {
    $(element).html(data);
}

function CardsRetriever(viewURL, element, timer){
    var apply = function(data) {
        preloadImages(
            getImagesFromHTML(data),
            function () {refreshElementOnScreen(element, data);}
        );
    };
    setInterval(retrieveElement, timer * 1000, viewURL, apply);
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

function QRRetriever(viewURL, element, timer){
    var apply = function(data) {
        var qrTextOnPage = document.getElementById("qr-code").getAttribute("data-qr-text");
        var qrTextReceived = getQRLinkFromHTML(data);
        if (qrTextReceived !== qrTextOnPage) {
            refreshElementOnScreen(element, data);
            displayQRCode();
        }
    };
    setInterval(retrieveElement, timer * 1000, viewURL, apply);
}

function getQRLinkFromHTML(data) {
    var dummy = $('<div></div>');
    dummy.html(data);
    return $('#qr-code', dummy).data('qr-text');
}

function displayQRCode() {
    var qrElement = document.getElementById("qr-code");
    var qrText = qrElement.getAttribute("data-qr-text");
    new QRCode(qrElement, qrText);
}
