from stage import levelStage

def load_level_and_move():
    st = levelStage()
    st.load_level(1)
    st.show_in_cmd()
    for direction in [1, 1, 3, 3, 1, 2, 2, 4, 4, 4, 3, 3, 3]:
        st.move(direction)
        print("="*60)
        st.show_in_cmd()

def level_1_game_win():
    st = levelStage()
    st.load_level(1)
    for direction in [3, 1, 2, 2, 4, 1, 1, 3, 4, 4]:
        st.player_direction_signal_handler(direction)

if __name__ == "__main__":
    level_1_game_win()
