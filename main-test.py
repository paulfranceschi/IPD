
import axelrod as axl
import random

# Set seed for reproducibility
SEED = 1000
random.seed(SEED)

class FourDualityOptimizer1(axl.Player):
    """
    A strategy that operates as follows:
    cooperate by default;
    ignore betrayals of length 1;
    when the other agent performs a series of betrayals of length greater than 1,
    respond with a series of betrayals whose number is equal to the number
    of series of betrayals performed by the other agent since the beginning.

    Names:
    4-Duality Optimizer 1 original by Paul Franceschi
    """
    name = "4-Duality Optimizer 1"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        # Calculate the number of opponent betrayal streaks of length > 1
        waves_greater_than_one = 0
        current_wave_length = 0
        for action in opponent.history:
            if action == axl.Action.D:
                current_wave_length += 1
            else:
                if current_wave_length > 1:
                    waves_greater_than_one += 1
                current_wave_length = 0

        # Calculate the length of our current betrayal streak
        consecutive_our_defections = 0
        for i in range(len(self.history) - 1, -1, -1):
            if self.history[i] == axl.Action.D:
                consecutive_our_defections += 1
            else:
                break

        # Calculate the length of the opponent's current betrayal streak
        consecutive_opp_defections = 0
        for i in range(len(opponent.history) - 1, -1, -1):
            if opponent.history[i] == axl.Action.D:
                consecutive_opp_defections += 1
            else:
                break

        # Decision rules
        if consecutive_opp_defections >= 2:
            return axl.Action.D

        if consecutive_our_defections > 0 and consecutive_our_defections < waves_greater_than_one:
            return axl.Action.D

        return axl.Action.C


class FourDualityOptimizer1B(axl.Player):
    """
    variant of 4-Duality Optimizer 1 with boundary
    A strategy that operates as follows:
    cooperate by default;
    ignore betrayals of length 1;
    when the other agent performs a series of betrayals of length greater than 1,
    respond with a series of betrayals whose number is equal to the number
    of series of betrayals performed by the other agent since the beginning.

    Names:
    4-Duality Optimizer 1B original by Paul Franceschi
    """
    name = "4-Duality Optimizer 1B"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        # Calculate the number of opponent betrayal streaks of length > 1
        waves_greater_than_one = 0
        current_wave_length = 0
        for action in opponent.history:
            if action == axl.Action.D:
                current_wave_length += 1
            else:
                if current_wave_length > 1:
                    waves_greater_than_one += 1
                current_wave_length = 0

        # In case the history ends with a streak longer than 1, count it too.
        # This is the only difference with 4-Duality Optimizer 1.
        if current_wave_length > 1:
            waves_greater_than_one += 1

        # Calculate the length of our current betrayal streak
        consecutive_our_defections = 0
        for i in range(len(self.history) - 1, -1, -1):
            if self.history[i] == axl.Action.D:
                consecutive_our_defections += 1
            else:
                break

        # Calculate the length of the opponent's current betrayal streak
        consecutive_opp_defections = 0
        for i in range(len(opponent.history) - 1, -1, -1):
            if opponent.history[i] == axl.Action.D:
                consecutive_opp_defections += 1
            else:
                break

        # Decision rules
        if consecutive_opp_defections >= 2:
            return axl.Action.D

        if consecutive_our_defections > 0 and consecutive_our_defections < waves_greater_than_one:
            return axl.Action.D

        return axl.Action.C


# Select random strategies + 4-Duality Optimizer strategy
random_strategies = [cls() for cls in random.sample(axl.strategies, 30)]
players = random_strategies + [FourDualityOptimizer1()] + [FourDualityOptimizer1B()]

print(f"\nRunning tournament with {len(players)} players...")
print("\nSelected strategies:")
for i, player in enumerate(players, 1):
    print(f"  {i:>2}. {player.name}")
tournament = axl.Tournament(players, turns=200, repetitions=5, noise=0.05)
results = tournament.play()

# RDisplay results: Build mapping from name to original index
if hasattr(results.players[0], 'name'):
    result_names = [p.name for p in results.players]
else:
    result_names = results.players

name_to_index = {name: i for i, name in enumerate(result_names)}

# Determine if results.players contains objects with .name or just strings
if hasattr(results.players[0], 'name'):
    # list of player objects
    player_names = [p.name for p in results.players]
    # scores are still aligned by index
    score_name_list = [(sum(results.scores[i]), player_names[i]) for i in range(len(results.players))]
else:
    # results.players is already list of strings
    player_names = results.players
    score_name_list = [(sum(results.scores[i]), player_names[i]) for i in range(len(results.players))]

# Sort descending by total score
score_name_list.sort(reverse=True, key=lambda x: x[0])

print("\n" + "="*60)
print("TOURNAMENT RESULTS (total score across all turns & repetitions):")
print("="*60)

for rank, (total_score, name) in enumerate(score_name_list, 1):
    print(f"{rank:>2}. {name:<30} : {total_score:>8.2f} points")
