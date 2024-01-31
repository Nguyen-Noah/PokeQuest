import pygame
from utils.elements import Element

# SimpleHeuristicsPlayer
class TrainerAI(Element):

    SPEED_TIER_COEFICIENT = 0.1
    HP_FRACTION_COEFICIENT = 0.4
    SWITCH_OUT_MATCHUP_THRESHOLD = -2

    def __init__(self, parent, custom_id=None, singleton=False, register=False):
        super().__init__(custom_id, singleton, register)
        self.parent = parent
        
    def _estimate_matchup(self, opponent):
        mon = self.parent.active_pokemon

        score = max([opponent.damage_multiplier(t) for t in mon.types if t is not None])
        score -= max(
            [mon.damage_multiplier(t) for t in opponent.types if t is not None]
        )
        if mon.speed > opponent.speed:
            score += self.SPEED_TIER_COEFICIENT
        elif opponent.speed > mon.speed:
            score -= self.SPEED_TIER_COEFICIENT

        score += mon.current_hp_fraction * self.HP_FRACTION_COEFICIENT
        score -= mon.current_hp_fraction * self.HP_FRACTION_COEFICIENT

    def _should_switch_out(self):
        mon = self.parent.active_pokemon
        opponent = self.e['World'].player.active_pokemon

        if [
            m
            for m in self.parent.available_switches
            if self._estimate_matchup(m, opponent) > 0
        ]:
            if mon.boosts['defense'] <= -3 or mon.boosts['speed'] <= -3:
                return True
            if (mon.boosts['attack'] <= -3 and mon.attack <= mon.special_attack):
                return True
            if (mon.boosts['special_attack'] <= -3 and mon.attack <= mon.special_attack):
                return True
            if (self._estimate_matchup(mon, opponent) < self.SWITCH_OUT_MATCHUP_THRESHOLD):
                return True
            
        return False
    
    def _stat_estimation(self, stat):
        mon = self.parent.active_pokemon

        if mon.boosts[stat] > 1:
            boost= (2 + mon.boosts[stat]) / 2
        else:
            boost = 2 / (2 - mon.boosts[stat])

        attr = getattr(mon, stat)
        return ((2 * attr + 31) + 5) * boost
    
    def choose_move(self):
        mon = self.parent.active_pokemon
        opponent = self.e['World'].player.active_pokemon

        physical_ratio = self._stat_estimation(mon, 'attack') / self._stat_estimation(opponent, 'defense')
        special_ratio = self._stat_estimation(mon, 'special_attack') / self._stat_estimation(opponent, 'special_defense')

        