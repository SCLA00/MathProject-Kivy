import operator
import random
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.relativelayout import RelativeLayout

Builder.load_file('menu.kv')


class MainWidget(RelativeLayout):
    # not sure if I should use relative or box layout
    time_label = StringProperty('00')
    top_label = StringProperty('')
    middle_label = StringProperty('Welcome')
    bottom_label = StringProperty('Press Enter')
    menu_widget = ObjectProperty()

    timer = 60
    time_toggle = False

    firstvalue = None
    secondvalue = None
    answer = None
    ops = None
    randomOp = None
    divisor = None

    list_of_correct = None
    list_of_incorrect = None

    game_toggle = False

    # menu_tile = 'Play Again?'
    menu_button_one = 'Again'
    menu_button_two = 'Quit'

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
            self.ops = {'/': operator.truediv}
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
                self.new_question()
            elif self.answer != int(self.ids.text_input.text):
                self.top_label = 'Wrong'
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
        self.timer = 5
        self.time_toggle = False
        self.firstvalue = None
        self.secondvalue = None
        self.answer = None
        self.ops = None
        self.randomOp = None

        # Is this needed? Yes Timer doesn't work without it
        Clock.schedule_interval(self.update, 1)

        # Button are hidden
        self.menu_widget.opacity = 0


    def on_menu_button_one_press(self):
        print('Left Button was press')
        self.reset()

    def on_menu_button_two_press(self):
        print('The game quited by user')

    def note_to_self(self):
        '''
        my problem is that after the times up the enter still works. In the menu you can
        see a new math problem appeal in the background.
        things i have tried,
        1) disabling and enable text input.
        2) set the focus to False / True
        3) play with unbinding, not sure if im using that code correctly

        This problem of showing the show math problem, happen because i set the enter key
        as the trigger to start the timer and show the math problem.

        ex. init Timer set to False
        press enter set the Timer to True and show math problem

        --------------------------------------------------------------------------------------
        should i use a different key to trigger timer, that way the enter key wouldnt work
        unless the timer is set to True??

        use space?

        i dont know how to trigger both timer and show new_problem. will it effect the end game
        screen.
        --------------------------------------------------------------------------------------

        review 3) and the problem solve with unbinding and bind window keyboard
        --------------------------------------------------------------------------------------

        plan: add a function that saving all the given problem.
        show the number of right and wrong answer. maybe fraction number? x/y

        maybe added a hidden button to show problem at the end game.
        color code the right and wrong answer?

        '''


class MainApp(App):
    pass


if __name__ == '__main__':
    MainApp().run()
