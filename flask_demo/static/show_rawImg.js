function setImage(flag, img_stream) {
    console.log("show raw img.",flag)

    if (flag === 1) {
        console.log("set Image");
        var canvas = document.getElementById('select_pic_canvas');
        var cw = canvas.clientWidth;
        var ch = canvas.clientHeight;


        /// var ctx = canvas.getContext('2d');
        var image = new Image();
        image.src = "data:;base64," + img_stream;
        // image.src = img_stream
        var w = "";
        var h = "";
        image.onload = function () {
            w = image.width
            h = image.height
            var cxt = canvas.getContext('2d');
            cxt.clearRect(0, 0, cw, ch);
            cxt.drawImage(image, (cw - w) / 2, (ch - h) / 2);
        };
    }
}