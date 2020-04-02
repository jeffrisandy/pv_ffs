import pandas as pd


class IntegrityAnalysis():
    """
    This class is to calculate basic function in evaluation integrity of vessel
    It includes calc : corrosion rate, remaining life, MAWP
    """

    def t_shell(self, DP, OD, S, E):
        """
        Calc t required for tubular shell
        INPUT :
          DP = psi, design pressure
          OD = inch, outside diamter
          S = psi, all. stress
          E = joint efficiency
        OUTPUT : a tuple of
          t_req_cir = mm, due to cir stress / long joints
        """

        R = (OD / 2)

        # circ stress / long joint
        t_circ = DP * R
        t_circ /= (S * E) + (0.4 * DP)
        t_circ = t_circ * 25.4  # convert to mm

        return round(t_circ, 4)

    def t_head(DP, OD, S, E, K=1, head_type="ellipsoidal"):
        """
        Calc t required for head ellips and hemis
        INPUT :
          DP = psi, design pressure
          OD = inch, outside diamter
          S = psi, all. stress
          E = joint efficiency
        OUTPUT : a tuple of
          t_req = mm, due to cir stress / long joints
        """
        if head_type.lower() == "ellipsoidal":
            t = DP * OD * 1
            t /= (2 * S * E) + (2 * DP * (K - 0.1))
        elif head_type.lower() == "hemispherical":
            t = DP * OD * 0.5
            t /= (2 * S * E) + (0.8 * DP)
        else:
            return print("Please input head_type: hemispherical or ellipsoidal")

        return round(t * 25.4, 4)  # convert back to mm

    def t_nozzle(self, DP, OD, S, E):
        """
        Calc t required for tubular nozzle
        INPUT :
          DP = psi, design pressure
          OD = inch, outside diamter
          S = psi, all. stress
          E = joint efficiency
        OUTPUT : a tuple of
          t_req = mm
        """
        t_req = DP * OD
        t_req /= 2 * S * E
        return round(t_req * 25.4, 4)  # convert back to mm

    def calc_cr(self, tNom, tNow, tPrev, dateNow, datePrev, yearBuilt):
        """
        INPUT :
          tNom, mm - nominal thick
          tNow, mm - current thick
          tPrev, mm - previous thick
          dateNow & datePrev, string of current inspection date with format date/month/year
          yearBuilt, int of year built
        OUTPUT : long CR, short CR in mm/year
        """
        # parse date
        date_now = pd.to_datetime(dateNow, dayfirst=True)

        # calc long term CR
        cr_long = tNom - tNow
        cr_long /= date_now.year - yearBuilt
        cr_long = round(cr_long, 4)
        if cr_long < 0:
            cr_long = 0.00001

            # calc short term CR
        if tPrev:
            date_prev = pd.to_datetime(datePrev, dayfirst=True)
            delta_year = round((date_now - date_prev).days / 365.25, 2)
            cr_short = tPrev - tNow
            cr_short /= delta_year
            cr_short = round(cr_short, 4)
            if cr_short < 0:
                cr_short = 0.00001
        else:
            cr_short = None

        return cr_long, cr_short

    def remaining_life(self, t_act, t_req, cr):
        rl = (t_act - t_req) / cr
        rl = min(rl, 100)
        if rl < 0:
            rl = 0
        return round(rl, 2)

    def mawp_shell(self, t_act, cr, S, E, oR, interval):
        """
        MAWP for SHELL
        INPUT :
          t_act = mm, current thickness
          cr = mm/year, corrosion rate
          S = psi, allowable stress
          E = joint efficiency
          oR = inch, outside radius
          interval, int years of inspection interval
        OUTPU :
          mawp = psig, maximum allowable working pressure
        """

        # convert unit of t_act and cr
        t_act = t_act * 0.03937  # inch
        cr = cr * 0.03937  # inch per year

        # calc mawp
        mawp = S * E * (t_act - (2 * cr * interval))
        mawp /= oR - (0.4 * (2 * cr * interval))
        return mawp

    def mawp_head(self, t_act, cr, S, E, OD, interval, K=1, head_type="ellipsoidal"):
        """
        MAWP for HEAD
        INPUT :
          t_act = mm, current thickness
          cr = mm/year, corrosion rate
          S = psi, allowable stress
          E = joint efficiency
          interval = int, years, mawp at next inspection year
          OD = inch, outside dia
          K = 1, default for ellips 2:1
          interval, int years of inspection interval
        OUTPU :
          mawp = psig, maximum allowable working pressure
        """

        # convert unit of t_act and cr
        t_act = t_act * 0.03937  # inch
        cr = cr * 0.03937  # inch per year
        t_pred = t_act - (2 * cr * interval)

        if head_type.lower() == "ellipsoidal":
            mawp = 2 * S * E * t_pred
            mawp /= (K * OD) - (2 * t_pred * (K - 0.1))
        elif head_type.lower() == "hemispherical":
            mawp = 2 * S * E * t_pred
            mawp /= (OD / 2) - (0.8 * t_pred)
        else:
            return print("Please input head_type: hemispherical or ellipsoidal")

        return mawp

    def mawp_nozzle(self, t_act, cr, S, E, OD, h, interval):
        """
        MAWP for HEAD
        INPUT :
          t_act = mm, current thickness
          cr = mm/year, corrosion rate
          S = psi, allowable stress
          E = joint efficiency
         OD = inch, outside dia
         h = inch height nozzle location measured from top
         interval, int years of inspection interval
        OUTPUT :
          mawp = psig, maximum allowable working pressure
        """
        # convert unit of t_act and cr
        t_act = t_act * 0.03937  # inch
        cr = cr * 0.03937  # inch per year

        t_pred = t_act - (2 * cr * interval)
        mawp = 2 * S * E * t_pred / OD
        return mawp
