import random
import time
import numpy as np
import keyboard
from collections import defaultdict

class HumanKeyboard:
    def __init__(self,
                 wpm=70,
                 error_rate=0.04,
                 thinking_delay=150,
                 fatigue_max=1.3,
                 fatigue_increase=0.001,
                 fatigue_recovery=0.0005,
                 punctuation_multiplier=1.2,
                 number_multiplier=1.1,
                 space_multiplier=0.6,
                 shift_delay=50,
                 correction_delay=250,
                 backspace_delay=50,
                 distance_matrix=None):
        """
        Initialize typing model with customizable parameters.
        All parameters serve as means for their respective distributions.
        
        Args:
            wpm (float): Base words per minute
            error_rate (float): Base error rate (0-1)
            thinking_delay (float): Base delay (ms) when starting new words
            fatigue_max (float): Maximum fatigue multiplier
            fatigue_increase (float): Rate of fatigue increase per keystroke
            fatigue_recovery (float): Rate of fatigue recovery per second
            punctuation_multiplier (float): Timing multiplier for punctuation
            number_multiplier (float): Timing multiplier for numbers
            space_multiplier (float): Timing multiplier for spaces
            shift_delay (float): Additional delay (ms) for shifted characters
            correction_delay (float): Base delay (ms) before error correction
            backspace_delay (float): Base delay (ms) between backspaces
            distance_matrix (dict): Custom keyboard distance matrix
        """
        # Base typing speed with natural variation
        self.wpm = random.gauss(wpm, wpm * 0.1)
        self.baseline_delay = 60 / (self.wpm * 5) * 1000  # Convert WPM to ms per character
        self.distance_matrix = distance_matrix or self._default_distance_matrix()
        
        # Timing variations using natural distributions
        self.thinking_delay_mean = random.gauss(thinking_delay, thinking_delay * 0.1)
        self.thinking_delay_std = self.thinking_delay_mean * 0.2
        self.spacebar_multiplier = random.gauss(space_multiplier, space_multiplier * 0.08)
        self.shift_delay = random.gauss(shift_delay, shift_delay * 0.15)
        
        # Error and fatigue parameters
        self.error_rate = max(0.01, random.gauss(error_rate, error_rate * 0.2))
        self.fatigue_factor = random.gauss(1.0, 0.05)
        self.max_fatigue = random.gauss(fatigue_max, fatigue_max * 0.05)
        self.fatigue_increase_rate = random.gauss(fatigue_increase, fatigue_increase * 0.1)
        self.recovery_rate = random.gauss(fatigue_recovery, fatigue_recovery * 0.1)
        
        # Timing multipliers using log-normal for positive skew
        self.punctuation_delay = np.random.lognormal(
            np.log(punctuation_multiplier), 0.1)
        self.number_delay = np.random.lognormal(
            np.log(number_multiplier), 0.08)
        
        # Error correction parameters
        self.correction_delay_mean = random.gauss(correction_delay, correction_delay * 0.12)
        self.backspace_delay_mean = random.gauss(backspace_delay, backspace_delay * 0.15)
        
        # State tracking
        self.last_keystroke_time = time.time()
        self.common_bigrams = self._initialize_common_bigrams()
    
    def _initialize_common_bigrams(self):
        common_bigrams = {
            'th': 0.8, 'he': 0.8, 'in': 0.8, 'er': 0.8, 'an': 0.8,
            're': 0.8, 'on': 0.8, 'at': 0.8, 'en': 0.8, 'nd': 0.8,
            'ti': 0.8, 'es': 0.8, 'or': 0.8, 'te': 0.8, 'of': 0.8
        }
        return common_bigrams

    def _default_distance_matrix(self):
        keyboard_layout = {
            '`': (0, 0), '1': (1, 0), '2': (2, 0), '3': (3, 0), '4': (4, 0), '5': (5, 0),
            '6': (6, 0), '7': (7, 0), '8': (8, 0), '9': (9, 0), '0': (10, 0), '-': (11, 0),
            '=': (12, 0),
            'q': (1.5, 1), 'w': (2.5, 1), 'e': (3.5, 1), 'r': (4.5, 1), 't': (5.5, 1),
            'y': (6.5, 1), 'u': (7.5, 1), 'i': (8.5, 1), 'o': (9.5, 1), 'p': (10.5, 1),
            '[': (11.5, 1), ']': (12.5, 1), '\\': (13.5, 1),
            'a': (1.75, 2), 's': (2.75, 2), 'd': (3.75, 2), 'f': (4.75, 2), 'g': (5.75, 2),
            'h': (6.75, 2), 'j': (7.75, 2), 'k': (8.75, 2), 'l': (9.75, 2), ';': (10.75, 2),
            "'": (11.75, 2),
            'z': (2.25, 3), 'x': (3.25, 3), 'c': (4.25, 3), 'v': (5.25, 3), 'b': (6.25, 3),
            'n': (7.25, 3), 'm': (8.25, 3), ',': (9.25, 3), '.': (10.25, 3), '/': (11.25, 3),
            ' ': (6, 4)
        }
        matrix = defaultdict(lambda: defaultdict(float))
        
        for char1, pos1 in keyboard_layout.items():
            for char2, pos2 in keyboard_layout.items():
                dx = pos1[0] - pos2[0]
                dy = pos1[1] - pos2[1]
                distance = np.sqrt(dx**2 + dy**2) * 15
                
                if char1 == char2:
                    distance = 0
                elif char1 == ' ' or char2 == ' ':
                    distance *= 0.8
                elif abs(pos1[1] - pos2[1]) < 0.1:
                    distance *= 0.9
                
                matrix[char1][char2] = distance
        return matrix

    def _update_fatigue(self):
        current_time = time.time()
        time_since_last_keystroke = current_time - self.last_keystroke_time
        
        self.fatigue_factor += self.fatigue_increase_rate
        
        if time_since_last_keystroke > 1.0:
            self.fatigue_factor -= self.recovery_rate * time_since_last_keystroke
            
        self.fatigue_factor = min(self.max_fatigue, max(1.0, self.fatigue_factor))
        self.last_keystroke_time = current_time

    def calculate_delay(self, char1, char2, is_new_word=False, is_capital=False):
        self._update_fatigue()
        delay = self.baseline_delay * self.fatigue_factor

        if char1 and char2:
            bigram = char1.lower() + char2.lower()
            if bigram in self.common_bigrams:
                delay *= self.common_bigrams[bigram]

        if char1 and char2:
            char1_lower = char1.lower()
            char2_lower = char2.lower()
            if char1_lower in self.distance_matrix and char2_lower in self.distance_matrix[char1_lower]:
                delay += self.distance_matrix[char1_lower][char2_lower]

        if is_new_word:
            delay += np.random.normal(self.thinking_delay_mean, self.thinking_delay_std)
        if char2 in '.,!?;:':
            delay *= self.punctuation_delay
        elif char2.isdigit():
            delay *= self.number_delay
        elif char2 == ' ':
            delay *= self.spacebar_multiplier
        
        if is_capital:
            delay += self.shift_delay + np.random.normal(20, 5)
        delay *= np.random.normal(1, 0.1)
        return max(10, delay)

    def _get_nearby_keys(self, char):
        # Simple keyboard adjacency for QWERTY layout
        adjacency = {
            'a': 'qwsz', 'b': 'vghn', 'c': 'xdfv', 'd': 'ersfcx',
            'e': 'rdsw34', 'f': 'rtgvcd', 'g': 'tyhbvf', 'h': 'yujnbg',
            'i': 'ujko89', 'j': 'uikmnh', 'k': 'iml,jn', 'l': 'op;.,k',
            'm': 'njk,', 'n': 'bhjm', 'o': 'pkl9i', 'p': 'ol;0',
            'q': 'was21', 'r': 'tfd45e', 's': 'wedxzaz', 't': 'ygf45r',
            'u': 'hyjki78', 'v': 'cfgb', 'w': 'qase32', 'x': 'zasdc',
            'y': 'uhgt6t', 'z': 'asx', '1': '2q', '2': '13wq',
            '3': '24e', '4': '35r', '5': '46t', '6': '57y',
            '7': '68u', '8': '79i', '9': '80o', '0': '9p',
            ' ': ' '
        }
        char = char.lower()
        if char in adjacency:
            return list(adjacency[char])
        else:
            return [char]

    def generate_typing_with_errors(self, text):
        """
        Simulates typing the given text, introducing and correcting errors.
        
        Args:
            text (str): The text to type.
        
        Returns:
            list: A list of tuples containing (character_to_type, delay_in_ms).
        """
        typed_text = ""
        timings = []
        error_made = False

        i = 0  # Index in the original text
        while i < len(text):
            char = text[i]

            # Update fatigue and calculate delay
            self._update_fatigue()

            # Determine if an error should occur
            if not error_made and random.random() < self.error_rate:
                error_made = True
                # Choose an error type
                error_type = random.choices(
                    ['typo', 'double_letter', 'skip_letter', 'swap'],
                    weights=[0.4, 0.2, 0.2, 0.2],
                    k=1
                )[0]

                if error_type == 'typo':
                    # Replace current character with a typo
                    nearby_keys = self._get_nearby_keys(char)
                    typo_char = random.choice(nearby_keys)
                    # Add typo character
                    delay = self.calculate_delay(
                        typed_text[-1] if typed_text else None,
                        typo_char,
                        is_new_word=(typed_text and typed_text[-1] == ' '),
                        is_capital=typo_char.isupper()
                    )
                    timings.append((typo_char, delay))
                    typed_text += typo_char

                    # Simulate correction
                    correction_delay = self.correction_delay_mean
                    timings.append(('#wait', correction_delay))  # Wait before correcting
                    # Backspace the typo
                    backspace_delay = self.backspace_delay_mean
                    timings.append(('#backspace', backspace_delay))
                    typed_text = typed_text[:-1]

                    # Type the correct character
                    delay = self.calculate_delay(
                        typed_text[-1] if typed_text else None,
                        char,
                        is_new_word=(typed_text and typed_text[-1] == ' '),
                        is_capital=char.isupper()
                    )
                    timings.append((char, delay))
                    typed_text += char

                elif error_type == 'double_letter':
                    # Type the current character twice
                    for _ in range(2):
                        delay = self.calculate_delay(
                            typed_text[-1] if typed_text else None,
                            char,
                            is_new_word=(typed_text and typed_text[-1] == ' '),
                            is_capital=char.isupper()
                        )
                        timings.append((char, delay))
                        typed_text += char
                    # Simulate correction
                    correction_delay = self.correction_delay_mean
                    timings.append(('#wait', correction_delay))
                    # Backspace the extra character
                    backspace_delay = self.backspace_delay_mean
                    timings.append(('#backspace', backspace_delay))
                    typed_text = typed_text[:-1]

                elif error_type == 'skip_letter':
                    # Skip the current character (do nothing)
                    # Simulate correction
                    correction_delay = self.correction_delay_mean
                    timings.append(('#wait', correction_delay))
                    # Type the missing character
                    delay = self.calculate_delay(
                        typed_text[-1] if typed_text else None,
                        char,
                        is_new_word=(typed_text and typed_text[-1] == ' '),
                        is_capital=char.isupper()
                    )
                    timings.append((char, delay))
                    typed_text += char

                elif error_type == 'swap' and i < len(text) - 1:
                    # Swap current character with the next character
                    next_char = text[i + 1]
                    # Type the next character first
                    delay = self.calculate_delay(
                        typed_text[-1] if typed_text else None,
                        next_char,
                        is_new_word=(typed_text and typed_text[-1] == ' '),
                        is_capital=next_char.isupper()
                    )
                    timings.append((next_char, delay))
                    typed_text += next_char
                    # Type the current character
                    delay = self.calculate_delay(
                        typed_text[-1],
                        char,
                        is_new_word=(typed_text and typed_text[-1] == ' '),
                        is_capital=char.isupper()
                    )
                    timings.append((char, delay))
                    typed_text += char
                    i += 1  # We have consumed the next character already
                    # Simulate correction
                    correction_delay = self.correction_delay_mean
                    timings.append(('#wait', correction_delay))
                    # Backspace the two characters
                    backspace_delay = self.backspace_delay_mean
                    timings.extend([
                        ('#backspace', backspace_delay),
                        ('#backspace', backspace_delay)
                    ])
                    typed_text = typed_text[:-2]
                    # Type the correct characters in order
                    for c in [char, next_char]:
                        delay = self.calculate_delay(
                            typed_text[-1] if typed_text else None,
                            c,
                            is_new_word=(typed_text and typed_text[-1] == ' '),
                            is_capital=c.isupper()
                        )
                        timings.append((c, delay))
                        typed_text += c
                else:
                    # If swap not possible (at end of text), treat as typo
                    # (Alternative handling can be implemented)
                    pass

                error_made = False  # Reset error flag
            else:
                # No error, normal typing
                delay = self.calculate_delay(
                    typed_text[-1] if typed_text else None,
                    char,
                    is_new_word=(typed_text and typed_text[-1] == ' '),
                    is_capital=char.isupper()
                )
                timings.append((char, delay))
                typed_text += char

            i += 1  # Move to next character

        return timings, typed_text

    def type_text(self, text, real_time=True):
        timings, final_text = self.generate_typing_with_errors(text)

        if not real_time:
            keyboard.write(final_text)
            return

        typed_text = ""
        for char, delay in timings:
            if char == "#wait":
                time.sleep(delay / 1000)
                continue
            elif char == "#backspace":
                keyboard.press_and_release("backspace")
                typed_text = typed_text[:-1]
            else:
                if char.isupper() or char in '~!@#$%^&*()_+{}|:"<>?':
                    # Use keyboard.send to handle Shift + character
                    keyboard.send('shift+' + char.lower())
                else:
                    # For normal characters, use keyboard.write
                    keyboard.write(char)
                typed_text += char

            # Natural variation in timing using log-normal distribution
            actual_delay = delay * np.random.lognormal(-0.05, 0.1)
            time.sleep(max(10, actual_delay) / 1000)

if __name__ == "__main__":
    print("Switching to typing window in 5 seconds...")
    time.sleep(5)
    model = HumanKeyboard(wpm=110)
    text = "The quick brown fox jumps over the lázy dôg. This is a test sentence with some Capitals and numbers 12345."
    model.type_text(text)