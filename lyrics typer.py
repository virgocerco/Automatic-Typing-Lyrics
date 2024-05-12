import time

# Delay for 10 seconds
initial_delay = 5
print(f"Starting in {initial_delay} seconds...")
time.sleep(initial_delay)

from pynput.keyboard import Controller, Key, Listener
import time
import threading
import pygame

stop_typing = False

def type_sentence_with_timing(sentences_with_timing, max_duration):
    global stop_typing
    keyboard = Controller()
    current_time = 0
    
    for sentence, start_time, end_time in sentences_with_timing:
        # Convert start and end times from the format "minutes:seconds:milliseconds" to seconds
        start_seconds = sum(x * int(t) for x, t in zip([60, 1, 0.001], start_time.split(":")))
        end_seconds = sum(x * int(t) for x, t in zip([60, 1, 0.001], end_time.split(":")))

        # Wait until the start time for the next sentence
        delay_before_start = max(start_seconds - current_time, 0)
        time.sleep(delay_before_start)
        
        if stop_typing:
            break
        
        # Calculate the duration available for typing the sentence
        duration = end_seconds - start_seconds

        # Calculate the delay per letter based on the length of the sentence and available duration
        delay_per_letter = duration / len(sentence)

        # Start the stopwatch for this sentence
        start_stopwatch = time.time()

        for letter in sentence:
            if stop_typing:
                break
            
            keyboard.press(letter)
            time.sleep(delay_per_letter)
            keyboard.release(letter)

            # Print elapsed time in the console
            elapsed_time = time.time() - start_stopwatch
            print(f"Elapsed Time: {elapsed_time:.2f}s / {duration}s", end="\r")
        
        current_time = end_seconds  # Update current time
        
        if current_time >= max_duration:
            stop_typing = True
            break

def stopwatch():
    global stop_typing
    start_time = time.time()
    pygame.mixer.init()
    pygame.mixer.music.load("C:\\Users\\Desktop\\music.mp3")
    pygame.mixer.music.play()
    while True:
        if stop_typing or not pygame.mixer.music.get_busy():
            break
        elapsed_time = time.time() - start_time
        music_time = pygame.mixer.music.get_pos() / 1000
        print(f"Stopwatch: {elapsed_time:.2f}s\tMusic Time: {music_time:.2f}s", end="\r")
        time.sleep(0.1)  # Update every 0.1 seconds

def on_release(key):
    global stop_typing
    if key == Key.esc:
        stop_typing = True
        return False

sentences_with_timing = [

    # chorus
    ("intro", "0:00:000", "0:02:000"),
    ("... ", "0:04:000", "0:6:000"),
    ("Imahinasyon-Lanzeta.mp3 ", "0:06:100", "0:10:000"),
    ("................. ", "0:010:100", "0:19:000"),
    ("gawa lang ba sa isip na malalim? ", "0:19:050", "0:22:000"),
    ("o sa imahinasyon ka lang ba galing? ", "0:22:150", "0:26:050"),
    ("sana mag tapat kana at sa pag-amin ", "0:26:100", "0:30:050"),
    ("ay maging totoo ka sa ", "0:31:000", "0:33:000"),
    ("akin ~~ ", "0:33:100", "0:35:100"),

    # first verse
    ("tunay ka nga ba talaga? ", "0:36:250", "0:38:500"),
    ("pagkat wala kang katulad at kagaya sa ", "0:39:100", "0:42:500"),
    ("ganda nya na tulala ka sa pantasya na ", "0:43:100", "0:46:500"),
    ("dala dalagang may mukang kaaya-aya sya ", "0:47:000", "0:50:100"),

    ("ang tipo ", "0:50:200", "0:51:000"),
    ("na paraisong ", "0:51:400", "0:52:400"),
    ("diwata ka na nandirito ", "0:52:900", "0:54:800"),
    ("sa may kastilyong ", "0:55:000", "0:56:500"),

    ("ikaw ang syang may ari ", "0:56:900", "0:58:400"),
    ("diyosang aparisyon ", "0:58:800", "1:00:500"),
    ("himalang pangyayari ", "1:00:700", "1:02:000"),
    ("iyo na syang ambisyon hiraya manawari ", "1:02:500", "1:05:800")

]

# Specify the maximum duration (in seconds)
max_duration = 180

# Start the stopwatch in a separate thread
stopwatch_thread = threading.Thread(target=stopwatch)
stopwatch_thread.start()

# Type the sentences with the specified start and end times
type_sentence_with_timing(sentences_with_timing, max_duration)

# Start listener to capture the key press to stop typing
with Listener(on_release=on_release) as listener:
    listener.join()
