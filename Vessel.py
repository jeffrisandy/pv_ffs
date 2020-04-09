import pandas as pd
import datetime
from IntegrityAnalysis import IntegrityAnalysis


class Section(IntegrityAnalysis):
    def __init__(self, data):
        # init DATA
        self.DATA = data
        self.part_name = None
        
        # init data required
        self.t_nom = None
        self.t_now = None
        self.t_prev = None
        self.t_req = None
        self.date_now = self.DATA['insp_date_now']
        self.date_prev = self.DATA['insp_date_prev']
        self.year_built = self.DATA['YEAR_BUILT']
        self.interval = self.DATA['INTERVAL']
        self.E = None
        self.S = None
        self.OD = self.DATA['OD']
        self.OR = self.OD / 2
        self.DP = self.DATA['DP']

    def calc_t_req(self):
        pass

    def calc_cr_section(self):
        return self.calc_cr(self.t_nom, self.t_now, self.t_prev, \
                            self.date_now, self.date_prev, self.year_built)

    def choose_cr(self):
        if self.cr_short == None:
            return self.cr_long
        else:
            return max(self.cr_long, self.cr_short)

    def calc_rl(self):
        return self.remaining_life(self.t_now, self.t_req, self.cr)

    def rl_date(self, rl=None):
        """
        rl = years
        """
        if not rl:
            rl = self.rl
        end_life_date = pd.to_datetime(self.date_now, dayfirst=True) + datetime.timedelta(rl * 365.25)
        return end_life_date.strftime("%d-%b-%Y")

    def calc_mawp(self, interval=None):
        pass

    def isFit(self, interval=None):
        if not interval:
            interval = self.interval
        mawp = self.calc_mawp(interval)
        return mawp >= self.DP

    def print_ffs(self, interval=None):
        if not interval:
            interval = self.interval

        mawp = self.calc_mawp(interval)
        if self.isFit(interval):
            return f"The Vessel if fit for service at next inspection date. The MAWP is {mawp} psig which is larger than design pressure ({self.DP} psig)."
        else:
            return f"The Vessel is NOT fit for service at next inspection. The MAWP is {mawp} psig which is lower than design pressure ({self.DP} psig)."

    def derating_projection(self, increment=1, n=20, interval=None):
        if not interval:
            interval = self.interval

        print("          DERATING PRESSURE VS REMAINING LIFE")
        print("         " + "+" * 57)
        print("          |  Pressure(psig) |   RL Date      |   Next Insp. Date   ")
        print("         " + "+" * 57)

        for i in range(n):
            P = self.DP - (i * increment)
            t_req = self.t_shell(P, self.OD, self.S, self.E)
            rl = self.remaining_life(self.t_now, t_req, self.cr)
            rl_date = self.rl_date(rl)
            print(f"          | {P}              |   {rl_date}  |   {self.rl_date(min(interval, rl / 2))}    |")
        print('         ' + '-' * 57)

    def print_summary(self, interval=None):
        if not interval:
            interval = self.interval

        mawp = self.calc_mawp(interval)
        string = f"""
      *Corrosion rate*
      - Long Term Corrosion Rate = {self.cr_long} mm/year
      - Short Term Corrosion Rate = {self.cr_short} mm/year
      - Selected Corrosion Rate is {self.cr} mm/year

      *Thickness* 
      - Thickness actual = {self.t_now} mm.
      - Thickness Required = {self.t_req} mm.

      *Integrity*
      - Remaining life = {self.rl} years.
      - MAWP @next inspection at interval {interval} years = {mawp} psig.
      - Part anomaly status = {self.anomaly_status(self.rl)}

      *Conclusion*
      """
        if self.isFit(interval):
            string += f"""
      The {self.part_name} of the Vessel is fit for service within {interval} years interval at the next inspection date in {self.rl_date(
                interval)}. 
      The MAWP is {mawp} psig which is larger than the design pressure ({self.DP} psig).
      The remaining life is {self.rl} years which is due in {self.rl_date()}. 
      """
            print(string)
        else:
            string += f"""
      The {self.part_name} of the Vessel is NOT fit for service witin {interval} years interval at the next inspection in {self.rl_date(
                interval)} 
      The MAWP is {mawp} psig which is lower than the design pressure ({self.DP} psig).
      
      Recommendations are staged as per proposed local procedure:
         1. Shorten inspection interval.
         2. Derating, if possible.
         3. Repair.

      Below is the projection derating pressure and remaining life date.
      Note: derating pressure should be selected as appropriate.    
        """
            print(string)
            self.derating_projection(interval=interval)


class Shell(Section):
    def __init__(self, data):
        # init DATA
        super().__init__(data)

        # init data required specific for SHELL
        self.part_name = "Shell"
        self.t_nom = self.DATA['t_nom_shell']
        self.t_now = self.DATA['t_now_shell']
        self.t_prev = self.DATA['t_prev_shell']
        self.E = self.DATA['E_SHELL']
        self.S = self.DATA['S_SHELL']

        # suggest to use max value of current inspection if actual thick > nominal thick; skip NoneType tNow
        if not isinstance(self.t_now, (str, type(None))):
            if self.t_now > self.t_nom:
                print(
                    f"""    TML [{self.part_name}]: actual {self.t_now} > nominal thickness {self.t_nom}, use tNom={self.t_now}""")
                self.t_nom = self.t_now

        # calc t-Req
        self.t_req = self.calc_t_req()

        # calc corrosion rate
        self.cr_long, self.cr_short = self.calc_cr_section()
        self.cr = self.choose_cr()

        # calc remaining life
        self.rl = self.calc_rl()

    def calc_t_req(self):
        """
        Calc t required for tubular shell
        OUTPUT : a tuple of
          t_req_cir = mm, due to cir stress / long joints
        """

        return self.t_shell(self.DP, self.OD, self.S, self.E)

    def calc_mawp(self, interval=None):
        if not interval:
            interval = self.interval
        mawp = self.mawp_shell(self.t_now, self.cr, self.S, self.E, self.OR, interval)
        return round(mawp, 2)


class Head(Section):
    def __init__(self, data, label="head1"):
        # init DATA

        super().__init__(data)

        # init data required specific for HEAD
        self.part_name = self.DATA[f'{label}_name']
        self.t_nom = self.DATA[f't_nom_head']
        self.t_now = self.DATA[f't_now_{label}']
        self.t_prev = self.DATA[f't_prev_{label}']
        self.E = self.DATA['E_HEAD']
        self.S = self.DATA['S_HEAD']
        self.L = self.DATA['L']
        self.K = self.DATA['K']
        self.head_type = self.DATA['HEAD_TYPE']

        # suggest to use max value of current inspection if actual thick > nominal thick; skip NoneType tNow
        if not isinstance(self.t_now, (str, type(None))):
            if self.t_now > self.t_nom:
                print(
                    f"""    TML [{self.part_name}]: actual {self.t_now} > nominal thickness {self.t_nom}, use tNom={self.t_now}""")
                self.t_nom = self.t_now

        # calc t-Req
        self.t_req = self.calc_t_req()

        # calc corrosion rate
        self.cr_long, self.cr_short = self.calc_cr_section()
        self.cr = self.choose_cr()

        # calc remaining life
        self.rl = self.calc_rl()

    def calc_t_req(self):
        """
        Calc t required for tubular shell
        OUTPUT : a tuple of
          t_req_cir = mm
        """

        if "bottom" in self.part_name.lower():
            self.DP += 0.433 * self.L * 0.0833  # self.L in inch, so we need to convert it to feet unit

        t_req = self.t_shell(self.DP, self.OD, self.S, self.E)
        return t_req

    def calc_mawp(self, interval=None):
        if not interval:
            interval = self.interval
        mawp = self.mawp_head(self.t_now, self.cr, self.S, self.E, self.OD, interval, K=self.K,
                              head_type=self.head_type)
        return round(mawp, 2)


class Nozzle(Section):
    def __init__(self, data, nozzleID, size, height, tNom, tNow, tPrev, S, E):
        """
        INPUT:
          data = DATA dictionary
          nozzleID = int ID of nozzle
          size = NPS inch
          height = inch, nozzle location height measured from top
          tNom = mm, nominal thick
          tNow = mm, current thick
          tPrev = mm, previous thick
          S = psi, all. stress
          E = joint eff
        """
        # init DATA

        super().__init__(data)

        # init data required specific for NOZZLE
        self.part_name = nozzleID
        self.t_nom = tNom  # mm
        self.t_now = tNow  # mm
        self.t_prev = tPrev  # mm
        self.size = size  # NPS, inch
        self.height = height  # inch
        self.E = E
        self.S = S  # psi

        # suggest to use max value of current inspection if actual thick > nominal thick; skip NoneType tNow
        if not isinstance(self.t_now, (str, type(None))):
            if self.t_now > self.t_nom:
                print(
                    f"""    TML [{self.part_name}]: actual {self.t_now} > nominal thickness {self.t_nom}, use tNom={self.t_now}""")
                self.t_nom = self.t_now

        # calc t-Req
        self.t_req = self.calc_t_req()

        # calc corrosion rate
        self.cr_long, self.cr_short = self.calc_cr_section()
        self.cr = self.choose_cr()

        # calc remaining life
        self.rl = self.calc_rl()

    def calc_t_req(self):
        """
        Calc t required for tubular nozzle
        OUTPUT : a tuple of
          t_req_cir = mm, due to cir stress / long joints
        """
        DP = self.DP  # psi
        DP += 0.433 * self.height * 0.0833  # self.height in inch, so we need to convert it to feet unit

        t_req = self.t_nozzle(DP, self.size, self.S, self.E)  # mm
        return max(2.54, t_req)  # mm

    def calc_mawp(self, interval=None):
        """ return psig """
        if not interval:
            interval = self.interval
        mawp = self.mawp_nozzle(self.t_now, self.cr, self.S, self.E, self.size, self.height, interval)
        return round(mawp, 2)  # psig