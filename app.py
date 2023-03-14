from flask import Flask, render_template, request
import urllib.parse, urllib.request, urllib.error, json

app = Flask(__name__)


#loading main screen
@app.route('/')
def index():
    return render_template('forms.html', page_title="Search Recipes")

#generating recipe dictionary
def getRecipes(max_carbs = "0", meal_type = "main course"):

    url_base = "https://api.spoonacular.com/recipes/complexSearch"
    API_KEY = "efe364c1f18344ac80c406a856014d9c"

    query_string = {"maxCarbs": str(max_carbs), "type": str(meal_type), "apiKey": API_KEY}
    query_string = urllib.parse.urlencode(query_string)
    # url_request = url_base + "?" + urllib.parse.urlencode(query_string)

    headers = {"User-Agent": "Bella HCDE 310 Final"}
    # req = urllib.request.Request(url_request,headers=headers)
    # Data = urllib.request.urlopen(req).read()
    # recipes_dict = json.loads(Data)

    recipes_dict = safe_get(url_base, query_string)
    recipes_dict = json.loads(recipes_dict)
    recipes_dict = recipes_dict["results"]
    id_dictionary = {}

    for recipe in recipes_dict:
        id = recipe["id"]
        title = recipe["title"]
        imageLink = recipe["image"]
        id_dictionary[id] = [title, imageLink]
        url_query_string = {"includeNutrition": False, "apiKey": API_KEY}
        url_query_string = urllib.parse.urlencode(url_query_string)
        url_id = "https://api.spoonacular.com/recipes/" + str(id) + "/information/"
        urls_dict = safe_get(url_id, url_query_string)
        urls_dict = json.loads(urls_dict)
        print(urls_dict)
        url = urls_dict["sourceUrl"]
        id_dictionary[id].append(url)
        # request = url_base + "?" + urllib.parse.urlencode(url_query_string)
        # req_url = urllib.request.Request(request,headers=headers)
        # Data_url = urllib.request.urlopen(req_url).read()
        # urls_dict = json.loads(Data_url)

    return id_dictionary

def safe_get(base_url, args):
    url = base_url + "?" + args
    try:
        req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Learning Python'
        }
        )
        f = urllib.request.urlopen(req)
        data = f.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print('Error from server. Error code: ', e.code)
        return None
    except urllib.error.URLError as e:
        print('Failed to reach server. Reason: ', e.reason)
        return None
    return(data)

getRecipes("100", "main course")


@app.route("/response")
def response_handling():

    maxCarbs = request.args.get('maxCarbs')
    meal_type = request.args.get('type')

    recipes = getRecipes(maxCarbs, meal_type)

    if meal_type == None:
        return render_template('forms.html', page_title="Search Recipes", prompt="Please Select a meal type to get Search Results!")

    if recipes == {}:
        return render_template('forms.html', page_title="Search Recipes", prompt="There were no recipes under those filters, please try other filters!")

    return render_template('results.html',
        page_title = "Recipe results", recipes = recipes)


