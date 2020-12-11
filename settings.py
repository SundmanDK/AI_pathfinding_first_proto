class Settings:
    """Global value Storage."""
    def __init__(self):
        """Initial globally encompassing values."""
        # Colors
        BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        RED = (255, 0, 0)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        # Game settings
        self.screen_height = 600
        self.screen_width = 800
        self.bg_color = self.BLACK
        self.time_step = 0
        self.running = True
        self.FPS = 600
        self.allow_update = True

        # Data collection
        self.max_gen = 300  # Number of generations in each run.
        self.runs = 3  # How many runs of a given amount of generations you want.
        self.run_counter = 0  # Keep track of which run is currently in progress
        self.gather_data = False  # Change to True if you want to get a CSV with data on the champions of each generation.

        # Dot settings
        self.dot_start_x = int(self.screen_width/2)
        self.dot_start_y = int(self.screen_height - 50)
        self.dot_radius = 5
        self.dot_color = self.WHITE
        self.champ_color = BLUE
        self.list_length = 7000  # Length of the vector list for the dots' route.
        self.dot_amount = 100  # Number of dots in each generation.
        self.all_dead = False
        self.gen = 1
        self.dot_speed = 5
        self.mutate_steps = 3
        # Dot move list
        self.move_list = [  # List of legal moves.
            (-1, 1),
            (0, 1),
            (1, 1),
            (-1, 0),
            (1, 0),
            (-1, -1),
            (0, -1),
            (1, -1)]
        # Obstacle settings
        self.obstacle_color = RED
        # wall settings
        wall_short = 10
        wall_long = self.screen_width
        # Top left
        top_left_x = 0
        top_left_y = 0
        # Top right
        top_right_x = self.screen_width - wall_short
        top_right_y = 0
        # Bottom left
        bottom_left_x = 0
        bottom_left_y = self.screen_height - wall_short
        # Obstacle 1
        x_1 = 0
        y_1 = 400
        w_1 = 430
        h_1 = wall_short
        # Obstacle 2
        x_2 = 800 - 430
        y_2 = 200
        w_2 = 430
        h_2 = wall_short

        # Dictionary containing info on each wall and boundary.
        self.wall_dict = {'x_coordinate': [top_left_x, top_left_x, top_right_x, bottom_left_x, x_1, x_2],
                          'y_coordinate': [top_left_y, top_left_y, top_right_y, bottom_left_y, y_1, y_2],
                          'width': [wall_long, wall_short, wall_short, wall_long, w_1, w_2],
                          'height': [wall_short, wall_long, wall_long, wall_short, h_1, h_2]
                          }

        # Goal settings
        self.goal_color = self.GREEN
        self.goal_pos_x = int(self.screen_width / 2)
        self.goal_pos_y = 30
        self.goal_radius = self.dot_radius * 2

