import numpy as np
import pynanovna
from datetime import datetime
import skrf as rf
#from skrf.vi.vna.nanovna import NanoVNAv2
import matplotlib.pyplot as plt
import subprocess
import time
import os

vna = pynanovna.VNA()
#vna = NanoVNAv2("ASRL/dev/ttyACM0::INSTR")
print(vna)

plotting_enabled = True
start_freq = 1e6
stop_freq = 1.5e6
points = 99 #10 #101

plt.ion()
fig, ax = plt.subplots()
smith_chart = rf.setup_plotting()

def set_global_filename(filename_concat):
    global filename_glb 
    filename_glb = filename_concat
    return None

def get_global_filename():
    return filename_glb

def safe_sweep(vna, retries=3, delay=2):
    for attempt in range(retries):
        try:
            s11, s21, freqs = vna.sweep()
            s11 = np.array(s11, dtype=complex)
            s21 = np.array(s21, dtype=complex)
            freqs = np.array(freqs)

            s12 = np.zeros_like(s11) # generate empty S12
            s22 = np.zeros_like(s21) # generate empty S22

            return s11, s21, s12, s22, freqs
        except Exception as e:
            print(f"Error on sweep attempt {attempt+1}: {e}")
            time.sleep(delay)
    raise RuntimeError("Failed to complete sweep after multiple retires")

def capture_data(filename, start_freq, stop_freq, points):

    vna.set_sweep(start_freq, stop_freq, points)

    s11, s21, s12, s22, freqs = safe_sweep(vna, 3, 2)

    save_2port = True
    if save_2port:
        N = len(freqs)
        s = np.zeros((N, 2, 2), dtype=complex)
        s[:, 0, 0] = s11
        s[:, 0, 1] = s21
        s[:, 1, 0] = s12
        s[:, 1, 1] = s22

        freq_obj = rf.Frequency.from_f(freqs, unit='Hz')
        ntwk = rf.Network(frequency=freq_obj, s=s, name="NanoVNA 2-port")
        filename_concat = filename + "testdata.s2p"
        set_global_filename(filename_concat)
        ntwk.write_touchstone(filename_concat)
        print(f"Saved 2-port Touchstone as {filename_concat}")
        #if(plotting_enabled):
        #    ntwk.plot_s_smith()
        #    plt.show()
    else:
        N = len(freqs)
        s = s11.reshape(N, 1, 1)

        freq_obj = rf.Frequency.from_f(freqs, unit='Hz')
        ntwk = rf.Network(frequency=freq_obj, s=s, name="NanoVNA 1-port")
        filename_concat = filename + "testdata.s1p"
        set_global_filename(filename_concat)
        ntwk.write_touchstone(filename_concat)
        print(f"Saved 2-port Touchstone as {filename_concat}")
        #if(plotting_enabled):
        #    ntwk.plot_s_smith()
        #    plt.show()
    return freqs,s11,s21

#if __name__ == "__main__":
try:
    while(True):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        timestamp_year = datetime.now().strftime("%Y%m%d")
        filepath = f"/home/chiptamper/chiptamper/data/{timestamp_year}"

        if not os.path.exists(filepath):
           #os.makedirs(filepath)
           subprocess.run(["sudo", "mkdir", "-p", filepath])
           subprocess.run(["sudo", "chown", "chiptamper:chiptamper", filepath])

        print(timestamp)
        filename = filepath + f"/measurement_{timestamp}_"

        print("Taking measurement...")
        freqs,s11,s21 = capture_data(filename=filename, start_freq=1e6, stop_freq=1.5e6, points=10)#101)

        ax.clear()
#        smith_chart = rf.
   #     ntwk = rf.Network(get_global_filename())
   #     ntwk.plot_s_smith(ax=ax)
   #     ax.set_title(f"Smith Chart @ {get_global_filename()}")
   #     plt.draw()
        plt.pause(1)

        time.sleep(1)

except KeyboardInterrupt:
    print("stopped")

#finally:
#    vna.close()
#    plt.ioff()
#    plt.show()
