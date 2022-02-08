from abc import update_abstractmethods
from stage import LevelStage
import pygame

class Display:
    """
        显示游戏界面的窗口
    """
    def __init__(self):
        self.stage = LevelStage()
        self.init_img_src()

    def init_img_src(self):
        """
            初始化图像素材
        """
        self.player_gif_img_list = [pygame.image.load("./img/player_gif/player_1.png"), pygame.image.load("./img/player_gif/player_2.png")]
        self.aim_pos_img = pygame.image.load("./img/aim_pos.png")
        self.box_img = pygame.image.load("./img/box.png")
        self.box_complete_img = pygame.image.load("./img/box_complete.png")
        self.carpet_img = pygame.image.load("./img/carpet.png")
        self.wall_img = pygame.image.load("./img/wall.png")

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
        self.grid_size = 50
        self.screen_size = (self.stage.get_map_size()[0] * self.grid_size, self.stage.get_map_size()[1] * self.grid_size)
        # 初始化图形界面
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.main_loop()

    def main_loop(self):
        """
            图形界面的主循环
        """
        self.time_stamp = 0
        self.fps = 60
        while True:
            events = pygame.event.get()
            for event in events:
                if(event.type == pygame.QUIT):
                    exit()
            # 绘制游戏界面
            self.game_stage_draw()
            pygame.display.update()
            # 更新时间戳
            self.update_time_stamp()

    def update_time_stamp(self):
        pygame.time.delay(int(1 / self.fps))
        self.time_stamp += 1
        self.time_stamp = self.time_stamp % self.fps

    def game_stage_draw(self):
        """
            绘制游戏界面
        """
        # 初始化-黑屏
        self.screen.fill((0,0,0))
        # 绘制地毯/墙壁/目标点
        carpet_rect = self.carpet_img.get_rect()
        wall_rect = self.wall_img.get_rect()
        aim_pos_rect = self.aim_pos_img.get_rect()
        level_map = self.stage.level_map
        [level_map_width, level_map_height] = self.stage.get_map_size()
        for i in range(level_map_height):
            for j in range(level_map_width):
                if(level_map[i][j] == 'C'):
                    img_list = [self.carpet_img]
                    rect_list = [carpet_rect]
                elif(level_map[i][j] == "X"):
                    img_list = [self.wall_img]
                    rect_list = [wall_rect]
                elif(level_map[i][j] == "H"):
                    img_list = [self.carpet_img, self.aim_pos_img]
                    rect_list = [carpet_rect, aim_pos_rect]
                else:
                    continue
                centerx = self.grid_size * (0.5 + j)
                centery = self.grid_size * (0.5 + i)
                for img, rect in zip(img_list, rect_list):
                    rect.centerx = centerx
                    rect.centery = centery
                    self.screen.blit(img, rect)
