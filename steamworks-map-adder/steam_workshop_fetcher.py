"""
Request the steam workshop link and parse for the id (from url)
and the name of the map the creater has given
"""
import bs4
import urllib.request
import logging

class FetchWorkshopInfo:
    logger = logging.getLogger(__name__)


    def __init__(self):
        pass

    def fetch_page(self, url):
        """
        Grab the steam workshop page and parse it
        """
        value = urllib.request.urlopen(url)
        title = self._parse_steam_page_for_name(value)
        workshop_id = self._parse_url_for_id(url)
        self.logger.info("Got workshop info name:'%s' with id:%s", title, workshop_id)
        return (title, workshop_id)
        

    def _parse_steam_page_for_name(self, webpage):
        """
        Grab the name of the map form the workshop link
        """
        ret_val = ""
        try:
            soup_website = bs4.BeautifulSoup(webpage.read(), "html.parser")
            ret_val = str(soup_website.find("div", class_="workshopItemTitle")).split(">")[-2].split("<")[0]
        except:
            self.logger.error("There was an issue trying to get the div from the steam website")
        return ret_val
    
    def _parse_url_for_id(self, url):
        """
        Grab the workshop id from the url link to be used in the container to download
        """
        ret_val = ""
        try:
            end_of_url = url.split("?")[-1]
            arguments = end_of_url.split("&")
            id_argument = arguments[0].split("=")
            workshop_id = id_argument[-1]
            ret_val = int(workshop_id)
        except:
            self.logger.error("There wasn an issue trying to get the workshop id from the link")
        return ret_val

