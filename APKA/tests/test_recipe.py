import pytest
from recipe import Recipe

@pytest.mark.parametrize("name, ingredients, kcal, protein, fat, carbs", [
    ("Smoothie", {"banana": 1, "milk": 200}, 180, 5, 3, 35),
    ("Soup", {"water": 500, "carrot": 100}, 90, 2, 1, 10),
    ("Rice", {"rice": 100}, 130, 3, 1, 30),
    ("Omelette", {"eggs": 2, "cheese": 50}, 250, 15, 20, 2),
    ("Pancakes", {"flour": 100, "milk": 200}, 300, 7, 6, 40),
])
def test_valid_recipes(name, ingredients, kcal, protein, fat, carbs):
    r = Recipe(name, ingredients, kcal, protein, fat, carbs)
    nutrients = r.total_nutrients()
    assert nutrients["kcal"] == kcal
    assert nutrients["protein"] == protein
    assert nutrients["fat"] == fat
    assert nutrients["carbs"] == carbs

@pytest.mark.parametrize("name, kcal, protein, fat, carbs", [
    ("", 100, 5, 5, 5),
    ("Invalid", -10, 5, 5, 5),
    ("Invalid", 100, -5, 5, 5),
    ("Invalid", 100, 5, -5, 5),
    ("Invalid", 100, 5, 5, -5),
])
def test_invalid_recipes(name, kcal, protein, fat, carbs):
    with pytest.raises(ValueError):
        Recipe(name, {}, kcal, protein, fat, carbs)

def test_large_values_recipe():
    r = Recipe("Mega Meal", {"meat": 1000, "rice": 500}, 10000, 500, 200, 600)
    nutrients = r.total_nutrients()
    assert nutrients["kcal"] == 10000
    assert nutrients["protein"] == 500
    assert nutrients["fat"] == 200
    assert nutrients["carbs"] == 600

def test_negative_ingredient_quantity():
    # Ujemna ilość składników nie podnosi wyjątku w konstruktorze, ale możemy to wykryć później
    r = Recipe("Strange", {"milk": -200}, 100, 5, 5, 5)
    assert r.ingredients["milk"] == -200

def test_empty_ingredients():
    r = Recipe("Water Fast", {}, 0, 0, 0, 0)
    assert r.total_nutrients() == {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}

@pytest.mark.parametrize("name", [
    "A" * 1000,  # bardzo długa nazwa
    "汉字",       # znaki chińskie
    "😊🍎🍞",     # emoji
])
def test_unicode_and_long_names(name):
    r = Recipe(name, {"air": 0}, 0, 0, 0, 0)
    assert r.name == name

def test_zero_ingredient_quantity():
    r = Recipe("ZeroFood", {"water": 0}, 0, 0, 0, 0)
    assert r.ingredients["water"] == 0

def test_recipe_with_zero_values_everywhere():
    r = Recipe("ZeroMeal", {}, 0, 0, 0, 0)
    assert r.total_nutrients() == {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}

def test_recipe_with_mixed_units():
    r = Recipe("Mixed", {"rice (g)": 100, "milk (ml)": 200}, 350, 15, 10, 40)
    assert "milk (ml)" in r.ingredients

def test_recipe_str_name_is_preserved():
    name = "Śniadanie #1 – 🥐🍳"
    r = Recipe(name, {"jajko": 1}, 120, 10, 8, 1)
    assert r.name == name

def test_recipe_float_values_in_ingredients():
    r = Recipe("PłynnaZupa", {"bulion": 250.5}, 100, 2, 2, 10)
    assert isinstance(r.ingredients["bulion"], float)

def test_recipe_zero_protein_meal():
    r = Recipe("Woda", {"woda": 200}, 0, 0, 0, 0)
    nutrients = r.total_nutrients()
    assert nutrients["protein"] == 0

@pytest.mark.parametrize("ingredients", [
    {},  # brak składników
    {"cukier": 0},  # składnik o zerowej ilości
    {"mąka": 99999},  # duża ilość
])
def test_recipe_edge_ingredients(ingredients):
    r = Recipe("Edge", ingredients, 100, 1, 1, 1)
    assert isinstance(r.ingredients, dict)

@pytest.mark.parametrize("name", [
    "Śniadanie", "lunch@12", "kolacja_3", "🥗🍝🍷", "汉字"
])
def test_recipe_name_variations(name):
    r = Recipe(name, {"x": 1}, 100, 1, 1, 1)
    assert r.name == name
