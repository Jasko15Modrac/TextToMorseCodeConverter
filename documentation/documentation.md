# Text to Morse Code Converter

The program **main.py** provides a graphical user interface (GUI) for converting text to Morse code and playing it as audio or light signals. The program is implemented using the PyQt5 library for the GUI components and the pydub library for audio playback.

## Prerequisites

The following libraries need to be installed to run the program:

* **PyQt5**
* **pydub**

Additionally, the program requires two audio files, **morse_dot.wav** and **morse_slash.wav**, which are used to represent the Morse code signals for a dot and a slash (dash), respectively.

## Program Files

The program consists of three files:

* **main.py:** This is the main script that initializes the GUI and connects the UI elements to the corresponding functions.
* **morse_code_list.py:** This file defines a dictionary MORSE_CODE that maps each character to its Morse code representation.
* **text_to_morse_code_converter.py:** This file contains the MainWindow class that implements the GUI functionality for converting text to Morse code and playing it as audio or light signals.

**Usage:** To run the program, execute the main.py script. This will launch the GUI window with the following components:

* **Input Text:** A text area where you can enter the text you want to convert to Morse code.
* **Converted Text:** A text area that displays the converted Morse code representation of the input text.
* **Convert Button:** Clicking this button converts the input text to Morse code and displays it in the Converted Text area.
* **Play Sound Button:** Clicking this button plays the Morse code audio signals corresponding to the converted text.
* **Light:** A visual representation of the Morse code signals using a light bar.
* **Speed Slider:** A slider to adjust the speed of audio or light signal playback.
* **Speed Value:** Displays the current speed value selected by the slider.

## Converting Text to Morse Code

1. Enter the text you want to convert in the Input Text area.
2. Click the Convert button to convert the text to Morse code.
3. The converted Morse code will be displayed in the Converted Text area.

## Playing Morse Code as Audio Signals

1. Convert the text to Morse code as described in the previous section.
2. Click the Play Sound button to play the Morse code audio signals.
3. The audio signals will be played according to the timing defined by the speed slider. The dot signal corresponds to a short beep, and the slash (dash) signal corresponds to a longer beep.

## Playing Morse Code as Light Signals

1. Convert the text to Morse code as described in the first section.
2. Click the Light button to play the Morse code light signals.
3. The light bar will flash according to the timing defined by the speed slider. The bar will be lit during the dot signal and the slash (dash) signal, and it will be off during spaces between signals.

## Adjusting the Speed

* Move the Speed Slider left or right to decrease or increase the speed, respectively. 
* The Speed Value label will display the current speed value selected by the slider. 

## Class Documentation

### class MainWindow(QMainWindow)

The MainWindow class is responsible for creating and managing the main GUI window.

Methods:
* **__init__(self):** Initializes the MainWindow class and sets up the GUI components.
* **initUI(self):** Sets up the layout and creates the GUI components.
* **show_dialog(self):** Displays a message box with information about the representation of unknown characters in Morse code.
* **current_speed(self):** Updates the current speed value based on the speed slider position.
* **get_input_text(self):** Retrieves the input text from the Input Text area and adds spaces between characters and words according to Morse code rules.
* **to_morse(self):** Converts the input text to Morse code using the MORSE_CODE dictionary and returns the converted text.
* **display_morse_code(self):** Displays the converted Morse code in the Converted Text area.
* **conv_play(self):** Converts the Morse code to audio signals and plays them.
* **play_beep(self):** Plays the audio signals corresponding to the Morse code.
* **change_color(self):** Changes the color of the light bar to indicate the Morse code signals.
* **revert_to_black(self):** Resets the color of the light bar to black.
* **convert(self):** Converts the Morse code to light signals and plays them.
* **play_lights(self):** Controls the light signals based on the Morse code.

**Note:** The above documentation provides an overview of the program and its functionalities. For detailed understanding, you may refer to the code comments present in the respective files.