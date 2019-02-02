#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, pygame
from enum import Enum
import random

class Color(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (123, 123, 123)
    
class GameView:
    def __init__(self):
        # Inicializa
        pygame.init()
        self.font = pygame.font.init()

        self.width, self.height = 600, 600

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Jogo da Forca")
        self.clock = pygame.time.Clock()

        self.images = []
        try:
            for i in range(7):
                self.images.append(pygame.image.load("assets/images/" + str(i) + ".png"))

            self.sound_on = pygame.image.load("assets/images/sound_on.png")
            self.sound_off = pygame.image.load("assets/images/sound_off.png")
            self.exit = pygame.image.load("assets/images/exit.png")
            self.restart = pygame.image.load("assets/images/restart.png")
            self.music = pygame.mixer.music.load("assets/music.mp3")

        except:
            print("Imagens não carregadas com sucesso.")

        # Tocar musica
        pygame.mixer.music.play()
        self.screen.blit(pygame.transform.smoothscale(self.sound_on, (25, 25)), (550, 30))

        self.alphabet = {}
        self.create_initial_alphabet(Color.BLACK.value)
        self.drawn_word = [] #Palavra sorteada
        self.load_word("words.txt")
        print(self.drawn_word)
        self.draft_word = [] #Palavra desenhada
        self.draft_word = " "*len(self.drawn_word)
        self.word = []
        self.create_word(self.draft_word)
        self.score = []

    def load_word(self, file):
        try:
            arq = open(file, "r")
            dicionary = arq.readlines()
            self.drawn_word = random.choice(dicionary).rstrip()
            arq.close()
        except:
            print("Palavra não carregada.")
            exit(1)

    def create_letter(self, letter, color, size, position):
        self.font = pygame.font.Font("assets/3-DSketch-Regular.otf", size)
        textSurface = self.font.render(letter, True, color)
        TextSurf, TextRect = textSurface, textSurface.get_rect()
        TextRect.center = position
        return TextSurf, TextRect

    def create_word(self, word):
        self.word = []
        p = 231
        for i in range(len(word)):
            position = (int(self.width * 0.02) + p, int(self.height/3 - (self.height * 0.01)))
            self.word.append(self.create_letter(word.upper()[i], Color.BLACK.value, int(300 / len(word)), position))

            p += 263 / len(word)

    def create_score(self, score):
        p = 231
        for i in range(len(score)):
            position = (int(self.width * 0.02) + p, int(self.height/1.4 - (self.height * 0.01)))
            self.score.append(self.create_letter(score.upper()[i], Color.BLACK.value, int(350 / len(score)), position))

            p += 150 / len(score)

    def create_initial_alphabet(self, color):
        p = 110
        for i, j in zip(range(65, 78), range(78, 91)):
            letter = chr(i)
            position = (int(self.width * 0.02) + p, int(self.height/2 - (self.height * 0.01)))
            self.alphabet[letter] = self.create_letter(letter, color, 40, position)

            letter = chr(j)
            position = (int(self.width * 0.02) + p, int(self.height/1.7 - (self.height * 0.01)))
            self.alphabet[letter] = self.create_letter(letter, color, 40, position)

            p += 30

    def display_line_letter(self, letter, entity):
        pygame.draw.line(self.screen, Color.GRAY.value, entity[letter][1].bottomleft, entity[letter][1].bottomright, 4)
        self.screen.blit(entity[letter][0], entity[letter][1])

    def display_letter(self, letter, entity):
        self.screen.blit(entity[letter][0], entity[letter][1])

    def display_alphabet(self):
        for i in range(65, 91):
            self.display_line_letter(chr(i), self.alphabet)

    def display_word(self):
        for i in range(len(self.word)):
            self.display_line_letter(i, self.word)

    def display_score(self):
        for i in range(len(self.score)):
            self.display_letter(i, self.score)

    def capture_letter(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if click[0] == 1:
            # Se o click do mouse está em alfabeto
            if 110 <= mouse[0] <= 495 and 270 <= mouse[1] <= 370:
                if 270 <= mouse[1] <= 320:
                    letter = chr(int((mouse[0] - 110)/30)+65)
                elif 320 <= mouse[1] <= 370:
                    letter = chr(int((mouse[0] - 110)/30)+78)
                self.alphabet[letter] = self.create_letter(letter, Color.RED.value, 38, self.alphabet[letter][1].center)
                return letter


    def music_buttom(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if click[0] == 1 and 550 <= mouse[0] <= 575 and 30 <= mouse[1] <= 55:
            if pygame.mixer.music.get_busy(): pygame.mixer.music.stop()
            elif not pygame.mixer.music.get_busy(): pygame.mixer.music.play()

        if pygame.mixer.music.get_busy(): self.screen.blit(pygame.transform.smoothscale(self.sound_on, (25, 25)), (550, 30))
        elif not pygame.mixer.music.get_busy(): self.screen.blit(pygame.transform.smoothscale(self.sound_off, (25, 25)), (550, 30))

    def power_buttom(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        self.screen.blit(pygame.transform.smoothscale(self.exit, (25, 25)), (500, 30))
        if click[0] == 1 and 500 <= mouse[0] <= 525 and 30 <= mouse[1] <= 55:
            pygame.quit()
            sys.quit()

    def restar_buttom(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        self.screen.blit(pygame.transform.smoothscale(self.restart, (25, 25)), (450, 30))
        if click[0] == 1 and 425 <= mouse[0] <= 500 and 30 <= mouse[1] <= 55:
            self.screen.fill(Color.WHITE.value)
            pygame.display.flip()
            self.__init__()
            self.run()

    def run(self):
        img = 0
        accert = False
        end_game = False
        while True:
            images = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.unicode.isalpha():
                        letter = event.unicode.upper()
                        self.alphabet[letter] = self.create_letter(letter, Color.RED.value, 38, self.alphabet[letter][1].center)

            # Carregar imagem
            for image in self.images:
                images.append(pygame.transform.smoothscale(image, (int(self.width * 0.5), int(self.height * 0.5))))

            # Captura a letra selecionada pelo mouse
            letter = self.capture_letter()
            if letter is None:
                letter = " "

            #Verifica se a letra selecionada existe na palavra
            for i in range(0, len(self.drawn_word)):
                if self.drawn_word[i] is letter:
                    w = self.draft_word[:i] + letter + self.draft_word[i+1:]
                    self.draft_word = w
                    self.create_word(self.draft_word)
                    accert = True

            if letter is not " ":
                if accert is False:
                    if end_game is False:
                        img += 1

            accert = False;

            # Atualizar a janela
            self.screen.fill(Color.WHITE.value)

            if img >= 6:
                end_game = True
                self.create_word(self.drawn_word)
                self.create_score("Fim de Jogo!")
                self.display_word()
                self.display_score()

            if " " not in self.draft_word:
                end_game = True
                self.create_score("Voce Acertou!")
                self.display_score()

            # Exibe textos (alfabeto+palavra+tema)
            self.display_word()
            self.display_alphabet()

            pygame.display.update()

            # Exibir a imagem
            self.screen.blit(images[img % 7], (0, 0))

            self.music_buttom()
            self.power_buttom()
            self.restar_buttom()

            pygame.display.flip()

            self.clock.tick(5)

if __name__ == '__main__':
    g = GameView()
    g.run()
