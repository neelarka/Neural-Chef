 var items = [];
var SearchBtn = d3.select("#ingredientsSearchBtn");
var ingredient = d3.select("#ingredientsSearchBar");
SearchBtn.on("click", SearchBtnClick);

function SearchBtnClick() {
	d3.event.preventDefault();
	var filterData = ingredient.property("value");
	console.log(filterData);
	var ingredients = filterData;
	$('#ingredients-list').empty();
	var tbody = d3.select("#ingredients-list");
	// tbody.append("li").text(ingredients)
	items.push(ingredients)
	console.log(items);
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
			recipeCaption.addClass('caption');
			
			//recipeCaption.addClass('text-center');
			caloriesP.text(calories + ' Calories');
			recipeCaption.append(caloriesP)
			recipeImage.attr('src', results[i].recipe.image);
			recipeDiv.addClass('thumbnail col-md-4 recipe');
			recipeDiv.append(recipeImage);
			recipeTitle.push(results[i]["recipe"]["label"])
			recipeCaption.append($('<div>').text(results[i].recipe.label).addClass('recipeName'));
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



