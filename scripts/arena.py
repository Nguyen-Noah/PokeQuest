import pygame, math
from utils.elements import ElementSingleton
from utils.core_funcs import center_img_x
from .trainer import Trainer

class Arena(ElementSingleton):
    def __init__(self, enemy_trainer, terrain_id=1):
        super().__init__()
        self.enemy_trainer = enemy_trainer
        self.rival = Trainer(self.enemy_trainer)
        self.terrain_id = terrain_id
        self.assets = self.e['Assets'].battle_assets[str(self.terrain_id)]
        self.player_assets = self.e['Assets'].player
        self.trainer_assets = self.e['Assets'].trainers
        self.state = 'transitioning'
        self.current_player_asset = self.player_assets['arena_idle']

        # audio
        self.e['Audio'].load('battle_theme.wav', 1.0)
        self.e['Audio'].play('battle_theme')

        # font
        self.text = pygame.font.Font('data/fonts/pokemon-ds-font.ttf', 40)
        self.text_counter = 0

        # timer for when the battle sequence starts
        self.transition = 160

        # little intro where the platforms transition to position
        self.shifting_plats = True
        self.plat_offset = 800

        # absolute positions to blit
        self.back_plat_pos = (self.e['Window'].display.get_width() - self.assets['back'].get_width() + 30, self.assets['back'].get_height())
        self.front_plat_pos = (0 - (self.assets['front'].get_width() / 4), self.assets['bg'].get_height() - self.assets['front'].get_height())

        self.player_pos = (self.player_assets['arena_idle'].get_width() - 140, self.assets['bg'].get_height() - self.player_assets['arena_idle'].get_height())
        self.enemy_pos = (self.assets['bg'].get_width() - self.trainer_assets[self.enemy_trainer].get_width() - 80, 10)

        # misc
        self.pokeball_spin = 0          # degrees
        self.player_throw_timer = 0
        self.player_throw_offset = 0

    def render_text(self, surf, text, newline):
        text_surf = self.text.render(text[:math.floor(self.text_counter)], True, (100, 100, 100))
        self.text_counter += 0.5
        surf.blit(text_surf, (36, 455))

    def update(self):
        if self.transition >= 0:
            self.transition -= 1
        else:
            self.state = 'prebattle'
            if self.shifting_plats:
                self.plat_offset -= 10
                if self.plat_offset <= 0:
                    self.shifting_plats = False

        if self.state == 'deploying':
            self.pokeball_spin += 10
            self.player_throw_timer += 1
            self.player_throw_offset += 5
            if self.player_throw_timer >= 30:
                self.current_player_asset = self.player_assets['arena_throw']

    def render(self, surf):
        if self.transitioning <= 0:
            surf.blit(self.assets['bg'], (0, 0))

            # platforms
            surf.blit(self.assets['back'], (self.back_plat_pos[0] - self.plat_offset, self.back_plat_pos[1]))
            surf.blit(self.assets['front'], (self.front_plat_pos[0] + self.plat_offset, self.front_plat_pos[1]))

            # enemy
            surf.blit(self.trainer_assets[self.enemy_trainer], (self.enemy_pos[0] - self.plat_offset, self.enemy_pos[1]))

            # player
            surf.blit(self.current_player_asset, (self.player_pos[0] + self.plat_offset, self.player_pos[1]))

            # text box
            pygame.draw.rect(surf, (0, 0, 0), (0, self.assets['bg'].get_height(), self.assets['bg'].get_width(), surf.get_height() - self.assets['bg'].get_height()))
            text_box_pos = (center_img_x(surf, self.e['Assets'].text_boxes['hg']), self.e['Window'].display.get_height() - self.e['Assets'].text_boxes['hg'].get_height() - 3)
            surf.blit(self.e['Assets'].text_boxes['hg'], text_box_pos)

            # START OF THE BATTLE LOOP ------------------------------------ #
            if self.plat_offset <= 0:
                if self.state == 'prebattle':
                    # text
                    self.render_text(surf, f'You are challenged by trainer {self.enemy_trainer.upper()}!', 20)
                    
                    if self.e['Input'].mouse_state['left_click']:
                        self.state = 'deploying'
                        self.current_player_asset = self.player_assets['arena_charge']

                if self.state == 'deploying':
                    surf.blit(self.current_player_asset, (self.player_pos[0] - self.player_throw_offset, self.player_pos[1]))
                    """ img = self.e['Assets'].misc['pokeball']
                    img = pygame.transform.rotate(img, -self.pokeball_spin)
                    img.set_colorkey((255, 255, 255))
                    surf.blit(img, (self.player_pos[0] - (img.get_width() // 2), self.player_pos[1] - (img.get_height() // 2))) """

