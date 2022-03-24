from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


class Parser():
    """ A parser for 60 Series Toyota Land Cruiser listings on BringATrailer.com (BAT)
    
    Method
    -------
    parse(page_source)
        Parses and retrieves auction and vehicle information from listing page
    
    """

    def parse_auction(self, auction_meta_details):
        """ Parses the auction meta details

        Returns auction closing price, selling date, seller location, number of comments, watchers, and bids

        Parameters
        ----------
        auction_meta_details: (bs4.element.Tag * bs4.element.Tag * bs4.element.Tag)

        Returns
        -------
        price, sell_date, seller_location, no_comments, no_views, no_watchers, no_bids : str
        """

        auction_details, auction_stats, auction_essentials = auction_meta_details
        # auction details
        price = auction_details.find('span', {'class' : 'info-value noborder-tiny'}).strong.text.split('$')[-1]
        auction_date = auction_details.find('span', {'class': 'date'}).text.split(' ')[-1]
        no_comments = auction_details.find('span', {'class' : 'comments_header_html'}).find('span', {'class' :'info-value'}).text

        # auction stats
        no_views, no_watchers = tuple([stat.text.split(' ')[0] for stat in auction_stats.find('td', {'class': 'listing-stats-views'}).find_all('span')])
        no_bids = auction_stats.find('td', {'class': 'listing-stats-value number-bids-value'}).text
        # reserve met
        sold = '1'
        bid_result = auction_stats.find('td', {'class' : 'listing-stats-value'}).text.lower()
        bid_result_split = bid_result.split(' ')
        bid_result_split = [substring.strip(' (),') for substring in bid_result_split]
        bid_result = ' '.join(bid_result_split)
        if 'reserve not met' in bid_result:
            sold = '0'

        # selling location
        seller_location = auction_essentials.find_all('a', href=True)[2].text.lower()
        
        return price, auction_date, sold, seller_location, no_comments, no_views, no_watchers, no_bids

    def parse_year(self, title_str):
        """ Parses year
        
        Parameters
        ----------
        title_str : str

        Returns
        -------
        year_str: str

        """

        year_str = np.nan
        # Format 1: '198x'
        if '198' in title_str:
            idx = title_str.find('198')
            year_str = title_str[idx:idx+4]
        elif '199' in title_str:
            idx = title_str.find('199')
            year_str = title_str[idx:idx+4]
        return year_str

    def parse_body_code(self, title_str):
        """ Parses series
        
        """

        code = np.nan
        if 'j' in title_str:
            idx = title_str.find('j') - 1
            code = title_str[idx:idx+4]
        return code
    
    def parse_title(self, title_str):
        """ Parses listing title and returns the year and series code

        Parameters
        ----------
        title_str: str
            listing title that has follows approximate form: '19xx Toyota Land Cruiser yJ6y'

        Returns
        -------
        year: str
            year of land cruiser
        series: str
            code indicating series/generation (e.g., 'fj60', 'hj60', 'fj62', 'hj61',)

        """

        # lowercase title
        title_str = title_str.lower()
        # parse year from title
        year_str = self.parse_year(title_str)
        # parse body code
        code = self.parse_body_code(title_str)
        return year_str, code

    def parse_mileage(self, string):
        """ Parses indicated mileage

        Parameters
        ----------

        Returns
        -------
        
        """

        miles = np.nan
        split = string.split(' ')
        split = [substring.strip(' ()~,') for substring in split]
        string = ' '.join(split)
        # Format 1: 'xxx.xxx miles shown'
        if 'miles shown' in string:
            miles = string.split(' miles shown')[0].split(' ')[-1]
        # Format 2: 'xxx.xxx indicated miles' 
        elif 'indicated miles' in string:
            miles = string.split(' indicated miles')[0].split(' ')[-1]
        # Format 3: 'xxx.xxx reported chassis miles'
        elif 'reported chassis miles' in string:
            miles = string.split(' reported chassis miles')[0].split(' ')[-1]
        # Format 3: 'xxx.xxxx miles'
        elif 'miles' in string:
            miles = string.split(' miles')[0].split(' ')[-1]
        # Format 4: 'xxx.xxx shown'
        elif 'shown' in string:
            miles = string.split(' shown')[0].split(' ')[-1]

        return miles

    def parse_transmission(self, string):
        """ Parses indicated transmission

        Parameters
        ----------

        Returns
        -------
        
        """

        trans = np.nan
        if 'automatic' in string:
            trans = 'automatic'
        elif 'manual' in string:
            trans = 'manual'
        return trans

    def parse_exterior(self, string):
        """ Parses exterior description

        Parameters
        ----------

        Returns 
        -------
        
        """

        pass
    
    def parse_vehicle(self, listing_details):
        """ Parses 'Listing Details' section of listing page

        Returns the mileage, engine, transmission type, as well as paint scheme, interior, and misc. items

        Parameters
        ----------
        listing_details: list of str
            listing details that follow ~approximate form:

            [   Chassis: **VIN**,
                **Miles Description**,
                **Engine Description**,
                **Transmission Description**,
                **Transfer Case Description**,
                **Paint Description**,
                **Interior Description**,
                **Misc. Items**
            ]

            Note:
                Descriptions vary tremendously from listing to listing, the exact index occurence of items often change,
                and items are sometimes not listed. However the overall item structure is predictable. 
                (E.g., interior description is always after exterior description, transfer is after transmission, etc.)

        Returns
        -------
        miles, engine, trans, paint, interior: str
        misc: list of str

        """
        
        # initialize all details as null
        miles = engine = trans = paint = interior = np.nan
        # lower case details
        listing_details = [spec.lower() for spec in listing_details]
        # keyword occurence to identify details
        mileage_keywords = ['miles', 'shown']
        engine_keywords = ['3.4', '4.0', '4.2', '-liter', 'inline', 'v8', 'diesel', 'straight', 'cylinder']
        transmission_keywords = ['manual', 'automatic', 'transmis', 'gear', 'box'] 
        paint_keywords = ['paint', 'exterior', 'metallic', 'finish', 'tone', 'wrap', 'over', 'decal', 
                          'light', 'silver', 'white', 'gray', 'beige', 'brown', 'blue', 'red', 'tan']

        interior_keywords = ['cloth', 'vinyl', 'upholstery', 'interior', 'fabric', 'leather']

        # loop items
        for s in listing_details:
            if any(keyword in s for keyword in mileage_keywords) & (pd.isna(miles)):
                miles = self.parse_mileage(s)
            elif any(keyword in s for keyword in engine_keywords) & (pd.isna(engine)):
                engine = s
            elif any(keyword in s for keyword in transmission_keywords) & (pd.isna(trans)):
                trans = self.parse_transmission(s)
            elif any(keyword in s for keyword in paint_keywords) & (pd.isna(paint)):
                no_paint_keywords = sum([1 for keyword in paint_keywords if keyword in s])
                no_interior_keywords = sum([1 for keyword in interior_keywords if keyword in s])
                # temporary fix; spaghetti code! 
                if ('tank' in s or 'tooth' in s or 'over' in s or 'tone' in s or 'light' in s) & (no_paint_keywords == 1):
                    pass
                elif (no_paint_keywords >= no_interior_keywords):
                    paint = s
            elif any(keyword in s for keyword in interior_keywords) & (pd.isna(interior)):
                interior = s

        misc = listing_details[1:]
        return miles, engine, trans, paint, interior, misc
    
    
    def parse_page(self, page_source):
        """ Parses and retrieves auction and vehicle information from a listing page
        
        Parameters
        ----------
        page_source: str
            
        Returns
        -------
        list of str
            
        """
        
        soup = BeautifulSoup(page_source, 'lxml')
        # auction meta details
        auction_details = soup.find('div', {'class' : 'listing-available-info'})
        auction_stats = soup.find('div', {'id': 'listing-bid-container'})
        auction_essentials = soup.find('div', {'class' : 'essentials'})
        # parse meta details
        auction_meta_details = (auction_details, auction_stats, auction_essentials)
        price, auction_date, sold, seller_location, no_comments, no_views, no_watchers, no_bids = self.parse_auction(auction_meta_details)
        
        # listing title
        listing_title = soup.find('h1', class_='post-title listing-post-title').text
        # parse listing title
        year, code = self.parse_title(listing_title)
        
        # listing details
        listing_details = soup.find('div', class_='essentials')
        listing_specs = [spec.text for spec in listing_details.find('ul').find_all('li')]
        # parse listing details
        miles, engine, trans, exterior_paint, interior, misc = self.parse_vehicle(listing_specs)
        
        # scraped information
        scraped_page = [listing_title, price, auction_date, sold, no_views, no_watchers, no_comments, no_bids, 
                        seller_location, year, code, miles, engine, trans, exterior_paint, interior, misc]
        return scraped_page