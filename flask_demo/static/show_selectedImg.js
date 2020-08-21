function show_selectedImage() {
    /// get select files.
    var selected_files = document.getElementById("select_pic").files;
    for (var file of selected_files) {
        /// console.log(file.webkitRelativePath);

        /// read file content.
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = function () {
            /// deal data.
            var img = new Image();
            /// after loader, result storage the file content result.
            img.src = this.result;


            img.onload = function () {
                var canvas = document.getElementById("select_pic_canvas");
                var w = img.width;
                var h = img.height;
                var cxt = canvas.getContext('2d');
                cxt.clearRect(0, 0, canvas.clientWidth, canvas.clientHeight);
                cxt.drawImage(img, (canvas.clientWidth - w) / 2, (canvas.clientHeight - h) / 2);
            }
        }
    }
}
