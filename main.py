import sys
import io
import requests
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, BLACK, WHITE
from api_client import PokeAPIClient
from entities import Player, Bullet

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

def load_image_from_url(url):
    """Descarga una imagen de internet directamente para Pygame."""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            image_file = io.BytesIO(response.content)
            return pygame.image.load(image_file).convert_alpha()
    except Exception as e:
        print(f"Error al descargar imagen: {e}")
    
    # Cuadro rojo si falla la carga
    fallback = pygame.Surface((64, 64))
    fallback.fill((255, 0, 0))
    return fallback

# 1. Obtener Pokémon desde PokeAPI
print("Cargando datos desde PokéAPI...")
blastoise_data = PokeAPIClient.get_pokemon_data("blastoise")
gastly_data = PokeAPIClient.get_pokemon_data("gastly")

# 2. Cargar Sprites
player_img = load_image_from_url(blastoise_data["sprite_url"])
enemy_img = load_image_from_url(gastly_data["sprite_url"])
enemy_img = pygame.transform.scale(enemy_img, (64, 64))

# 3. Grupos de Sprites
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Crear Jugador
player = Player(player_img, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
all_sprites.add(player)

# Posición del enemigo
enemy_rect = enemy_img.get_rect(center=(SCREEN_WIDTH // 2, 100))

# Bucle Principal
running = True
score = 0
font = pygame.font.SysFont("Arial", 24)

while running:
    clock.tick(FPS)
    
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    # Actualizar estado
    all_sprites.update()

    # Colisión bala - enemigo
    for bullet in bullets:
        if enemy_rect.colliderect(bullet.rect):
            bullet.kill()
            score += 10
            enemy_rect.x = (enemy_rect.x + 150) % (SCREEN_WIDTH - 64)

    # Dibujar en pantalla
    screen.fill(BLACK)
    all_sprites.draw(screen)
    screen.blit(enemy_img, enemy_rect)

    # Mostrar Puntos
    score_text = font.render(f"Puntos: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
