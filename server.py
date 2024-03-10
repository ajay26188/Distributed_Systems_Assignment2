import xmlrpc.server
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
from datetime import datetime

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# XML Database file
XML_FILE = 'db.xml'

class NoteServer:
    def __init__(self):
        #Loading existing XML datatbase or creating a new one
        try:
            self.tree = ET.parse(XML_FILE)
            self.root = self.tree.getroot()
        except FileNotFoundError:
            self.root = ET.Element("data")
            self.tree = ET.ElementTree(self.root)

    def add_note(self, topic, text):
        #Checking if the topic exists
        topic_element = self.root.find(f"topic[@name='{topic}']")

        if topic_element is not None:
            #If there is such existing topic, append the new note to it.
            note_element = ET.SubElement(topic_element, "note")
            
            first_note_name = topic_element.find("note").get("name")
            note_element.set("name", first_note_name)

        else:
            #If there is no such existing topic, create a new topic and append the note to it.
            topic_element = ET.SubElement(self.root, "topic")
            topic_element.set("name", topic)

            #Creating a new note element
            note_element = ET.SubElement(topic_element, "note")
            note_element.set("name", "Note_1")

        #Add text and timestamp to the note
        text_element = ET.SubElement(note_element, "text")
        text_element.text = text

        timestamp_element = ET.SubElement(note_element, "timestamp")
        timestamp_element.text = datetime.now().strftime("%m%d%y - %H:%M:%S")

        #Saving changes to existing db.xml file
        self.indent(self.root)
        self.tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)

        #If note is added successfully
        return "New topic and note added successfully!"
        
    def get_notes(self, topic):
        #Finding notes based of the topic
        notes = []
        topic_element = self.root.find(f"topic[@name='{topic}']")
        if topic_element is not None:
            for note in topic_element.findall("note"):
                note_info = {
                    "name": note.get("name"),
                    "text": note.find("text").text,
                    "timestamp": note.find("timestamp").text
                }
                notes.append(note_info)

        return notes
    
    def indent(self, elem, level=0):
        i = "\n" + level * " "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + " "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i

        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i


#Creating server
server = xmlrpc.server.SimpleXMLRPCServer(("localhost",8000),requestHandler=RequestHandler, allow_none=True)
server.register_instance(NoteServer())

#Running the sever's main loop
print("Server listening on port 8000")
server.serve_forever()