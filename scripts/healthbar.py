import pygame
from utils.elements import Element

class Healthbar(Element):
    def __init__(self, owner, custom_id=None, singleton=False, register=False):
        super().__init__(custom_id, singleton, register)
        self.owner = owner
        self.health = self.owner.current_hp
        self.player = self.owner.owner
        self.assets = self.e['Assets'].health_bars
        if self.player.type == 'player':
            self.transition_offset = self.assets[self.player.type + '_main'].get_width()
        else:
            self.transition_offset = -self.assets[self.player.type + '_main'].get_width()
        self.name_font = pygame.font.Font('data/fonts/pokemon-ds-font.ttf', 45)

    def update(self):
        pass

    def render(self, surf):
        if self.player.type == 'player':
            name_offset = (60, 25)
            render_pos = (surf.get_width() - self.assets[self.player.type + '_main'].get_width(), 280)
            if self.transition_offset > 0:
                self.transition_offset -= min(12, self.transition_offset)
        else:
            name_offset = (10, 25)
            render_pos = (0, 50)
            if self.transition_offset <= 0:
                self.transition_offset += min(12, abs(self.transition_offset))

        render_pos = (render_pos[0] + self.transition_offset, render_pos[1])
        surf.blit(self.assets[self.player.type + '_main'], render_pos)

        text_surf = self.name_font.render(self.owner.name.capitalize(), True, (80, 80, 80))
        shadow_surf = self.name_font.render(self.owner.name.capitalize(), True, (200, 200, 200))
        surf.blit(shadow_surf, (render_pos[0] + name_offset[0] + 2, render_pos[1] + name_offset[1]))
        surf.blit(shadow_surf, (render_pos[0] + name_offset[0] + 2, render_pos[1] + name_offset[1] + 2))
        surf.blit(shadow_surf, (render_pos[0] + name_offset[0], render_pos[1] + name_offset[1] + 2))
        surf.blit(text_surf, (render_pos[0] + name_offset[0], render_pos[1] + name_offset[1]))
 