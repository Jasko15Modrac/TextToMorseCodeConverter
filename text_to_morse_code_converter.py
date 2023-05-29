from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QWidget, QGridLayout, QTextEdit, QSlider, QSizePolicy, \
    QMessageBox
from PyQt5.QtCore import QTimer, Qt
from morse_code_list import MORSE_CODE
from pydub import AudioSegment
from pydub.playback import play

# Loading audio files
sample_rate = 44100
AUDIO_DOT = AudioSegment.from_wav('audio_files/morse_dot.wav')
AUDIO_SLASH = AudioSegment.from_wav('audio_files/morse_slash.wav')

if AUDIO_DOT.frame_rate != sample_rate:
    AUDIO_DOT = AUDIO_DOT.set_frame_rate(sample_rate)

if AUDIO_SLASH.frame_rate != sample_rate:
    AUDIO_SLASH = AUDIO_SLASH.set_frame_rate(sample_rate)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer_1 = QTimer()
        self.initUI()

    def initUI(self):

        # Set window title
        self.setWindowTitle("Text To Morse Code Converter")

        # Set the width and height of the window
        self.setGeometry(300, 300, 700, 300)

        # Set up layout manager
        self.layout = QGridLayout()

        # Set the layout on the main window
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Create widgets
        self.input_label = QLabel("Enter the text you want to convert to Morse code")
        self.input_text = QTextEdit()
        self.output_label = QLabel("Converted text")
        self.output_text = QTextEdit()
        self.convert_btn = QPushButton("Convert")
        self.play_sound_btn = QPushButton("Play sound")
        self.light_bar = QLabel()
        self.light_btn = QPushButton("Light")
        self.slider_label = QLabel("Speed")
        self.speed_value = QLabel()
        self.slider = QSlider()

        # Settings for light bar
        self.light_bar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.light_bar.setFixedWidth(200)
        self.light_bar.setStyleSheet("background-color: black;")

        # Settings for slider
        self.slider.setRange(5, 100)
        self.slider.setTickPosition(QSlider.NoTicks)
        self.slider.setSliderPosition(50)
        self.slider.setToolTip("The higher the value the slower the reproduction will be ")

        # Adding widgets to layout
        self.layout.addWidget(self.input_label, 1, 1, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.input_text, 2, 1)
        self.layout.addWidget(self.output_label, 1, 2, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.output_text, 2, 2)
        self.layout.addWidget(self.convert_btn, 3, 1)
        self.layout.addWidget(self.play_sound_btn, 3, 2)
        self.layout.addWidget(self.light_bar, 2, 3, 1, 1)
        self.layout.addWidget(self.light_btn, 3, 3)
        self.layout.addWidget(self.slider_label, 1, 4)
        self.layout.addWidget(self.slider, 2, 4, 1, 1, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.speed_value, 3, 4, alignment=Qt.AlignHCenter)

        # Setting margins for widgets
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Connecting functions with buttons
        self.convert_btn.clicked.connect(self.show_dialog)
        self.play_sound_btn.clicked.connect(self.conv_play)
        self.light_btn.clicked.connect(self.convert)
        self.slider.valueChanged.connect(self.current_speed)

        # Setting the starting timing_unit value. It will change later when user adjusts slider
        self.timing_unit = self.slider.value() * 10

    def show_dialog(self):
        """Function that shows message box explaining representation of unknown characters"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("If the character cannot be translated it will be represented as '#'")
        msg_box.setStandardButtons(QMessageBox.Ok)
        # Connecting the message box button to display_morse_code() function
        msg_box.buttonClicked.connect(self.display_morse_code)
        msg_box.exec_()

    def current_speed(self):
        """Function that changes and displays speed of reproduction"""
        current_value = self.slider.value()
        self.speed_value.setText(str(current_value))
        self.timing_unit = int(current_value) * 10

    def get_input_text(self):
        """Function that collects user input text and adds space between characters(' ') and between words('  ')"""
        in_text = self.input_text.toPlainText().upper()
        txt_len = len(in_text) - 1
        new_in_text = ""
        for ind, character in enumerate(in_text):
            if character == ' ':
                new_in_text += '   '
            elif character != ' ' and ind + 1 < txt_len and in_text[ind + 1] == ' ':
                new_in_text += character
            else:
                new_in_text += character + '  '
        return new_in_text

    def to_morse(self):
        """Converts text to morse code, returns the converted text as morse code"""
        ph = self.get_input_text()
        morse_code_phrase = ''
        new_morse_code_phrase = ''
        for elm in ph:
            try:
                morse_code_phrase += MORSE_CODE[elm]
            except KeyError:
                morse_code_phrase += '#'

        phrase_length = len(morse_code_phrase) + 1
        # Using enumerate to iterate over morse code characters and add space between components of one character
        for inde, ch in enumerate(morse_code_phrase):
            if ch != ' ' and inde + 1 < phrase_length and morse_code_phrase[inde + 1] != ' ':
                new_morse_code_phrase += ch + ' '
            else:
                new_morse_code_phrase += ch

        # Replaces all the '   ' with '/'. That is the sign that separates two words in morse code.
        new_morse_code_phrase = new_morse_code_phrase.replace('   ', '/')

        return new_morse_code_phrase

    def display_morse_code(self):
        """Displays morse code in output_text field"""
        m_code = self.to_morse()
        self.output_text.setText(m_code)

    #### ---------------------------------- METHODS RESPONSIBLE FOR PLAYING SOUND ----------------------------######

    def conv_play(self):
        # In this function we add two new attributes to self.timer (c_text and index) so that we can fetch them in
        # play_beep function.
        self.timer_1.c_text = self.to_morse()
        self.timer_1.index = 0

        # Here we connect timer timeout signal to play_beep function. Every time timer sends timeout signal
        # the play_beep function will be called
        self.timer_1.timeout.connect(self.play_beep)
        # Start the timer with self.timing_unit determining the frequency of timeout signals
        self.timer_1.start(self.timing_unit)

    # Play sound
    def play_beep(self):
        """Function that converts morse code text into audio signals"""
        # Here we fetch those attributes we created in conv_play function
        c_text = self.timer_1.c_text
        index = self.timer_1.index

        # When method reaches the end of phrase stop and disconnect timer and exit method
        if index >= len(c_text):
            self.timer_1.stop()
            self.timer_1.disconnect()
            return

        # Iterating over phrase
        element = c_text[index]

        if element == '.':
            play(AUDIO_DOT)
            self.timer_1.setInterval(self.timing_unit)
        elif element == '-':
            play(AUDIO_SLASH)
            self.timer_1.setInterval(self.timing_unit)
        elif element == ' ':
            self.timer_1.setInterval(self.timing_unit)
        elif element == '  ':
            self.timer_1.setInterval(self.timing_unit * 3)
        elif element == '/':
            self.timer_1.setInterval(self.timing_unit * 7)
        else:
            self.timer_1.setInterval(self.timing_unit)

        self.timer_1.index += 1

#### --------------------------------------------METHODS RESPONISBLE FOR LIGHT SIGNALS-----------------------------####
    def change_color(self):
        self.light_bar.setStyleSheet("background-color: yellow;")

    def revert_to_black(self):
        self.light_bar.setStyleSheet("background-color: black;")

    def convert(self):
        self.timer.text = self.to_morse()
        self.timer.index = 0

        self.timer.timeout.connect(self.play_lights)
        self.timer.start(self.timing_unit)

    def play_lights(self):

        text = self.timer.text
        index = self.timer.index

        if index >= len(text):
            self.timer.stop()
            self.timer.disconnect()
            return

        element = text[index]

        if element == '.':
            self.change_color()
            self.timer.setInterval(self.timing_unit)
        elif element == '-':
            self.change_color()
            self.timer.setInterval(self.timing_unit * 3)
        elif element == ' ':
            self.revert_to_black()
            self.timer.setInterval(self.timing_unit)
        elif element == '  ':
            self.revert_to_black()
            self.timer.setInterval(self.timing_unit * 3)
        elif element == '/':
            self.revert_to_black()
            self.timer.setInterval(self.timing_unit * 7)
        else:
            self.timer.setInterval(self.timing_unit)

        self.timer.index += 1

