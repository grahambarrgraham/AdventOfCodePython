import itertools
from pathlib import Path
import sys
import re
import collections
import numpy as np
import plotting

Valve = collections.namedtuple("Valve", "name, rate, tunnels")

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):
    return v


def phase2(v):
    return -1


def parse(line):
    pattern = re.compile("Valve (.+) has flow rate=(.+); tunnels* leads* to valves* (.+)")
    m = pattern.match(line)
    tunnels = m.group(3).split(", ")
    return Valve(m.group(1), int(m.group(2)), tunnels)


def create_epsilon_greedy_policy(q_function, epsilon, num_actions):
    """
    Creates an epsilon-greedy policy based
    on a given Q-function and epsilon.

    Returns a function that takes the state
    as an input and returns the probabilities
    for each action in the form of a numpy array
    of length of the action space(set of possible actions).
    """

    def policy_function(state):
        action_probabilities = np.ones(num_actions, dtype=float) * epsilon / num_actions
        best_action = np.argmax(q_function[state])
        action_probabilities[best_action] += (1.0 - epsilon)
        return action_probabilities

    return policy_function


def q_learning(env, num_episodes, discount_factor=1.0, alpha=0.6, epsilon=0.1):
    """
    Q-Learning algorithm: Off-policy TD control.
    Finds the optimal greedy policy while improving
    following an epsilon-greedy policy"""

    # Action value function
    # A nested dictionary that maps
    # state -> (action -> action-value).
    q_function = collections.defaultdict(lambda: np.zeros(env.action_space.n))

    # Keeps track of useful statistics
    stats = plotting.EpisodeStats(
        episode_lengths=np.zeros(num_episodes),
        episode_rewards=np.zeros(num_episodes))

    # Create an epsilon greedy policy function
    # appropriately for environment action space
    policy = create_epsilon_greedy_policy(q_function, epsilon, env.action_space.n)

    # For every episode
    for ith_episode in range(num_episodes):

        # Reset the environment and pick the first action
        state = env.reset()

        for t in itertools.count():

            # get probabilities of all actions from current state
            action_probabilities = policy(state)

            # choose action according to
            # the probability distribution
            action = np.random.choice(np.arange(
                len(action_probabilities)),
                p=action_probabilities)

            # take action and get reward, transit to next state
            next_state, reward, done, _ = env.step(action)

            # Update statistics
            stats.episode_rewards[ith_episode] += reward
            stats.episode_lengths[ith_episode] = t

            # TD Update
            best_next_action = np.argmax(q_function[next_state])
            td_target = reward + discount_factor * q_function[next_state][best_next_action]
            td_delta = td_target - q_function[state][action]
            q_function[state][action] += alpha * td_delta

            # done is True if episode terminated
            if done:
                break

            state = next_state

    return q_function, stats


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day16_sample" if TEST_MODE else "input/day16").open() as f:
        values = [parse(i.strip()) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
