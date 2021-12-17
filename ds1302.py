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
# Structure of a Byte
# | 7 |    6    | 5  | 4  | 3  | 2  | 1  |   0    |
# | 1 | RAM/^CK | A4 | A3 | A2 | A1 | A0 | RD/^WR |
# Writing Sequence: little endian
#

from machine import Pin

REG_SECONDS  = 0x80
REG_MINUTES  = 0x82
REG_HOUR     = 0x84
REG_DATE     = 0x86
REG_MONTH    = 0x88
REG_WEEK_DAY = 0x8A
REG_YEAR     = 0x8C
REG_WP       = 0x8E  # Write protect
REG_RAM      = 0xC0
REG_CONTROL  = 0x90

class DS1302:
    
    def __init__(self, dio, ce, clk):
        """dio, ce and clk are all pin objects"""
        self.dio = dio
        self.ce = ce
        self.clk = clk
        self.clk.init(Pin.OUT)
        self.ce.init(Pin.OUT)
    
    # Register methods
    def _write_byte(self, data):
        """Low level write to I/O pin"""
        self.dio.init(Pin.OUT)
        for i in range(8):
            self.dio.value((data>>i) & 1)
            self.clk.value(1)
            self.clk.value(0)
        
    def _read_byte(self):
        """Low level read of I/O pin"""
        self.dio.init(Pin.IN)
        data = 0
        for i in range(8):
            data = data | (self.dio.value()<<i)
            self.clk.value(1)
            self.clk.value(0)
        return data
    
    def _set_reg(self, register, data):
        """Higher level write of register, takes register and data"""
        data = self._dec_to_hex(data)
        self.ce.value(1)
        self._write_byte(register)
        self._write_byte(data)
        self.ce.value(0)
    
    def _read_reg(self, register):
        """Lower level read of register, returns read"""
        register += 1                   # always is reg plus one
        self.ce.value(1)
        self._write_byte(register)
        data = self._read_byte()
        data = self._hex_to_dec(data)
        self.ce.value(0)
        return data
    
    def _hex_to_dec(self, number):
        """Needed because DS1302 returns hex numbers as if they were decimal"""
        return (number//16)*10 + (number%16)
    
    def _dec_to_hex(self, number):
        """Needed because DS1302 receives hex numbers as if they were decimal"""
        return (number//10)*16 + (number%10)
    
    # Time methods
    def datetime(self, date_time=None):
        """Sets a datetime if given, else returns the current datetime \n
        datetime tuple is (year, month, day, hour, minuutes, second)"""
        # TO DO: create a function to calculate day of week
        if date_time == None:
            print("returning date time ")
            return (
                self.year(),
                self.month(),
                self.week_day(),
                self.date(),
                self.hours(),
                self.minutes(),
                self.seconds())
        else:
            print("setting date and time")
            self.year(date_time[0])
            self.month(date_time[1])
            self.week_day(date_time[2])
            self.date(date_time[3])
            self.hours(date_time[4])
            self.minutes(date_time[5])
            self.seconds(date_time[6])
            
    
    def seconds(self, second=None):
        """Sets _ if given, else returns the current \n
        | 7  | 6 - 4  |  3 - 0   | Range | \n
        | CH | 10 sec | seconds  | 00-59 |"""
        if second == None:
            return self._read_reg(REG_SECONDS)
        else:
            self._set_reg(REG_SECONDS, second)
    
    def minutes(self, minute=None):
        """Sets minutes if given, else returns the current minute \n
        | 7 | 6 - 4  |  3 - 0  | Range | \n
        | * | 10 min | minutes | 00-59 |"""
        if minute == None:
            return self._read_reg(REG_MINUTES)
        else:
            self._set_reg(REG_MINUTES, minute)
    
    def hours(self, hour=None):
        """Sets the hour if given, else returns the current hour \n
        |   7    | 6 |        5      |  4   | 3 - 0  |    Range    | \n
        | 12/^24 | 0 | ^AM/PM \ 10hr | 10hr | Hour   | 1-12 \ 0-23 |"""
        if hour == None:
            return self._read_reg(REG_HOUR)
        else:
            self._set_reg(REG_HOUR, hour)
            
    
    def date(self, curr_date=None):
        """Sets day of month if given, else returns the current day of month \n
        | 7 - 6 | 5 - 4  | 3 - 0 | Range | \n
        |   0   | 10 day |  day  | 01-31 |"""
        if curr_date == None:
            return self._read_reg(REG_DATE)
        else:
            self._set_reg(REG_DATE, curr_date)
    
    def month(self, months=None):
        """Sets month if given, else returns the current month \n
        | 7 - 5 |    4    |  3 - 0 | Range | \n
        |   0   | 10 mnth |  mnth  | 01-12 |"""
        if months == None:
            return self._read_reg(REG_MONTH)
        else:
            self._set_reg(REG_MONTH, months)
    
    def week_day(self, days=None):
        """Sets the day of the week if given, else returns the current day \n
        | 7 - 3 | 2 - 0  | Range | \n
        |   0   |  day   | 01-07 |"""
        if days == None:
            return self._read_reg(REG_WEEK_DAY)
        else:
            self._set_reg(REG_WEEK_DAY, days)
    
    def year(self, years=None):
        """Sets year if given, else returns the current year\n
        | 7 - 4  | 3 - 0  | Range | \n
        |  10yr  | year   | 00-99 |"""
        if years == None:
            return self._read_reg(REG_YEAR)
        else:
            self._set_reg(REG_YEAR, years)
    
    def clock_halt(self, halt=True):
        """Halts the clock if called, if arg halt=None resumes the clock \n
        sets or lowers the 7th bit of the seconds register"""
        if halt == True:
            command = self.seconds() | 0x10000000 # 0x80
        else:
            command = self.seconds() & 0x01111111 # 0x7F
        self.seconds(command)
    
    # RAM methods
    def ram(self, ram_adress, data=None):
        """Reads a section in RAM memory"""
        pass
    
    def ram_burst(self, data=None):
        """Returns all of the RAM in a burst"""
        pass
    
#
# Guia personal para desarrollo personal, para quitar al final del proyecto
#   azul - Vcc - riel de 3V3
# morado - GND - riel de gnd
#   gris - CLK - pin 16
# blanco - DAT - pin 17
#  negro - RST - pin 18
#
