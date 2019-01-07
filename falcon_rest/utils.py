import uuid
import datetime

import xml.etree.ElementTree as ET

    
def timestamp_uuid():
    return ( str( datetime.datetime.utcnow().timestamp() ).split('.')[0] ) + uuid.uuid4().hex

def convert_xml_to_dict(xml):
    root=ET.fromstring(xml.decode())
    it=root.iter()

    d={}
    for i in it:
        if len(i)==0:
            tag=i.tag.strip()
            if '}' in tag:
                tag=(tag.split('}')[1]).strip()
            text=i.text.strip()

            d.update({tag:text})

    return d