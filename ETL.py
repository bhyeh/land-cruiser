import numpy as np
import pandas as pd

class Clean():
    """
    
    """

    def string_to_int(self, str_num):
        """ Converts string number representation to integer

        Use for price, number of views, watchers, comments, and bids

        Parameters
        ----------
        str_num: str

        Returns
        -------
        int_num: int

        """

        str_num = str_num.replace(',', '')
        int_num = int(str_num)
        return int_num
    
    def transform_miles(self, str_miles):
        """ Parses and transforms 'mileage' to int

        Parameters
        ----------
        str_miles: str

        Returns
        -------
        int_miles: int

        """

        # Format 1: 'xxxK'
        if 'k' in str_miles:
            str_miles = str_miles.strip(' k')
            int_miles = int(str_miles) * 1000
            
        # Format 2: 'xxx,xxx'
        else:
            str_miles = str_miles.replace(',', '')
            int_miles = int(str_miles)

        return int_miles

    def stem_exterior(self, exterior_description):
        """

        Parameters
        ---------- 

        Returns
        -------

        """

        # Format 1: ''

        pass