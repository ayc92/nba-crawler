import re
from scrapy import Spider
from scrapy.http import Request

from NBACrawler.items import (
    PlayerInfoItem
)

class PlayersSpider(Spider):
    name = 'players'

    def __init__(self, *args, **kwargs):
        super(PlayersSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ["espn.go.com"]
        self.espn = "http://espn.go.com"
        self.start_urls = ["http://espn.go.com/nba/players"]

    """
    HELPER FUNCTIONS
    """
    def get_player_id(self, response):
        """
        Extract player id from response
        """
        url = response.url.split('/')
        id_idx = url.index('id')
        return int(url[id_idx + 1])

    def get_gamelog_year(self, url):
        """
        Extract gamelog year from URL
        """
        url = url.split('/')
        year_idx = url.index('year')
        return int(url[year_idx + 1])

    def get_player_name(self, response):
        """
        Extract player name from response
        """
        p_name = response.selector.css(".mod-page-header .mod-content h1::text")
        p_name = p_name.extract()[0]
        return p_name

    def get_player_info(self, response):
        """
        Extract other player information
        """
        player_data = {}

        info = response.selector.css(".player-bio")

        # general info
        position, physique = info.css(".general-info li::text").extract()[:2]

        # get position
        position = position.split()[1]
        player_data['position'] = position

        # get height and weight
        height, weight = physique.replace(' ', '').split(',')
        player_data['height'] = height
        player_data['weight'] = weight

        # player metadata
        p_meta = info.css(".player-metadata li")
        p_meta_txt = p_meta.css("li::text").extract()

        # Some caviats:
        #   - Rookies do not have the 'experience' field.
        #   - Undrafted players do not have a 'drafted' field.
        #   - Some player have 'college' listed as 'None'.
        if len(p_meta) == 4:
            born, draft, edu, exp = p_meta_txt
        else:
            meta_labels = p_meta.css('span::text').extract()
            if 'Drafted' not in meta_labels and 'Experience' not in meta_labels:
                born, edu = p_meta_txt
                draft, exp = None, 0
            elif 'Drafted' not in meta_labels and 'Experience' in meta_labels:
                born, edu, exp = p_meta_txt
                draft = None
            else:
                born, draft, edu = p_meta_txt
                exp = 0

        # get birth info
        match = re.search('(.*) (in .+)?\(Age\: (\d+)\)', born)
        player_data['birth_date'] = match.group(1)
        player_data['birth_loc']  = match.group(2)
        player_data['age']        = int(match.group(3))

        # get draft info
        if draft:
            match = re.search('\d+\: (1|2)st|nd Rnd\, (\d+)st|nd|th by ([A-Z]+)', draft)
            player_data['draft_round'] = match.group(1)
            player_data['draft_num']   = match.group(2)
            player_data['draft_team']  = match.group(3)
        else:
            player_data['draft_round'] = None
            player_data['draft_num']   = None
            player_data['draft_team']  = None

        # education
        player_data['education'] = edu

        # experience
        if exp != 0:
            match = re.search('(\d+) year(s?)', exp)
            player_data['experience'] = int(match.group(1))
        else:
            player_data['experience'] = exp
        return player_data

    def get_player_resource(self, response, resource):
        """
        Add a player resource to the URL and return it.
        e.g. espn.go.com/nba/player/_/id/2768/jarret-jack
             => espn.go.com/nba/player/stats/_/id/2768/jarret-jack
        """
        url = response.url.split('/')
        player_str_index = url.index('player')
        url.insert(player_str_index + 1, resource)
        url = '/'.join(url)
        return url


    """
    NETWORK REQUEST CALLBACKS
    """
    def parse(self, response):
        """
        The initial parse function. Grabs and follows all team links.

        URL: http://espn.go.com/nba/players
        """
        team_links = response.selector.css(".small-logos li div a::attr(href)").extract()
        for link in team_links:
            espn_team_link = "%s%s" % (self.espn, link)
            yield Request(espn_team_link, self.parse_team)

    def parse_team(self, response):
        """
        Follows each player link on a team page.

        URL: http://espn.go.com/nba/roster/_/name/por/portland-trail-blazers
        """
        player_links = response.selector.css(".sortcell a::attr(href)").extract()
        for link in player_links:
            yield Request(link, self.parse_player)

    def parse_player(self, response):
        """
        Parses player info, and follows the 'Stats'
        and 'Game Log' tabs on the player page.

        URL: http://espn.go.com/nba/player/_/id/2983/lamarcus-aldridge
        """
        p_info = {}
        # Get player id from URL
        p_id = self.get_player_id(response)
        p_info['id'] = p_id

        # Get player name from page.
        p_name = self.get_player_name(response)
        p_info['name'] = p_name

        # Get player bio info
        p_bio = self.get_player_info(response)
        p_info = dict(p_info, **p_bio)

        # Create and yield new PlayerInfoItem
        yield PlayerInfoItem(p_info)

        # Build and follow 'Stats' link
        # next_url = self.get_player_resource(response, 'stats')
        # yield Request(next_url, self.parse_player_stats)

        # Follow the 'Game Log' link
        # next_url = self.get_player_resource(response, 'gamelog')
        # yield Request(next_url, self.parse_player_gamelogs)

    def parse_player_stats(self, response):
        """
        Parses the player's stats page into corresponding items.
        """
        pass

    def parse_player_gamelogs(self, response):
        """
        Follows each link in the gamelog years dropdown selector on the gamelog page.
        """
        # Iterate through gamelog URLs, going back till 2012-2013 season.
        # Ignore the 0th element, which is the 'select' option.
        gamelog_urls = response.selector.css(".tablesm option::attr(value)")[1:].extract()
        for url in gamelog_urls:
            if self.get_gamelog_year(url) > 2013:
                yield Request(url, self.parse_player_gamelog)

    def parse_player_gamelog(self, response):
        """
        Parses a player's gamelog for a specific season in corresponding items.
        """
        pass
