import pygame
from utils.elements import Element

class Healthbar(Element):
    def __init__(self, owner, custom_id=None, singleton=False, register=False):
        super().__init__(custom_id, singleton, register)
        self.owner = owner
        self.health = self.owner.current_hp
        self.player = self.owner.owner
        self.assets = self.e['Assets'].health_bars
        self.name_font = pygame.font.Font('data/fonts/pokemon-ds-font.ttf', 45)
        if self.player.type == 'player':
            self.transition_offset = self.assets[self.player.type + '_main'].get_width()
            self.exp_bar = self.assets['exp_bar']
        else:
            self.transition_offset = -self.assets[self.player.type + '_main'].get_width()
            self.exp_bar = None

        hp_percent = self.owner.current_hp / self.owner.max_hp
        if hp_percent > 0.5:
            self.healthbar = self.assets['green_health']
        elif hp_percent > 0.2 and hp_percent < 0.5:
            self.healthbar = self.assets['yellow_health']
        else:
            self.healthbar = self.assets['red_health']

    def render_name(self, surf, pos):
        text_surf = self.name_font.render(self.owner.name.capitalize(), True, (80, 80, 80))
        shadow_surf = self.name_font.render(self.owner.name.capitalize(), True, (200, 200, 200))
        surf.blit(shadow_surf, (pos[0] + 2, pos[1]))
        surf.blit(shadow_surf, (pos[0] + 2, pos[1] + 2))
        surf.blit(shadow_surf, (pos[0], pos[1] + 2))
        surf.blit(text_surf, pos)

    def update(self):
        # healthbar
        health_ratio = self.owner.current_hp / self.owner.max_hp

        if health_ratio < 0.5 and health_ratio > 0.2:
            self.healthbar = self.assets['yellow_health']
        if health_ratio < 0.2:
            self.healthbar = self.assets['red_health']

        if health_ratio > 0:
            healthbar_width = self.assets['green_health'].get_width() * health_ratio        # use width from assets b/c full healthbar width is needed
            self.healthbar = pygame.transform.scale(self.healthbar, (healthbar_width, self.healthbar.get_height()))
        else:
            self.healthbar = pygame.transform.scale(self.healthbar, (0, self.healthbar.get_height()))

        # exp
        if self.exp_bar:
            exp_ratio = self.owner.exp / self.owner.exp_to_level_up
            exp_bar_width = self.assets['exp_bar'].get_width() * exp_ratio
            #self.exp_bar = pygame.transform.scale(self.exp_bar, (exp_bar_width, self.exp_bar.get_height()))

    def render(self, surf):
        if self.player.type == 'player':
            name_offset = (60, 25)
            health_pos = (600, 355)
            level_pos = (696, 316)
            render_pos = (surf.get_width() - self.assets[self.player.type + '_main'].get_width(), 280)
            if self.transition_offset > 0:
                self.transition_offset -= min(12, self.transition_offset)    
        else:
            name_offset = (10, 25)
            health_pos = (150, 122)
            render_pos = (0, 50)
            level_pos = (246, 82)
            if self.transition_offset <= 0:
                self.transition_offset += min(12, abs(self.transition_offset))

        # the base health asset
        render_pos = (render_pos[0] + self.transition_offset, render_pos[1])
        surf.blit(self.assets[self.player.type + '_main'], render_pos)

        # the healthbar
        surf.blit(self.healthbar, (health_pos[0] + self.transition_offset, health_pos[1]))

        # the name
        self.render_name(surf, (render_pos[0] + name_offset[0], render_pos[1] + name_offset[1]))

        # the level
        self.e['Assets'].health_font.render(surf, str(self.owner.level), (level_pos[0] + self.transition_offset, level_pos[1]))

        if self.player.type == 'player':
            # the health
            self.e['Assets'].health_font.render(surf, str(int(self.owner.max_hp)), (670 + self.transition_offset, 376))
            number_offset = 25 * (len(str(int(self.owner.current_hp))) - 1)
            self.e['Assets'].health_font.render(surf, str(int(self.owner.current_hp)), (626 - number_offset + self.transition_offset, 376))

            # the exp
            surf.blit(self.exp_bar, (456 + self.transition_offset, 406))