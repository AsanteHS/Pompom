function ElementRetriever(viewURL, element, timer, doAfterRetrieve) {
    doAfterRetrieve = defaultFor(doAfterRetrieve, function(data) {
        refreshElementOnScreen(element, data);
    });
    setInterval(retrieveElement, timer * 1000, viewURL, doAfterRetrieve);
}

function defaultFor(arg, val) {
    return typeof arg === 'undefined' ? val : arg;
}

function retrieveElement(viewURL, doAfterRetrieve) {
    $.ajax({
        url : viewURL,
        success : function(data) {
            doAfterRetrieve(data);
        }
    });
}

function refreshElementOnScreen(element, data) {
    $(element).html(data);
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
    var dummy = $('<div></div>');
    dummy.html(data);
    return $('img', dummy).map(function() { return this.src; });
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
    var dummy = $('<div></div>');
    dummy.html(data);
    return $('#qr-code', dummy).data('qr-text');
}

function displayQRCode() {
    var qrElement = document.getElementById("qr-code");
    var qrText = qrElement.getAttribute("data-qr-text");
    new QRCode(qrElement, qrText);
}
