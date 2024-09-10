# Chess-Analysis
Chess Blunder Analysis Using Stockfish
This project analyzes chess games by detecting blunders using the Stockfish chess engine. The games are categorized based on their time control (Bullet, Blitz, and Classical) and evaluated for blunder frequency. Additionally, statistical analysis is performed to compute win rates, draw rates, and blunder frequency across different time controls. Pearson correlation is used to study the relationship between time control length and blunders.

Requirements:
Python 3.x
Chess: A Python package for working with chess games, boards, and engines.
Stockfish: A powerful chess engine for analyzing positions.
Pandas: For data manipulation and analysis.
Numpy: For numerical operations.
Concurrent Futures: For parallel processing to speed up the analysis of large datasets.
Required Python Libraries
You can install the required libraries using pip:
pip install chess pandas numpy

Stockfish Chess Engine
You will need to download and set up Stockfish on your system. Ensure that the path to the Stockfish executable is correct in the code.
Download Stockfish from the official Stockfish website.
Unzip the downloaded file.
In the main() function, provide the correct path to the Stockfish executable file on your system.

PGN File
This program processes Portable Game Notation (PGN) chess files. Ensure you have a valid PGN file containing the chess games you want to analyze.

How to Use
1. Modify the Script
Ensure that you provide the correct file paths for:

The Stockfish executable (stockfish_path in the script).
The PGN file containing the chess games (pgn_file).
stockfish_path = "path_to_stockfish"
pgn_file = open("path_to_your_pgn_file.pgn")

2. Run the Script
Once the paths are correctly set, you can run the script in your Python environment.

python chess_blunder_analysis.py

3. Output
The script will:

Parse the PGN file, identifying games and their respective time controls.
Use Stockfish to analyze each game for blunders (moves that cause a significant drop in material, equivalent to two pawns or more).
Calculate statistics like win rates, draw rates, and the average number of blunders for each time control.
Print the results for each time control:
Win Rate
Draw Rate
Average Blunders

Calculate the Pearson correlation between time control length and blunders, and print the correlation coefficient.

Bullet - Win Rate: 96.55%, Draw Rate: 3.45%, Avg. Blunders: 27.80
Blitz - Win Rate: 96.54%, Draw Rate: 3.46%, Avg. Blunders: 26.69
Classical - Win Rate: 96.52%, Draw Rate: 3.48%, Avg. Blunders: 26.60
Pearson Correlation (Time Control vs Blunders): -0.01

How It Works:
Functions
analyze_blunders(game_data):

Analyzes each chess game for blunders using Stockfish.
Blunders are identified as moves that cause a significant drop in evaluation score (greater than 200 centipawns, equivalent to 2 pawns).
parse_pgn_games(pgn_file, max_games_per_time_control):

Parses games from the provided PGN file and categorizes them into Bullet, Blitz, and Classical based on the time control.
Limits the number of games analyzed per time control to avoid excessive processing time.
calculate_stats(subset):

Computes win rates, draw rates, and average blunders for a subset of games.
Parallel Processing
To speed up the analysis of large datasets, the script uses ProcessPoolExecutor from the concurrent.futures library to analyze multiple games in parallel.

Customization
Adjust Time Control Categories: You can change the time control criteria in the parse_pgn_games() function. For example, the script currently categorizes games based on their time control:

Bullet: 60 seconds or less per player.
Blitz: Between 60 and 300 seconds per player.
Classical: More than 300 seconds.

Max Games Per Time Control: The max_games_per_time_control argument can be adjusted to limit or increase the number of games analyzed for each time control.

Known Issues
Ensure that Stockfish is properly configured and that the correct path is provided.
The PGN file needs to be valid and follow standard chess notation for the parser to work.
Large datasets may require significant computational resources and time to process, though parallelization helps mitigate this.
