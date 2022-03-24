import numpy as np
import pandas as pd

class Transform():
    """
    
    """

    def string_to_int(self, str_num : str):
        """ Converts string number representation to integer

        Use for transforming price, number of views, watchers, comments, and bids

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
    
    def transform_miles(self, str_miles: str):
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

    def transform_engine(self, df: pd.DataFrame):
        """ Normalizes engine description
        
        60
            3B : 3.4-Liter Diesel
            2F : 4.2-Liter Gasoline 
            2H : 4.0-Liter Diesel
        61
            3B : 3.4-Liter Diesel
            12H-T : 4.0-Liter Disel
        62
            3F-E : 4.0-Liter Gasoline

        """

        pass

    def stem_exterior(self, exterior_description):
        """

        Parameters
        ---------- 

        Returns
        -------

        """

        pass