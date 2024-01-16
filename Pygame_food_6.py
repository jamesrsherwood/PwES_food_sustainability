import pygame
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

#Most data from Poore, Frankowska, but extra pasta data from https://link.springer.com/chapter/10.1007/978-3-642-41263-9_48

# Initialize Pygame
pygame.init()
data_screen = True

# Constants
WIDTH, HEIGHT = 1200, 750  # window size
FPS = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 220, 0)
BLACK = (0, 0, 0)
PURPLE = (100,30,225)

# health and impact bar position
bar_x = 750 #start pos
bar_l = 250 #length

#food grid sizing
w = 30 #start width
h = 385 #start height
col = 120 #column space
row = 30 #row space

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sustainable food game")
clock = pygame.time.Clock()

# Game variables
selected_foods = {}
food_data = {
    "Lamb": {"quantity": 90, "calories": 264.6, "fibre": 0, "protein": 18.009, "portions_fruit_veg": 0, "climate_change": 4.45, "land_use": 33.28, "water_use": 163, "NU_cal": 0.872, "NU_fibre": 0, "NU_protein": 1.886, "NU_veg": 0},
    "Beef": {"quantity": 90, "calories": 249.3, "fibre": 0, "protein": 17.946, "portions_fruit_veg": 0, "climate_change": 9.83, "land_use": 29.36, "water_use": 131, "NU_cal": 0.821, "NU_fibre": 0, "NU_protein": 1.88, "NU_veg": 0},
    "Pork": {"quantity": 90, "calories": 229.5, "fibre": 0, "protein": 14.562, "portions_fruit_veg": 0, "climate_change": 1.94, "land_use": 1.57, "water_use": 162, "NU_cal": 0.756, "NU_fibre": 0, "NU_protein": 1.525, "NU_veg": 0},
    "Chicken": {"quantity": 90, "calories": 215.1, "fibre": 0, "protein": 15.588, "portions_fruit_veg": 0, "climate_change": 1.65, "land_use": 1.1, "water_use": 60, "NU_cal": 0.709, "NU_fibre": 0, "NU_protein": 1.633, "NU_veg": 0},
    "Egg": {"quantity": 120, "calories": 186, "fibre": 0, "protein": 13.3152, "portions_fruit_veg": 0, "climate_change": 0.64, "land_use": 0.76, "water_use": 70, "NU_cal": 0.46, "NU_fibre": 0, "NU_protein": 1.046, "NU_veg": 0},
    "Milk": {"quantity": 200, "calories": 124, "fibre": 0, "protein": 6.6, "portions_fruit_veg": 0, "climate_change": 0.61, "land_use": 1.74, "water_use": 122, "NU_cal": 0.184, "NU_fibre": 0, "NU_protein": 0.311, "NU_veg": 0},
    "Cheese": {"quantity": 30, "calories": 100.2, "fibre": 0, "protein": 6.24, "portions_fruit_veg": 0, "climate_change": 0.72, "land_use": 2.63, "water_use": 168, "NU_cal": 0.99, "NU_fibre": 0, "NU_protein": 1.961, "NU_veg": 0},
    "Salmon": {"quantity": 134, "calories": 170.18, "fibre": 0, "protein": 27.47, "portions_fruit_veg": 0, "climate_change": 1.91, "land_use": 1.13, "water_use": 495, "NU_cal": 0.377, "NU_fibre": 0, "NU_protein": 1.932, "NU_veg": 0},
    "Prawns": {"quantity": 120, "calories": 102, "fibre": 0, "protein": 25.2, "portions_fruit_veg": 0, "climate_change": 3.28, "land_use": 0.36, "water_use": 422, "NU_cal": 0.252, "NU_fibre": 0, "NU_protein": 1.979, "NU_veg": 0},
    "Beans": {"quantity": 80, "calories": 23.2, "fibre": 1.92, "protein": 1.92, "portions_fruit_veg": 1, "climate_change": 0.09, "land_use": 0.13, "water_use": 76, "NU_cal": 0.086, "NU_fibre": 0.909, "NU_protein": 0.226, "NU_veg": 2.309},
    "Peas": {"quantity": 75, "calories": 60.75, "fibre": 4.275, "protein": 3.75, "portions_fruit_veg": 0.9375, "climate_change": 0.17, "land_use": 0.56, "water_use": 30, "NU_cal": 0.24, "NU_fibre": 2.158, "NU_protein": 0.471, "NU_veg": 2.309},
    "Tofu": {"quantity": 105, "calories": 152.25, "fibre": 0.63, "protein": 13.335, "portions_fruit_veg": 0, "climate_change": 0.47, "land_use": 0.37, "water_use": 16, "NU_cal": 0.43, "NU_fibre": 0.227, "NU_protein": 1.197, "NU_veg": 0},
    "Soymilk": {"quantity": 250, "calories": 132.5, "fibre": 0, "protein": 8.5, "portions_fruit_veg": 0, "climate_change": 0.25, "land_use": 0.15, "water_use": 7, "NU_cal": 0.157, "NU_fibre": 0, "NU_protein": 0.32, "NU_veg": 0},
    "Lentils": {"quantity": 150, "calories": 174, "fibre": 16.05, "protein": 32.115, "portions_fruit_veg": 1.875, "climate_change": 0.5, "land_use": 2.34, "water_use": 66, "NU_cal": 0.344, "NU_fibre": 4.052, "NU_protein": 2.018, "NU_veg": 2.309},
    "Peanuts": {"quantity": 30, "calories": 170.1, "fibre": 2.55, "protein": 7.854, "portions_fruit_veg": 0, "climate_change": 0.1, "land_use": 0.27, "water_use": 56, "NU_cal": 1.681, "NU_fibre": 3.219, "NU_protein": 2.468, "NU_veg": 0},
    "Cashews": {"quantity": 30, "calories": 165.9, "fibre": 0.9, "protein": 5.4, "portions_fruit_veg": 0, "climate_change": 0.01, "land_use": 0.39, "water_use": 124, "NU_cal": 1.639, "NU_fibre": 1.136, "NU_protein": 1.697, "NU_veg": 0},
    "Walnuts": {"quantity": 30, "calories": 196.2, "fibre": 2.01, "protein": 4.5, "portions_fruit_veg": 0, "climate_change": 0.01, "land_use": 0.39, "water_use": 124, "NU_cal": 1.939, "NU_fibre": 2.537, "NU_protein": 1.414, "NU_veg": 0},
    "Carrots": {"quantity": 80, "calories": 32.8, "fibre": 2.24, "protein": 0.744, "portions_fruit_veg": 1, "climate_change": 0.03, "land_use": 0.02, "water_use": 2, "NU_cal": 0.122, "NU_fibre": 1.06, "NU_protein": 0.088, "NU_veg": 2.309},
    "Onions": {"quantity": 59, "calories": 23.6, "fibre": 1.003, "protein": 0.649, "portions_fruit_veg": 0.7375, "climate_change": 0.11, "land_use": 0.02, "water_use": 1, "NU_cal": 0.119, "NU_fibre": 0.644, "NU_protein": 0.104, "NU_veg": 2.309},
    "Lettuce": {"quantity": 80, "calories": 12, "fibre": 0.96, "protein": 1.12, "portions_fruit_veg": 1, "climate_change": 0, "land_use": 0.01, "water_use": 7, "NU_cal": 0.044, "NU_fibre": 0.454, "NU_protein": 0.132, "NU_veg": 2.309},
    "Peppers": {"quantity": 80, "calories": 20.8, "fibre": 1.68, "protein": 0.792, "portions_fruit_veg": 1, "climate_change": 0.01, "land_use": 0.01, "water_use": 26, "NU_cal": 0.077, "NU_fibre": 0.795, "NU_protein": 0.093, "NU_veg": 2.309},
    "Sweetcorn": {"quantity": 80, "calories": 68.8, "fibre": 1.6, "protein": 2.616, "portions_fruit_veg": 1, "climate_change": 0.08, "land_use": 0.04, "water_use": 8, "NU_cal": 0.255, "NU_fibre": 0.757, "NU_protein": 0.308, "NU_veg": 2.309},
    "Cauliflower": {"quantity": 80, "calories": 20, "fibre": 1.6, "protein": 1.52, "portions_fruit_veg": 1, "climate_change": 0.18, "land_use": 0.05, "water_use": 10, "NU_cal": 0.074, "NU_fibre": 0.757, "NU_protein": 0.179, "NU_veg": 2.309},
    "Broccoli": {"quantity": 80, "calories": 27.2, "fibre": 2.08, "protein": 2.256, "portions_fruit_veg": 1, "climate_change": 0.115, "land_use": 0.05, "water_use": 10, "NU_cal": 0.101, "NU_fibre": 0.985, "NU_protein": 0.266, "NU_veg": 2.309},
    "Spinach": {"quantity": 80, "calories": 18.4, "fibre": 1.76, "protein": 2.32, "portions_fruit_veg": 1, "climate_change": 0.03, "land_use": 0, "water_use": 8, "NU_cal": 0.068, "NU_fibre": 0.833, "NU_protein": 0.273, "NU_veg": 2.309},
    "Tomatoes": {"quantity": 80, "calories": 14.4, "fibre": 0.96, "protein": 0.72, "portions_fruit_veg": 1, "climate_change": 0.17, "land_use": 0.06, "water_use": 30, "NU_cal": 0.053, "NU_fibre": 0.454, "NU_protein": 0.085, "NU_veg": 2.309},
    "Brussel sprouts": {"quantity": 80, "calories": 34.4, "fibre": 3.04, "protein": 2.704, "portions_fruit_veg": 1, "climate_change": 0.1, "land_use": 0.01, "water_use": 8, "NU_cal": 0.127, "NU_fibre": 1.439, "NU_protein": 0.319, "NU_veg": 2.309},
    "Cucumber": {"quantity": 80, "calories": 12.4, "fibre": 0.56, "protein": 0.56, "portions_fruit_veg": 1, "climate_change": 0, "land_use": 0, "water_use": 7, "NU_cal": 0.046, "NU_fibre": 0.265, "NU_protein": 0.066, "NU_veg": 2.309},
    "Apples": {"quantity": 80, "calories": 41.6, "fibre": 1.92, "protein": 0.24, "portions_fruit_veg": 1, "climate_change": 0.03, "land_use": 0.05, "water_use": 14, "NU_cal": 0.154, "NU_fibre": 0.909, "NU_protein": 0.028, "NU_veg": 2.309},
    "Oranges": {"quantity": 80, "calories": 37.6, "fibre": 1.92, "protein": 0.72, "portions_fruit_veg": 1, "climate_change": 0.03, "land_use": 0.07, "water_use": 7, "NU_cal": 0.139, "NU_fibre": 0.909, "NU_protein": 0.085, "NU_veg": 2.309},
    "Strawberries": {"quantity": 80, "calories": 26.4, "fibre": 1.6, "protein": 0.56, "portions_fruit_veg": 1, "climate_change": 0.12, "land_use": 0.19, "water_use": 34, "NU_cal": 0.098, "NU_fibre": 0.757, "NU_protein": 0.066, "NU_veg": 2.309},
    "Grapefruits": {"quantity": 80, "calories": 25.6, "fibre": 0.88, "protein": 0.48, "portions_fruit_veg": 1, "climate_change": 0.03, "land_use": 0.07, "water_use": 7, "NU_cal": 0.095, "NU_fibre": 0.417, "NU_protein": 0.057, "NU_veg": 2.309},
    "Lemons": {"quantity": 80, "calories": 23.2, "fibre": 2.24, "protein": 0.88, "portions_fruit_veg": 1, "climate_change": 0.03, "land_use": 0.07, "water_use": 7, "NU_cal": 0.086, "NU_fibre": 1.06, "NU_protein": 0.104, "NU_veg": 2.309},
    "Raspberries": {"quantity": 80, "calories": 41.6, "fibre": 5.2, "protein": 0.96, "portions_fruit_veg": 1, "climate_change": 0.12, "land_use": 0.19, "water_use": 34, "NU_cal": 0.154, "NU_fibre": 2.461, "NU_protein": 0.113, "NU_veg": 2.309},
    "Grapes": {"quantity": 80, "calories": 53.6, "fibre": 0.72, "protein": 0.48, "portions_fruit_veg": 1, "climate_change": 0.12, "land_use": 0.19, "water_use": 34, "NU_cal": 0.199, "NU_fibre": 0.341, "NU_protein": 0.057, "NU_veg": 2.309},
    "Pineapples": {"quantity": 80, "calories": 40, "fibre": 1.12, "protein": 0.4, "portions_fruit_veg": 1, "climate_change": 0.01, "land_use": 0.04, "water_use": 26, "NU_cal": 0.148, "NU_fibre": 0.53, "NU_protein": 0.047, "NU_veg": 2.309},
    "Melons": {"quantity": 80, "calories": 27.2, "fibre": 7.2, "protein": 0.64, "portions_fruit_veg": 1, "climate_change": 0.01, "land_use": 0.01, "water_use": 26, "NU_cal": 0.101, "NU_fibre": 3.408, "NU_protein": 0.075, "NU_veg": 2.309},
    "Avocados": {"quantity": 80, "calories": 128, "fibre": 5.36, "protein": 1.6, "portions_fruit_veg": 1, "climate_change": 0.01, "land_use": 0.14, "water_use": 26, "NU_cal": 0.474, "NU_fibre": 2.537, "NU_protein": 0.189, "NU_veg": 2.309},
    "Bananas": {"quantity": 80, "calories": 71.2, "fibre": 2.08, "protein": 0.88, "portions_fruit_veg": 1, "climate_change": 0.07, "land_use": 0.15, "water_use": 9, "NU_cal": 0.264, "NU_fibre": 0.985, "NU_protein": 0.104, "NU_veg": 2.309},
    "Bread": {"quantity": 88, "calories": 209.44, "fibre": 8.096, "protein": 9.416, "portions_fruit_veg": 0, "climate_change": 0.14, "land_use": 0.34, "water_use": 57, "NU_cal": 0.706, "NU_fibre": 3.484, "NU_protein": 1.009, "NU_veg": 0},
    "Potatoes": {"quantity": 180, "calories": 131.76, "fibre": 3.78, "protein": 3.6, "portions_fruit_veg": 0, "climate_change": 0.3, "land_use": 0.16, "water_use": 12, "NU_cal": 0.217, "NU_fibre": 0.795, "NU_protein": 0.189, "NU_veg": 0},
    "Rice": {"quantity": 75, "calories": 276.45, "fibre": 5.025, "protein": 2.025, "portions_fruit_veg": 0, "climate_change": 0.48, "land_use": 0.21, "water_use": 169, "NU_cal": 1.093, "NU_fibre": 2.537, "NU_protein": 0.255, "NU_veg": 0},
    "Pasta": {"quantity": 75, "calories": 292.5, "fibre": 3, "protein": 9.75, "portions_fruit_veg": 0, "climate_change": 0.22, "land_use": 0.82, "water_use": 120, "NU_cal": 1.156, "NU_fibre": 1.515, "NU_protein": 1.225, "NU_veg": 0},
    "Oats": {"quantity": 40, "calories": 104.92, "fibre": 4.04, "protein": 0.56, "portions_fruit_veg": 0, "climate_change": 0.19, "land_use": 0.3, "water_use": 19, "NU_cal": 0.778, "NU_fibre": 3.824, "NU_protein": 0.132, "NU_veg": 0},
    "Beer": {"quantity": 560, "calories": 229.6, "fibre": 0, "protein": 2.016, "portions_fruit_veg": 0, "climate_change": 0.65, "land_use": 0.62, "water_use": 9, "NU_cal": 0.122, "NU_fibre": 0, "NU_protein": 0.034, "NU_veg": 0},
    "Wine": {"quantity": 200, "calories": 170, "fibre": 0, "protein": 0.14, "portions_fruit_veg": 0, "climate_change": 0.33, "land_use": 0.32, "water_use": 15, "NU_cal": 0.252, "NU_fibre": 0, "NU_protein": 0.007, "NU_veg": 0},
    "Dark chocolate": {"quantity": 45, "calories": 269.1, "fibre": 4.905, "protein": 3.5055, "portions_fruit_veg": 0, "climate_change": 2.1, "land_use": 3.11, "water_use": 24, "NU_cal": 1.773, "NU_fibre": 4.127, "NU_protein": 0.734, "NU_veg": 0},
    "Cane sugar": {"quantity": 12.5, "calories": 48.375, "fibre": 0, "protein": 0, "portions_fruit_veg": 0, "climate_change": 0.04, "land_use": 0.03, "water_use": 8, "NU_cal": 1.147, "NU_fibre": 0, "NU_protein": 0, "NU_veg": 0},
    "Rapeseed oil": {"quantity": 11, "calories": 97.24, "fibre": 0, "protein": 0, "portions_fruit_veg": 0, "climate_change": 0.04, "land_use": 0.11, "water_use": 2, "NU_cal": 2.621, "NU_fibre": 0, "NU_protein": 0, "NU_veg": 0},
    "Olive oil": {"quantity": 11, "calories": 97.24, "fibre": 0, "protein": 0, "portions_fruit_veg": 0, "climate_change": 0.06, "land_use": 0.31, "water_use": 4, "NU_cal": 2.621, "NU_fibre": 0, "NU_protein": 0, "NU_veg": 0},
}

# NHS guide
nhs_cal = 2000
nhs_fibre = 30
nhs_protein = 50
nhs_portions = 5

# Maximum values for health bars
max_calories = nhs_cal*2
max_fibre = nhs_fibre*2
max_protein = nhs_protein*2
max_portions_fruit_veg = nhs_portions*2

# Current values for health bars
total_calories = 0
total_fibre = 0
total_protein = 0
total_portions_fruit_veg = 0

# Maximum values for impact bars - gets updated later was line ~300
max_climate_change = 15
max_land_use = 3
max_water_use = 1500

# Current values for impact bars
total_climate_change = 0
total_land_use = 0
total_water_use = 0
PwES_climate = 1
PwES_land = 1
PwES_water = 1

#buttons for clearing (clear_rect) shopping list   
clear_button_rect = pygame.Rect(bar_x+80,620,100,100)
pygame.draw.rect(screen, WHITE, clear_button_rect)
clear_image = f'Desktop/VS code/Graphics/Food/clear_button.jpg'
clear_button = pygame.image.load(clear_image).convert()
clear_button = pygame.transform.scale(clear_button, (100, 100))

# Define food items and their positions
food_items = ["Lamb", "Beef", "Pork", "Chicken", "Egg", "Milk", "Cheese", "Salmon", "Prawns", "Beans", "Peas", "Tofu", "Soymilk", "Lentils", "Peanuts", "Cashews", "Walnuts", "Carrots", "Onions", "Lettuce", "Peppers", "Sweetcorn", "Cauliflower", "Broccoli", "Spinach", "Tomatoes", "Brussel sprouts", "Cucumber", "Apples", "Oranges", "Strawberries", "Grapefruits", "Lemons", "Raspberries", "Grapes", "Pineapples", "Melons", "Avocados", "Bananas", "Bread", "Potatoes", "Rice", "Pasta", "Oats", "Beer", "Wine", "Dark chocolate", "Cane sugar", "Rapeseed oil", "Olive oil", 
]

#Food images
food_images = {}
for food_item in food_items:
    image_path = f'Desktop/VS code/Graphics/Food/{food_item}.jpg'
    original_image = pygame.image.load(image_path).convert_alpha()
    # Resize the image to a fixed size 
    food_images[food_item] = pygame.transform.scale(original_image, (80, 80))

food_positions = [(w, h), (w, h+row), (w, h+2*row), (w, h+3*row), (w, h+4*row), (w, h+5*row), (w, h+6*row), (w, h+7*row), (w, h+8*row),
                  (w+col, h), (w+col, h+row), (w+col, h+2*row), (w+col, h+3*row), (w+col, h+4*row), (w+col, h+5*row), (w+col, h+6*row), (w+col, h+7*row),
                  (w+col+col, h), (w+col+col, h+row), (w+col+col, h+2*row), (w+col+col, h+3*row), (w+col+col, h+4*row), (w+col+col, h+5*row), (w+col+col, h+6*row), (w+col+col, h+36*row), (w+col+col, h+7*row), (w+col+col, h+8*row), (w+col+col, h+9*row),
                  (w+3*col, h), (w+3*col, h+row), (w+3*col, h+2*row), (w+3*col, h+3*row), (w+3*col, h+4*row), (w+3*col, h+5*row), (w+3*col, h+6*row), (w+3*col, h+7*row), (w+3*col, h+8*row), (w+3*col, h+9*row), (w+3*col, h+10*row),
                  (w+4*col, h), (w+4*col, h+row), (w+4*col, h+2*row), (w+4*col, h+3*row), (w+4*col, h+4*row), (w+4*col, h+5*row), (w+4*col, h+6*row), (w+4*col, h+7*row), (w+4*col, h+8*row), (w+4*col, h+9*row), (w+4*col, h+10*row)]
gap_height = 0  # % of the gray box height

    # Draw the health bars - with the def function this code can be recalled if needed later
def draw_health_bars():
    health_bar_width_calories = (total_calories / max_calories) * bar_l
    health_bar_width_fibre = (total_fibre / max_fibre) * bar_l
    health_bar_width_protein = (total_protein / max_protein) * bar_l
    health_bar_width_portions_fruit_veg = (total_portions_fruit_veg / max_portions_fruit_veg) * bar_l

    pygame.draw.rect(screen, GREEN, (bar_x-50, h-180+10, health_bar_width_calories, 20))  # Calories health bar
    pygame.draw.rect(screen, GREEN, (bar_x-50, h-180+40, health_bar_width_fibre, 20))  # Fibre health bar
    pygame.draw.rect(screen, GREEN, (bar_x-50, h-180+70, health_bar_width_protein, 20))  # Protein health bar
    pygame.draw.rect(screen, GREEN, (bar_x-50, h-180+100, health_bar_width_portions_fruit_veg, 20))  # Portions of Fruit and Veg health bar

#NHS guidelines
    pygame.draw.line(screen,PURPLE,(bar_x-50 + bar_l*nhs_cal/max_calories,h-180+10),(bar_x-50 + bar_l*nhs_cal/max_calories,h-180+30))
    pygame.draw.line(screen,PURPLE,(bar_x-50 + bar_l*nhs_fibre/max_fibre,h-180+40),(bar_x-50 + bar_l*nhs_fibre/max_fibre,h-180+60))
    pygame.draw.line(screen,PURPLE,(bar_x-50 + bar_l*nhs_protein/max_protein,h-180+70),(bar_x-50 + bar_l*nhs_protein/max_protein,h-180+90))
    pygame.draw.line(screen,PURPLE,(bar_x-50 + bar_l*nhs_portions/max_portions_fruit_veg,h-180+100),(bar_x-50 + bar_l*nhs_portions/max_portions_fruit_veg,h-180+120))
    pygame.draw.line(screen,PURPLE,(bar_x+75,h-230),(bar_x+75, h-250)) #line towards NHS guidance statement    
    nhs_text = food_titles_font.render("NHS guidelines", True, PURPLE) #NHS guidance statement
    screen.blit(nhs_text, (bar_x+80, h-250))
#in-between lines
    pygame.draw.line(screen,(250, 200, 250),(bar_x+75,h-230),(bar_x-50 + bar_l*nhs_cal/max_calories,h-180+10))
    pygame.draw.line(screen,(250, 200, 250),(bar_x-50 + bar_l*nhs_fibre/max_fibre,h-180+40),(bar_x-50 + bar_l*nhs_cal/max_calories,h-180+30))
    pygame.draw.line(screen,(250, 200, 250),(bar_x-50 + bar_l*nhs_protein/max_protein,h-180+70),(bar_x-50 + bar_l*nhs_fibre/max_fibre,h-180+60))
    pygame.draw.line(screen,(250, 200, 250),(bar_x-50 + bar_l*nhs_portions/max_portions_fruit_veg,h-180+100),(bar_x-50 + bar_l*nhs_protein/max_protein,h-180+90))

#other lines to make it look nice
    pygame.draw.line(screen,(30,30,250),(col - 90,h+10),(col - 90,h+265))
    pygame.draw.line(screen,(100,30,225),(col*2 - 90,h+10),(col*2 - 90,h+235))
    pygame.draw.line(screen,(150,50,200),(col*3 - 90,h+10),(col*3 - 90,h+295))
    pygame.draw.line(screen,(170,85,140),(col*4 - 90,h+10),(col*4 - 90,h+325))
    pygame.draw.line(screen,(150,120,120),(col*5 - 90,h+10),(col*5 - 90,h+325))

# Annotate the health bars with total values
    calories_text = food_data_font.render(f"{round(total_calories, 0)} kcal", True, BLACK)
    fibre_text = food_data_font.render(f"{round(total_fibre, 1)} g fibre", True, BLACK)
    protein_text = food_data_font.render(f"{round(total_protein, 1)} g protein", True, BLACK)
    portions_text = food_data_font.render(f"{round(total_portions_fruit_veg, 1)} portions of fruit and veg", True, BLACK)

    screen.blit(calories_text, (bar_x-50, h-180+10))
    screen.blit(fibre_text, (bar_x-50, h-180+40))
    screen.blit(protein_text, (bar_x-50, h-180+70))
    screen.blit(portions_text, (bar_x-50, h-180+100))

    list_text = food_titles_font.render("Nutrition:", True, BLACK)
    screen.blit(list_text, (bar_x-50, h-200))

    clear_button_text = food_data_font.render("Clear menu", True, BLACK)
    screen.blit(clear_button_text, (bar_x+88,590))

    # Draw the impact bars                    
def draw_impact_bars():
    impact_bar_width_climate_change = (total_climate_change / max_climate_change) * bar_l
    impact_bar_width_land_use = (total_land_use / max_land_use) * bar_l
    impact_bar_width_water_use = (total_water_use / max_water_use) * bar_l

    pygame.draw.rect(screen, GRAY, (bar_x-50, h-150+160, impact_bar_width_climate_change, 20)) 
    pygame.draw.rect(screen, GRAY, (bar_x-50, h-150+190, impact_bar_width_land_use, 20))
    pygame.draw.rect(screen, GRAY, (bar_x-50, h-150+220, impact_bar_width_water_use, 20)) 

    climate_change_text = food_data_font.render(f"{round(total_climate_change, 1)} kg CO2-eq", True, BLACK)
    land_use_text = food_data_font.render(f"{round(total_land_use, 1)} m2-year", True, BLACK)
    water_use_text = food_data_font.render(f"{round(total_water_use, 1)} L", True, BLACK)

    screen.blit(climate_change_text, (bar_x-50, h-150+160))
    screen.blit(land_use_text, (bar_x-50, h-150+190))
    screen.blit(water_use_text, (bar_x-50, h-150+220))

    list_text = food_titles_font.render("Impact:", True, BLACK)
    screen.blit(list_text, (bar_x-50, h-150+130))

#Impact guidelines
    target_climate_change = total_climate_change/PwES_climate
    target_land_use = total_land_use/PwES_land
    target_water_use = total_water_use/PwES_water

    pygame.draw.line(screen,PURPLE,(bar_x-50 + bar_l*(target_climate_change / max_climate_change),h+10),(bar_x-50 + bar_l*(target_climate_change / max_climate_change),h+10+20))
    pygame.draw.line(screen,PURPLE,(bar_x-50 + bar_l*(target_land_use / max_land_use),h+40),(bar_x-50 + bar_l*(target_land_use / max_land_use),h+40+20))
    pygame.draw.line(screen,PURPLE,(bar_x-50 + bar_l*(target_water_use / max_water_use),h+70),(bar_x-50 + bar_l*(target_water_use / max_water_use),h+70+20))
    pygame.draw.line(screen,(250, 200, 250),(bar_x-50 + bar_l*(target_water_use / max_water_use),h+70+20),(bar_x-50 + 15,h+100+20))
    pygame.draw.line(screen,PURPLE,(bar_x-50+15, h+100+20),(bar_x-50+15, h+140))
    impact_text = food_titles_font.render("Target impacts:", True, PURPLE) #annotations
    screen.blit(impact_text, (bar_x-50 + 20, h+100+20))
    climate_target_text = food_data_font.render(f"{round(target_climate_change, 1)} kg CO2-eq", True, PURPLE) 
    screen.blit(climate_target_text, (bar_x-30 + 20, h+140))
    land_target_text = food_data_font.render(f"{round(target_land_use, 1)} m2-year", True, PURPLE) 
    screen.blit(land_target_text, (bar_x-30 + 20, h+160))
    water_target_text = food_data_font.render(f"{round(target_water_use, 1)} L", True, PURPLE) 
    screen.blit(water_target_text, (bar_x-30 + 20, h+180))

#in-between lines
    pygame.draw.line(screen,(250, 200, 250),(bar_x-50 + bar_l*(target_land_use / max_land_use),h+40+20),(bar_x-50 + bar_l*(target_water_use / max_water_use),h+70))
    pygame.draw.line(screen,(250, 200, 250),(bar_x-50 + bar_l*(target_climate_change / max_climate_change),h+30),(bar_x-50 + bar_l*(target_land_use / max_land_use),h+40))



# Draw the food names on the left side with a gap
def draw_food_items():
    for i, pos in enumerate(food_positions):
        header_text = header_font.render(food_items[i], True, BLACK)
        screen.blit(header_text, (pos[0] + 10, pos[1] + i * gap_height + 8))

# PwES metric
demand_national_calories = 8.31E+13

demand_personal_calories = 3373
demand_personal_fibre = 26
demand_personal_protein = 106
demand_personal_veg = 5.4

energy_economic_allocation = 0.2998
protein_economic_allocation = 0.4844
veg_economic_allocation = 0.0943
fibre_economic_allocation = 0.1195
full_economic_allocation = energy_economic_allocation+fibre_economic_allocation+protein_economic_allocation+veg_economic_allocation

climate_pb_cal = 1.32E10
land_pb_cal = 3.33E10
water_pb_cal = 5.7E12

# Fonts
title_font = pygame.font.Font("Desktop\VS code\Font\FiraSans-SemiBold.ttf", 30)
result_font = pygame.font.Font("Desktop\VS code\Font\FiraSans-SemiBold.ttf", 25)
food_titles_font = pygame.font.Font("Desktop\VS code\Font\FiraSans-SemiBold.ttf", 15)
header_font = pygame.font.Font("Desktop\VS code\Font\FiraSans-Regular.ttf", 15)
food_data_font = pygame.font.Font("Desktop\VS code\Font\FiraSans-Light.ttf", 15)

# Variable to store the index of the currently hovered food
hovered_food_index = None

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the player clicked on the food list on the right
            mouse_pos = pygame.mouse.get_pos()
            list_height = h-180+10
            # Clear the list of chosen food
            if clear_button_rect.collidepoint(event.pos):
                selected_foods = {}
                total_calories = 0
                total_fibre = 0
                total_protein = 0
                total_portions_fruit_veg = 0
                total_climate_change = 0
                total_land_use = 0
                total_water_use = 0
                max_calories = nhs_cal*2
                max_fibre = nhs_fibre*2
                max_protein = nhs_protein*2
                max_portions_fruit_veg = nhs_portions*2
                max_climate_change = 15
                max_land_use = 3
                max_water_use = 1500
            for food_name, quantity in selected_foods.items():
                rect = pygame.Rect(975, list_height, 50, 20)
                if rect.collidepoint(mouse_pos):
                    # Remove one unit of the clicked food item from the list
                    selected_foods[food_name] -= 1
                    if selected_foods[food_name] == 0:
                        del selected_foods[food_name]
                    # Adjust the list_height for the next food item
                    
                    # Update total values for nutrients and impact
                    total_calories -= food_data[food_name]["calories"]
                    total_fibre -= food_data[food_name]["fibre"]
                    total_protein -= food_data[food_name]["protein"]
                    total_portions_fruit_veg -= food_data[food_name]["portions_fruit_veg"]
                    total_climate_change -= food_data[food_name]["climate_change"]
                    total_land_use -= food_data[food_name]["land_use"]
                    total_water_use -= food_data[food_name]["water_use"]

                    # Ensure total values do not go below zero
                    total_calories = max(total_calories, 0)
                    total_fibre = max(total_fibre, 0)
                    total_protein = max(total_protein, 0)
                    total_portions_fruit_veg = max(total_portions_fruit_veg, 0)
                    total_climate_change = max(total_climate_change, 0)
                    total_land_use = max(total_land_use, 0)
                    total_water_use = max(total_water_use, 0)

                    break  # Exit the loop after removing the item
                list_height += 30

            # Check if the player clicked on a food item
            for i, pos in enumerate(food_positions):
                if pos[0] <= mouse_pos[0] <= pos[0] + 90 and pos[1] <= mouse_pos[1] <= pos[1] + 30:
                    # Add a food item to the basket with quantity
                    food_name = food_items[i]
                    if food_name in selected_foods:
                        selected_foods[food_name] += 1
                    else:
                        selected_foods[food_name] = 1

                    # Update total values for nutrients
                    total_calories += food_data[food_name]["calories"]
                    total_fibre += food_data[food_name]["fibre"]
                    total_protein += food_data[food_name]["protein"]
                    total_portions_fruit_veg += food_data[food_name]["portions_fruit_veg"]
                    total_climate_change += food_data[food_name]["climate_change"]
                    total_land_use += food_data[food_name]["land_use"]
                    total_water_use += food_data[food_name]["water_use"]

    # Draw the game window
    screen.fill(WHITE)

    # Draw the title and sub titles
    title_text = title_font.render("Sustainable Food Menu Optimiser: Choose a daily meal plan", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))

    column_one_text = food_titles_font.render("Animal", True, (50,30,250))
    screen.blit(column_one_text, (w,h-20))
    column_two_text = food_titles_font.render("Plant protein", True, (100,30,225))
    screen.blit(column_two_text, (w+col,h-20))
    column_three_text = food_titles_font.render("Vegetables", True, (150,50,200))
    screen.blit(column_three_text, (w+2*col,h-20))
    column_four_text = food_titles_font.render("Fruits", True, (170,85,140))
    screen.blit(column_four_text, (w+3*col,h-20))
    column_five_text = food_titles_font.render("Carbs and fats", True, (150,120,120))
    screen.blit(column_five_text, (w+4*col,h-20))

    #shopping list background
    shop_rect = pygame.Rect(960, 170, 210, 550)
    pygame.draw.rect(screen, (240,230,240), shop_rect)

# Check if the mouse is over a food item and store the index    
    mouse_pos = pygame.mouse.get_pos()
    for i, pos in enumerate(food_positions):
        if pos[0] <= mouse_pos[0] <= pos[0] + col-20 and pos[1] - row * 0.1 <= mouse_pos[1] <= pos[1] + row + i * gap_height:
            hovered_food_index = i
            break
    else:
        hovered_food_index = None

    # Draw selected foods and their quantities on the right
    list_text = food_titles_font.render("Selected Foods:", True, BLACK)
    screen.blit(list_text, (975, h-200))

    # Draw nutritional information for the hovered food
    if hovered_food_index is not None:
        hovered_food_name = food_items[hovered_food_index]
        info_box_rect = pygame.Rect(120, 80, 250, 120)
        pygame.draw.rect(screen, WHITE, info_box_rect, 2)  # Draw a box with a border
        info_lines = [
            f"Quantity: {food_data[hovered_food_name]['quantity']} g, "
            f"Calories: {food_data[hovered_food_name]['calories']} kcal, "
            f"Fibre: {food_data[hovered_food_name]['fibre']} g, "
            f"Protein: {food_data[hovered_food_name]['protein']} g, "
            f"Portions of fruit and veg: {food_data[hovered_food_name]['portions_fruit_veg']}",
        ]

        line_height = 16  # Adjust the line height as needed
        for i, line in enumerate(info_lines):
            line_text = food_data_font.render(line, True, BLACK)
            screen.blit(line_text, (info_box_rect.x + 10, info_box_rect.y + 10 + i * line_height))

    # Draw environmental information for the hovered food
    if hovered_food_index is not None:
        hovered_food_name = food_items[hovered_food_index]
        info_box_rect = pygame.Rect(120, 120, 250, 120)
        pygame.draw.rect(screen, WHITE, info_box_rect, 2)  # Draw a box with a border
        info_lines = [
            #f"Quantity: {food_data[hovered_food_name]['quantity']}, "
            f"Climate change: {food_data[hovered_food_name]['climate_change']} kg-CO2-eq., "
            f"Land use: {food_data[hovered_food_name]['land_use']} m2-year, "
            f"Water use: {food_data[hovered_food_name]['water_use']} L",
        ]
        line_height = 16  # Adjust the line height as needed
        for i, line in enumerate(info_lines):
            line_text = food_data_font.render(line, True, BLACK)
            screen.blit(line_text, (info_box_rect.x + 10, info_box_rect.y + 10 + i * line_height))

    #show image of hovered food
    if hovered_food_index is not None:
        hovered_food_name = food_items[hovered_food_index]
        food_box_rect = pygame.Rect(30, 70, 30, 30)
        pygame.draw.rect(screen, WHITE, food_box_rect, 2)  # Draw a box with a border
        food_image_shown = food_images[hovered_food_name]
        screen.blit(food_image_shown, food_box_rect)

    #show buttons
    screen.blit(clear_button,clear_button_rect) 

    draw_food_items()

    list_height = h-180+10
    for food_name, quantity in selected_foods.items():
        pygame.draw.rect(screen, RED, (975, list_height, 20, 20))  # Adjusted position
        header_text = header_font.render(f"{food_name} x{quantity}", True, BLACK)
        screen.blit(header_text, (1000, list_height))
        list_height += 30

#results display
    if total_calories > 0:  # Check if foods have been selected
        meal_NU_cal = total_calories / demand_personal_calories
        meal_NU_fibre = total_fibre / demand_personal_fibre
        meal_NU_protein = total_protein / demand_personal_protein
        meal_NU_veg = total_portions_fruit_veg / demand_personal_veg

        impact_alloc_cal = ((meal_NU_cal*energy_economic_allocation*full_economic_allocation)/((meal_NU_cal*energy_economic_allocation*full_economic_allocation)+(meal_NU_fibre*fibre_economic_allocation*full_economic_allocation)+(meal_NU_protein*protein_economic_allocation*full_economic_allocation)+(meal_NU_veg*veg_economic_allocation*full_economic_allocation)))
        PwES_climate = (total_climate_change * impact_alloc_cal / total_calories) / (climate_pb_cal / demand_national_calories)
        PwES_land = (total_land_use * impact_alloc_cal / total_calories) / (land_pb_cal / demand_national_calories)
        PwES_water = (total_water_use * impact_alloc_cal / total_calories) / (water_pb_cal / demand_national_calories)

        if PwES_climate >= 1:
            climate_warning = RED
        else:
            climate_warning = GREEN
        PwES_climate_result = result_font.render("Climate change sustainability: ""{:.0%}".format(PwES_climate), True, climate_warning)
        screen.blit(PwES_climate_result, (w,210))

        if PwES_land >= 1:
            land_warning = RED
        else:
            land_warning = GREEN
        PwES_land_result = result_font.render("Land use sustainability: ""{:.0%}".format(PwES_land), True, land_warning)
        screen.blit(PwES_land_result, (w,250))

        if PwES_water >= 1:
            water_warning = RED
        else:
            water_warning = GREEN
        PwES_water_result = result_font.render("Water use sustainability: ""{:.0%}".format(PwES_water), True, water_warning)
        screen.blit(PwES_water_result, (w,290))

#prior to drawing bars, sort scaling
    if total_calories >= max_calories:
        max_calories = total_calories
    if total_fibre >= max_fibre:
        max_fibre = total_fibre
    if total_protein >= max_protein:
        max_protein = total_protein
    if total_portions_fruit_veg >= max_portions_fruit_veg:
        max_portions_fruit_veg = total_portions_fruit_veg
    if total_climate_change >= max_climate_change:
        max_climate_change = total_climate_change
    if total_land_use >= max_land_use:
        max_land_use = total_land_use
    if total_water_use >= max_water_use:
        max_water_use = total_water_use

    draw_health_bars()
    draw_impact_bars()

#chart labels
    list_text = food_titles_font.render("Sustainability:", True, BLACK)
    screen.blit(list_text, (w, 185))

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()