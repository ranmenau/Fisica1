import pygame
import sys
import time

# Inicializar pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 700  # Aumentamos la altura para incluir el área de datos
GAME_HEIGHT = 600  # Altura del área de juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game Mejorado")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Configuración de la paleta
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
INITIAL_PADDLE_SPEED = 8
paddle_speed = INITIAL_PADDLE_SPEED

# Configuración de la pelota
BALL_RADIUS = 8
initial_ball_speed_x = 4
initial_ball_speed_y = -4

# Configuración de los bloques
BLOCK_ROWS = 5
BLOCK_COLUMNS = 10
BLOCK_WIDTH = WIDTH // BLOCK_COLUMNS
BLOCK_HEIGHT = 20

# Fuente
font = pygame.font.Font(None, 36)

# Función para reiniciar el juego
# Esta función inicializa las posiciones de la paleta, pelota, bloques, y variables de estado del juego
# También establece la velocidad inicial de la pelota
# Se utiliza para reiniciar el juego después de perder o al inicio
def reset_game():
    global paddle_x, paddle_y, ball_x, ball_y, ball_speed_x, ball_speed_y, blocks, score, start_time, running, game_over
    # Posición inicial de la paleta
    paddle_x = (WIDTH - PADDLE_WIDTH) // 2
    paddle_y = GAME_HEIGHT - 30
    # Posición inicial de la pelota
    ball_x = WIDTH // 2
    ball_y = GAME_HEIGHT // 2
    # Velocidad inicial de la pelota
    ball_speed_x = initial_ball_speed_x
    ball_speed_y = initial_ball_speed_y
    # Creación de bloques en una cuadrícula
    blocks = [pygame.Rect(col * BLOCK_WIDTH, row * BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT)
              for row in range(BLOCK_ROWS) for col in range(BLOCK_COLUMNS)]
    # Inicialización del puntaje y tiempo
    score = 0
    start_time = time.time()
    # Estado del juego
    running = True
    game_over = False
    global paddle_speed, speed_boost_applied
    paddle_speed = INITIAL_PADDLE_SPEED
    speed_boost_applied = False

reset_game()

# Bucle del juego
while True:
    screen.fill(BLACK)
    
    if not game_over:
        # Dibujar área de datos
        pygame.draw.rect(screen, GRAY, (0, GAME_HEIGHT, WIDTH, HEIGHT - GAME_HEIGHT))
        
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Movimiento de la paleta
        keys = pygame.key.get_pressed()
        #agregi una variable para tener la posicion antes de moverse
        previous_paddle_x = paddle_x
        #fin de linea nueva
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
            paddle_x += paddle_speed
        
        # Movimiento de la pelota
        # Actualizamos la posición de la pelota sumando su velocidad en x y en y
        # Esto representa el desplazamiento de la pelota en cada eje en función del tiempo
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Colisión con las paredes
        # Si la pelota toca los bordes izquierdo o derecho, invertimos su velocidad en x
        # Esto simula un rebote elástico en el eje horizontal, donde la pelota conserva su velocidad pero cambia de dirección
        # En un rebote elástico, la energía cinética y la cantidad de movimiento se conservan
        if ball_x <= 0 or ball_x >= WIDTH - BALL_RADIUS:
            ball_speed_x *= -1  # Cambio de dirección en el eje x

        # Si la pelota toca el borde superior, invertimos su velocidad en y
        # Esto también simula un rebote elástico, pero en el eje vertical
        # Al igual que en el eje x, la energía cinética se conserva y solo se invierte la dirección del movimiento
        if ball_y <= 0:
            ball_speed_y *= -1  # Cambio de dirección en el eje y
        
        # Colisión con la paleta
        # Creamos un rectángulo para la paleta y verificamos si colisiona con la pelota
        # Si hay colisión, invertimos la velocidad en el eje y para simular el rebote
        # Este rebote elástico ocurre porque la pelota choca con un objeto móvil (la paleta)
        # Aunque no se calcula el ángulo de rebote basado en el punto de impacto, se invierte la dirección en el eje y
        paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        if paddle_rect.colliderect(pygame.Rect(ball_x, ball_y, BALL_RADIUS, BALL_RADIUS)):
            ball_speed_y *= -1  # Cambio de dirección en el eje y al rebotar en la paleta
            paddle_velocity=paddle_x-previous_paddle_x
            k=0.1
            ball_speed_x+=k*paddle_velocity
            
       
        
        # Colisión con los bloques
        # Iteramos sobre los bloques y verificamos si colisionan con la pelota
        # Si hay colisión, eliminamos el bloque y cambiamos la dirección de la pelota en el eje y
        # Este rebote elástico simula la interacción entre la pelota y un objeto estático (el bloque)
        # La dirección de la pelota en el eje y se invierte, pero no se considera el ángulo de impacto
        for block in blocks[:]:
            if pygame.Rect(ball_x, ball_y, BALL_RADIUS, BALL_RADIUS).colliderect(block):
                blocks.remove(block)  # Eliminamos el bloque colisionado
                ball_speed_y *= -1  # Cambio de dirección en el eje y al rebotar en un bloque
                score += 10  # Incrementamos el puntaje
                # Incrementar velocidad cada 50 puntos
                # Aumentamos la magnitud de la velocidad en ambos ejes para hacer el juego más desafiante
                if score % 150 == 0 and not speed_boost_applied:
                    ball_speed_x += 2 if ball_speed_x > 0 else -2  # Aumentamos la velocidad en x
                    ball_speed_y += 2 if ball_speed_y > 0 else -2  # Aumentamos la velocidad en y
                    paddle_speed = int(paddle_speed * 2)
                    speed_boost_applied = True
        # Game over si la pelota cae
        # Si la pelota supera la altura del área de juego, el juego termina
        if ball_y >= GAME_HEIGHT:
            game_over = True
        
        # Dibujar bloques
        for block in blocks:
            pygame.draw.rect(screen, RED, block)
            pygame.draw.rect(screen, GRAY, block, 2)  # Bordes de los bloques
        
        # Dibujar paleta y pelota
        pygame.draw.rect(screen, BLUE, paddle_rect)
        pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)
        
        # Calcular velocidad de la pelota
        # Usamos el teorema de Pitágoras para calcular la magnitud de la velocidad
        # La velocidad de la pelota se compone de dos componentes: velocidad en el eje x (ball_speed_x) y velocidad en el eje y (ball_speed_y)
        # Para obtener la magnitud de la velocidad total, aplicamos la fórmula de la distancia en un triángulo rectángulo:
        # velocidad_total = sqrt((velocidad_x)^2 + (velocidad_y)^2)
        # Esto nos da la magnitud del vector velocidad, que representa la rapidez de la pelota sin importar la dirección
        speed = (ball_speed_x**2 + ball_speed_y**2)**0.5
        
        # Calcular tiempo transcurrido
        # Restamos el tiempo actual menos el tiempo de inicio
        elapsed_time = time.time() - start_time
        
        # Mostrar datos en tres columnas
        score_text = font.render(f"Puntaje: {score}", True, BLACK)
        speed_text = font.render(f"Velocidad: {speed:.2f}", True, BLACK)
        time_text = font.render(f"Tiempo: {elapsed_time:.1f} s", True, BLACK)
        screen.blit(score_text, (10, GAME_HEIGHT + 10))
        screen.blit(speed_text, (WIDTH // 3, GAME_HEIGHT + 10))
        screen.blit(time_text, (2 * WIDTH // 3, GAME_HEIGHT + 10))
    else:
        # Pantalla de "Perdiste"
        game_over_text = font.render("¡Perdiste!", True, WHITE)
        play_again_text = font.render("Jugar de nuevo", True, GREEN)
        quit_text = font.render("Salir", True, RED)
        
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        play_again_rect = screen.blit(play_again_text, (WIDTH // 2 - play_again_text.get_width() // 2, HEIGHT // 2))
        quit_rect = screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 50))
        
        # Manejo de eventos en la pantalla de "Perdiste"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(event.pos):
                    reset_game()
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
    
    # Actualizar pantalla
    pygame.display.flip()
    pygame.time.delay(16)  # Aproximadamente 60 FPS