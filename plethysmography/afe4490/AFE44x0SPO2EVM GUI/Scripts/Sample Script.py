GUI_Module=__import__('Device_GUI')
GUI=GUI_Module.Device_GUI("AFE44x0SPO2EVM GUI")

for i in range (10):
    GUI=GUI_Module.Device_GUI("AFE44x0SPO2EVM GUI")
    GUI.write_register("AFE4490","LED2STC",0x1770)
    GUI.write_register("AFE4490","LED2ENDC",0x1F3E)
    GUI.write_register("AFE4490","LED2LEDSTC",0x1770)
    GUI.write_register("AFE4490","LED2LEDENDC",0x1F3F)
    GUI.write_register("AFE4490","ALED2ENDC",0x7CE)
    GUI.write_register("AFE4490","LED1STC",0x7D0)
    GUI.write_register("AFE4490","LED1ENDC",0xF9E)
    GUI.write_register("AFE4490","LED1LEDSTC",0x7D0)
    GUI.write_register("AFE4490","LED1LEDENDC",0xF9F)
    GUI.write_register("AFE4490","ALED1STC",0xFA0)
    GUI.write_register("AFE4490","ALED1ENDC",0x176E)
    GUI.write_register("AFE4490","LED2CONVST",0x2)
    GUI.write_register("AFE4490","LED2CONVEND",0x7CF)
    GUI.write_register("AFE4490","ALED2CONVST",0x7D2)
    GUI.write_register("AFE4490","ALED2CONVEND",0xF9F)
    GUI.write_register("AFE4490","LED1CONVST",0xFA2)
    GUI.write_register("AFE4490","LED1CONVEND",0x176F)
    GUI.write_register("AFE4490","ALED1CONVST",0x1772)
    GUI.write_register("AFE4490","ALED1CONVEND",0x1F3F)
    GUI.write_register("AFE4490","ADCRSTCT1",0x7D0)
    GUI.write_register("AFE4490","ADCRENDCT1",0x7D0)
    GUI.write_register("AFE4490","ADCRSTCT2",0xFA0)
    GUI.write_register("AFE4490","ADCRENDCT2",0xFA0)
    GUI.write_register("AFE4490","ADCRSTCT3",0x1770)
    GUI.write_register("AFE4490","ADCRENDCT3",0x1770)
    GUI.write_register("AFE4490","PRPCOUNT",0x1F3F)
    GUI.write_register("AFE4490","CONTROL1",0x101)
    GUI.write_register("AFE4490","LEDCNTRL",0x11414)
    GUI.write_register("AFE4490","TIAGAIN",0x0)
    GUI.read_register("AFE4490","ALED1CONVST")
    GUI.read_register("AFE4490","ALED1CONVEND")
    GUI.read_register("AFE4490","ADCRSTCT0")
    GUI.read_register("AFE4490","ADCRENDCT0")
    GUI.read_register("AFE4490","ADCRSTCT1")
    GUI.read_register("AFE4490","ADCRENDCT1")
    GUI.read_register("AFE4490","ADCRSTCT2")
    GUI.read_register("AFE4490","ADCRENDCT2")
    GUI.read_register("AFE4490","ADCRSTCT3")
    GUI.read_register("AFE4490","ADCRENDCT3")
    GUI.read_register("AFE4490","PRPCOUNT")
    GUI.read_register("AFE4490","CONTROL1")
    GUI.read_register("AFE4490","SPARE1")
    GUI.read_register("AFE4490","TIAGAIN")
    GUI.read_register("AFE4490","TIA_AMB_GAIN")
    GUI.read_register("AFE4490","LEDCNTRL")
    GUI.read_register("AFE4490","ALED1VAL")
    GUI.read_register("AFE4490","LED2-ALED2VAL")
    GUI.read_register("AFE4490","LED1-ALED1VAL")
    GUI.read_register("AFE4490","DIAGNOSTICS")
GUI.__del__()
