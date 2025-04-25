from typing import Dict
from mealplan import MealPlan

def generate_shopping_list(meal_plan: MealPlan) -> Dict[str, float]:
    shopping_list: Dict[str, float] = {}
    for meals in meal_plan.plan.values():
        for recipe in meals:
            for ingredient, quantity in recipe.ingredients.items():
                if ingredient in shopping_list:
                    shopping_list[ingredient] += quantity
                else:
                    shopping_list[ingredient] = quantity
    return shopping_list
