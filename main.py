import operator
import random

import kivy.uix.popup
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.popup import Popup

Builder.load_file('menu.kv')


class MainWidget(RelativeLayout):
    # not sure if I should use relative or box layout
    time_label = StringProperty('')
    top_label = StringProperty('')
    middle_label = StringProperty('Welcome')
    bottom_label = StringProperty('Press Enter')
    menu_widget = ObjectProperty()

    popup_label = StringProperty('Text place holder here.')

    timer = 60
    time_toggle = False

    firstvalue = None
    secondvalue = None
    answer = None
    ops = None
    randomOp = None
    divisor = None

    list_of_correct = []
    list_of_incorrect = []

    game_toggle = False

    # menu_tile = 'Play Again?'
    menu_button_one = 'Again'
    menu_button_two = 'Quit'

    popup = None

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.keyboard = Window.request_keyboard(self.on_keyboard_down, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)
        Clock.schedule_interval(self.update, 1)
        Clock.schedule_interval(self.the_flash, 2)

    def on_keyboard_down(self, *args):
        # args are [keyboard, keycode, text, modifiers]
        if len(args) == 0:
            return
        elif args[1][1] == 'enter' and self.time_toggle is False:  # use was time_toggle, need more testing
            self.time_toggle = True
            self.new_question()
            self.enable_input()

        # else:
        #     print(f'the keycode key for', args[1][1], 'is', args[1][0])
        return True

    def disable_input(self):
        # going to need and enabler_input function
        text_input = self.ids.text_input
        text_input.focus = False
        text_input.disabled = True

    def enable_input(self):
        self.clear_input()
        text_input = self.ids.text_input
        text_input.focus = True
        text_input.disabled = False

    def update(self, dt):
        if self.timer != 0 and self.time_toggle is True:
            self.timer -= 1
            self.time_label = str(self.timer)
        elif self.timer == 0:
            Clock.unschedule(self.update)

            self.time_toggle = False
            self.top_label = ''
            self.middle_label = 'Times Up'
            self.menu_widget.opacity = 1

            # disable keyboard or text input??
            self.disable_input()
            self.keyboard.unbind(on_key_down=self.on_keyboard_down)

    def the_flash(self, dt):
        # clear the correction text after 2 sec.
        self.top_label = ''

    def on_text_validate(self):
        self.bottom_label = ''

    def clear_input(self):
        # clear text on input, after enter has been press
        self.ids.text_input.text = ''

    def new_question(self):
        # make this a while loop do cycle bad math problem for subtraction and division
        while True:
            self.ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
            # self.ops = {'+': operator.add}
            self.randomOp = random.choice(list(self.ops.keys()))
            self.firstvalue = random.randint(1, 12)
            self.secondvalue = random.randint(1, 12)
            if self.randomOp == '+':
                self.answer = self.firstvalue + self.secondvalue
                self.middle_label = f'{self.firstvalue} {self.randomOp} {self.secondvalue}'
                return self.answer
            elif self.randomOp == '-':
                if self.firstvalue > self.secondvalue:
                    self.answer = self.firstvalue - self.secondvalue
                    self.middle_label = f'{self.firstvalue} {self.randomOp} {self.secondvalue}'
                    return self.answer
            elif self.randomOp == '*':
                self.answer = self.firstvalue * self.secondvalue
                self.middle_label = f'{self.firstvalue} {self.randomOp} {self.secondvalue}'
                return self.answer
            elif self.randomOp == '/':
                self.divisor = self.firstvalue * self.secondvalue
                if self.divisor % self.secondvalue == 0:
                    self.answer = self.divisor / self.secondvalue
                    self.middle_label = f'{self.divisor} {self.randomOp} {self.secondvalue}'
                    return self.answer

    def check_answer(self):
        try:
            # valueError self.answer is int only
            if self.answer == int(self.ids.text_input.text):
                self.top_label = 'Correct'
                # save question and user answer on to a list or
                if self.middle_label not in self.list_of_correct:
                    self.list_of_correct.append(f'{self.middle_label} = {int(self.ids.text_input.text)}')
                self.new_question()
            elif self.answer != int(self.ids.text_input.text):
                self.top_label = 'Wrong'
                if self.middle_label not in self.list_of_incorrect:
                    self.list_of_incorrect.append(f'{self.middle_label} = {int(self.ids.text_input.text)}')
                self.clear_input()
        except ValueError:
            print('Invalid Entry')

    def reset(self):
        # enable keyboard
        self.keyboard.bind(on_key_down=self.on_keyboard_down)
        self.enable_input()

        # Reset the labels and input fields
        self.time_label = '00'
        self.top_label = ''
        self.middle_label = 'Weclome'
        # this line is set but doesn't appeal in new game
        self.bottom_label = 'Press Enter'

        # Reset the game variables to their initial states
        self.timer = 60
        self.time_toggle = False
        self.firstvalue = None
        self.secondvalue = None
        self.answer = None
        self.ops = None
        self.randomOp = None
        self.divisor = None

        self.list_of_correct = []
        self.list_of_incorrect = []

        # Is this needed? Yes Timer doesn't work without it
        Clock.schedule_interval(self.update, 1)

        # Button are hidden
        self.menu_widget.opacity = 0

    def on_menu_button_one_press(self):
        print('game continue by user.')
        self.reset()

    def on_menu_button_two_press(self):
        print('The game quited by user.')

    def on_menu_button_review(self):
        pass

    def popup_content(self):
        self.popup_label = ('\n'.join(self.list_of_incorrect))

    def note_to_self(self):
        '''
        how to make list more readable?
        '''


class MainApp(App):
    pass


if __name__ == '__main__':
    MainApp().run()