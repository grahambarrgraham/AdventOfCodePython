import functools
import math
import sys

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(players_pos):
    players_score = [0, 0]

    dice = 0
    player = 0
    rolls = 0
    rolls_per_player = 3

    while max(players_score) < 1000:
        roll = roll_dice(dice, rolls_per_player)
        dice = (dice + rolls_per_player) % 100
        players_pos[player] = (players_pos[player] + roll) % 10
        players_score[player] += players_pos[player] + 1
        player = (player + 1) % 2
        rolls += rolls_per_player

    return min(players_score) * rolls


def phase2(p1_pos, p2_pos):
    return play_dirac_game(p1_pos, 0, p2_pos, 0)


@functools.cache
def play_dirac_game(player1_pos: int, player1_score: int, player2_pos: int, player2_score: int) -> (
        int, int
):
    p1_wins, p2_wins = 0, 0
    limit = 21
    for p1_move, p1_qty in [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]:
        next_player1_pos = move_player(player1_pos, p1_move)
        next_p1_score = player1_score + next_player1_pos

        if next_p1_score >= limit:
            p1_wins += p1_qty
            continue

        for p2_move, p2_qty in [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]:
            next_player2_pos = move_player(player2_pos, p2_move)
            next_p2_score = player2_score + next_player2_pos

            if next_p2_score >= limit:
                p2_wins += p2_qty * p1_qty
                continue

            p1_win, p2_win = play_dirac_game(next_player1_pos, next_p1_score, next_player2_pos, next_p2_score)
            p1_wins += p1_win * p1_qty * p2_qty
            p2_wins += p2_win * p1_qty * p2_qty

    return p1_wins, p2_wins


def move_player(pos: int, move: int) -> int:
    return (pos + move - 1) % 10 + 1


def phase2_1(players_pos):
    player_wins = [[], []]
    sequences = [(c,) for c in range(3, 10)]
    while len(sequences) > 0:
        winning_seqs = set()
        for seq in sequences:
            winner = play_sequence(seq, players_pos)
            if winner is not None:
                player_wins[winner].append(calc_universes(seq))
                winning_seqs.add(seq)
        sequences = generate([s for s in sequences if s not in winning_seqs])

    wins_ = [sum(universes) for universes in player_wins]
    counts_ = [len(universes) for universes in player_wins]
    print(wins_)
    print(counts_)
    return max(wins_)


def generate(sequences):
    resp = []
    if len(sequences) > 0:
        print(f"generating {len(sequences)} s {len(sequences[0])} d)")
    for seq in sequences:
        for val in [(c,) for c in range(3, 10)]:
            resp.append(seq + val)
    return resp


version_dict = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}


def calc_universes(seq):
    return math.prod([version_dict[roll] for roll in seq])
    # return 1


def play_sequence(roll_seq, players_pos):
    players_score = [0, 0]
    player = 0
    # print(roll_seq)
    for roll in roll_seq:
        players_pos[player] = (players_pos[player] + roll) % 10
        players_score[player] += players_pos[player] + 1
        # print(players_score)
        if players_score[player] > 21:
            # print(f"winner {player} seq={roll_seq}")
            return player
        player = (player + 1) % 2
    return None


def roll_dice(dice, num_rolls):
    res = 0
    for i in range(num_rolls):
        res += dice + 1 + i
    return res


if __name__ == "__main__":
    players_pos = [3, 7] if TEST_MODE else [2, 9]
    print(phase1(players_pos))
    print(phase2(4, 8) if TEST_MODE else phase2(3, 10))

    # print(play_sequence([6, 15, 24, 33, 42, 51, 60], [3, 7]))
    # print(generate([(9, 3,), (6, 1,)]))
