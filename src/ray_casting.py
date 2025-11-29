import pygame
import numpy as np
import math

WIDTH, HEIGHT = 400, 300
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ray Casting - Esfera")

camera_pos = np.array([0.0, 0.0, -5.0])
sphere_pos = np.array([0.0, 0.0, 0.0])
sphere_radius = 1.0

def ray_sphere_intersection(ray_origin, ray_direction, sphere_center, sphere_radius):
    oc = ray_origin - sphere_center
    
    a = np.dot(ray_direction, ray_direction)
    b = 2.0 * np.dot(ray_direction, oc)
    c = np.dot(oc, oc) - sphere_radius**2
    
    discriminant = b**2 - 4 * a * c
    
    if discriminant < 0:
        return False, None
    
    t = (-b - np.sqrt(discriminant)) / (2 * a)
    
    if t >= 0:
        return True, t
    
    return False, None

def render():
    aspect_ratio = WIDTH / HEIGHT
    fov = 60
    fov_factor = math.tan(math.radians(fov) / 2.0)
    
    for y in range(HEIGHT):
        for x in range(WIDTH):
            nx = (2.0 * x / WIDTH - 1.0) * aspect_ratio
            ny = 1.0 - 2.0 * y / HEIGHT
            
            ray_dir = np.array([nx * fov_factor, ny * fov_factor, 1.0])
            ray_dir = ray_dir / np.linalg.norm(ray_dir)
            
            hit, t = ray_sphere_intersection(camera_pos, ray_dir, sphere_pos, sphere_radius)
            
            if hit:
                hit_point = camera_pos + ray_dir * t
    
                normal = (hit_point - sphere_pos) / sphere_radius
                
                # Luz direccional (viene de arriba-derecha)
                light_dir = np.array([0.3, 1.0, -0.5])
                light_dir = light_dir / np.linalg.norm(light_dir)
                
                # Iluminación difusa
                brightness = max(0, np.dot(normal, light_dir))
                
                # Color rojo con iluminación
                color = (int(200 * brightness + 55), int(50 * brightness), int(50 * brightness))
            else:
                color = (10, 10, 30)  # Fondo azul oscuro
            
            screen.set_at((x, y), color)
    
    pygame.display.flip()

print("Renderizando... (puede tardar unos segundos)")
render()
print("¡Listo! Cierra la ventana para salir.")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()