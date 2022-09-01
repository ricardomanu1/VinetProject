import xml.etree.cElementTree as ET
import os

class XML():

    def esXML(self,response,tag,language):
        speak = ET.Element("speak", version ="1.0", xmls = "http://www.w3.org/2001/10/synthesis", attrib={"xmlns:mstts" : "https://www.w3.org/2001/mstts","xmlns:emo":"http://www.w3.org/2009/10/emotionml", "xml:lang": language})
        voice = ET.SubElement(speak, "voice", name = "es-ES-ElviraNeural") 
        # Calm
        prosody = ET.SubElement(voice, "prosody", rate = "0.00%", pitch = "0.00%")
        # Cheerful
        if tag == "Excited":
            response = "¡" + str(response) + "!"
        # Sad
        if tag == "Sad":
            prosody = ET.SubElement(lang, "prosody", rate = "-8.00%", pitch = "-4.00%")
        prosody.text = response
        arbol = ET.ElementTree(speak)
        arbol.write("respuesta.xml")
        return "echo"

    # SSML english
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
        arbol.write("respuesta.xml")
        return "echo"

    # SSML french
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
        arbol.write("respuesta.xml")
        return "echo"

    # SSML japanese
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
        arbol.write("respuesta.xml")
        return "echo"

    ## SSML inglés multilingüe emocional (en desarrollo)   
    def MultiSSML(self,response,tag,language,voice_name):
        speak = ET.Element("speak", version ="1.0", xmls = "http://www.w3.org/2001/10/synthesis", attrib={"xmlns:mstts" : "https://www.w3.org/2001/mstts","xmlns:emo":"http://www.w3.org/2009/10/emotionml", "xml:lang": language})
        voice = ET.SubElement(speak, "voice", name = en-US-JennyMultilingualNeural) 
        lang = ET.SubElement(voice, "lang", attrib={"xml:lang":"es-ES"})
        mstts = ET.SubElement(lang, "mstts:express-as", style = tag )
        prosody = ET.SubElement(mstts, "prosody", rate = "0.00%", pitch = "0.00%")
        prosody.text = response
        arbol = ET.ElementTree(speak)
        arbol.write("respuesta.xml")
        return "echo"