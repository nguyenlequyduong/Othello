import random
import time

from ai.search_algorithms.search_algorithm import SearchAlgorithm
from engine.GameState import GameState
from engine.Move import Move


class Minimax(SearchAlgorithm):
    """Implements the Minimax algorithm."""

    def find_move(self, game_state: GameState, depth: int) -> (int, int):
        self.start_time = time.time()
        best_score = float('-inf') if game_state.current_player == 'W' else float('inf')
        best_move = None
        candidate_best_move = []
        for move in Move.get_valid_moves(game_state):
            next_state = self.create_copy(game_state)
            Move.make_move(next_state, move)
            score = self.minimax(next_state, depth, game_state.current_player == 'W')
            if game_state.current_player == 'W' and score > best_score:
                best_score = score
                best_move = move
                candidate_best_move.clear()
                candidate_best_move.append(move)
            elif game_state.current_player == 'B' and score < best_score:
                best_score = score
                best_move = move
                candidate_best_move.clear()
                candidate_best_move.append(move)
            else:
                candidate_best_move.append(move)
        if candidate_best_move:
            best_move = random.choice(candidate_best_move)
        return best_move

    def minimax(self, game_state: GameState, depth: int, is_maximizing: bool) -> int:
        """Minimax algorithm.
        Looks ahead to the end of the game tree and evaluates the game state.
        Selects the move that maximizes the score for the current player and minimizes the score for the opponent.
        Stops searching after reaching the maximum depth or when the game is over or after 0.5 seconds.
        """
        if depth == 0 or game_state.is_game_over() or time.time() - self.start_time > 0.5:
            return self.evaluate(game_state)

        if is_maximizing:
            best_score = float('-inf')
            for move in Move.get_valid_moves(game_state):
                next_state = self.create_copy(game_state)
                Move.make_move(next_state, move)
                score = self.minimax(next_state, depth - 1, False)
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in Move.get_valid_moves(game_state):
                next_state = self.create_copy(game_state)
                Move.make_move(next_state, move)
                score = self.minimax(next_state, depth - 1, True)
                best_score = min(score, best_score)
            return best_score
