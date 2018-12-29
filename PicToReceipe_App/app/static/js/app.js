$(".imgAdd").click(function(){
  $(this).closest(".row").find('.imgAdd').before(
                    '<div class="col-lg-3 col-sm-3 imgUp"> \
                    <figcaption class="figure-caption" id="image-name">A caption for the below image.</figcaption>\
                    <br>\
                    <div class="form-group"> \
                    <div class="imagePreview"></div> \
                    <div class="upload-options"> \
                    <label><input type="file" name="file" class="image-upload" accept="image/*" /></label> \
                    </div></div></div>\
                    <i class="fa fa-times del"></i></div>');
});


$(document).on("click", "i.del" , function() {
	$(this).parent().remove();
});


$(function() {
    $(document).on("change",".image-upload", function(){
        var uploadFile = $(this);
        var files = !!this.files ? this.files : [];
        if (!files.length || !window.FileReader) return; // no file selected, or no FileReader support

        if (/^image/.test( files[0].type)){ // only image file
            var reader = new FileReader(); // instance of the FileReader
            reader.readAsDataURL(files[0]); // read the local file

            reader.onloadend = function(){ // set image data as background of div
                //alert(uploadFile.closest(".upimage").find('.imagePreview').length);
            uploadFile.closest(".imgUp").find('.imagePreview').css("background-image", "url("+this.result+")");
            }
        }
    });
});

$(document).ready(function(){
    $('.predictButton').on('click', function() {
        let image_id = $('.image-upload').val();
        let image_ids = document.getElementsByClassName("image-upload");
        console.log(image_ids.length);
        var image_names = [];
        var i;
        for (i = 0; i < image_ids.length; i++) {
            // console.log(image_ids[i].value);
            image_names.push(image_ids[i].value)
        }
        console.log("_____________________________")
        console.log(image_names)

        req = $.ajax({
            url : '/update',
            type : 'POST',
            data : {image : image_names}
        });

        req.done(function(data) {
            console.log('------------------------------');
            console.log(data.predictions[0]);

            let image_ids = document.getElementsByClassName("image-upload");
            let captions = document.getElementsByClassName("figure-caption");
            for (i = 0; i < captions.length; i++) {
                captions[i].textContent = data.predictions[i][1]
            }
        });
    });
});
