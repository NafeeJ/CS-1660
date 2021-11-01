print("Welcome to Big Data Processing Application")
print("Please type the number that corresponds to the application you want to run:")

def print_options():
    print("-----")
    print("1. Apache Hadoop")
    print("2. Apache Spark")
    print("3. Jupyter Notebook")
    print("4. SonarQube and SonarScanner")
    print("5. Quit")
    print("-----")

while True:
    print_options()
    try:
        app = int(input("Type the number here > "))
        if app == 1:
            print("Launching Apache Hadoop")
            print()
        elif app == 2:
            print("Launching Apache Spark")
            print()  
        elif app == 3:
            print("Launching Jupyter Notebook")
            print()
        elif app == 4:
            print("Launching SonarQube and SonarScanner")
            print()
        elif app == 5:
            break
        else:
            print("Not an option")
            print()
    except:
        print("Give a number")
        print()