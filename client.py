
import xmlrpc.client

#Creating client proxy to connect to the server
proxy = xmlrpc.client.ServerProxy("http://localhost:8000/RPC2", allow_none=True)

#Function to add a note
def add_note():
    topic = input("Enter topic: ")
    text = input("Enter note text: ")


    #Calling the server method to add the note with or without Wikipedia information
    result = proxy.add_note(topic, text) 
    print(result)

#Function to get notes based on topic
def get_notes():
    topic = input("Enter topic to get notes from: ")
    notes = proxy.get_notes(topic) #Calling the get_notes method from the server side with provided user's topic
    if notes:
        #If notes are found for the topic, print each note's information
        print(f"Notes from topic '{topic}':")
        for note in notes:
            print(f"Name: {note['name']}")
            print(f"Text: {note['text']}")
            print(f"Timestamp: {note['timestamp']}")
    
    else:
        print(f"No notes found on topic '{topic}'.")

#Creating a loop for user input
while True:
    print("\nOptions:")
    print("1. Add a note")
    print("2. Get notes from a topic")
    print("3. Exit")

    user_input = input("Enter your choice: ")

    if user_input == '1':
        add_note()

    elif user_input == '2':
        get_notes()

    elif user_input == '3':
        break #Break out the loop and terminate the program
    else:
        print("Invalid input. Please type the correct user input.")