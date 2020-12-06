import pygame
import sys
from settings import Settings
from dot import Dot
from obstacles import Obstacle
from brain import Brain


class Game:
    """Main class for organizing and running the program."""
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,
             self.settings.screen_height)
        )
        pygame.display.set_caption("AI Pathfinding")
        self.objects()
        self.dead_dots = []
        self.brain = Brain(self)
        self.gen_counter()

    def run(self):
        """Main loop of the program."""
        while self.settings.running:
            self.check_events()
            self.check_alive()
            self.update_screen()
            if self.settings.allow_update:  # If you press space then the dots stop updating.
                for dot in self.dot_group.sprites():
                    if dot.alive:
                        dot.update()
                self.settings.time_step += 1

            if self.settings.all_dead:
                self.create_next_gen()

            if self.settings.gather_data == False:
                self.clock.tick(self.settings.FPS)

    def check_events(self):
        """Checks user input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.settings.allow_update = not(self.settings.allow_update)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def update_screen(self):
        """Graphical updates."""
        self.screen.fill(self.settings.bg_color)
        if self.settings.gen > 1:
            if self.settings.gather_data == False:
                # Not while gathering data
                self.draw_champion_path(self.champion_vect_list)
        for wall in self.wall_group.sprites():
            wall.draw_obstacle()
        self.goal.draw_obstacle()
        self.screen.blit(self.text, self.textRect)
        for dot in self.dot_group.sprites():
            dot.draw_dot()

        # Flip screen
        pygame.display.flip()

    def gen_counter(self):
        """draw the gen counter on screen"""
        self.font = pygame.font.Font(None, 32)
        self.text = self.font.render(f'Generation: {self.settings.gen}', True, self.settings.WHITE, self.settings.BLACK)
        self.textRect = self.text.get_rect()
        self.textRect.left = 10
        self.textRect.top = 10

    def draw_champion_path(self, champ_list):
        """draws a line along the champions path."""
        startpos_x = self.settings.dot_start_x
        startpos_y = self.settings.dot_start_y

        for i in range(len(champ_list)-1):
            startpos_x += champ_list[i][0]
            startpos_y += champ_list[i][1]
            endpos_x = startpos_x + champ_list[i+1][0]
            endpos_y = startpos_y + champ_list[i+1][1]
            pygame.draw.line(self.screen,
                             self.settings.GREEN,
                             (startpos_x, startpos_y),
                             (endpos_x, endpos_y),
                             )

    def objects(self):
        """Creates the initial objects of the program."""
        # Outer bounds
        self.wall_group = pygame.sprite.Group()
        for i in range(len(self.settings.wall_dict['x_coordinate'])):
            new_obstacle_or_wall = Obstacle(self,
                                    self.settings.wall_dict["x_coordinate"][i],
                                    self.settings.wall_dict["y_coordinate"][i],
                                    self.settings.wall_dict["width"][i],
                                    self.settings.wall_dict["height"][i],
                                    self.settings.obstacle_color
                                    )
            self.wall_group.add(new_obstacle_or_wall)

        # Goal
        self.goal_group = pygame.sprite.GroupSingle()
        # Creates the goal as an instance of Obstacle at the coordinates (0,0)
        self.goal = Obstacle(self,
                             0,0,
                             self.settings.goal_radius * 2,
                             self.settings.goal_radius * 2,
                             self.settings.goal_color)
        # Moves the goal to its correct position.
        self.goal.rect.centerx = self.settings.goal_pos_x
        self.goal.rect.centery = self.settings.goal_pos_y
        self.goal_group.add(self.goal)

        self.creat_first_gen_dots()

    def creat_first_gen_dots(self):
        # Dots
        self.dot_group = pygame.sprite.Group()

        ID = 0
        for dot in range(self.settings.dot_amount):
            new_dot = Dot(self,[], self.settings.dot_color, ID)
            self.dot_group.add(new_dot)
            ID += 1

    def check_collision(self):
        """Checks for collision between the dots and the walls and boundaries, and the goal."""
        obs_collision_list = pygame.sprite.groupcollide(self.dot_group, self.wall_group, False, False)
        goal_collision_list = pygame.sprite.groupcollide(self.dot_group, self.goal_group, False, False)
        for dot in obs_collision_list:
            dot.alive = False
        for dot in goal_collision_list:
            dot.alive = False
            dot.reached_goal = True

    def check_alive(self):
        """
        Checks if the individual dot is alive.
        Kills dots if they run out of steps on their rute.
        Adds all dots to a list to be worked on by the Ai.
        """
        self.check_collision()
        if self.settings.time_step >= self.settings.list_length:
            for dot in self.dot_group:
                dot.alive = False
                self.dead_dots.append(dot)

            # All dots are killed above
            self.settings.all_dead = True

    def create_next_gen(self):
        """Deletes the old generation(?) and creates a new one. """
        champion = self.brain.find_champ(self.dead_dots)
        self.champion_vect_list = champion.vect_list

        if self.settings.gather_data:
            # Data
            self.brain.write_to_DataFrame(champion.fitness,
                                          champion.time_alive,
                                          self.settings.gen,
                                          champion.ID,
                                          champion.reached_goal,
                                          self.settings.run_counter)

            if self.settings.gen == self.settings.max_gen:
                self.settings.gen = 1
                self.settings.run_counter += 1
                if self.settings.run_counter == self.settings.runs:
                    # Write finished DataFrame to CSV
                    self.brain.final_data.to_csv('Final_data.csv')
                    print(f"run nr. {self.settings.run_counter} over")
                    pygame.quit()
                    sys.exit()
                else:
                    # reset to new run
                    self.dead_dots.clear()
                    self.settings.time_step = 0
                    self.settings.all_dead = False
                    self.creat_first_gen_dots()
                    self.gen_counter()
                    print(f"run nr. {self.settings.run_counter} over")
                    return None

        # Kills previous generation
        for dot in self.dot_group:
            del dot
        self.dot_group.empty()

        # Make the next generation
        self.settings.gen += 1
        self.gen_counter()
        ID = 0
        for dot in range(self.settings.dot_amount -1):
            mutated_list = self.brain.mutate(self.champion_vect_list)
            next_gen_dot = Dot(self, mutated_list, self.settings.dot_color, ID)
            self.dot_group.add(next_gen_dot)
            ID += 1
        champion_dot = Dot(self, self.champion_vect_list, self.settings.champ_color, ID)
        self.dot_group.add(champion_dot)

        # reset
        self.dead_dots.clear()
        self.settings.time_step = 0
        self.settings.all_dead = False


if __name__ == '__main__':
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
