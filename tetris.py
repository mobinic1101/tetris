# --------------------------TETRIS v1.0.4 (final)----------------------------------#
import pygame
import random
import json
pygame.init()


class GameInfo:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    DARK_GRAY = 10, 10, 10
    GRAY = 120, 120, 120
    YELLOW = 255, 255, 0
    CYAN = 0, 255, 255
    PURPLE = 128, 0, 128
    GREEN = 0, 255, 0
    BLUE = 0, 0, 255
    RED = 255, 0, 0
    ORANGE = 255, 165, 0
    BLOCK_COLORS = {
        'o': YELLOW, 'i': BLUE, 's': RED, 'z': GREEN,
        'l': ORANGE, 'j': PURPLE, 't': CYAN}
    PADDING = 10

    NEXT_FONT = pygame.font.SysFont('arial', 30)
    SCORE_FONT = pygame.font.SysFont('arial', 20)
    LARGE_FONT = pygame.font.SysFont('arial', 70)

    def __init__(self, width=700, hight=700, caption="PyTetris"):
        self.screen_width = width
        self.screen_hight = hight
        self.width, self.hight = self.screen_width - \
            self.PADDING, self.screen_hight - self.PADDING

        self.__set_surface(caption)
        self.__set_block()
        self.__get_board_matrix()
        self.__set_grid_lines()

    def __set_block(self):
        block_width_hight = self.middle_rect.width // 10
        self.block_width = block_width_hight
        self.block_hight = block_width_hight
        self.block_vel = block_width_hight

    def __set_surface(self, caption):
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_hight))
        pygame.display.set_caption(caption)

        left_right_width = (self.width // 2) // 2
        self.left_rect = pygame.Rect(
            self.PADDING, self.PADDING, left_right_width - self.PADDING - 5, self.hight - self.PADDING)
        self.right_rect = pygame.Rect(
            self.width // 2 + left_right_width, self.PADDING, left_right_width, self.hight - self.PADDING)
        self.middle_rect = pygame.Rect(
            left_right_width, self.PADDING, self.width // 2 - 5, self.hight - self.PADDING)

    def __get_board_matrix(self, other_class=False):
        matrix = []
        for c in range(self.middle_rect.top, self.middle_rect.bottom + 1, self.block_vel):
            row = []
            for r in range(self.middle_rect.left, self.middle_rect.right + 1, self.block_vel):
                row.append((r, c))
            matrix.append(row)
        if other_class:
            return matrix
        self.board_matrix = matrix

    def __set_grid_lines(self):
        lines = []
        for row in self.board_matrix:
            x_line = (row[0], row[-1])
            for i, col in enumerate(row):
                start = col
                stop = self.board_matrix[-1][i]
                y_line = (start, stop)

                lines.append(y_line)
            lines.append(x_line)
        self.grid_lines = lines


class Blocks(GameInfo):
    def __init__(self, width=700, hight=700, caption="PyTetris"):
        super().__init__(width, hight, caption)
        self.top_middle = self.board_matrix[0][len(self.board_matrix[0]) // 2]
        b_hight = self.block_hight
        self.BLOCKS = {'o': [
            self.top_middle, (self.top_middle[0], self.top_middle[1] - b_hight), (self.top_middle[0] + b_hight, self.top_middle[1] - b_hight), (self.top_middle[0] + b_hight, self.top_middle[1])],
            'i': [(self.top_middle[0], self.top_middle[1] - i * b_hight) for i in range(4)],
            's': [self.top_middle, (self.top_middle[0] + self.block_width, self.top_middle[1]), (self.top_middle[0], self.top_middle[1] - self.block_hight), (self.top_middle[0] - self.block_hight, self.top_middle[1] - self.block_hight)],
            'z': [self.top_middle, (self.top_middle[0] - self.block_hight, self.top_middle[1]), (self.top_middle[0], self.top_middle[1] - self.block_hight), (self.top_middle[0] + self.block_hight, self.top_middle[1] - self.block_hight)],
            'l': [self.top_middle, (self.top_middle[0] + b_hight, self.top_middle[1]), (self.top_middle[0], self.top_middle[1] - b_hight), (self.top_middle[0], self.top_middle[1] - b_hight - b_hight)],
            'j': [self.top_middle, (self.top_middle[0] + b_hight, self.top_middle[1]), (self.top_middle[0] + b_hight, self.top_middle[1] - b_hight), (self.top_middle[0] + b_hight, self.top_middle[1] - b_hight - b_hight)],
            't': [self.top_middle, (self.top_middle[0], self.top_middle[1] - b_hight), (self.top_middle[0] + b_hight, self.top_middle[1] - b_hight), (self.top_middle[0] - b_hight, self.top_middle[1] - b_hight)]}
        self.shapes = self.get_starting_shapes()
        self.all_shapes = []

    def get_starting_shapes(self):
        shapes = []
        keys = 'iszljto'
        prev_key = None
        n = 0
        while n != 2:
            key = random.choice(keys)
            if key != prev_key:
                shapes.append({key:self.BLOCKS[key]})
                n += 1
            prev_key = key
        return shapes

    def get_shape(self):
        all_keys = [key for key in self.BLOCKS.keys()]
        print(f'all_keys: {all_keys}')
        current_keys = [str(*shape.keys()) for shape in self.shapes]
        print(f'self.shapes = {self.shapes}')
        print(f"current_keys: {current_keys}")
        while True:
            key = random.choice(all_keys)
            if key not in current_keys:
                return {key: self.BLOCKS[key]}

    def move(self, direction: int):  # expected: <+ self.block_vel or - self.block_vel>
        key = str(*self.shapes[0].keys())
        new_shape = []
        shapes = self.shapes[0][key]
        for block in shapes:
            x = block[0] + direction
            y = block[1]
            new_shape.append((x, y))
        return {key: new_shape}

    def rotate(self):
        shapes = self.shapes[0]
        key = str(*shapes.keys())
        rotation_point = shapes[key][1]
        if key == 'i' or key == 'o':
            rotation_point = shapes[key][2]
        elif key == 'l':
            rotation_point = shapes[key][0]

        new_shape_values = []
        for block in shapes[key]:
            translated_x, translated_y = block[0] - \
                rotation_point[0], block[1] - rotation_point[1]
            new_x, new_y = -translated_y, translated_x
            rotated_x = new_x + rotation_point[0]
            rotated_y = new_y + rotation_point[1]
            new_shape_values.append((rotated_x, rotated_y))
        new_shape = {key: new_shape_values}
        return new_shape

    def drop(self):
        key = str(*self.shapes[0].keys())
        shape = self.shapes[0][key]
        new_shape = []
        for block in shape:
            x = block[0]
            y = block[1] + self.block_vel
            new_shape.append((x, y))
        self.shapes[0] = {key: new_shape}

    def check_collision(self, other=None, move=False):
        shape = self.shapes[0]
        if not other == None:
            shape = other
        key = str(*shape.keys())
        shape = shape[key]
        all_blocks = []
        for all_shapes_block in self.all_shapes:
            all_shapes_block = all_shapes_block[str(*all_shapes_block.keys())]
            for block in all_shapes_block:
                all_blocks.append(block)

        # checking for ground and all_shape collision
        collide = False
        
        for block in shape:
            if move:
                if block in all_blocks:
                    return True
                continue
                               
            block = block[0], block[1] + self.block_hight
            if block in all_blocks or (block[0], block[1] - self.block_hight) in all_blocks or block[1] == self.middle_rect.bottom:
                collide = True
        
        return collide

    def check_winning_lines(self):
        line_length = len(self.board_matrix[0]) - 1

        keys = [str(*shape.keys()) for shape in self.all_shapes]
        all_blocks = [shape_dict[key]
                      for key, shape_dict in zip(keys, self.all_shapes)]
        all_blocks = [block for shape in all_blocks for block in shape]

        winning_lines = []

        for row in self.board_matrix:
            blocks_in_a_row = []
            for block in all_blocks:
                if block in row:
                    blocks_in_a_row.append(block)

                if len(blocks_in_a_row) == line_length:
                    winning_lines.append(blocks_in_a_row)
                    break

        return winning_lines, keys


class Player:
    def __init__(self, name='Player', _id=None):
        self.name = name
        self._id = _id
        self.lines_completed = 0
        self.score = 0
        self.highest_score = 0

    def save_info(self):
        with open('records.json', 'w') as records:
            json.dump({
                'name': self.name,
                'id': self._id,
                'lines_completed': self.lines_completed}, records)

    def load_info(self):
        with open('records.json', 'r') as records:
            data = json.load(records)
            return data


def draw_surfaces(game):
    game.screen.fill(game.BLACK)
    pygame.draw.rect(game.screen, game.DARK_GRAY, game.left_rect)
    pygame.draw.rect(game.screen, game.DARK_GRAY, game.middle_rect)
    pygame.draw.rect(game.screen, game.DARK_GRAY, game.right_rect)


def draw_gird_lines(game):
    for line in game.grid_lines:
        pygame.draw.line(game.screen, game.GRAY, *line)


def draw_shapes(game):
    shapes = game.shapes[0]
    color = shapes.keys()
    color = str(*color)
    for shape in shapes.values():
        for block_ in shape:
            rect_value = pygame.Rect(
                *block_, game.block_width, game.block_hight)  # type:ignore
            pygame.draw.rect(game.screen, game.BLOCK_COLORS[color], rect_value)

    for shape in game.all_shapes:
        color = str(*shape.keys())
        for block in shape[color]:
            rect_value = pygame.Rect(
                block[0], block[1], game.block_width, game.block_hight)
            pygame.draw.rect(game.screen, game.BLOCK_COLORS[color], rect_value)


def draw_next_shape(game):
    next_shape = game.shapes[-1]
    color = str(*next_shape.keys())
    next_shape = next_shape[color].copy()
    # distance form original position
    half_rect_x = (game.top_middle[0] // 2) // 2
    half_rect_y = game.board_matrix[len(game.board_matrix) // 2][0][1]

    distance_x = ((game.right_rect.left - game.top_middle[0]) + half_rect_x) // game.block_vel
    distance_y = half_rect_y // game.block_vel
    for block in next_shape:
        x, y = block
        block = (x + distance_x * game.block_width,
        y + distance_y * game.block_hight, game.block_width, game.block_hight)
        pygame.draw.rect(game.screen, game.BLOCK_COLORS[color], block)


def draw_next_text(game):
    next_text = game.NEXT_FONT.render('next', 1, game.WHITE)
    x = ((game.right_rect.left + ((game.top_middle[0] // 2) // 2))) - (next_text.get_width() // 2)
    y = game.board_matrix[len(game.board_matrix) // 2][0][1] - (game.right_rect.bottom // 2) // 2
    print(x, y)
    game.screen.blit(next_text, (x, y))


def is_between_walls(game, shape):
    key = str(*shape.keys())
    blocks = shape[key]
    between_walls = []
    for block in blocks:
        block_x = block[0]
        if block_x >= game.middle_rect.left and block_x < game.middle_rect.right:
            between_walls.append(True)
        else:
            between_walls.append(False)
    return all(between_walls)


def check_events(game, run):
    key_pressed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = not run
            break
        if event.type != pygame.KEYDOWN:
            continue
        block_vel = game.block_vel
        if event.key == pygame.K_LEFT:  # left
            shape = game.move(-block_vel)
            between_walls = is_between_walls(game, shape)
            collide = game.check_collision(other=shape, move=True)
            if between_walls and not collide:
                print('moving left')
                game.shapes[0] = shape
                key_pressed = True

        elif event.key == pygame.K_RIGHT:  # right
            block_vel = game.block_vel
            shape = game.move(+block_vel)
            between_walls = is_between_walls(game, shape)
            collide = game.check_collision(other=shape, move=True)
            if between_walls and not collide:
                game.shapes[0] = shape
                print('moving right')
                key_pressed = True

        elif event.key == pygame.K_DOWN:  # down
            collide = game.check_collision()
            if not collide:
                game.drop()

        elif event.key == pygame.K_SPACE:  # space
            key_pressed = True
            shape = game.rotate()
            if is_between_walls(game, shape) and not game.check_collision(other=shape):
                game.shapes[0] = shape
    return run, key_pressed


# removes the line and drops the remaining blocks.
def remove_and_drop(game, winning_line):
    winning_line, keys = winning_line
    # y coordinate of last line in winning line
    y = winning_line[-1][0][1]

    step_down = len(winning_line) * game.block_vel

    # unpacking all winning_line lines into one list
    winning_line = [block for line in winning_line for block in line]

    # removing the winning lines by replacing the shape blocks with \
    #  blocks that are not in wining_line.
    for key, shape in zip(keys, game.all_shapes):
        blocks = shape[key]
        new_blocks = []
        for block in blocks:
            if block not in winning_line:
                if block[1] < y:
                    block = block[0], block[1] + step_down
                new_blocks.append(block)

        shape[key] = new_blocks


def display_game_over_screen(game):
    screen = game.screen
    game_over = game.LARGE_FONT.render('GAME OVER', 1, game.RED)
    play_again = game.NEXT_FONT.render('wanna play again y/n', 1, game.WHITE)

    screen.fill(game.BLACK)
    screen.blit(game_over, ((game.screen_width // 2) - (game_over.get_width() // 2), game.screen_hight // 2 - game_over.get_height() - 10))
    screen.blit(play_again, ((game.screen_width // 2), game.screen_hight // 2 + 10))
    pygame.display.update()


def main():
    game = Blocks()

    FPS = 30
    main_clock = pygame.time.Clock()
    clock = pygame.time.Clock()

    frame = 0
    frame_to_drop = 15

    run = True
    game_over = False
    while run:
        main_clock.tick(FPS)
        frame += 1

        draw_surfaces(game)
        draw_shapes(game)
        draw_next_shape(game)
        draw_next_text(game)
        draw_gird_lines(game)
        pygame.display.update()

        run = check_events(game, run)[0]

        if frame == frame_to_drop:
            collide = game.check_collision()
            if not collide:
                game.drop()
            else:
                frame_count = 0
                frame_to_complete = 10 # fame to complete move
                while not frame_count == frame_to_complete:
                    clock.tick(FPS)
                    key_pressed = check_events(game, run)[1]
                    if key_pressed:
                        print('key_pressed')
                        pygame.draw.rect(game.screen, game.DARK_GRAY, game.middle_rect)
                        draw_shapes(game)
                        draw_gird_lines(game)
                        pygame.display.update()
                        frame_count = 0
                        continue
                    frame_count += 1

                collide = game.check_collision()
                if collide:
                    game.all_shapes.append(game.shapes[0])
                    new_shape = game.get_shape()
                    game.shapes.append(new_shape)
                    game.shapes.remove(game.shapes[0])
                    game_over = game.check_collision()

                    if game_over:
                        screen_running = True
                        while screen_running:
                            display_game_over_screen(game)

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    game_over = False
                                    run = False
                                if event.type != pygame.KEYDOWN:
                                    continue
                                elif event.key == pygame.K_y:
                                    screen_running = False
                                    game.shapes.clear()
                                    game.shapes = game.get_starting_shapes()
                                    game.all_shapes.clear()
                                elif event.key == pygame.K_n:
                                    screen_running = False
                                    run = False
                                    print("bye")
                        
                    winning_line = game.check_winning_lines()
                    if winning_line[0]:
                        remove_and_drop(game, winning_line)

            frame = 0


if __name__ == '__main__':
    main()
