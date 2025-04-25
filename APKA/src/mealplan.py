from typing import Dict, List
from recipe import Recipe

class MealPlan:
    def __init__(self):
        self.plan: Dict[str, List[Recipe]] = {day: [] for day in [
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

    def add_meal(self, day: str, meal: Recipe):
        if day not in self.plan:
            raise ValueError("Invalid day")
        self.plan[day].append(meal)

    def daily_summary(self, day: str) -> Dict[str, int]:
        if day not in self.plan:
            raise ValueError("Invalid day")
        total = {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}
        for recipe in self.plan[day]:
            nutrients = recipe.total_nutrients()
            for key in total:
                total[key] += nutrients[key]
        return total
