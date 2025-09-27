import pynanovna
import datetime

vna = pynanovna.VNA()

filename = '/home/chiptamper/chiptamper/logs/nanovna_' + str(datetime.datetime.now()) + '.csv'
calibrationFile = '/home/chiptamper/chiptamper/Calibration_1758496936.2956493.cal'

vna.load_calibration(calibrationFile)
print(vna.info())
#vna.stream_to_csv(filename, nr_sweeps=100, skip_start=5, sweepdivider='sweepnumber: ')

vna.set_sweep(120000, 140000000, 101)
#s11, s21, frequencies = vna.sweep()
#print(s11)
#print(s21)
#print(frequencies)

# continuous sweep
for s11, s21, frequencies in vna.stream():
    print(s11, s21, frequencies)
#    # Do what I want with each sweep here
