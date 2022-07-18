import xml.etree.cElementTree as ET
import os

class XML():

    def name(self,response,tag,language,voice_name):
        speak = ET.Element("speak", version ="1.0", xmls = "http://www.w3.org/2001/10/synthesis", attrib={"xmlns:mstts" : "https://www.w3.org/2001/mstts","xmlns:emo":"http://www.w3.org/2009/10/emotionml", "xml:lang": language})
        voice = ET.SubElement(speak, "voice", name = voice_name) 
        # Calm
        prosody = ET.SubElement(voice, "prosody", rate = "0.00%", pitch = "0.00%")
        # Cheerful
        if tag == "Cheerful":
            response = "¡" + str(response) + "!"
        # Sad
        if tag == "Sad":
            prosody = ET.SubElement(lang, "prosody", rate = "-8.00%", pitch = "-4.00%")
        prosody.text = response
        arbol = ET.ElementTree(speak)
        arbol.write("respuesta.xml")
        return "echo"