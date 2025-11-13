import random
import pygame

# CONSTANTS
GAME_TITLE = "Game Test"
WIDTH = 800
HEIGHT = 600

MENU_STATE = "MENU"
PLAYING_STATE = "PLAYING"
GAME_OVER_STATE = "GAME_OVER"
PAUSED_STATE= "PAUSED"
EXIT_STATE = "EXIT"

# init screen
pygame.init()

screen = pygame.display.set_mode(
    size=(WIDTH, HEIGHT)
)

# Caption 
pygame.display.set_caption(
    title=GAME_TITLE
)

# Enemy
class Enemy:
    def __init__(self, pos, color="yellow", speed=100, size=15):
        self.color = color
        self.size = size
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)      # velocidad (vx, vy)
        self.surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        self.random_direction(speed)
    
    def update_polygon(self):
        """Dibuja el triángulo basado en el tamaño actual."""
        self.surface.fill((0, 0, 0, 0))  # limpiar con transparencia
        points = [(self.size, 0), (0, self.size * 2), (self.size * 2, self.size * 2)]
        pygame.draw.polygon(self.surface, self.color, points)

    def random_direction(self, speed):
        """Cambia la dirección aleatoriamente."""
        angle = random.uniform(0, 360)
        self.vel.from_polar((speed, angle))
    
    def move(self, screen_rect, dt):
        """Actualiza la posición según la velocidad, y rebota en los bordes."""
        self.pos += self.vel * dt
        if not screen_rect.contains(self.surface.get_rect(center=self.pos)):
            # Rebote simple
            if self.pos.x < 0 or self.pos.x > screen_rect.width:
                self.vel.x *= -1
            if self.pos.y < 0 or self.pos.y > screen_rect.height:
                self.vel.y *= -1
            self.pos += self.vel  # corrige la posición después del rebote
    
    def draw(self, screen):
        """Dibuja el triángulo rotado según su dirección de movimiento."""
        angle = self.vel.angle_to(pygame.Vector2(0, -1))
        base_points = [
            pygame.Vector2(0, -self.size),
            pygame.Vector2(-self.size, self.size),
            pygame.Vector2(self.size, self.size),
        ]
        points = [self.pos + p.rotate(angle) for p in base_points]
        pygame.draw.polygon(screen, self.color, points)

# Player
class Player:
    def __init__(self, pos, color="red", speed=300, radius=20):
        self.pos = pygame.Vector2(pos)
        self.color = color
        self.speed = speed
        self.radius = radius

    def handle_input(self, dt):
        """Mueve al jugador según las teclas presionadas (WASD)."""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.pos.y -= self.speed * dt
        if keys[pygame.K_s]:
            self.pos.y += self.speed * dt
        if keys[pygame.K_a]:
            self.pos.x -= self.speed * dt
        if keys[pygame.K_d]:
            self.pos.x += self.speed * dt

    def draw(self, surface):
        """Dibuja el jugador como un círculo."""
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

    def check_collision(self, enemy : Enemy):
        """Devuelve True si hay colisión circular con el enemigo."""
        distance = self.pos.distance_to(enemy.pos)
        return distance < (self.radius + enemy.size)

# GAME
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.state = MENU_STATE
        
    def start(self):
        """Inicializa una nueva partida."""
        self.score = 0
        self.time_accumulator = 0
        self.state = PLAYING_STATE
        
        self.player = Player((WIDTH/2, HEIGHT/2))
        self.enemies = [Enemy((random.randint(50, 750), random.randint(50, 550))) for _ in range(5)]
    
    def reset_to_menu(self):
        """Vuelve al menú principal."""
        self.state = MENU_STATE

    def toggle_pause(self):
        """Alterna entre pausado y jugando."""
        if self.state == PLAYING_STATE:
            self.state = PAUSED_STATE
        elif self.state == PAUSED_STATE:
            self.state = PLAYING_STATE

    def set_exit_state(self):
        self.state = EXIT_STATE

    def reset(self):
        self.__init__(self.screen)

    def update(self, dt):
        """Actualiza la lógica principal del juego."""
        if self.state == PLAYING_STATE:
            self.player.handle_input(dt)
            self.update_score(dt)
            self.update_enemies(dt)
            self.check_collisions()

    def update_score(self, dt):
        """Lógica de puntaje basada en tiempo."""
        self.time_accumulator += dt
        if self.time_accumulator >= 5:   # cada 5 segundos
            self.score += 10
            self.time_accumulator = 0

    def update_enemies(self, dt):
        """Actualiza todos los enemigos."""
        for enemy in self.enemies:
            enemy.move(self.screen_rect, dt)

    def check_collisions(self):
        """Verifica colisiones jugador-enemigo."""
        for enemy in self.enemies:
            if self.player.pos.distance_squared_to(enemy.pos) < (self.player.radius + enemy.size) ** 2:
                self.state = GAME_OVER_STATE

    def draw(self):
        """Renderiza todo el contenido en pantalla."""
        self.screen.fill("purple")
        if self.state == MENU_STATE:
            self.draw_menu()
        elif self.state == PLAYING_STATE:
            self.draw_playing()
        elif self.state == PAUSED_STATE:
            self.draw_playing()
            self.draw_pause_overlay()
        elif self.state == GAME_OVER_STATE:
            self.draw_game_over()
        pygame.display.flip()

    def draw_menu(self):
        draw_text(self.screen, "🚀 DODGE THE TRIANGLES 🚀", 64, "white", (400, 220))
        draw_text(self.screen, "Presiona ENTER para comenzar", 36, "gray", (400, 320))
        draw_text(self.screen, "Presiona Q para Salir del juego", 30, "gray", (400, 350))
        draw_text(self.screen, "Usa W, A, S, D para moverte", 28, "gray", (400, 380))

    def draw_playing(self):
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        draw_text(self.screen, f"SCORE: {self.score}", 36, "white", (100, 30))

    def draw_pause_overlay(self):
        """Dibuja la pantalla de pausa encima del juego."""
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # semitransparente
        self.screen.blit(overlay, (0, 0))
        draw_text(self.screen, "⏸ PAUSA ⏸", 72, "yellow", (400, 250))
        draw_text(self.screen, "Presiona SPACE para continuar", 36, "white", (400, 340))
        draw_text(self.screen, "Presiona M para ir al menú", 32, "gray", (400, 390))
        draw_text(self.screen, "Presiona Q para salir del juego", 32, "gray", (400, 410))

    def draw_game_over(self):
        draw_text(self.screen, "💀 GAME OVER 💀", 72, "red", (400, 260))
        draw_text(self.screen, f"FINAL SCORE: {self.score}", 48, "white", (400, 340))
        draw_text(self.screen, "Presiona R para reiniciar o ESC para menú", 36, "gray", (400, 420))

# --- Lógica del juego ---
def draw_text(surface, text, size, color, pos):
    font = pygame.font.Font(None, size)
    txt = font.render(text, True, color)
    rect = txt.get_rect(center=pos)
    surface.blit(txt, rect)


# --- Inicialización ---
clock = pygame.time.Clock()
running = True
dt = 0

game = Game(screen)

score = 0
time_accumulator = 0


while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT or game.state == EXIT_STATE:
            running = False

        if game.state == MENU_STATE:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game.start()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                game.set_exit_state()
        elif game.state == PLAYING_STATE and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.toggle_pause()
        elif game.state == PAUSED_STATE and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.toggle_pause()
            elif event.key == pygame.K_m:
                game.reset_to_menu()
            elif event.key == pygame.K_q:
                game.set_exit_state()
        elif game.state == GAME_OVER_STATE and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game.start()
            elif event.key == pygame.K_ESCAPE:
                game.reset_to_menu()
    
    game.update(dt=dt)
    game.draw()

pygame.quit()