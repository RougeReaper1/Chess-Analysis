import chess.pgn
import chess.engine
import pandas as pd
import numpy as np
from concurrent.futures import ProcessPoolExecutor

# Function to analyze blunders using Stockfish
def analyze_blunders(game_data):
    game, stockfish_path = game_data
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    
    board = game.board()
    blunders = 0
    move_num = 0
    
    # Iterate over the moves in the game
    for move in game.mainline_moves():
        board.push(move)
        move_num += 1
        if move_num < 20:  # Exclude games with fewer than 20 moves
            continue
        
        # Evaluate position using Stockfish
        info = engine.analyse(board, chess.engine.Limit(depth=10))
        score = info['score'].relative
        
        # Check for blunders (2 pawn drop or more)
        if score.is_mate():
            continue  # Skip positions with checkmate
        if abs(score.score()) > 200:  # 200 centipawns = 2 pawns
            blunders += 1
    print(f"Processing game {game.headers.get('White')} vs {game.headers.get('Black')} at move {move_num}")
  
    engine.quit()  # Ensure the engine is properly closed
    return blunders

# Parse games from the PGN file
def parse_pgn_games(pgn_file, max_games_per_time_control = 110000):
    games = {'bullet': [], 'blitz': [], 'classical': []}
    time_controls = {'bullet': 0, 'blitz': 0, 'classical': 0}
    results = []
    
    while True:
        game = chess.pgn.read_game(pgn_file)
        if game is None:
            break
        
        time_control = game.headers.get("TimeControl", "classical")
        if '60' in time_control:
            time_control = 'bullet'
        elif '300' in time_control:
            time_control = 'blitz'
        else:
            time_control = 'classical'
        
        print(f"Detected Time Control: {time_control}")  # Debugging print statement
        
        if time_controls[time_control] < max_games_per_time_control:
            games[time_control].append(game)
            time_controls[time_control] += 1
            results.append(game.headers.get("Result", "*"))
            
            # Print progress
            print(f"Added game to {time_control}. Count: {time_controls[time_control]}")
        
        # Stop if all time controls have reached their limits
        if all(count >= max_games_per_time_control for count in time_controls.values()):
            break
        print(f"Processed {len(results)} games")
    
    # Print the number of games collected for each time control
    print("Final count of games in each time control category:")
    for tc, count in time_controls.items():
        print(f"{tc.capitalize()}: {count} games")
    
    return games, results

def main():
    stockfish_path = ""
    pgn_file = open(eg:- 'Chess_Data.pgn')  #Only accepts Pgn (Portable Chess Notation) Format
    
    # Parse PGN games
    games_dict, results = parse_pgn_games(pgn_file, max_games_per_time_control=50000)
    
    # Flatten the list of games and assign time controls
    games = []
    time_controls = []
    for time_control, game_list in games_dict.items():
        games.extend(game_list)
        time_controls.extend([time_control] * len(game_list))
    
    # Use ProcessPoolExecutor for parallel analysis
    with ProcessPoolExecutor(max_workers=16) as executor: 
        game_data = [(game, stockfish_path) for game in games]
        blunders_list = list(executor.map(analyze_blunders, game_data))
    
    # Combine results into a DataFrame
    data = pd.DataFrame({
        'time_control': time_controls,
        'result': results,
        'blunders': blunders_list
    })
    
    # Filter games based on time control
    data['time_control_value'] = data['time_control'].apply(lambda x: 'bullet' if x == 'bullet' else 'blitz' if x == 'blitz' else 'classical')
    
    # Compute statistics
    def calculate_stats(subset):
        total_games = len(subset)
        wins = len(subset[subset['result'].isin(['1-0', '0-1'])])
        draws = len(subset[subset['result'] == '1/2-1/2'])
        blunder_avg = np.mean(subset['blunders'])
        
        win_rate = wins / total_games * 100 if total_games > 0 else 0
        draw_rate = draws / total_games * 100 if total_games > 0 else 0
        
        return win_rate, draw_rate, blunder_avg



    for label, time_control in zip(['Bullet', 'Blitz', 'Classical'], ['bullet', 'blitz', 'classical']):
        subset = data[data['time_control_value'] == time_control]
        win_rate, draw_rate, blunder_avg = calculate_stats(subset)
        print(f"{label} - Win Rate: {win_rate:.2f}%, Draw Rate: {draw_rate:.2f}%, Avg. Blunders: {blunder_avg:.2f}")

    # Pearson correlation between time control and blunders
    time_control_mapping = {'bullet': 1, 'blitz': 3, 'classical': 30}
    data['time_control_numeric'] = data['time_control_value'].map(time_control_mapping)
    blunder_corr = data[['time_control_numeric', 'blunders']].corr(method='pearson').iloc[0, 1]
    print(f"Pearson Correlation (Time Control vs Blunders): {blunder_corr:.2f}")


if __name__ == '__main__':
    main()