import chess
import chess.svg
import streamlit as st
from autogen import ConversableAgent, register_function

if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = None
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
if "made_move" not in st.session_state:
    st.session_state.made_move = False
if "board_svg" not in st.session_state:
    st.session_state.board_svg = None
if "move_history" not in st.session_state:
    st.session_state.move_history = []
if "max_turns" not in st.session_state:
    st.session_state.max_turns = 5
if "white_level" not in st.session_state:
    st.session_state.white_level = "Expert"
if "black_level" not in st.session_state:
    st.session_state.black_level = "Expert"

# Custom CSS to make the selectbox containers wider
st.markdown("""
    <style>
    div[data-baseweb="select"] > div {
        min-width: 200px;
    }
    </style>
""", unsafe_allow_html=True)

# Create a container for the top-right level selectors
_, _, level_col1, level_col2 = st.columns([0.5, 0.5, 1.5, 1.5])

with level_col1:
    white_level = st.selectbox(
        "White AI Difficulty",
        ["Beginner (800-1200 rating)", "Intermediate (1200 rating)", "Expert (2000 rating)", "GrandMaster (2200 rating)"],
        index=2,
        key="white_level_select"
    )
    st.session_state.white_level = white_level

with level_col2:
    black_level = st.selectbox(
        "Black AI Difficulty",
        ["Beginner (800-1200 rating)", "Intermediate (1200 rating)", "Expert (2000 rating)", "GrandMaster (2200 rating)"],
        index=2,
        key="black_level_select"
    )
    st.session_state.black_level = black_level

# Main title
st.title("Chess with AutoGen Agents")

st.sidebar.title("Chess Agent Configuration")
# openai_api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")
# if openai_api_key:
#     st.session_state.openai_api_key = openai_api_key
#     st.sidebar.success("API key saved!")

st.sidebar.info("""
For a complete chess game with potential checkmate, it would take max_turns > 200 approximately.
However, this will consume significant API credits and a lot of time.
For demo purposes, using 5-10 turns is recommended.
""")

max_turns_input = st.sidebar.number_input(
    "Enter the number of turns (max_turns):",
    min_value=1,
    max_value=1000,
    value=st.session_state.max_turns,
    step=1
)

if max_turns_input:
    st.session_state.max_turns = max_turns_input
    st.sidebar.success(f"Max turns of total chess moves set to {st.session_state.max_turns}!")

# Add Coming Soon section in sidebar
st.sidebar.markdown("---")  # Separator line
st.sidebar.markdown("### Coming Soon")

# Custom CSS for disabled buttons with hover effect
st.markdown("""
    <style>
    .disabled-button {
        background-color: #808080;
        color: #ffffff;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        margin: 5px 0;
        width: 100%;
        opacity: 0.6;
        cursor: not-allowed !important;
        position: relative;
    }
    
    .disabled-button:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        left: 100%;
        top: 50%;
        transform: translateY(-50%);
        background-color: #333;
        color: white;
        padding: 5px;
        border-radius: 5px;
        font-size: 12px;
        white-space: nowrap;
        margin-left: 10px;
        z-index: 1;
    }
    </style>
""", unsafe_allow_html=True)

# Add disabled buttons with hover tooltips
st.sidebar.markdown("""
    <button class="disabled-button">
        Create Your Agent
    </button>
    
    <button class="disabled-button">
        Agent Progress Tracker
    </button>
    
    <button class="disabled-button">
        Competition Mode
    </button>
""", unsafe_allow_html=True)

def available_moves() -> str:
    available_moves = [str(move) for move in st.session_state.board.legal_moves]
    return "Available moves are: " + ",".join(available_moves)

def execute_move(move: str) -> str:
    try:
        chess_move = chess.Move.from_uci(move)
        if chess_move not in st.session_state.board.legal_moves:
            return f"Invalid move: {move}. Please call available_moves() to see valid moves."
        
        # Update board state
        st.session_state.board.push(chess_move)
        st.session_state.made_move = True

        # Generate and store board visualization
        board_svg = chess.svg.board(st.session_state.board,
                                  arrows=[(chess_move.from_square, chess_move.to_square)],
                                  fill={chess_move.from_square: "gray"},
                                  size=400)
        st.session_state.board_svg = board_svg
        st.session_state.move_history.append(board_svg)

        # Get piece information
        moved_piece = st.session_state.board.piece_at(chess_move.to_square)
        piece_unicode = moved_piece.unicode_symbol()
        piece_type_name = chess.piece_name(moved_piece.piece_type)
        piece_name = piece_type_name.capitalize() if piece_unicode.isupper() else piece_type_name
        
        # Generate move description
        from_square = chess.SQUARE_NAMES[chess_move.from_square]
        to_square = chess.SQUARE_NAMES[chess_move.to_square]
        move_desc = f"Moved {piece_name} ({piece_unicode}) from {from_square} to {to_square}."
        if st.session_state.board.is_checkmate():
            winner = 'White' if st.session_state.board.turn == chess.BLACK else 'Black'
            move_desc += f"\nCheckmate! {winner} wins!"
        elif st.session_state.board.is_stalemate():
            move_desc += "\nGame ended in stalemate!"
        elif st.session_state.board.is_insufficient_material():
            move_desc += "\nGame ended - insufficient material to checkmate!"
        elif st.session_state.board.is_check():
            move_desc += "\nCheck!"

        return move_desc
    except ValueError:
        return f"Invalid move format: {move}. Please use UCI format (e.g., 'e2e4')."

def check_made_move(msg):
    if st.session_state.made_move:
        st.session_state.made_move = False
        return True
    else:
        return False

if st.session_state.openai_api_key:
    try:
        agent_white_config_list = [
            {
                "model": "gpt-4o-mini",
                "api_key": st.session_state.openai_api_key,
            },
        ]

        agent_black_config_list = [
            {
                "model": "gpt-4o-mini",
                "api_key": st.session_state.openai_api_key,
            },
        ]

        agent_white = ConversableAgent(
            name="Agent_White",  
            system_message="You are a professional chess player and you play as white. "
            "First call available_moves() first, to get list of legal available moves. "
            "Then call execute_move(move) to make a move.",
            llm_config={"config_list": agent_white_config_list, "cache_seed": None},
        )

        agent_black = ConversableAgent(
            name="Agent_Black",  
            system_message="You are a professional chess player and you play as black. "
            "First call available_moves() first, to get list of legal available moves. "
            "Then call execute_move(move) to make a move.",
            llm_config={"config_list": agent_black_config_list, "cache_seed": None},
        )

        game_master = ConversableAgent(
            name="Game_Master",  
            llm_config=False,
            is_termination_msg=check_made_move,
            default_auto_reply="Please make a move.",
            human_input_mode="NEVER",
        )

        register_function(
            execute_move,
            caller=agent_white,
            executor=game_master,
            name="execute_move",
            description="Call this tool to make a move.",
        )

        register_function(
            available_moves,
            caller=agent_white,
            executor=game_master,
            name="available_moves",
            description="Get legal moves.",
        )

        register_function(
            execute_move,
            caller=agent_black,
            executor=game_master,
            name="execute_move",
            description="Call this tool to make a move.",
        )

        register_function(
            available_moves,
            caller=agent_black,
            executor=game_master,
            name="available_moves",
            description="Get legal moves.",
        )

        agent_white.register_nested_chats(
            trigger=agent_black,
            chat_queue=[
                {
                    "sender": game_master,
                    "recipient": agent_white,
                    "summary_method": "last_msg",
                }
            ],
        )

        agent_black.register_nested_chats(
            trigger=agent_white,
            chat_queue=[
                {
                    "sender": game_master,
                    "recipient": agent_black,
                    "summary_method": "last_msg",
                }
            ],
        )

        st.info("""
This chess game is played between two AG2 AI agents:
- **Agent White**: A GPT-4o-mini powered chess player controlling white pieces
- **Agent Black**: A GPT-4o-mini powered chess player controlling black pieces

The game is managed by a **Game Master** that:
- Validates all moves
- Updates the chess board
- Manages turn-taking between players
- Provides legal move information
""")

        initial_board_svg = chess.svg.board(st.session_state.board, size=300)
        st.subheader("Initial Board")
        st.image(initial_board_svg)

        if st.button("Start Game"):
            st.session_state.board.reset()
            st.session_state.made_move = False
            st.session_state.move_history = []
            st.session_state.board_svg = chess.svg.board(st.session_state.board, size=300)
            st.info("The AI agents will now play against each other. Each agent will analyze the board, " 
                   "request legal moves from the Game Master (proxy agent), and make strategic decisions.")
            st.success("You can view the interaction between the agents in the terminal output, after the turns between agents end, you get view all the chess board moves displayed below!")
            st.write("Game started! White's turn.")

            chat_result = agent_black.initiate_chat(
                recipient=agent_white, 
                message="Let's play chess! You go first, its your move.",
                max_turns=st.session_state.max_turns,
                summary_method="reflection_with_llm"
            )
            st.markdown(chat_result.summary)

            # Display the move history (boards for each move)
            st.subheader("Move History")
            for i, move_svg in enumerate(st.session_state.move_history):
                # Determine which agent made the move
                if i % 2 == 0:
                    move_by = "Agent White"  # Even-indexed moves are by White
                else:
                    move_by = "Agent Black"  # Odd-indexed moves are by Black
                
                st.write(f"Move {i + 1} by {move_by}")
                st.image(move_svg)

        if st.button("Reset Game"):
            st.session_state.board.reset()
            st.session_state.made_move = False
            st.session_state.move_history = []
            st.session_state.board_svg = None
            st.write("Game reset! Click 'Start Game' to begin a new game.")

    except Exception as e:
        st.error(f"An error occurred: {e}. Please check your API key and try again.")

else:
    st.warning("Please choose your ai agent ratings before starting the game.")