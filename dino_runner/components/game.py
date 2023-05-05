import pygame

from pygame import mixer

from dino_runner.utils.constants import BG2, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, CLOUD, MUSIC_THEME, DEFAULT_TYPE

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.ranking import Ranking

from dino_runner.components.obstacles.obstacle_manager import ObstacleManager

from dino_runner.utils.text_utils import draw_message_component

from dino_runner.components.powerups.power_up_manager import PowerUpManager


class Game:

    # Construtor
    def __init__(self):
        pygame.init() # instancia o pygame
        mixer.init() # instancia o mixer (biblioteca do pygame para lidar com os efeitos sonoros)
        pygame.display.set_caption(TITLE) # atribui o titulo no cabeçalho da tela 
        pygame.display.set_icon(ICON) # adiciona um icone a janela
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # configura tamanho da tela
        self.clock = pygame.time.Clock() 
        self.playing = False
        self.running = False
        self.score = 0
        self.death_count = 0
        self.game_speed = 20
        self.x_pos_bg = 1280 # Define a posição do background na tela
        self.y_pos_bg = 380 # Define a posição do background na tela
        self.x_pos_cloud = 1280 # Define a posição da bola de fogo na tela
        self.y_pos_cloud = 100 # Define a posição da bola de fogo na tela
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    #Função executa o game chamando o menu
    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()
    
    #Inicia o game loop
    def run(self):
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.game_speed = 20
        self.score = 0
        while self.playing:
            self.events()
            self.update()
            self.draw()

    #Função que lida com os eventos
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    #Função do update para atualizar os estados 
    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self.score, self.game_speed, self.player)

    #Atualiza os pontos
    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 5

    #Renderiza as jogo de modo geral(Visulização do game)
    def draw(self):
        self.clock.tick(FPS)
        self.screen.blit(BG2,(0,0)) # Altera para a imagem(background) de fundo
        self.draw_score()
        self.draw_power_up_time()
        self.draw_background() # Responsvel para animação de fundo EX: bola de fogo
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    #Renderiza animação dos componentes do background Ex: Bola de Fogo
    def draw_background(self):
        cloud_img = CLOUD.get_width()
        self.screen.blit(CLOUD, (cloud_img + self.x_pos_cloud, self.y_pos_cloud))
        self.x_pos_bg = -10
        self.x_pos_cloud -= self.game_speed // 2
        self.screen.blit(CLOUD, (cloud_img + self.x_pos_cloud, self.y_pos_cloud))
        if self.x_pos_cloud < -cloud_img:
            self.x_pos_cloud = SCREEN_WIDTH

    #Criação da visualização do score em tela
    # Mudou:
    #   Fonte, Cor, Posição e Tamanho
    def draw_score(self):
        draw_message_component(
            f"Pontos: {self.score}",
            self.screen,
            pos_x_center=1000,
            pos_y_center=50,
            font_size = 35,
            font_color=(0,128,0)
        )

    #Criação da visualização do time de poder em tela
    # Mudou:
    #   Fonte, Cor, Posição e Tamanho
    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round(
                (self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                draw_message_component(
                    f"{self.player.type.capitalize()} habilitado por {time_to_show} segundos",
                    self.screen,
                    font_size=18,
                    pos_x_center=500,
                    pos_y_center=40,
                    font_color=(0,128,0)
                )
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE


    #Lida com os eventos da entrada do usuario no game
    # Ex: Menu
    # Mudou:
    #   Local da chamada da musica - Criando uma Função para isso
    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # Se ele pressionar enter ele vai iniciar o jogo                    
                    self.music_play(MUSIC_THEME)
                    self.run()

                elif event.key == pygame.K_TAB: # Se ele pressionar TAB ele mostra o Ranking
                    self.ranking()

                elif event.key == pygame.K_e: # Se ele pressionar a tecla 'E' ele envia o score do jogador para o ranking 
                    ranking = Ranking()
                    ranking.save("Teste", self.score)
                    print("Enviado para o Ranking!")

                elif event.key == pygame.K_BACKSPACE: # Se ele pressionar a tecla backspace ele sai do game 
                    pygame.quit()

    
    # Função responsavel pela arte do menu
    def show_menu(self):
        self.screen.fill((255, 255,255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            draw_message_component(
                "[Enter] - Iniciar o Jogo",
                self.screen,
                pos_y_center=half_screen_height - 40
            )
            draw_message_component(
                "[TAB] - Ranking",
                self.screen,
                pos_y_center= half_screen_height
            )
            draw_message_component(
                "[BACKSPACE] - Sair do Jogo",
                self.screen,
                pos_y_center= half_screen_height + 50
            )
        else:
            draw_message_component(
                f"Sua Pontuacao {self.score}",
                self.screen,
                pos_y_center=half_screen_height - 150,
            )
            draw_message_component(
                f"Contagem de Vida: {self.death_count}",
                self.screen,
                pos_y_center= half_screen_height - 100
            )
            draw_message_component(
                "[Enter] - Reiniciar o Jogo",
                self.screen,
                pos_y_center= half_screen_height + 140
            )
            draw_message_component(
                "[E] - Enviar Save",
                self.screen,
                pos_y_center= half_screen_height + 170
            )
            draw_message_component(
                "[BACKSPACE] - Sair do Jogo",
                self.screen,
                pos_y_center= half_screen_height + 200
            )
            self.screen.blit(ICON, (half_screen_width - 40, half_screen_height - 30))
        pygame.display.flip()
        self.handle_events_on_menu()


    # Função para cuidar da criação da segunda tela, Ranking.
    def ranking(self):
        pygame.display.set_caption("Ranking")
        while True:

            #Instancia a classe Ranking - Responsavel pela requisição http na API MOCK API
            response = Ranking()
            data = response.get()
            data_json = data.json()

            # Criação da tela de Ranking 
            self.screen.fill("black")

            draw_message_component(
                "Ranking",
                self.screen,
                (255,255,255),
                pos_y_center= 100
            )

            for i in data_json:
                for y in range(0,len(data_json)):
                    draw_message_component(
                        f"{i[y]}   {i[y]}",
                        self.screen,
                        pos_y_center= 200*y,
                        pos_x_center= 500,
                        font_color= (255,255,255)
                    )



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.K_TAB:
                    self.show_menu()

            pygame.display.update()
       
    # Função para inicializar os efeitos sonoros.
    def music_play(self, music): 
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)
