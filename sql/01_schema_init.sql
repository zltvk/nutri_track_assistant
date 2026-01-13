-- creating database 
CREATE DATABASE nutri_track_db;
USE nutri_track_db;

CREATE TABLE food_items(
id INT UNSIGNED AUTO_INCREMENT, 
name VARCHAR (150) NOT NULL,
is_composite BOOLEAN, -- True if it has ingredients
calories_100g FLOAT,
protein_100g FLOAT,
fat_100g FLOAT,
carbohydrates_100g FLOAT,
salt_100g FLOAT,
sugar_100g FLOAT,
CONSTRAINT PK_food_items PRIMARY KEY(id));

CREATE TABLE recipe_ingredients(
parent_food_id INT UNSIGNED, 
child_food_id INT UNSIGNED, 
weight_grams FLOAT, 
CONSTRAINT PK_recipe_ingredients PRIMARY KEY(parent_food_id, child_food_id), 
CONSTRAINT FK_recipe_ingredients_parent FOREIGN KEY(parent_food_id) REFERENCES food_items(id),  
CONSTRAINT FK_recipe_ingredients_child FOREIGN KEY(child_food_id) REFERENCES food_items(id)
);  

CREATE TABLE users(
id INT UNSIGNED AUTO_INCREMENT, 
username VARCHAR(150) NOT NULL,
target_calories INT UNSIGNED,
CONSTRAINT PK_users PRIMARY KEY(id)
);

CREATE TABLE consumption_log(
id INT UNSIGNED AUTO_INCREMENT,
user_id INT UNSIGNED NOT NULL, 
food_item_id INT UNSIGNED NOT NULL, 
weight_consumed FLOAT, 
consumed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
CONSTRAINT PK_consumption_log PRIMARY KEY(id), 
CONSTRAINT FK_consumption_log_user_id FOREIGN KEY(user_id) REFERENCES users(id), 
CONSTRAINT FK_consumption_log_food_item_id FOREIGN KEY(food_item_id) REFERENCES food_items(id)
);




