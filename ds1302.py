# MicroPython driver for DS1302 Trickle Charge Timekeeping Chip
# Taken from https://www.mouser.mx/datasheet/2/256/DS1302-1292062.pdf
#
#      Chip Pinout 
#         _____
# V_CC2 -|  U  |- V_CC1
#    X1 -|     |- SCLK
#    X2 -|     |- I/O
#   GND -|_____|- CE
#
# Guia personal para desarrollo personal, par quitar al final del proyecto
# azul - Vcc - riel de 3V3
# morado - GND - riel de gnd
# gris - CLK - pin 16
# blanco - DAT pin 17
# negro - RST - pin 18

REG_SECONDS = 0x80
REG_MINUTES = 0x82
REG_HOUR    = 0x84
REG_DATE    = 0x86
REG_MONTH   = 0x88
REG_DAY     = 0x8A
REG_YEAR    = 0x8C
REG_RAM     = 0xC0

class DS1302:
    
    def __init__(self, dio, ce, clk):
        """dio, ce and clk are all pin objects"""
        self.dio = dio
        self.ce = ce
        self.clk = clk
        
    def _write_byte(self):
        pass
        
    def _read_byte(self):
        pass
    
    def _set_reg(self):
        pass
    
    def _read_reg(self):
        pass
    
    def second(self, data=None):
        pass
    
    def minutes(self, data=None):
        pass
    
    def hour(self, data=None):
        pass
    
    def date(self, data=None):
        pass
    
    def month(self, data=None):
        pass
    
    def day(self, data=None):
        pass
    
    def year(self, data=None):
        pass
    
    def ram(self, data=None):
        pass