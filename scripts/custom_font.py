import pygame
from utils.elements import Element
from utils.core_funcs import clip

class Font(Element):
    def __init__(self, path, nums=False):
        super().__init__()
        if nums:
            self.character_order = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        else:
            self.character_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '?', '.', ',', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '$', '/']
        self.spacing = 1
        font_img = pygame.image.load(path).convert()
        font_img.set_colorkey((255, 255, 255))
        current_char_width = 0
        self.characters = {}
        self.letter_spacing = []
        character_count = 0

        last_x = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 100:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                char_img = pygame.transform.scale(char_img, (char_img.get_width() * self.e['Assets'].scale_ratio, char_img.get_height() * self.e['Assets'].scale_ratio))
                self.characters[self.character_order[character_count]] = char_img
                self.letter_spacing.append(x - last_x)
                last_x = x - 1
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1

        if nums:
            self.space_width = self.characters['0'].get_width()
        else:
            self.space_width = self.characters['A'].get_width()
    
    def width(self, text):
        text_width = 0
        for char in text:
            if char == ' ':
                text_width += self.space_width + self.spacing
            else:
                text_width += self.letter_spacing[self.character_order.index(char)] + self.spacing
        return text_width

    def render(self, surf, text, loc):
        x_offset = 0
        for char in text:
            if char != ' ':
                surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing