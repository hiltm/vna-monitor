import pynanovna
import datetime
import skrf as rf

vna = pynanovna.VNA()

filename = '/home/chiptamper/chiptamper/logs/nanovna_' + str(datetime.datetime.now()) + '.csv'
calibrationFile = '/home/chiptamper/chiptamper/Calibration_1758496936.2956493.cal'

vna.load_calibration(calibrationFile)
print(vna.info())

for data in vna.stream():
    frequencies = data[0]
    s21 = data[1]
    s22 = data[2]

#frequencies, s21, s22 = vna.stream()

    print(f"{'Index':>5} | {'Frequency (Hz)':>15} | {'S21':>12} | {'S22':>12}")
    print("-" * 55)

    for i, (f, val21, val22) in enumerate(zip(frequencies, s21, s22)):
        print(f"{i:5d} | {f:15.2f} | {val21:12.6f} | {val22:12.6f}")