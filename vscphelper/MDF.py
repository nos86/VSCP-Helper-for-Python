import requests
from xml.etree import ElementTree

class MDF(object):
    """This class manages all information about MDF file"""
    def __init__(self, mdf_url):
        self.url = mdf_url
        data = requests.get(mdf_url)
        self.root = ElementTree.fromstring(data.text)
        self.manufacturer = self.root.find('module/manufacturer')
        self.registers = self.root.find('module/registers')
        self.decisionMatrix = self.root.find('module/dmatrix')
        self.name = self.root.findall('module/name')[0].text

    def getManufacturerInfo(self):
        pass

    def getRegisterInformation(self, address, page=0):
        fields = ['name', 'access', 'help', 'description']
        data = {}
        for field in fields:
            node = self.registers.find('reg[@page="{}"][@offset="{}"]/{}'.format(page,address, field))
            if not node is None:
                data[field] = node.text
        return data

    def getRegisterName(self, address, page=0):
        reg = self.getRegisterInformation(address, page)
        return reg['name'] if 'name' in reg else 'N/A'
         
                                                     
    def decodeRegisterValue(self, address, page, value):
        result = {'name': self.getRegisterName(address, page), 'value': value}
        #Search for valuelist field
        if not self.registers.find('reg[@page="{}"][@offset="{}"]/valuelist'.format(page, address)) is None:
            for node in self.registers.findall('reg[@page="{}"][@offset="{}"]/valuelist/item'.format(page, address)):
                if value == int(node.get('value'), 0):
                    result['value'] = node.find('name').text
                    return result
        elif  not self.registers.find('reg[@page="{}"][@offset="{}"]/bit'.format(page, address)) is None:  #search for bit field
            result['value'] = {}
            for node in self.registers.findall('reg[@page="{}"][@offset="{}"]/bit'.format(page, address)):
                result['value'][node.find('name').text] = ((value & (2**int(node.get('pos')))) >0)
        return result
