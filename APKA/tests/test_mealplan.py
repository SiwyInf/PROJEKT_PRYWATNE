import pytest
from mealplan import MealPlan
from recipe import Recipe

@pytest.fixture
def basic_recipe():
    return Recipe("Toast", {"bread": 2}, 150, 5, 2, 20)

@pytest.mark.parametrize("day", [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
])
def test_add_meal_and_summary_all_days(day, basic_recipe):
    plan = MealPlan()
    plan.add_meal(day, basic_recipe)
    summary = plan.daily_summary(day)
    assert summary["kcal"] == 150
    assert summary["protein"] == 5

@pytest.mark.parametrize("day", ["Funday", "Yesterday", "" ])
def test_invalid_day_add(day, basic_recipe):
    plan = MealPlan()
    with pytest.raises(ValueError):
        plan.add_meal(day, basic_recipe)

@pytest.mark.parametrize("day,recipes", [
    ("Monday", [Recipe("A", {"x": 1}, 100, 10, 5, 5), Recipe("B", {"y": 2}, 200, 20, 10, 10)]),
    ("Tuesday", [Recipe("C", {"z": 3}, 150, 15, 7, 7)]),
    ("Wednesday", [Recipe("D", {"a": 1}, 80, 8, 4, 3), Recipe("E", {"b": 2}, 120, 10, 5, 5)]),
    ("Thursday", [Recipe("F", {"c": 1}, 300, 25, 12, 15)]),
    ("Friday", [Recipe("G", {"d": 2}, 180, 12, 9, 8)]),
    ("Saturday", [Recipe("H", {"e": 1}, 90, 5, 2, 6)]),
    ("Sunday", [Recipe("I", {"f": 3}, 250, 20, 15, 10)])
])
def test_multiple_days_summary(day, recipes):
    plan = MealPlan()
    for r in recipes:
        plan.add_meal(day, r)
    total_kcal = sum(r.kcal for r in recipes)
    total_protein = sum(r.protein for r in recipes)
    summary = plan.daily_summary(day)
    assert summary["kcal"] == total_kcal
    assert summary["protein"] == total_protein
def test_none_day_meal_add_raises():
    plan = MealPlan()
    recipe = Recipe("Test", {"bread": 1}, 100, 5, 2, 10)
    with pytest.raises(ValueError):
        plan.add_meal(None, recipe)

def test_adding_100_recipes_in_one_day():
    plan = MealPlan()
    for i in range(100):
        r = Recipe(f"R{i}", {"thing": 1}, 10, 1, 1, 1)
        plan.add_meal("Monday", r)
    summary = plan.daily_summary("Monday")
    assert summary["kcal"] == 1000

def test_mealplan_with_empty_days():
    plan = MealPlan()
    for day in ["Monday", "Tuesday", "Wednesday"]:
        plan.plan[day] = []  # jawnie pusto
        assert plan.daily_summary(day) == {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}

def test_mealplan_adding_same_recipe_multiple_times():
    plan = MealPlan()
    r = Recipe("Repeat", {"x": 1}, 100, 5, 5, 5)
    for _ in range(10):
        plan.add_meal("Friday", r)
    summary = plan.daily_summary("Friday")
    assert summary["kcal"] == 1000

def test_mealplan_adding_same_meal_different_days():
    plan = MealPlan()
    r = Recipe("Multi", {"a": 1}, 100, 10, 1, 1)
    for day in plan.plan.keys():
        plan.add_meal(day, r)
    for day in plan.plan:
        assert plan.daily_summary(day)["kcal"] == 100

def test_mealplan_100_meals_summary_correct():
    plan = MealPlan()
    r = Recipe("R", {"z": 1}, 10, 1, 1, 1)
    for _ in range(100):
        plan.add_meal("Monday", r)
    assert plan.daily_summary("Monday")["kcal"] == 1000

def test_mealplan_summary_multiple_recipes_varied():
    plan = MealPlan()
    r1 = Recipe("L1", {"a": 1}, 50, 2, 1, 5)
    r2 = Recipe("L2", {"b": 1}, 100, 3, 1, 10)
    plan.add_meal("Wednesday", r1)
    plan.add_meal("Wednesday", r2)
    summary = plan.daily_summary("Wednesday")
    assert summary["kcal"] == 150
    assert summary["protein"] == 5

def test_mealplan_summary_empty_day():
    plan = MealPlan()
    summary = plan.daily_summary("Friday")
    assert summary == {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}
