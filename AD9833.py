"""AD9833, micropython module to use the AD983X
programable waveform generators

created June 2, 2023
modified June 2, 2023
"""

"""
Copyright 2023 Owain Martin

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import machine
import utime as time
from math import pi, radians

class AD9833:
    
    def __init__(self, sdo, clk, cs, fmclk = 25):
        """__init__, set up AD9833 object"""

        self.fmclk = fmclk*10**6

        # set up SPI connection details
        # had to use phase = 1 even though the datasheet
        # specifies phase = 0, on Pi SBC used phase = 0.
        self.sdo = machine.Pin(sdo)
        self.clk = machine.Pin(clk)
        self.cs = machine.Pin(cs, machine.Pin.OUT)
        self.cs.value(1)
        self.spi = machine.SPI(0, baudrate = 4000000, polarity = 1, phase =  1, sck= self.clk, mosi = self.sdo)      

        self.set_control_reg(B28 = 1, RESET = 1)

        self.mode = "RESET"
        self.writeMode = "BOTH"
        self.freq0 = 0
        self.freq1 = 0
        self.phase0 = 0
        self.phase1 = 0        

        return

    def write_data(self, data):
        """write_data, function to write data to
        the AD983x chip"""
        
        #print(data)        
        data = bytearray(data) # creates buffer object      
        
        self.cs.value(0)                   
        self.spi.write(data)        
        self.cs.value(1)       

        return

    def set_control_reg(self, B28 = 1, HLB = 0, FS = 0, PS = 0, RESET = 0, SLP1 = 0, SLP12 = 0, OP= 0, DIV2 = 0, MODE = 0):
        """set_control_reg, function to set any/all of the bits
        of the AD9833 control register"""

        self.B28 = B28
        self.HLB = HLB
        self.FS = FS
        self.PS = PS
        self.RESET = RESET
        self.SLP1 = SLP1
        self.SLP12 = SLP12
        self.OP = OP
        self.DIV2 = DIV2
        self.MODE = MODE

        controlReg = (B28<<13) + (HLB<<12) + (FS<<11) + (PS<<10) + (RESET<<8) + (SLP1<<7) + (SLP12<<6) + (OP<<5) + (DIV2<<3) + (MODE<<1)

        #print(hex(controlReg))
        
        controlRegList = [(controlReg & 0xFF00)>>8, controlReg & 0x00FF]

        self.write_data(controlRegList)

        return

    def set_frequency(self, fout, freqSelect):
        """set_frequency, function to set the frequency registers"""

        # calculate frequncy register value from fout
        freqR = int((fout*pow(2,28))/self.fmclk)

        # split frequency register value into 2
        # 14 bit segments
        fMSB = (freqR & 0xFFFC000)>>14
        fLSB = freqR & 0x3FFF

        # add register address to each 14 bit segment
        if freqSelect == 0:
            addr = 0b01
            self.freq0 = fout
        else:
            addr = 0b10
            self.freq1 = fout

        fMSB = fMSB + (addr<<14)
        fLSB = fLSB + (addr<<14)
        
        #print(hex(fLSB), hex(fMSB))

        # split fMSB & fLSB into 8 bits segements
        # for writing to AD9833 freq registers

        fLSBList = [(fLSB & 0xFF00)>>8, fLSB & 0x00FF]
        fMSBList = [(fMSB & 0xFF00)>>8, fMSB & 0x00FF]
        fBoth = fLSBList + fMSBList        

        if self.writeMode == 'MSB':
            self.write_data(fMSBList)
        elif self.writeMode == 'LSB':
            self.write_data(fLSBList)
        else:
            self.write_data(fBoth)

        return

    def set_phase(self, pout, phaseSelect, rads = True):
        """set_phase, function to set the phase registers"""

        # calculate the phase register value
        if rads == False:
            # convert degrees to radians
            pout = radians(pout)

        phaseR = int(pout*4096/(2*pi))

        # add phase address
        # 12 bit regValue
        # 1 bit - don't care
        # 3 bit address   
        phaseR = phaseR + (0b11<<14) + (phaseSelect<<13)

        # split phaseR into 8 bits segements
        # for writing to AD9833 phase registers
        phaseRList = [(phaseR & 0xFF00)>>8, phaseR & 0x00FF]

        self.write_data(phaseRList)

        return        

    def set_mode(self, mode = 'SIN'):
        """set_mode, function to set the mode/output type of the
        AD9833 as well as the active frequency and phase registers.
        Valid modes include: 'RESET', 'OFF', 'SIN','TRIANGLE',
        'SQUARE', 'SQUARE/2'"""

        self.mode = mode        

        if mode == 'SIN':
            self.set_control_reg(B28 = self.B28, HLB = self.HLB, FS = self.FS, PS = self.PS, RESET = 0, MODE = 0)
        elif mode == 'TRIANGLE':
            self.set_control_reg(B28 = self.B28, HLB = self.HLB, FS = self.FS, PS = self.PS, RESET = 0, MODE = 1)
        elif mode == 'SQUARE':
            self.set_control_reg(B28 = self.B28, HLB = self.HLB, FS = self.FS, PS = self.PS, RESET = 0, SLP12 = 1,
                                 OP = 1, DIV2 = 1, MODE = 0)
        elif mode == 'SQUARE/2':
            self.set_control_reg(B28 = self.B28, HLB = self.HLB, FS = self.FS, PS = self.PS, RESET = 0, SLP12 = 1,
                                 OP = 1, DIV2 = 0, MODE = 0)
        elif mode == 'RESET':
            self.set_control_reg(B28 = self.B28, HLB = self.HLB, FS = self.FS, PS = self.PS, RESET = 1)
        elif mode == 'OFF':
            self.set_control_reg(B28 = self.B28, HLB = self.HLB, FS = self.FS, PS = self.PS, RESET = 1, SLP1 = 1, SLP12 = 1)

        return

    def set_write_mode(self, writeMode = 'BOTH'):
        """set_write_mode, function to set the B28 and HLB bits in the
        control register which control how data is written to the
        frequency registers. Valid value for writeMode are 'BOTH',
        'MSB' and 'LSB'"""

        B28 = 1
        HLB = 0
        self.writeMode = 'BOTH'

        if writeMode == 'MSB':
            B28 = 0
            HLB = 1
            self.writeMode = 'MSB'
        elif writeMode == 'LSB':
            B28 = 0
            HLB = 0
            self.writeMode = 'LSB'

        self.set_control_reg(B28 = B28, HLB = HLB, FS = self.FS, PS = self.PS, RESET = self.RESET, SLP1 = self.SLP1,
                             SLP12 = self.SLP12, OP = self.OP, DIV2 = self.DIV2, MODE = self.MODE)

        return
        

    def select_freq_phase(self, FS, PS):
        """select_freq_phase, function to select which frequency and phase register
        the AD9833 uses and changes to them"""

        self.set_control_reg(B28 = self.B28, HLB = self.HLB, FS = FS, PS = PS, RESET = self.RESET, SLP1 = self.SLP1,
                             SLP12 = self.SLP12, OP = self.OP, DIV2 = self.DIV2, MODE = self.MODE)

        return
    

if __name__ == "__main__":

    #ad9833 = AD9833(sdo = 19, clk = 18, cs = 17,  fmclk = 25)
    ad9833 = AD9833(sdo = 3, clk = 2, cs = 1,  fmclk = 25)
    
    delay = 3
    
    ad9833.set_frequency(1100,0)
    ad9833.set_frequency(2200, 1)
    ad9833.set_phase(0, 0, rads = False)
    ad9833.set_phase(180, 1, rads = False)
    ad9833.select_freq_phase(0,0)
    ad9833.set_mode('SIN')
    time.sleep(delay)

    ad9833.set_write_mode('LSB')
    ad9833.set_frequency(1200,0)
    time.sleep(delay)
    
    ad9833.select_freq_phase(1,0)
    time.sleep(delay)
    
    ad9833.set_mode('TRIANGLE')
    time.sleep(delay)
    
    # freq 0 Triangle wave output
    ad9833.select_freq_phase(0,0)
    ad9833.set_mode('TRIANGLE')
    time.sleep(delay)

    # freq 0 Square wave output
    ad9833.set_mode('SQUARE')
    time.sleep(delay)

    # freq 0 divide by 2 Square wave output
    ad9833.set_mode('SQUARE/2')
    time.sleep(delay)    

    # change freq 0 to 1700 Hz, Sin wave output
    ad9833.set_write_mode('BOTH')
    ad9833.set_frequency(1700,0)
    ad9833.set_mode('SIN')
    time.sleep(delay)
    
    ad9833.set_mode('OFF')
        
        
