

class Settings:
    def __init__(self):
        BLUE = (0, 0, 255)
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        # Game settings
        self.screen_height = 600
        self.screen_width = 800
        self.bg_color = BLACK
        self.time_step = 0
        self.running = True
        self.FPS = 300


        # Dot settings
        self.dot_start_x = int(self.screen_width/2)
        self.dot_start_y = int(self.screen_height - 50)
        self.dot_radius = 5
        self.dot_color = WHITE
        self.list_length = 5000
        self.dot_amount = 100
        self.all_dead = False
        self.gen = 1
        # Dot move list
        # Vector move
        self.moved_up_left = (-1, 1)
        self.moved_up = (0, 1)
        self.moved_up_right = (1, 1)
        self.moved_left = (-1, 0)
        self.moved_right = (1, 0)
        self.moved_down_left = (-1, -1)
        self.moved_down = (0, -1)
        self.moved_down_right = (1, -1)
        # Move list
        self.move_list = [
            self.moved_up_left,
            self.moved_up,
            self.moved_up_right,
            self.moved_left,
            self.moved_right,
            self.moved_down_left,
            self.moved_down,
            self.moved_down_right]

        # Obstacle settings
        self.obstacle_color = RED

        # wall settings
        self.wall_short = 10
        self.wall_long = self.screen_width
        # Top left
        self.top_left_x = 0
        self.top_left_y = 0
        # Top right
        self.top_right_x = self.screen_width - self.wall_short
        self.top_right_y = 0
        # Bottom left
        self.bottom_left_x = 0
        self.bottom_left_y = self.screen_height - self.wall_short

        self.wall_dict = {'x_coordinate': [self.top_left_x, self.top_left_x, self.top_right_x, self.bottom_left_x, 0],
                          'y_coordinate': [self.top_left_y, self.top_left_y, self.top_right_y, self.bottom_left_y, 300],
                          'width': [self.wall_long, self.wall_short, self.wall_short, self.wall_long, 600],
                          'height': [self.wall_short, self.wall_long, self.wall_long, self.wall_short, 15]

                          }

        # Goal settings
        self.goal_color = GREEN
        self.goal_pos_x = int(self.screen_width / 2)
        self.goal_pos_y = 30
        self.goal_radius = self.dot_radius * 2

        # Brain settings
        self.mutate_factor = int(self.list_length * 0.10)
