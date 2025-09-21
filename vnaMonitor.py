import pynanovna
import datetime

vna = pynanovna.VNA()
print(vna.info())
filename = '/home/chiptamper/chiptamper/nanovna_' + str(datetime.datetime.now()) + '.csv'

vna.stream_to_csv(filename, nr_sweeps=100, skip_start=5, sweepdivider='sweepnumber: ')

#vna.set_sweep(1.0e9, 1.4e9, 101)
#s11, s21, frequencies = vna.sweep()
#print(s11)
#print(s21)
#print(frequencies)

# continuous sweep
#for s11, s21, frequencies in vna.stream():
#    print(s11, s21, frequencies)
#    # Do what I want with each sweep here
