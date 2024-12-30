import visa
import numpy as np


class GpibController:
    
    def __init__(self):
        pass

    def __enter__(self):
        self.rm = visa.ResourceManager()
        # print(rm.list_resources())

        # self.ANDO AQ6315A grey old: 'GPIB0::1::INSTR'
        self.ando = self.rm.open_resoufrce('GPIB0::1::INSTR')

    def __exit__(self, exc_type, exc_value, traceback):
        self._handle_exit()
        return True  # Suppress the exception (if any)

    def status(self):
        # TODO: does this work? example https://pyvisa.readthedocs.io/en/latest/introduction/communication.html
        self.ando.query('*IDN?')

    def get_trace(self, trace):
        # TODO: is this needed?
        # remove the leading and the trailing characters, split values, remove the first value showing number of values in a dataset
        wl = self.ando.query('WDAT' + trace).strip().split(',')[1:]
        intensity = self.ando.query('LDAT' + trace).strip().split(',')[1:]
        # list of strings -> numpy array (vector) of floats
        wl = np.asarray(wl, 'f').T
        intensity = np.asarray(intensity, 'f').T
        return wl, intensity
    
    def save_trace(self, wl, intensity, filename):
        # TODO: is this needed?
        wl = np.asarray(wl, 'str')
        intensity = np.asarray(intensity, 'str')
        data = np.column_stack((wl, intensity))
    
        with open(filename + '.txt', "w") as txt_file:
            for line in data:
                txt_file.write(" ".join(line) + "\n")
        # todo: add exception handler
        return
    
    def handle_save(self, trace, filename):
        wl, intensity = self.get_trace(trace)  # Assuming get_trace is defined elsewhere
        self.save_trace(wl, intensity, filename)  # Assuming save_trace is defined elsewhere
        print("Done! File saved.")
    
    def handle_range(self, start_wl: float, stop_wl: float):
        self.ando.query(f'STAWL{start_wl}.00')
        self.ando.query(f'STPWL{stop_wl}.00')
    
    def handle_ref(self, ref: float):
        self.ando.query(f'REFL{ref}.0')
    
    def handle_res(self, res):
        self.ando.query(f'RESLN{res}')
    
    def handle_active(self, command):
        trace_map = {'A': '0', 'B': '1', 'C': '2'}
        trace = trace_map.get(command[-1:].upper(), None)
        if trace is not None:
            self.ando.query('ACTV' + trace)
    
    def handle_disp(self, command):
        self.ando.query('DSP' + command[-1:].upper())
    
    def handle_blank(self, command):
        self.ando.query('BLK' + command[-1:].upper())
    
    def handle_write(self, command):
        self.ando.query('WRT' + command[-1:].upper())
    
    def handle_fix(self, command):
        self.ando.query('FIX' + command[-1:].upper())
    
    def handle_auto(self):
        self.ando.query('AUTO')
    
    def handle_single(self):
        self.ando.query('SGL')
    
    def handle_repeat(self):
        self.ando.query('RPT')
    
    def handle_stop(self):
        self.ando.query('STP')
    
    def handle_hold(self):
        self.ando.query('SNHD')
    
    def handle_auto_sens(self):
        self.ando.query('SNAT')
    
    def handle_high1(self):
        self.ando.query('SHI1')
    
    def handle_high2(self):
        self.ando.query('SHI2')
    
    def handle_high3(self):
        self.ando.query('SHI3')
    
    def _handle_exit(self):
        self.ando.close()
        return False  # Signal to break the loop
