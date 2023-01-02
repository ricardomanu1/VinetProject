import xml.etree.cElementTree as ET
import os

class XML():

    #tags = ['happy','sad','fear','anger','surprise','bored','anxious','lonely','tired']

    # XML Spanish
    def esXML(self,response,tag,language,polarity):
        speak = ET.Element("speak", version ="1.0", xmls = "http://www.w3.org/2001/10/synthesis", attrib={"xmlns:mstts" : "https://www.w3.org/2001/mstts","xmlns:emo":"http://www.w3.org/2009/10/emotionml", "xml:lang": language})
        voice = ET.SubElement(speak, "voice", name = "es-ES-ElviraNeural") 
        # Calm
        prosody = ET.SubElement(voice, "prosody", rate = "0.00%", pitch = "0.00%")
        # happy
        ##if tag == "happy":
        ##    prosody = ET.SubElement(voice, "prosody", rate = "10.00%", pitch = "3.00%")
        # sad
        ##if tag == "sad":
        ##    prosody = ET.SubElement(voice, "prosody", rate = "-20.00%", pitch = "-5.00%")
        prosody.text = response
        arbol = ET.ElementTree(speak)
        arbol.write("Response/respuesta.xml")
        return "echo"

    # SSML English
    def enSSML(self,response,tag,language):
        speak = ET.Element("speak", version ="1.0", xmls = "http://www.w3.org/2001/10/synthesis", attrib={"xmlns:mstts" : "https://www.w3.org/2001/mstts","xmlns:emo":"http://www.w3.org/2009/10/emotionml", "xml:lang": language})
        voice = ET.SubElement(speak, "voice", name = "en-US-JennyNeural")
        if tag in ['cheerful','sad','terrified','angry','excited','friendly','shouting','unfriendly','whispering','hopeful']:
            mstts = ET.SubElement(voice, "mstts:express-as", style = tag )
            prosody = ET.SubElement(mstts, "prosody", rate = "0.00%", pitch = "0.00%")
        else:
             prosody = ET.SubElement(voice, "prosody", rate = "0.00%", pitch = "0.00%")
        prosody.text = response
        arbol = ET.ElementTree(speak)
        arbol.write("Response/respuesta.xml")
        return "echo"

    # SSML French
    def frSSML(self,response,tag,language):
        speak = ET.Element("speak", version ="1.0", xmls = "http://www.w3.org/2001/10/synthesis", attrib={"xmlns:mstts" : "https://www.w3.org/2001/mstts","xmlns:emo":"http://www.w3.org/2009/10/emotionml", "xml:lang": language})
        voice = ET.SubElement(speak, "voice", name = "fr-FR-DeniseNeural") 
        if tag in ['cheerful','sad']:
            mstts = ET.SubElement(voice, "mstts:express-as", style = tag )
            prosody = ET.SubElement(mstts, "prosody", rate = "0.00%", pitch = "0.00%")
        else:
             prosody = ET.SubElement(voice, "prosody", rate = "0.00%", pitch = "0.00%")
        prosody.text = response
        arbol = ET.ElementTree(speak)
        arbol.write("Response/respuesta.xml")
        return "echo"

    # SSML Japanese
    def jpSSML(self,response,tag,language):
        speak = ET.Element("speak", version ="1.0", xmls = "http://www.w3.org/2001/10/synthesis", attrib={"xmlns:mstts" : "https://www.w3.org/2001/mstts","xmlns:emo":"http://www.w3.org/2009/10/emotionml", "xml:lang": language})
        voice = ET.SubElement(speak, "voice", name = "ja-JP-NanamiNeural") 
        if tag in ['cheerful']:
            mstts = ET.SubElement(voice, "mstts:express-as", style = tag )
            prosody = ET.SubElement(mstts, "prosody", rate = "0.00%", pitch = "0.00%")
        else:
             prosody = ET.SubElement(voice, "prosody", rate = "0.00%", pitch = "0.00%")
        prosody.text = response
        arbol = ET.ElementTree(speak)
        arbol.write("Response/respuesta.xml")
        return "echo"

    ## SSML English multilingual with emotions (developing)   
    def MultiSSML(self,response,tag,language,voice_name):
        speak = ET.Element("speak", version ="1.0", xmls = "http://www.w3.org/2001/10/synthesis", attrib={"xmlns:mstts" : "https://www.w3.org/2001/mstts","xmlns:emo":"http://www.w3.org/2009/10/emotionml", "xml:lang": language})
        voice = ET.SubElement(speak, "voice", name = en-US-JennyMultilingualNeural) 
        lang = ET.SubElement(voice, "lang", attrib={"xml:lang":"es-ES"})
        mstts = ET.SubElement(lang, "mstts:express-as", style = tag )
        prosody = ET.SubElement(mstts, "prosody", rate = "0.00%", pitch = "0.00%")
        prosody.text = response
        arbol = ET.ElementTree(speak)
        arbol.write("Response/respuesta.xml")
        return "echo"