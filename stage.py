import json
import numpy as np

class levelStage:
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
    """
    def __init__(self):
        self.level_map = "XXX\nX0X\nXXX"
        self.player_pos = [1, 1]
        self.box_pos_list = []
        self.level_file_path = "levelConfig.json"

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
