from os import system
import signal
import sys
import tty
import termios
import colorama

def clear_screen():
    _ = system('clear')


def alarmhandler(signum, frame):
    pass


def inputWait(wait_timeout=0.1):
    signal.signal(signal.SIGALRM, alarmhandler)
    signal.setitimer(signal.ITIMER_REAL, wait_timeout)

    try:
        charvar = '.'
        fedvar = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fedvar)
        try:
            tty.setraw(sys.stdin.fileno())
            charvar = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fedvar, termios.TCSADRAIN, old_settings)
        return charvar
    except:
        pass

    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return '.'
