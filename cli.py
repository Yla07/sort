from backend import sortowanie
import os


def wait_for_key():
    print("Press any key to continue...", end="", flush=True)
    if os.name == "nt":
        import msvcrt
        msvcrt.getch()
    else:
        import sys
        import termios
        import tty

        file_descriptor = sys.stdin.fileno()
        previous_settings = termios.tcgetattr(file_descriptor)
        try:
            tty.setraw(file_descriptor)
            sys.stdin.read(1)
        finally:
            termios.tcsetattr(file_descriptor, termios.TCSADRAIN, previous_settings)
    print()

def sort_menu(choice, sorter):

    if choice == '4':
        data = sorter.get_data()
        sorted_data = sorter.bubble_sort(data)
        print(f"Bubble Sorted items: {sorted_data}")
    elif choice == '5':
        data = sorter.get_data()
        sorted_data = sorter.quick_sort(data)
        print(f"Quick Sorted items: {sorted_data}")
    elif choice == '6': 
        data = sorter.get_data()
        sorted_data = sorter.insertion_sort(data)
        print(f"Insertion Sorted items: {sorted_data}")
    elif choice == '7':
        data = sorter.get_data()
        sorted_data = sorter.selection_sort(data)
        print(f"Selection Sorted items: {sorted_data}")

    wait_for_key()


def display_data(sorter):
    print("Current items:")
    print(sorter.get_data())
    wait_for_key()
     


def main():

    sorter = sortowanie()

    while True:
        print("Menu:")
        print("1. Add item")
        print("2. Display items")
        print("3. Clear items")
        print("4. Bubble Sort")
        print("5. Quick Sort")
        print("6. Insertion Sort")
        print("7. Selection Sort")
        print("8. Exit")
        print("9. Generate random items")

        choice = input("Enter your choice: ")

        if choice == '1':
            item = input("Enter item to add: ")
            sorter.add(item)
            print(f"Added: {item}")
        elif choice == '2':
            data = sorter.get_data()
            print(f"Items: {data}")
        elif choice == '3':
            sorter.clear()
            print("Items cleared.")

        elif choice == '8':
            print("Exiting...")
            break
        elif choice in ['4', '5', '6', '7']:
            sort_menu(choice, sorter)
        elif choice == '9':
            min_value = int(input("Enter minimum value: "))
            max_value = int(input("Enter maximum value: "))
            size = int(input("Enter number of items to generate: "))
            generated_data = sorter.generate_data(min_value, max_value, size)
            sorter.data = generated_data
            print(f"Generated items: {generated_data}")
        else:
            print("Invalid choice. Please try again.")
        

if __name__ == "__main__":
    main()