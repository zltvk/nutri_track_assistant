-- add products (is_composite = False)
INSERT INTO food_items (name, is_composite, calories_100g, protein_100g, fat_100g, carbohydrates_100g) 
VALUES 
('Eggs', FALSE, 155, 13, 11, 1.1),
('Mushrooms', FALSE, 22, 3.1, 0.3, 3.3),
('Chicken Breast', FALSE, 165, 31, 3.6, 0);

-- add dish (is_composite = True)
INSERT INTO food_items (name, is_composite) 
VALUES ('Mushroom Omelette', TRUE);

-- complete the recipe 
INSERT INTO recipe_ingredients (parent_food_id, child_food_id, weight_grams)
VALUES 
(4, 1, 100), -- 2 eggs = 100g
(4, 2, 50);  -- mushrooms 50g

-- add user for testing 
INSERT INTO users(username, target_calories) VALUES('Adam', 2800);

-- add to consumption log

INSERT INTO consumption_log(user_id, food_item_id, weight_consumed) VALUES
(1, 4, 200);


