# -*- coding: utf-8 -*-
"""
    Parametry k obchodování na burze
"""

__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"

class Trading:
    """
    Popis zvyklostí na burze.
    """

    # začátek obhodování v minutách
    # (menší z obou hodnot začátku obchodování v letním a zimním čase)
    START_MINITS = 13 * 60 + 30

    # konec obhodování v minutách (poslední minuta už v datech není)
    # (větší z obou hodnot konce obchodování v letním a zimním čase)
    STOP_MINITS = 21 * 60

    # konec obhodování v minutách (poslední minuta už v datech není)
    # v jednotkách, kde 1. minuta obchodování má číslo 0
    LAST_MINIT_OD_DAY = STOP_MINITS - START_MINITS

    def getDayMinits(self, hours, minits):
        """
        Hřepočítá hodiny a minuty na minuty od začátku obchodování
        """
        return hours * 60 + minits - self.START_MINITS

    def inTimeOfTrades(self, minit):
        '''
        Vrátí True právěkdyž minit je v čase, kdy se obchoduje.
        parametr minit je formátu získaném  metodo getDayMinits(...)
        '''
        return minit >= 0 and minit < self.LAST_MINIT_OD_DAY


    def getHHMMfromMinits(self, minitsFromStart):
        """
        Parametr minitsFromStart je počet minut od začátku obchodování.
        Vrátí řetězec odpovídající času v UTC0 ve formátu HHMM.
        """
        (hours,minits) = divmod(minitsFromStart + self.START_MINITS, 60)
        return "{0:02d}{1:02d}".format(hours, minits)
