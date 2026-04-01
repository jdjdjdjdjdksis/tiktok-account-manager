def show_menu():
    print("Welcome to the TikTok Account Manager!")
    print("1. View Account Details")
    print("2. Create a New Account")
    print("3. Delete an Account")
    print("4. Exit")

def main():
    while True:
        show_menu()
        choice = input("Please enter your choice: ")
        
        if choice == '1':
            print("Viewing account details...")
            # Add logic to view account details
        elif choice == '2':
            print("Creating a new account...")
            # Add logic to create a new account
        elif choice == '3':
            print("Deleting an account...")
            # Add logic to delete an account
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == '__main__':
    main()