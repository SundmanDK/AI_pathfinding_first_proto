import pygame
import sys
from settings import Settings
from dot import Dot
from obstacles import Obstacle
from obstacles import Goal
from brain import Brain
class Game:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,
             self.settings.screen_height)
        )
        self.objects()
        self.dead_dots = []
        self.brain = Brain(self)

    def objects(self):
        # outer bounds
        self.wall_group = pygame.sprite.Group()
        self.top_wall = Obstacle(self,
                                 self.settings.wall_dict["x_coordinate"][0],
                                 self.settings.wall_dict["y_coordinate"][0],
                                 self.settings.wall_dict["width"][0],
                                 self.settings.wall_dict["height"][0]
                                 )
        self.wall_group.add(self.top_wall)
        self.left_wall = Obstacle(self,
                                 self.settings.wall_dict["x_coordinate"][1],
                                 self.settings.wall_dict["y_coordinate"][1],
                                 self.settings.wall_dict["width"][1],
                                 self.settings.wall_dict["height"][1]
                                 )
        self.wall_group.add(self.left_wall)
        self.right_wall = Obstacle(self,
                                 self.settings.wall_dict["x_coordinate"][2],
                                 self.settings.wall_dict["y_coordinate"][2],
                                 self.settings.wall_dict["width"][2],
                                 self.settings.wall_dict["height"][2]
                                 )
        self.wall_group.add(self.right_wall)
        self.bottom_wall = Obstacle(self,
                                 self.settings.wall_dict["x_coordinate"][3],
                                 self.settings.wall_dict["y_coordinate"][3],
                                 self.settings.wall_dict["width"][3],
                                 self.settings.wall_dict["height"][3]
                                 )
        self.wall_group.add(self.bottom_wall)
        self.obstacle_1 = Obstacle(self,
                                 self.settings.wall_dict["x_coordinate"][4],
                                 self.settings.wall_dict["y_coordinate"][4],
                                 self.settings.wall_dict["width"][4],
                                 self.settings.wall_dict["height"][4]
                                 )
        #self.wall_group.add(self.obstacle_1)
        self.goal_group = pygame.sprite.GroupSingle()
        self.goal = Goal(self, self.settings.goal_pos_x, self.settings.goal_pos_y, self.settings.goal_radius * 2, self.settings.goal_radius * 2)
        self.goal_group.add(self.goal)

        self.dot_group = pygame.sprite.Group()
        for dot in range(self.settings.dot_amount):
            new_dot = Dot(self,[])
            self.dot_group.add(new_dot)

    def run(self):
        while self.settings.running:
            self.check_events()
            self.check_alive()
            self.update_screen()
            # self.dot_group.update()
            for dot in self.dot_group.sprites():
                if dot.alive:
                    dot.update()
            if self.settings.all_dead:
                self.create_next_gen()
            self.settings.time_step += 1


    def create_next_gen(self):
        self.settings.gen += 1
        champion_vect_list = self.brain.find_champ(self.dead_dots).vect_list
        for dot in self.dot_group:
            del dot
        self.dot_group.empty()
        for dot in range(self.settings.dot_amount):
            mutated_list = self.brain.mutate(champion_vect_list)
            next_gen_dot = Dot(self, mutated_list)
            self.dot_group.add(next_gen_dot)

            # reset
        self.settings.time_step = 0
        self.settings.all_dead = False

        # print(f"dot amount{len(self.dot_group))

    def update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for wall in self.wall_group.sprites():
            wall.draw_obstacle()
        self.goal.draw_goal()
        for dot in self.dot_group.sprites():
            dot.draw_dot()

        # Flip screen
        pygame.display.flip()
        self.clock.tick(self.settings.FPS)

    def check_collision(self):
        obs_collision_list = pygame.sprite.groupcollide(self.dot_group, self.wall_group, False, False)
        goal_collision_list = pygame.sprite.groupcollide(self.dot_group, self.goal_group, False, False)
        #print("fuck off")
        for dot in obs_collision_list:
            dot.alive = False
            self.dead_dots.append(dot)
            #print("i died")
        for dot in goal_collision_list:
            dot.alive = False
            dot.reached_goal = True
            self.dead_dots.append(dot)

        #print("i work")

    def check_alive(self):
        self.check_collision()
        if self.settings.time_step >= self.settings.list_length:
            for dot in self.dot_group:
                dot.alive = False
                self.dead_dots.append(dot)
        self.all_dots_dead()

    def all_dots_dead(self):
        for dot in self.dot_group:
            if dot.alive == True:
                self.settings.all_dead = False
            else:
                self.settings.all_dead = True


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

