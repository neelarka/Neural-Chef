import requests
import pandas as pd
from config import Spoonacular_API_key
import os
import glob


'''
Get the remaining limit
'''
def getremainigAPIcalls():
    #loop through API keys
    for key in Spoonacular_API_key:
        #make tiny request
        response = requests.post("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/cuisine",
        headers={
            "X-RapidAPI-Key": key,
            "Content-Type": "application/x-www-form-urlencoded"
            },
            params={
            "ingredientList": "",
            "title": ""
            }
            )
        try:
            calls_remaning = response.headers['X-RateLimit-requests-Remaining']
            tiny_calls_remaning = response.headers['x-ratelimit-tinyrequests-remaining']
            print(f"Request calls remailing = {calls_remaning} Tiny calls remailing = {tiny_calls_remaning}")
        except:
            print("move on")

        #Return the key only if there are calls remainig
        if (int(calls_remaning) > 0):
            return key

    return None

'''
getRecipeByUrl : query spoonacular API with the link
Return: Return the request
'''
def getRecipeByUrl(url):
    #Add payload
    payload = {
        'fillIngredients': True,
        'url': url,
        'limitLicense': True,
        'number': 2,
        'ranking': 1
    }

    # Check if any limit left
    key = getremainigAPIcalls()
    if (key):
        api_key = key
    else:
        return None

    endpoint = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/extract"

    headers={
        "X-RapidAPI-Key": api_key
    }

    #send the request
    result = requests.get(endpoint, params=payload, headers=headers)

    return result


'''
getRecipe : get the recipe and send it to the routes
cuisine: string
ingredients: list
Return: Return the request'''
def getRecipes(recipe_links):

    recipe_list = []
    info = {}

    #make a API call and get the recipe
    for link in recipe_links[0:3]:
        result = getRecipeByUrl(link)
        # print(result.json())

        if(result):
        #store the information
            try:
                info = {'title': result.json()['title'],
                        'sourceUrl': result.json()['sourceUrl'],
                        'cookingMinutes': result.json()['cookingMinutes'],
                        'preparationMinutes': result.json()['preparationMinutes'],
                        'image': result.json()['image'],
                        'instructions': result.json()['instructions'],
                        'ingredients' : [key['originalString'] for key in result.json()['extendedIngredients']]
                        }
            except:
                # pass
                print("Recipe not found")

            recipe_list.append(info)
            # print(recipe_list)

    return recipe_list

'''
getLinksFromcsv
return the list of recepies
'''
def getLinksFromcsv(cuisine="Indian", ingredients=[]):
    #make everything lower case
    ingredients= [x.lower().strip() for x in ingredients]
    cuisine = cuisine.lower().strip()

    #get the ingredients whoes recipes we have saved
    df = pd.read_csv(os.path.join('recipes', 'recipes.csv'), skipinitialspace=True)
    df.columns = map(str.lower, df.columns)

    #get the synonyms and append to ingredients
    syn_df = pd.read_csv(os.path.join('recipes', 'synonyms.csv'), skipinitialspace=True)
    syn_df.columns = map(str.lower, syn_df.columns)
    syn_df.dropna(inplace=True)
    print(syn_df)

    #if syninym found append to ingredient
    for ingredient in ingredients:
        try:
            ingredients.extend(syn_df[ingredient].tolist())
        except:
            pass
    print(ingredients)

    recipe_links_list = []
    #find the recipes
    try:
        recipe_links_list = df[cuisine][df[cuisine].str.contains('|'.join(ingredients))].tolist()
        print(recipe_links_list)
    except:
        print("not found")

    return recipe_links_list

# getLinksFromcsv('Indian', ['Spinach'])

'''
getdict()
Testing
'''
def getdict():
    return [{'title': 'spinach corn sandwich',
    'sourceUrl': 'https://hebbarskitchen.com/spinach-corn-sandwich-recipe/',
    'cookingMinutes': 10,
    'image': 'https://spoonacular.com/recipeImages/1047695-556x370.jpg',
    'instructions': 'Instructionsfirstly, in a large tawa heat 1 tsp butter and saute 2 tbsp onion.',
    'ingredients': ['1 tsp butter', '2 tbsp onion finely chopped', '1 cup palak / spinach finely chopped']},
    {'title': 'spinach corn sandwich',
    'sourceUrl': 'https://hebbarskitchen.com/spinach-corn-sandwich-recipe/',
    'cookingMinutes': 10,
    'image': 'https://hebbarskitchen.com/wp-content/uploads/mainPhotos/onion-tomato-chutney-recipe-tomato-onion-chutney-recipe-1.jpeg',
    'instructions': 'Instructionsfirstly, in a large tawa heat 1 tsp butter and saute 2 tbsp onion.',
    'ingredients': ['1 tsp butter', '2 tbsp onion finely chopped', '1 cup palak / spinach finely chopped']}]
