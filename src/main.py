# Imports
from db_handler import get_connection, add_food_item, add_recipe_ingredient, get_food_id_by_name, get_daily_report, log_consumption, get_user_goals
from chart import plot_nutrition, plot_calories_status

# Decorator: input error

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me valid information."
        except Exception:
            return "Something went wrong"
    return inner    

# Decorator: empty input

def get_non_empty_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print("The field is empty. Try again!")

# Parse user's command

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

# Is_composite verifying

def is_composite_verifying(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input == 'yes':
            return True
        elif user_input == 'no':
            return False
        else:
            print("Not valid command. Try again!")


# Handle all command

def main():
    db_connection = get_connection()
    if db_connection is None:
        return
    print("Welcome to the assistant bot!")
    while True:
        command, *args = parse_input(input("Enter a command: "))

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add-food":
            
            name = get_non_empty_input('Enter the food name:')
            
            is_composite = is_composite_verifying('Is this composite dish with ingredients? (yes/no):')

            if is_composite:
                add_food_item(name, 0, 0, 0, 0, is_composite=True)
                print(f"Composite dish '{name}' created! Now you can add ingredients to it using 'add-recipe'.")
                continue
            try:
                calories = float(get_non_empty_input("Enter calories (per 100g): "))
                protein = float(get_non_empty_input("Enter protein: "))
                fat = float(get_non_empty_input("Enter fat: "))
                carbs = float(get_non_empty_input("Enter carbohydrates: "))

                add_food_item(name, calories, protein, fat, carbs, is_composite=False)
                print(f"Product '{name}' added successfully!")
            except ValueError:
                print("Error: Nutrients must be numbers (e.g. 50.5). Try again!")

        elif command == "add-recipe":
            parent_name = get_non_empty_input("Enter the name of the composite dish: ")
            parent_id = get_food_id_by_name(parent_name)
            
            if not parent_id:
                print(f"Dish '{parent_name}' not found. Create it first using 'add-food'.")
                continue

            child_name = get_non_empty_input(f"Enter ingredient name for {parent_name}: ")
            child_id = get_food_id_by_name(child_name)
            
            if not child_id:
                print(f"Ingredient '{child_name}' not found. Add it to the database first.")
                continue

            try:
                weight = float(get_non_empty_input(f"How many grams of '{child_name}' in '{parent_name}'?: "))
                add_recipe_ingredient(parent_id, child_id, weight)
                print(f"Added {weight}g of {child_name} to {parent_name}!")
            except ValueError:
                print("Error: Weight must be a number.")
        
        elif command == "eat":
            food_name = get_non_empty_input("What did you eat?: ")
            food_id = get_food_id_by_name(food_name)
            
            if not food_id:
                print(f"Food '{food_name}' not found. Add it to the database first.")
                continue

            try:
                weight = float(get_non_empty_input(f"How many grams of '{food_name}'?: "))
                log_consumption(1, food_id, weight) 
                print(f"Logged {weight}g of {food_name}!")
            except ValueError:
                print("Error: Weight must be a number.")    
        
        elif command == "report":
            # Fetch today's data for the main user (ID = 1)
            rows = get_daily_report(1)
            
            if not rows:
                print("No consumption records found for today.")
                continue

            print("\n" + "="*45)
            print(f"{'PRODUCT':<20} | {'GRAMS':<7} | {'KCAL':<8}")
            print("-" * 45)


            total_kcal = 0
            total_p = 0
            total_f = 0
            total_c = 0

            for row in rows:
                name = row['product_name']
                weight = row['portion_grams']
                kcal = float(row['calories_gained'])
                
                total_kcal += kcal
                total_p += float(row['protein_gained'])
                total_f += float(row['fat_gained'])
                total_c += float(row['carbs_gained'])
                
                print(f"{name:<20} | {weight:<7.1f} | {kcal:<8.2f}")
            
            print("-" * 45)
            print(f"TOTAL CALORIES: {total_kcal:.2f} kcal")
            print(f"P: {total_p:.1f}g | F: {total_f:.1f}g | C: {total_c:.1f}g")
            print("="*45 + "\n")

        elif command == "chart":
            # Logic for visualizing the data using Matplotlib
            rows = get_daily_report(1)
            if rows:
                p = sum(float(r['protein_gained']) for r in rows)
                f = sum(float(r['fat_gained']) for r in rows)
                c = sum(float(r['carbs_gained']) for r in rows)
                
                # Check if there is data to plot (prevent division by zero)
                if p + f + c > 0:
                    plot_nutrition(p, f, c)
                else:
                    print("No macronutrients to display on chart.")
            else:
                print("No data available for today to generate a chart.")
    
        elif command == "status":
            # 1. Get the user's calorie goal
            user_goals = get_user_goals(1)
            target = float(user_goals['target_calories']) if user_goals else 2000.0 # Fallback to 2000

            # 2. Get today's total calories
            rows = get_daily_report(1)
            current = sum(float(row['calories_gained']) for row in rows) if rows else 0.0

            # 3. Print text summary
            remaining = target - current
            status_msg = "within limit" if remaining >= 0 else "exceeded"
            
            print(f"\n--- Calorie Status ---")
            print(f"Goal: {target} kcal")
            print(f"Current: {current:.2f} kcal")
            print(f"Remaining: {abs(remaining):.2f} kcal ({status_msg})")
            print("-" * 22)

            # 4. Trigger the comparison chart
            plot_calories_status(target, current)
        
        else:
            print("Invalid command.")
            continue


if __name__ == "__main__":
    main()
