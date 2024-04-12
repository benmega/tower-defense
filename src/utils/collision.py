# collision.py

def check_collision(object1, object2):
    """
    Check if two objects collide. This function assumes each object has grid_x, grid_y coordinates
    and a 'size' or 'radius' attribute for simplicity.
    """
    dx = object1.x - object2.x
    dy = object1.y - object2.y
    distance = (dx**2 + dy**2)**0.5

    max_collision_distance = object1.size + object2.size
    return distance < max_collision_distance

def is_enemy_reaching_target(enemy, target):
    """
    Check if an enemy has reached a target point (e.g., end of a path).
    This could be as simple as comparing positions if enemies move tile by tile.
    """
    return enemy.x == target.x and enemy.y == target.y
