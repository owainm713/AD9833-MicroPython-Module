# AD9833-MicroPython/Python-Module
MicroPython/Python module to use with the AD9833 programable waveform generator. Testing done with a AD9833 breakout
board off of Amazon and a Raspberry Pi Pico microcontroller for MicroPython and a Raspberry Pi3 for Python.

SPI requires py-spidev and python-dev modules for Python version.

SPI connections to the AD9833 board from the Pi Pico are as follows:
- Pico 3.3V to AD9833 Vin
- Pico Gnd to AD9833 DGND
- Pico IO2 SCLK to AD9833 SCLK
- Pico IO3 to AD9833 SDATA
- Pico IO1 to AD9833 FSynch

SPI connections to the AD9833 board from the Pi 3 are as follows:
- Pi 3.3V to AD9833 Vin
- Pi Gnd to AD9833 DGND
- Pi SCLK to AD9833 SCLK
- Pi MOSI  to AD9833 SDATA
- Pi CE0 or CE1 to AD9833 FSynch

Current functions include:
- set_frequency(fout, freqSelect) - function to set output frequencies (fout). Range 0 to 12.5MHz. Sets either the FREQ0 or FREQ1 registers - freqSelect 0 or 1.
- set_phase(pout, phaseSelect, rads = True) - function to set output phase (pout) in either degrees or radians. Sets either the PHASE0 or PHASE1 registers - phaseSelect 0 or 1.
- set_mode(mode = 'SIN') - function to output waveform shape. Valid values are; 'RESET','OFF','SIN','TRIANGLE','SQUARE','SQUARE/2 
- set_write_mode(writeMode = 'BOTH') - function to set how data is written to the frequency registers. Values values are; 'BOTH','MSB' and 'LSB' 
- select_freq_phase(FS, PS) - function to set which frequency and phase register values are used to set the output. FS & PS both can be either 0 or 1
- set_control_reg(B28 = 1, HLB = 0, FS = 0, PS = 0, RESET = 0, SLP1 = 0, SLP12 = 0, OP= 0, DIV2 = 0, MODE = 0) - function to set the individual bits of the control register.

See example file for sample usage.

Created Jun 12, 2023
Modified Jun 12, 2023