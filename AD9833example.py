"""AD9833example, example file on how to use the AD9833
micro python library

created June 1, 2023
modified June 17, 2023
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

import AD9833
import utime as time

ad9833 = AD9833.AD9833(sdo = 3, clk = 2, cs = 1,  fmclk = 25)

# setup frequency and phase registers
ad9833.set_frequency(1300,0)
ad9833.set_frequency(2600, 1)
ad9833.set_phase(0, 0, rads = False)
ad9833.set_phase(180, 1, rads = False)

delay = 1.5  # number of seconds to display each feature
time.sleep(delay)

# freq 0 Sin wave output
ad9833.select_freq_phase(0,0)
ad9833.set_mode('SIN')
time.sleep(delay)

# freq 1 Sin wave output
ad9833.select_freq_phase(1,0)
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

# freq 0 Sin wave output
ad9833.set_mode('SIN')
time.sleep(delay)

# change freq 0 to 1700 Hz, Sin wave output
ad9833.set_frequency(1700,0)
time.sleep(delay)

# output off
ad9833.set_mode('OFF')
