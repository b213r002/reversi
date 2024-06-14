"""Display
"""

import time
import abc


PLAYER_COLORS = ('black', 'white')


class AbstractDisplay(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def progress(self, board, black_player, white_player):
        pass

    @abc.abstractmethod
    def turn(self, player, legal_moves):
        pass

    @abc.abstractmethod
    def move(self, player, legal_moves):
        pass

    @abc.abstractmethod
    def foul(self, player):
        pass

    @abc.abstractmethod
    def win(self, player):
        pass

    @abc.abstractmethod
    def draw(self):
        pass


class ConsoleDisplay(AbstractDisplay):
    """Console Display"""
    def __init__(self, sleep_time_turn=1, sleep_time_move=1):
        self.sleep_time_turn = sleep_time_turn  # sec
        self.sleep_time_move = sleep_time_move  # sec

    def progress(self, board, black_player, white_player):
        """display progress"""
        self._setup_screen()

        score_b = str(black_player) + ':' + str(board._black_score)
        score_w = str(white_player) + ':' + str(board._white_score)

        print(score_b, score_w)
        self._show_board(board)

        self._teardown_screen()

    def turn(self, player, legal_moves):
        """display turn"""
        time.sleep(self.sleep_time_turn)
        print(str(player) + "'s turn")

        for index, value in enumerate(legal_moves, 1):
            coordinate = (chr(value[0] + 97), str(value[1] + 1))
            print(f'{index:2d}:', coordinate)

    def move(self, player, legal_moves):
        """display move"""
        x = chr(player.move[0] + 97)
        y = str(player.move[1] + 1)

        print('putted on', (x, y))
        print()
        time.sleep(self.sleep_time_move)

    def foul(self, player):
        """display foul player"""
        print(player, 'foul')

    def win(self, player):
        """display win player"""
        print(player, 'win')

    def draw(self):
        """display draw"""
        print('draw')

    def _setup_screen(self):
        # cursor-hyde, cursor-move-12row, erase-upto-end, cursor-move-top
        print("\033[?25l\033[12H\033[J\033[;H", end='')

    def _teardown_screen(self):
        # cursor-show
        print("\033[?25h", end='')

    def _show_board(self, board):
        disp = str(board)
        default = '\x1b[0m'
        fg = '\033[38;2;0;0;0m'
        bg = '\033[48;2;112;128;144m'
        disp = disp.replace('●', bg + '●' + default)
        disp = disp.replace('〇', bg + fg + '●' + default)
        disp = disp.replace('□', bg + '□' + default)
        print(disp)


class NoneDisplay(AbstractDisplay):
    """None Display"""
    def progress(self, board, black_player, white_player):
        pass

    def turn(self, player, legal_moves):
        pass

    def move(self, player, legal_moves):
        pass

    def foul(self, player):
        pass

    def win(self, player):
        pass

    def draw(self):
        pass


class WindowDisplay(AbstractDisplay):
    """GUI Window Display"""
    def __init__(self, window, sleep_time_turn=0.3, sleep_time_move=0.3):
        self.info = window.info
        self.board = window.board
        self.sleep_time_turn = sleep_time_turn  # sec
        self.sleep_time_move = sleep_time_move  # sec
        self.pre_move = None

    def progress(self, board, black_player, white_player):
        """display progress"""
        self.info.set_text('black', 'score', str(board._black_score))
        self.info.set_text('white', 'score', str(board._white_score))

    def turn(self, player, legal_moves):
        """display turn"""
        self.info.set_turn_text_on(player.color)  # 手番の表示
        self.board.enable_moves(legal_moves)      # 打てる候補を表示
        time.sleep(self.sleep_time_turn)

    def move(self, player, legal_moves):
        """display move"""
        x = chr(player.move[0] + 97)
        y = str(player.move[1] + 1)

        for color in PLAYER_COLORS:
            self.info.set_turn_text_off(color)  # 手番の表示を消す
            self.info.set_move_text_off(color)  # 打った手の表示を消す

        self.board.disable_moves(legal_moves)                # 打てる候補のハイライトをなくす
        if self.pre_move:
            self.board.disable_move(*self.pre_move)          # 前回打ったてのハイライトを消す
        self.board.enable_move(*player.move)                 # 打った手をハイライト
        self.board.put_disc(player.color, *player.move)      # 石を置く
        time.sleep(self.sleep_time_move)
        self.info.set_move_text_on(player.color, x, y)       # 打った手を表示
        self.board.turn_disc(player.color, player.captures)  # 石をひっくり返すアニメーション
        self.pre_move = player.move

    def foul(self, player):
        """display foul player"""
        self.info.set_foul_text_on(player.color)

    def win(self, player):
        """display win player"""
        winner, loser = ('black', 'white') if player.color == 'black' else ('white', 'black')
        self.info.set_win_text_on(winner)
        self.info.set_lose_text_on(loser)

    def draw(self):
        """display draw"""
        for color in PLAYER_COLORS:
            self.info.set_draw_text_on(color)
