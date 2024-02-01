import random
from utils.elements import Element

class SimpleHeuristicsPlayer(Element):

    SPEED_TIER_COEFICIENT = 0.1
    HP_FRACTION_COEFICIENT = 0.4
    SWITCH_OUT_MATCHUP_THRESHOLD = -2

    def __init__(self, parent, custom_id=None, singleton=False, register=False):
        super().__init__(custom_id, singleton, register)
        self.parent = parent
        
    def _estimate_matchup(self, mon, opponent):
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
    
    def _stat_estimation(self, mon, stat):
        if mon.boosts[stat] > 1:
            boost= (2 + mon.boosts[stat]) / 2
        else:
            boost = 2 / (2 - mon.boosts[stat])

        attr = getattr(mon, stat)
        return ((2 * attr + 31) + 5) * boost

    def choose_move(self, arena):
        mon = self.parent.active_pokemon
        opponent = self.e['World'].player.active_pokemon

        physical_ratio = self._stat_estimation(mon, 'attack') / self._stat_estimation(opponent, 'defense')
        special_ratio = self._stat_estimation(mon, 'special_attack') / self._stat_estimation(opponent, 'special_defense')

        if arena.available_moves and (not self._should_switch_out() or not arena.available_switches):
            n_remaining_mons = len([m for m in self.parent.team_pokemon if m.fainted is False])
            n_opp_remaining_mons = len([m for m in self.e['World'].player.team_pokemon if m.fainted is False]) #6 - len([m for m in self.e['World'].player.team_pokemon if m.fainted is True])

            print(n_opp_remaining_mons)

            for move in arena.available_moves:
                if (n_opp_remaining_mons >= 3):
                    return self.create_order(move)
                elif (n_remaining_mons >= 2):
                    return self.create_order(move)
                
            if (mon.current_hp_fraction == 1 and self._estimate_matchup(mon, opponent) > 0):
                for move in arena.available_moves:
                    if (move.boosts and sum(move.boosts.values()) >= 2 and move.target == 'user' and min([mon.boosts[s] for s, v in move.boosts.items() if v > 0]) < 6):
                        return self.create_order(move)
                    
            move = max(arena.available_moves, key=lambda m: m.base_power * (1.5 if m.type in mon.types else 1) * (physical_ratio if m.damage_class == 'physical' else special_ratio) * m.accuracy * m.expected_hits * opponent.damage_multiplier(m))
            return self.create_order(move)
        
        if arena.available_switches:
            switches = arena.available_switches
            return self.create_order(max(switches, key=lambda s: self._estimate_matchup(s, opponent)))
        
        return self.choose_random_move()

    def choose_random_move(self):
        available_moves = self.parent.active_pokemon.active_moves

        return available_moves[int(random.random() * len(available_moves))]