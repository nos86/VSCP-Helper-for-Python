from vscphelper.MDF import MDF

if __name__=="__main__":
    var = MDF("http://vscp.salvomusumeci.com/aug.xml")
    print(var.name)
    print(var.getRegisterName(1))
    print(var.decodeRegisterValue(1,0,1))
    print(var.decodeRegisterValue(8,0,5))