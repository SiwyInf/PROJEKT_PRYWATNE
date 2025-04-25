from mealplan import MealPlan
from recipe import Recipe
from shoppinglist import generate_shopping_list
import pytest

@pytest.mark.parametrize("recipes,expected", [
    (
        [
            Recipe("Test1", {"milk": 200}, 100, 5, 3, 10),
            Recipe("Test2", {"milk": 100, "bread": 2}, 150, 6, 4, 20),
        ],
        {"milk": 300, "bread": 2}
    ),
    (
        [
            Recipe("Test3", {"apple": 1}, 50, 1, 0, 12),
        ],
        {"apple": 1}
    ),
    (
        [
            Recipe("Test4", {"rice": 100}, 200, 4, 2, 45),
            Recipe("Test5", {"rice": 150, "chicken": 200}, 400, 30, 10, 0),
        ],
        {"rice": 250, "chicken": 200}
    ),
    (
        [
            Recipe("Combo", {"tomato": 100, "cheese": 50}, 200, 10, 8, 12),
            Recipe("Salad", {"tomato": 50, "lettuce": 100}, 100, 2, 1, 5),
        ],
        {"tomato": 150, "cheese": 50, "lettuce": 100}
    )
])
def test_generate_shopping_list_param(recipes, expected):
    plan = MealPlan()
    for r in recipes:
        plan.add_meal("Monday", r)
    result = generate_shopping_list(plan)
    assert result == expected

def test_shopping_list_multiple_days():
    plan = MealPlan()
    plan.add_meal("Monday", Recipe("A", {"milk": 100}, 100, 5, 3, 10))
    plan.add_meal("Tuesday", Recipe("B", {"milk": 150, "bread": 1}, 150, 6, 4, 20))
    result = generate_shopping_list(plan)
    assert result == {"milk": 250, "bread": 1}

def test_empty_mealplan_returns_empty_shopping_list():
    plan = MealPlan()
    result = generate_shopping_list(plan)
    assert result == {}

def test_single_ingredient_recipe():
    plan = MealPlan()
    plan.add_meal("Wednesday", Recipe("Simple", {"egg": 1}, 90, 6, 5, 1))
    result = generate_shopping_list(plan)
    assert result == {"egg": 1}

def test_shopping_list_ingredient_with_zero_quantity():
    plan = MealPlan()
    r = Recipe("WaterOnly", {"water": 0}, 0, 0, 0, 0)
    plan.add_meal("Monday", r)
    result = generate_shopping_list(plan)
    assert result["water"] == 0

def test_shopping_list_with_duplicated_ingredients():
    plan = MealPlan()
    r1 = Recipe("Meal1", {"flour": 100}, 300, 10, 5, 50)
    r2 = Recipe("Meal2", {"flour": 200}, 400, 12, 6, 60)
    plan.add_meal("Sunday", r1)
    plan.add_meal("Sunday", r2)
    result = generate_shopping_list(plan)
    assert result["flour"] == 300

def test_shopping_list_with_overlapping_ingredients():
    plan = MealPlan()
    plan.add_meal("Monday", Recipe("A", {"x": 1, "y": 2}, 100, 2, 1, 1))
    plan.add_meal("Tuesday", Recipe("B", {"x": 3, "z": 4}, 100, 2, 1, 1))
    result = generate_shopping_list(plan)
    assert result["x"] == 4
    assert result["y"] == 2
    assert result["z"] == 4

def test_shopping_list_with_unicode_ingredients():
    plan = MealPlan()
    plan.add_meal("Friday", Recipe("EmojiMeal", {"🍎": 2, "🥦": 1}, 100, 2, 2, 2))
    result = generate_shopping_list(plan)
    assert result["🍎"] == 2
    assert result["🥦"] == 1

def test_shopping_list_with_float_quantity():
    plan = MealPlan()
    r = Recipe("FloatMeal", {"oliwa": 12.5}, 200, 2, 20, 0)
    plan.add_meal("Monday", r)
    result = generate_shopping_list(plan)
    assert result["oliwa"] == 12.5

def test_shopping_list_with_many_items():
    plan = MealPlan()
    r = Recipe("BigMeal", {f"item{i}": i for i in range(10)}, 500, 10, 10, 10)
    plan.add_meal("Monday", r)
    result = generate_shopping_list(plan)
    assert len(result) == 10
