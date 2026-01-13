import matplotlib.pyplot as plt

def plot_nutrition(p, f, c):
    labels = [f'Proteins ({p}g)', f'Fats ({f}g)', f'Carbs ({c}g)']
    values = [p, f, c]
    colors = ['#ff9999','#66b3ff','#99ff99']
    
    plt.figure(figsize=(7, 7))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.title("Daily Macronutrients Ratio")
    plt.show()

def plot_calories_status(target, current):
    """Visualizes Goal vs Actual calorie intake."""
    labels = ['Target Goal', 'Current Intake']
    values = [target, current]
    colors = ['#cccccc', '#4CAF50' if current <= target else '#f44336'] # Green if within limit, Red if over

    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, values, color=colors)
    
    # Add text labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 20, f"{yval:.0f} kcal", ha='center', va='bottom', fontweight='bold')

    plt.title("Daily Calorie Intake: Goal vs Actual", fontsize=14)
    plt.ylabel("Calories (kcal)")
    plt.ylim(0, max(target, current) * 1.2) # Add some space at the top
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()