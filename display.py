from stage import LevelStage
import pygame

class Display:
    """
        显示游戏界面的窗口
    """
    def __init__(self):
        self.stage = LevelStage()

    def load_level(self, level_id):
        """
            读取关卡，读取完成后初始化图形界面

            Parameters
            ----------
            level_id : int
                关卡id
        """
        # 读取关卡
        self.stage.load_level(level_id)
        grid_size = 50
        self.screen_size = (self.stage.get_map_size()[0] * grid_size, self.stage.get_map_size()[1] * grid_size)
        # 初始化图形界面
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.main_loop()

    def main_loop(self):
        """
            图形界面的主循环
        """
        while True:
            events = pygame.event.get()
            for event in events:
                if(event.type == pygame.QUIT):
                    exit()
            # 绘制游戏界面
            self.game_stage_draw()
            pygame.display.update()

    def game_stage_draw(self):
        """
            绘制游戏界面
        """
        pass
