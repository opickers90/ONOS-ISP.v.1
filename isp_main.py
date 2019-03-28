from isp_script import running_program
from time import sleep


if __name__ == "__main__":
    counter = 1
    while counter == 1:
        print("Press 1 to Run Dijkstra's Shortest Path Calculation")
        print("Press 0 to QUIT\n")
        try:
            userInput = input("Enter Your Choice:")
            if userInput == "1":
                running_program()

            elif userInput == "0":
                sleep(1)
                print("Exit Program...")
                counter = 0

        except ValueError:
            print("Wrong Input")
            counter = 1
