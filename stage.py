import json
import numpy as np

class LevelStage:
    """
        level场景类

        Attributes
        ----------
        level_map : char[][]
            地图
        player_pos : int[2]
            玩家位置（行、列）
        box_pos_list : int[][2]
            各个箱子的位置（行、列）
        level_file_path : str
            level文件的路径
        undo_stack : list[][]
            用于撤销操作的栈（格式见注释最下方Info）
        redo_stack : list[][]
            用于重复操作的栈（格式见注释最下方Info）
        level_id : int
            当前所处的关卡编号
        
        Info
        ----
        undo/redo栈的格式：
        [[[-1（表示玩家）, [玩家上/下一步的行坐标, 玩家上/下一步的列坐标]],
         [（被移动的箱子的index）, [箱子上/下一步的行坐标, 箱子上/下一步的列坐标]]], ...]
    """
    def __init__(self):
        self.level_map = np.array(["XXX", "X0X", "XXX"])
        self.player_pos = [1, 1]
        self.box_pos_list = []
        self.level_file_path = "levelConfig.json"
        self.undo_stack = []
        self.redo_stack = []
        self.level_id = -1

    def load_level_map(self, level_map_file_path):
        """
            从level map文件中读取地图

            Parameters
            ----------
            level_map_file_path : str
                level map文件路径
        """
        level_map_file_path = np.loadtxt(level_map_file_path, dtype=str)
        return level_map_file_path

    def load_level(self, level_id):
        """
            从level文件中读取相应的level，初始化场景

            level文件的结构:
            ```
            [
                {
                    "level_id" : xxx,
                    "level_info" :
                    {
                        "level_map" : mapFilePath,
                        "player_pos" : [i, j],
                        "box_pos_list" : [[i1, j1], [i2, j2], ..., [in, jn]]
                    }
                }, ...
            ]
            ```

            地图文件的结构:
            ```
            XXXXXX
            XCCHXX
            XXXXX0
            ```
            X为障碍物，0为空气，C为地毯，H为箱子的目标位置

            Parameters
            ----------
            level_id : int
                level编号
        """
        with open(self.level_file_path, "r") as f:
            data = json.load(f)[level_id]
        self.level_map = self.load_level_map(data["level_info"]["level_map"])
        self.player_pos = data["level_info"]["player_pos"]
        self.box_pos_list = data["level_info"]["box_pos_list"]
        self.level_id = level_id

    def get_map_size(self):
        """
            获取地图的尺寸（单位：grid）

            Returns
            -------
            width : int
                宽
            height : int
                高
        """
        width = len(self.level_map[0])
        height = len(self.level_map)
        return [width, height]

    def restart_level(self):
        """
            重开本关
        """
        self.load_level(self.level_id)

    def move(self, direction):
        """
            玩家向某个指定的方向移动

            Parameters
            ----------
            direction : int
                移动方向的编号，其中：
                1 —— 上
                2 —— 左
                3 —— 下
                4 —— 右
        """
        # 编号转方向分量
        if(direction == 1):
            i = -1
            j = 0
        elif(direction == 2):
            i = 0
            j = -1
        elif(direction == 3):
            i = 1
            j = 0
        elif(direction == 4):
            i = 0
            j = 1
        # 玩家本该移动到的新位置
        new_pos = [self.player_pos[0]+i, self.player_pos[1]+j]
        # 如果是箱子，则判断箱子能否被推动
        if(new_pos in self.box_pos_list):
            box_new_pos = [new_pos[0]+i, new_pos[1]+j]
            # 如果箱子前面还是箱子，则不能推动
            if(box_new_pos in self.box_pos_list):
                return
            else:
                # 如果箱子前面是空气/传动点，则可以推动
                if(self.level_map[box_new_pos[0]][box_new_pos[1]] in ['C', 'H']):
                    # 将当前玩家和箱子所在位置添加到undo栈中，方便撤销操作
                    box_idx = self.box_pos_list.index(new_pos)
                    self.undo_stack.append([[-1, self.player_pos], [box_idx, self.box_pos_list[box_idx]]])
                    # 更新玩家位置
                    self.player_pos = new_pos
                    # 更新箱子位置
                    self.box_pos_list[box_idx] = box_new_pos
                # 否则不能推动
                else:
                    return
        # 如果是墙壁，则不能移动
        elif(self.level_map[new_pos[0]][new_pos[1]] == 'X'):
            return
        # 如果是空气/传动点，则可以移动
        elif(self.level_map[new_pos[0]][new_pos[1]] in ['C', 'H']):
            # 将当前玩家所在位置添加到undo栈中，方便撤销操作
            self.undo_stack.append([[-1, self.player_pos]])
            # 更新玩家位置
            self.player_pos = new_pos
        # 如果移动成功，则将redo栈清空，因为这种情况下就不能redo了
        self.redo_stack = []
        return

    def undo(self):
        """
            撤销操作
        """
        if(len(self.undo_stack) != 0):
            undo_info = self.undo_stack[-1]
            new_redo_info = []
            for each_undo_obj in undo_info:
                if(each_undo_obj[0] == -1):
                    new_redo_info.append([-1, self.player_pos])
                    self.player_pos = each_undo_obj[1]
                else:
                    box_idx = each_undo_obj[0]
                    new_redo_info.append([box_idx, self.box_pos_list[box_idx]])
                    self.box_pos_list[box_idx] = each_undo_obj[1]
            self.redo_stack.append(new_redo_info)
            self.undo_stack = self.undo_stack[:-1]

    def redo(self):
        """
            重做操作
        """
        if(len(self.redo_stack) != 0):
            redo_info = self.redo_stack[-1]
            new_undo_info = []
            for each_redo_obj in redo_info:
                if(each_redo_obj[0] == -1):
                    new_undo_info.append([-1, self.player_pos])
                    self.player_pos = each_redo_obj[1]
                else:
                    box_idx = each_redo_obj[0]
                    new_undo_info.append([box_idx, self.box_pos_list[box_idx]])
                    self.box_pos_list[box_idx] = each_redo_obj[1]
            self.undo_stack.append(new_undo_info)
            self.redo_stack = self.redo_stack[:-1]

    def is_game_win(self):
        """
            判断是否通关

            Returns
            -------
            True / False
        """
        flag = True
        for each_box_pos in self.box_pos_list:
            if(self.level_map[each_box_pos[0]][each_box_pos[1]] != 'H'):
                flag = False
                break
        return flag

    def player_direction_signal_handler(self, direction):
        """
            处理：玩家发出的方向信号

            Returns
            -------
            Ture / False : 是否游戏胜利
        """
        self.move(direction=direction)
        if(self.is_game_win()):
            print("Game Win!")
            return True
        return False

    def show_in_cmd(self):
        """
            在命令行中打印出当前的场景状态，用于调试
        """
        for i, eachLine in enumerate(self.level_map):
            for j, eachColumn in enumerate(eachLine):
                if([i, j] == self.player_pos):
                    each_char = 'P'
                elif([i, j] in self.box_pos_list):
                    each_char = '+'
                else:
                    if(eachColumn == 'X'):
                        each_char = '#'
                    elif(eachColumn in ['0', 'C']):
                        each_char = ' '
                    elif(eachColumn == 'H'):
                        each_char = '.'
                print(each_char, end="\t")
            print("")
