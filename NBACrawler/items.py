# -*- coding: utf-8 -*-

# Define here the models for your scraped items
from scrapy import Field, Item

class PlayerItem(Item):
    """
    This class should only be subclassed,
    never instantiated directly.
    """
    id   = Field()
    name = Field()


class PlayerInfoItem(PlayerItem):
    position    = Field()
    height      = Field()
    weight      = Field()
    birth_date  = Field()
    birth_loc   = Field()
    education   = Field()
    draft_year  = Field()
    draft_round = Field()
    draft_num   = Field()
    draft_team  = Field()
    age         = Field()
    experience  = Field()


class PlayerAveragesItem(PlayerItem):
    start_year          = Field()
    end_year            = Field()
    is_career           = Field()
    games_played        = Field()
    games_started       = Field()
    minutes             = Field()
    fg_attempted        = Field()
    fg_made             = Field()
    fg_percentage       = Field()
    threes_attempted    = Field()
    threes_made         = Field()
    threes_percentage   = Field()
    ft_attempted        = Field()
    ft_made             = Field()
    offensive_rebounds  = Field()
    defensive_rebounds  = Field()
    rebounds            = Field()
    assists             = Field()
    blocks              = Field()
    steal               = Field()
    personal_fouls      = Field()
    ppg                 = Field()


class PlayerSeasonAveragesItem(PlayerAveragesItem):
    team                = Field()


class PlayerGameStatsItem(PlayerItem):
    pass
