from display import Display
from stage import LevelStage

def load_level_and_move():
    st = LevelStage()
    st.load_level(1)
    st.show_in_cmd()
    for direction in [1, 1, 3, 3, 1, 2, 2, 4, 4, 4, 3, 3, 3]:
        st.move(direction)
        print("="*60)
        st.show_in_cmd()

def level_1_game_win():
    st = LevelStage()
    st.load_level(1)
    for direction in [3, 1, 2, 2, 4, 1, 1, 3, 4, 4]:
        st.player_direction_signal_handler(direction)

def undo_redo():
    st = LevelStage()
    st.load_level(1)
    st.show_in_cmd()
    print("="*60)
    st.player_direction_signal_handler(1)
    st.show_in_cmd()
    print("="*60)
    for dummy in range(2):
        st.undo()
        st.show_in_cmd()
        print("="*60)
    for dummy in range(2):
        st.redo()
        st.show_in_cmd()
        print("="*60)
    st.undo()
    for dummy in range(2):
        st.player_direction_signal_handler(3)
    st.show_in_cmd()
    print("="*60)
    for dummy in range(2):
        st.undo()
        st.show_in_cmd()
        print("="*60)
    for dummy in range(2):
        st.redo()
        st.show_in_cmd()
        print("="*60)

def test_restart():
    st = LevelStage()
    st.load_level(1)
    st.show_in_cmd()
    print("="*60)
    st.player_direction_signal_handler(2)
    st.player_direction_signal_handler(2)
    st.player_direction_signal_handler(2)
    st.show_in_cmd()
    print("="*60)
    st.restart_level()
    st.show_in_cmd()

def test_stage_show():
    d = Display()
    d.load_level(1)

if __name__ == "__main__":
    test_stage_show()
