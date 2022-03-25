import numpy as np
import pandas as pd
import re
from colour import Color

class Transformer():
    """ 
    
    Method
    -------
    transform(df)
        
    """


    def format_date(self, dates: pd.Series) -> pd.Series :
        """

        Parameters
        ---------- 

        Returns
        -------

        """

        pass 

    def string_to_int(self, str_num : str) -> int:
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
    
    def transform_miles(self, str_miles: str) -> int:
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

    def transform_engine(self, df: pd.DataFrame) -> pd.DataFrame:
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

        def parse_60series(str_engine: str) -> str:
            """

            Parameters
            ---------- 

            Returns
            -------

            """
            
            # 3B : 3.4-Liter Diesel
            if '3.4' in str_engine:
                engine = '3B'
            # 2F : 4.2-Liter Gasoline
            elif '4.2' in str_engine:
                engine = '2F'
            # 2H : 4.0-Liter Diesel
            elif '4.0' in str_engine:
                engine = '2H'
            # Other(Swapped)
            else:
                engine = 'Other(Swapped)'

            return engine

        def parse_61series(str_engine: str) -> str:
            """

            Parameters
            ---------- 

            Returns
            -------

            """
            
            # 3B : 3.4-Liter Diesel
            if '3.4' in str_engine:
                engine = '3B'
            # 12H-T : 4.0-Liter Diesel
            elif '4.0' in str_engine:
                engine = '12H-T'
            # Other(Swapped)
            else:
                engine = 'Other(Swapped)'

            return engine

        def parse_62series(str_engine: str) -> str:
            """

            Parameters
            ---------- 

            Returns
            -------

            """

            # 3F-E : 4.0-Liter
            if '4.0' in str_engine:
                engine = '3F-E'
            # Other(Swapped)
            else:
                engine = 'Other(Swapped)'

            return engine

        # Subset 60 Series
        subset_60series = np.nan

        # Subset 61 Series
        subset_61series = np.nan

        # Subset 62 Series
        subset_62series = np.nan

        pass

    def stem_exterior(self, exterior_description: pd.Series) -> pd.Series:
        """

        Parameters
        ---------- 

        Returns
        -------

        """

        def strip(string: str) -> str:
            """

            Parameters
            ---------- 

            Returns
            -------

            """
            
            string = re.sub('-', ' ', string)
            string = re.sub('/', ' ', string)
            split = string.split(' ')
            split = [substring.strip(' -') for substring in split]
            string = ' '.join(split).strip(' ')
            return string

        def sub_color(string):
            """

            Parameters
            ---------- 

            Returns
            -------

            """
            
            string = re.sub('copper', 'brown', string)
            string = re.sub('bronze', 'brown', string)
            string = re.sub('cream', 'tan', string)
            string = re.sub('creme', 'tan')
            return string

        def is_color(string):
            """

            Parameters
            ---------- 

            Returns
            -------

            """

            try:
                Color(string)
                return True
            except ValueError:
                return False
            
        def stem_color(string: str) -> str:
            """

            Parameters
            ---------- 

            Returns
            -------

            """
            
            color = [substring for substring in string.split(' ') if is_color(substring)]
            if len(color):
                color = color[0]
            else:
                color = np.nan
            return color

        pass

    def transform(self) -> pd.DataFrame:
        """

        Parameters
        ---------- 

        Returns
        -------

        """

        pass