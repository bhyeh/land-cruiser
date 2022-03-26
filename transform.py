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

        datetime = pd.to_datetime(dates, infer_datetime_format= True)

        return datetime

    def string_to_int(self, str_num : str) -> int:
        """ Converts string number representation to integer

        Auxiliary function for transforming price, number of views, watchers, comments, and bids

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

    def transform_location(self, location : str) -> str: 
        """
        
        """

        seller_state = location.split(', ')[-1].split(' ')
        if len(seller_state) > 2:
            seller_state = ' '.join(seller_state[:2])
        else:
            seller_state = seller_state[0]

        return seller_state
    
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

    def transform_engine(self, df: pd.DataFrame) -> pd.Series:
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

        Parameters
        ----------

        Returns
        -------

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

            # Correct listing mistake
            if '4.2' in str_engine:
                str_engine = re.sub('4.2', '4.0', str_engine)

            # 3F-E : 4.0-Liter
            if '4.0' in str_engine:
                engine = '3F-E'
            # Other(Swapped)
            else:
                engine = 'Other(Swapped)'

            return engine
        
        m, _ = df.shape
        engines = pd.Series(np.full(m, np.nan))

        # Subset 60 Series
        subset_60series = df[df.series.str.contains('60')].engine
        engine_60series = subset_60series.apply(parse_60series)
        idx_60series = engine_60series.index

        # Subset 61 Series
        subset_61series = df[df.series.str.contains('61')].engine
        engine_61series = subset_61series.apply(parse_61series)
        idx_61series = engine_61series.index

        # Subset 62 Series
        subset_62series = df[df.series.str.contains('62')].engine
        engine_62series = subset_62series.apply(parse_62series)
        idx_62series = engine_62series.index

        # Fill by index
        engines.loc[idx_60series] = engine_60series
        engines.loc[idx_61series] = engine_61series
        engines.loc[idx_62series] = engine_62series

        return engines

    def transform_exterior(self, exterior: pd.Series) -> pd.Series:
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

            substitutes = [('copper', 'brown'),
                            ('bronze', 'brown'),
                            ('cream', 'tan'),
                            ('creme', 'tan')]

            for pattern, replacement in substitutes:
                string = re.sub(pattern, replacement, string)

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
            
            colors = [substring for substring in string.split(' ') if is_color(substring)]
            if len(colors):
                color = colors[0]
            else:
                color = np.nan

            return color

        exterior = (exterior.apply(strip)
                            .apply(sub_color)
                            .apply(stem_color)
        )

        return exterior

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """

        Parameters
        ---------- 

        Returns
        -------

        """

        transformed_df = df.copy()

        # Format datetime
        transformed_df['closing_date'] = self.format_date(transformed_df.closing_date)
        # Transform string integers to integers
        transformed_df['price'] = transformed_df.price.apply(self.string_to_int)
        transformed_df['no_views'] = transformed_df.no_views.apply(self.string_to_int)
        transformed_df['no_watchers'] = transformed_df.no_watchers.apply(self.string_to_int)
        # Transform seller location to seller state
        transformed_df['seller_state'] = transformed_df.seller_state.apply(self.transform_location)
        # Transform string mileage to integer mileage
        transformed_df['miles'] = transformed_df.miles.apply(self.transform_miles)
        # Transform exterior description
        transformed_df['exterior'] = self.transform_exterior(transformed_df.exterior)
        # Transform engine description
        transformed_df['engine'] = self.transform_engine(transformed_df)

        # Drop
        transformed_df = transformed_df.drop(columns = ['interior', 'misc'])

        return transformed_df