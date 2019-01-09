$(".imgAdd").click(function () {
    $(this).closest(".row").find('.imgAdd').before(
        '<div class="col-lg-3 col-sm-3 imgUp"> \
                      <figcaption class="figure-caption" id="image-name" placeholder="Image name here.">Upload to Predict</figcaption>\
                      <br>\
                      <div class="form-group"> \
                      <div class="imagePreview"></div> \
                      <div class="upload-options"> \
                      <label><i class="fas fa-upload"></i><input type="file" name="file" class="image-upload" accept="image/*;capture=camera" /></label> \
                      </div></div> \
                      <i class="fa fa-times del"></i></div>');
});


$(document).on("click", "i.del", function () {
    $(this).parent().remove();
});


$(function () {
    $(document).on("change", ".image-upload", function () {
        var uploadFile = $(this);
        var files = !!this.files ? this.files : [];
        if (!files.length || !window.FileReader) return; // no file selected, or no FileReader support

        if (/^image/.test(files[0].type)) { // only image file
            var reader = new FileReader(); // instance of the FileReader
            reader.readAsDataURL(files[0]); // read the local file

            reader.onloadend = function () { // set image data as background of div
                //alert(uploadFile.closest(".upimage").find('.imagePreview').length);
                uploadFile.closest(".imgUp").find('.imagePreview').css("background-image", "url(" + this.result + ")");
                var form_data = new FormData();
                $.each($(".image-upload"), function (i, obj) {
                    $.each(obj.files, function (j, file) {
                        form_data.append('file', file); // is the var i against the var j, because the i is incremental the j is ever 0
                        console.log(file);
                    });
                });

                // form_data.append('file', $('.image-upload').prop('files')[0]);
                console.log(form_data);

                req = $.ajax({
                    url: '/',
                    type: 'POST',
                    contentType: false,
                    processData: false,
                    cache: false,
                    data: form_data,
                    success: function (data) {
                        console.log('------------------------------');
                        // console.log(data.predictions[0]);

                        let image_ids = document.getElementsByClassName("image-upload");
                        let captions = document.getElementsByClassName("figure-caption");
                        var list = []
                        for (i = 0; i < captions.length; i++) {
                            captions[i].textContent = data.predictions[i][1]
                            console.log(data.predictions[i][1]);
                            list.push(data.predictions[i][1]);
                        }
                    console.log(list)
                    var items = list;
                    var SearchBtn = d3.select("#ingredientsSearchBtn");
                    //var ingredient = d3.select("#ingredientsSearchBar");
                    SearchBtn.on("click", SearchBtnClick);

                    function SearchBtnClick() {
                        d3.event.preventDefault();
                        //var filterData = ingredient.property("value");
                        //console.log(filterData);
                        //var ingredients = filterData;
                        $('#ingredients-list').empty();
                        var tbody = d3.select("#ingredients-list");
                        // tbody.append("li").text(ingredients)
                        //items.push(ingredients)
                        //console.log(items);
                        items.forEach(function(value){
                            tbody.append("li").text(value)
                        })
                        // var url = 'https://api.edamam.com/search?q=' + items + '&app_id=your_api_id&app_key=your_api_key';
                        var url = 'https://api.edamam.com/search?q=' + items + '&app_id=b8fa8ec0&app_key=2e99e135530eaed01cb9620b24c1f1c0';
                        function displayRecipes() {
                        d3.json(url).then(function(response) {
                            console.log(response.hits[0]["recipe"]["label"])
                            var results = response.hits;
                            
                            $('#recipeDisplay').html('');
                            var recipeTitle = []
                            console.log(results.length)
                            for (i = 0; i < results.length; i++) {
                                var recipeImage = $('<img>');
                                var recipeDiv = $('<div>');
                                var recipeCaption = $('<div>');
                                var recipeBtnDiv = $('<div>');
                                var intCalories = (results[i].recipe.calories)/(results[i].recipe.yield);
                                var calories = (Math.floor(intCalories));
                                var caloriesP = $('<p>');
                                //recipeCaption.addClass('caption');
                                
                                //recipeCaption.addClass('text-center');
                                recipeCaption.append($('<p>').text(results[i].recipe.label).addClass('recipeName'))
                                caloriesP.text(calories + ' Calories');
                                recipeCaption.append(caloriesP)
                                recipeImage.attr('src', results[i].recipe.image);
                                recipeDiv.addClass('thumbnail col-md-3 recipe');
                                recipeDiv.append(recipeImage);
                                recipeDiv.addClass('image-center');
                                recipeTitle.push(results[i]["recipe"]["label"])
                                //recipeCaption.append($('<div>').text(results[i].recipe.label).addClass('recipeName'));
                                recipeCaption.addClass('text-center');
                                recipeDiv.append(recipeCaption);
                                recipeBtnDiv.append($('<a>').append($('<button>').addClass('btn recipeBtn').text('Go to recipe')).attr('href',results[i].recipe.url).attr('target','_blank'));
                                recipeCaption.append(recipeBtnDiv);
                                $('#recipeDisplay').prepend(recipeDiv);
                            }
                            console.log(recipeTitle)
                            //console.log(recipeCaption)
                        })
                        };
                        displayRecipes();
                    }
                    },
                });
            }
        }
    });
});

$(document).ready(function () {
    $('.predictButton').click(function () {
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
            url: '/update',
            type: 'POST',
            data: { image: image_names }
        });

        req.done(function (data) {
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