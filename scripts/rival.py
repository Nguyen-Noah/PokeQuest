import pygame, random
from .trainer import Trainer
from .trainer_ai import TrainerAI

class Rival(Trainer):
    def __init__(self, name):
        super().__init__('rival', TrainerAI)
        self.name = name
        self.num_pokemon = random.randint(1, 6)
        self.add_pokemon('umbreon')
        self.img = self.e['Assets'].trainers[self.name]
        self.deploy_offset = 0
        self.player_deploy_timer = 100

    def update(self):
        super().update()
        if self.e['Arena'].state == 'rival_deploying':
            self.deploy_offset += 6
            if self.deploy_offset >= 500:
                self.render_pokemon = True
                self.player_deploy_timer -= 2
                if self.player_deploy_timer <= 0:
                    self.e['Arena'].set_state('deploying')
                    self.e['Arena'].textbox.reset_text_counter()

    def render(self, surf):
        render_pos = (self.e['Arena'].assets['bg'].get_width() - self.img.get_width() - 80, 10)
        if self.e['Arena'].state == 'opening':
            surf.blit(self.img, (render_pos[0] - self.e['Arena'].plat_offset, render_pos[1]))
        elif self.e['Arena'].state == 'prebattle':
            surf.blit(self.img, render_pos)
        elif self.e['Arena'].state == 'rival_deploying':
            surf.blit(self.img, (render_pos[0] + self.deploy_offset, render_pos[1]))

            if not self.render_pokemon:
                pokeball_surf = pygame.Surface(self.e['Assets'].misc['pokeball'].get_size())
                pokeball_surf.blit(self.e['Assets'].misc['pokeball'], (0, 0))
                pokeball_surf.set_colorkey((0, 0, 0))
                surf.blit(pokeball_surf, (render_pos[0] + 100, render_pos[1] + 180))

        if self.render_pokemon:
            self.active_pokemon.render(surf, render_pos)