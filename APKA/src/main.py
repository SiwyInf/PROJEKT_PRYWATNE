from recipe import Recipe
from mealplan import MealPlan
from shoppinglist import generate_shopping_list

def main():
    r1 = Recipe("Kanapka", {"chleb": 2, "szynka": 1}, 300, 15, 10, 30)
    r2 = Recipe("Jajecznica", {"jajka": 3, "masło": 1}, 400, 20, 25, 5)

    plan = MealPlan()
    plan.add_meal("Monday", r1)
    plan.add_meal("Monday", r2)

    print("Podsumowanie poniedziałku:")
    print(plan.daily_summary("Monday"))

    print("\nLista zakupów:")
    print(generate_shopping_list(plan))

if __name__ == "__main__":
    main()
