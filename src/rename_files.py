''' Rename files. Built to make gifs in Latex.

Author: Bradley Reeves
Date: May 29, 2021

'''
import os

count = 0


def increment():
    global count
    count += 1


def main():
    # Move to the right directory
    os.chdir(r'../../../../Downloads/capbot')
    print(os.getcwd())

    # Do the renaming
    for f in os.listdir():
        f_name, f_ext = os.path.splitext(f)
        f_name = 'capbot-' + str(count)
        increment()

        new_name = '{}{}'.format(f_name, f_ext)
        os.rename(f, new_name)


if __name__ == "__main__":
    main()
