# Human-Keyboard - Simulate Human Typing Behavior with Realistic Timing and Errors

## Overview

**Human-Keyboard** is a Python library that simulates human typing behavior. It generates keystrokes with realistic timing delays, introduces common typing errors, and corrects them as a human would. This can be useful for creating automated typing simulations, testing typing interfaces, or generating realistic typing data for research purposes.

## Features

- **Simulated Typing Speed**: Set the Words Per Minute (WPM) to match different typing speeds.
- **Error Simulation**: Introduces realistic typing errors such as typos, double letters, skipped letters, and swapped letters.
- **Error Correction**: Automatically corrects errors after a delay, simulating human error correction.
- **Fatigue Modeling**: Simulates typing fatigue over time, affecting typing speed and error rate.
- **Customizable Parameters**: Adjust various parameters to model different typing behaviors.
- **Support for Special Characters**: Correct handling of capital letters, numbers, punctuation, and special symbols.

## Installation

You can install **Human-Keyboard** using `pip` (after uploading it to PyPI):

```bash
pip install human-keyboard
```

Alternatively, clone the repository and install it manually:

```bash
git clone https://github.com/yourusername/human-keyboard.git
cd human-keyboard
pip install .
```

## Usage

### Basic Example

```python
from human_keyboard import HumanKeyboard

# Create a HumanKeyboard instance with default parameters
model = HumanKeyboard()

# Text to simulate typing
text = "The quick brown fox jumps over the lazy dog."

# Simulate typing (real_time=True for actual typing effect)
model.type_text(text, real_time=True)
```

### Custom Parameters

You can customize the typing behavior by adjusting the parameters:

```python
model = HumanKeyboard(
    wpm=100,             # Words per minute
    error_rate=0.05,     # Error rate (5%)
    thinking_delay=200,  # Delay when starting new words (in ms)
    fatigue_max=1.5,     # Maximum fatigue multiplier
    # ... other parameters
)

text = "This is a test with custom parameters."
model.type_text(text, real_time=True)
```

### Non-Real-Time Simulation

If you want to generate the typed text without simulating real-time typing (useful for testing):

```python
model.type_text(text, real_time=False)
```

### Advanced Example

```python
# Simulate typing with error correction and fatigue modeling
model = HumanKeyboard(
    wpm=80,
    error_rate=0.1,
    fatigue_max=2.0,
    fatigue_increase=0.002,
    fatigue_recovery=0.001,
)

text = "HumanKeyboard simulates realistic typing behavior over time, including errors and fatigue."
model.type_text(text, real_time=True)
```

## Parameters

You can adjust the following parameters when creating a `HumanKeyboard` instance:

- **wpm** (`float`): Base words per minute.
- **error_rate** (`float`): Base error rate (0-1).
- **thinking_delay** (`float`): Base delay (ms) when starting new words.
- **fatigue_max** (`float`): Maximum fatigue multiplier.
- **fatigue_increase** (`float`): Rate of fatigue increase per keystroke.
- **fatigue_recovery** (`float`): Rate of fatigue recovery per second.
- **punctuation_multiplier** (`float`): Timing multiplier for punctuation.
- **number_multiplier** (`float`): Timing multiplier for numbers.
- **space_multiplier** (`float`): Timing multiplier for spaces.
- **shift_delay** (`float`): Additional delay (ms) for shifted characters.
- **correction_delay** (`float`): Base delay (ms) before error correction.
- **backspace_delay** (`float`): Base delay (ms) between backspaces.
- **distance_matrix** (`dict`): Custom keyboard distance matrix.

## Requirements

- Python 3.6 or higher
- `numpy`
- `keyboard` (requires root access on Linux and might require accessibility permissions on macOS)

## Installation Notes

**Windows Users**: The `keyboard` module requires you to run the script with administrator privileges.

**macOS Users**: You might need to enable accessibility permissions for Python in System Preferences.

**Linux Users**: The `keyboard` module requires the script to be run as root. Alternatively, you can use the `uinput` module or adjust your system settings to allow non-root keyboard input.

## Important Considerations

- **Safety**: Be cautious when using this library, as it simulates keyboard input that can interfere with your current tasks. Ensure that you have the focus on the intended window or application.
- **Permissions**: Depending on your operating system, you might need special permissions or run your script with elevated privileges.
- **Ethical Use**: Use this library responsibly and ethically. Do not use it for malicious purposes or to automate tasks without proper authorization.

## Contributing

Contributions are welcome! Please open an issue to discuss your idea or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.