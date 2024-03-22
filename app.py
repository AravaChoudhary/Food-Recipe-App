from flask import Flask, render_template, request
import requests
from urllib.parse import unquote

app = Flask(__name__)

API_KEY = '0d86ac6459074f2b970c1971ae5e58b0'

@app.route('/home', methods = ['GET'])
def home():
    return render_template('home.html',recipes=[], search_query='')

@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('search_query','')
        recipes = search_recipes(query)
        return render_template('home.html', recipes=recipes, search_query=query)
    
    #if it is a GET request or no form submitted
    search_query = request.args.get('search_query', '')
    decoded_search_query = unquote(search_query)
    #Performeing search of recipes with the decoded search query
    recipes = search_recipes(decoded_search_query)
    #Render the main page
    return render_template('home.html', recipes=recipes, search_query=decoded_search_query)

#Functions to search for recipes based on the provided search query
def search_recipes(query):
    url = f'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': API_KEY,
        'query': query,
        'number': 10,
        'instructionsRequired': True,
        'addRecipeInformation': True,
        'fillIngredients': True,

    }

    #Send a GET request to the API with query parameters
    response = requests.get(url, params=params)
    #If the API call succeeds
    if response.status_code == 200:
        # Parse the API response as JSON data
        data = response.json()
        return data['results']
    #If the API call fails
    return []


#Route to view a specific recipe with a given recipe ID
@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    #Get the search query from the URL parameters
    search_query = request.args.get('search_query', '')
    #Build the URL to get information about the recipe with the given ID
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params ={
        'apiKey': API_KEY,
    }

    #Send a get request to the API to get the recipe information
    response = requests.get(url, params=params)
    #If the API call succeeds
    if response.status_code == 200:
        recipe = response.json()
        return render_template('view_recipe.html', recipe=recipe, search_query=search_query)
    return 'Recipe not found',404


if __name__ == '__main__':
    app.run(debug=True)
        