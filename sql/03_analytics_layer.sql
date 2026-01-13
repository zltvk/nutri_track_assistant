-- analytics layer

CREATE VIEW v_composite_food_nutrition AS
SELECT 
    f_parent.id AS product_id,      -- ID from food_items
    f_parent.name AS product_name,  -- name from food_items
    
    -- Multiply the ingredient’s nutrients by its weight in the recipe
    ROUND(SUM((f_child.calories_100g / 100) * ri.weight_grams), 2) AS total_calories,
    ROUND(SUM((f_child.protein_100g / 100) * ri.weight_grams), 2) AS total_protein,
    ROUND(SUM((f_child.fat_100g / 100) * ri.weight_grams), 2) AS total_fat,
    ROUND(SUM((f_child.carbohydrates_100g / 100) * ri.weight_grams), 2) AS total_carbs
    
FROM food_items f_parent -- food_items as "dish"
JOIN recipe_ingredients ri ON f_parent.id = ri.parent_food_id
JOIN food_items f_child  -- food_items as "ingredient"
    ON ri.child_food_id = f_child.id

WHERE f_parent.is_composite = TRUE 
GROUP BY f_parent.id, f_parent.name;

CREATE VIEW v_simple_food_nutrition AS
SELECT 
    food_items.id AS product_id,      -- ID from food_items
    food_items.name AS product_name,  -- name from food_items
    
    -- Direct values for simple products
    food_items.calories_100g  AS total_calories,
    food_items.protein_100g AS total_protein,
    food_items.fat_100g AS total_fat,
    food_items.carbohydrates_100g AS total_carbs
    
FROM food_items -- food_items as "product"

WHERE food_items.is_composite = FALSE;

CREATE VIEW v_all_foods_unified AS
SELECT product_id, product_name, total_calories, total_protein, total_fat, total_carbs 
FROM v_composite_food_nutrition
UNION ALL
SELECT product_id, product_name, total_calories, total_protein, total_fat, total_carbs 
FROM v_simple_food_nutrition;


CREATE VIEW v_daily_consumption_analytics AS
SELECT 
    u.id AS user_id,
    u.username,
    cl.consumed_at,
    f.product_name,
    cl.weight_consumed AS portion_grams,
    -- Calculations for Portions
    ROUND((f.total_calories / 100) * cl.weight_consumed, 2) AS calories_gained,
    ROUND((f.total_protein / 100) * cl.weight_consumed, 2) AS protein_gained,
    ROUND((f.total_fat / 100) * cl.weight_consumed, 2) AS fat_gained,
    ROUND((f.total_carbs / 100) * cl.weight_consumed, 2) AS carbs_gained
FROM consumption_log cl
JOIN users u ON cl.user_id = u.id
JOIN v_all_foods_unified f ON cl.food_item_id = f.product_id;