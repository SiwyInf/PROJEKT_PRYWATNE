from typing import Dict

class Recipe:
    def __init__(self, name: str, ingredients: Dict[str, float], kcal: int, protein: int, fat: int, carbs: int):
        if not name or kcal < 0 or protein < 0 or fat < 0 or carbs < 0:
            raise ValueError("Invalid nutritional values or name")
        self.name = name
        self.ingredients = ingredients
        self.kcal = kcal
        self.protein = protein
        self.fat = fat
        self.carbs = carbs

    def total_nutrients(self) -> Dict[str, int]:
        return {
            "kcal": self.kcal,
            "protein": self.protein,
            "fat": self.fat,
            "carbs": self.carbs
        }
