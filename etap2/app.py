import threading
from time import sleep

def run(name):
    print(f'Thanks for subscribing to {name}')
    sleep(1)
    print('Your subscription went away')

def main():
    sources = []
    source_names = ["Cosmopolitan", "New Yorker", "Streetstyle"]
    for name in source_names:
        t = threading.Thread(target=run, args=[name])
        t.start()
        sources.append(t)
    
    # print("Which source would you like to subscribe to?")
    # choice = int(input("Insert your choice"))

if __name__ == '__main__':
    main()
