# Escape game

import pygame
import serial

display_width = 800
display_height = 600
display_fps = 60
countdown_time = 10

#colours
background_color = (155, 196, 226)
black = (0,0,0)
white = (255,255,255)

class SceneBase:
    def __init__(self):
        self.next = self

    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)


def run_game(width, height, fps, starting_scene):
    #ser = serial.Serial('COM20', 115200, timeout=1/display_fps)
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    # First active scene
    active_scene = starting_scene

    quit_attempt = False
    while quit_attempt is not True:
        #print ser.readline()
        pressed_keys = pygame.key.get_pressed()

        # Event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True

            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)

        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen)

        # next scene is controlled
        active_scene = active_scene.next

        pygame.display.flip()
        clock.tick(fps)



# The rest is code where you implement your game using the Scenes model


class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.image = pygame.image.load('images/title_scene.jpg')

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                # Move to the next scene when the user pressed Enter
                self.SwitchToScene(GameScene())

    def Update(self):
        pass

    def Render(self, screen):
        screen.fill(black)
        self.font = pygame.font.SysFont("comicsansms", 40)
        self.text = self.font.render("Press Enter to start!", True, (194, 59, 34))
        screen.blit(self.image, (0, 50))
        screen.blit(self.text, (display_width // 2 - self.text.get_width() // 2, 3 * display_height // 4 - self.text.get_height() // 2))

class EndScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                # Move to the next scene when the user pressed Enter
                self.SwitchToScene(TitleScene())

    def Update(self):
        pass

    def Render(self, screen):
        screen.fill(background_color)
        self.font = pygame.font.SysFont("comicsansms", 40)
        self.text = self.font.render("Game Over!", True, (255, 0, 40))
        screen.blit(self.text, (display_width // 2 - self.text.get_width() // 2, display_height // 4 - self.text.get_height() // 2))


class GameScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.font = pygame.font.SysFont("comicsansms", 40)
        self.textpos = None

        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
        self.countdown = countdown_time

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.USEREVENT + 1:
                self.countdown -= 1
                if self.countdown < 0:
                    self.countdown = 0
                    self.SwitchToScene(EndScene())

    def Update(self):
        self.text = self.font.render("Time left: " + str(self.countdown), True, (0 + 255 - self.countdown * 255 / countdown_time, self.countdown * 200 / countdown_time, 0))
        if self.textpos is None:
            self.textpos = display_width // 2 - self.text.get_width() // 2, display_height // 4 - self.text.get_height() // 2

    def Render(self, screen):
        screen.fill(background_color)
        screen.blit(self.text, self.textpos)

pygame.init()
run_game(display_width, display_height, display_fps, TitleScene())
