import sys


def main():
    sys.stdout.buffer.writelines(sys.stdin.buffer)


if __name__ == "__main__":
    main()
