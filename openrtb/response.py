# -*- coding: utf-8 -*-

from decimal import Decimal

from . import constants
from .base import Object, Array, Field


class Bid(Object):
    u"""
    For each bid, the “nurl” attribute contains the win notice URL.
    If the bidder wins the impression, the exchange calls this notice URL
        a) to inform the bidder of the win and
        b) to convey certain information using substitution macros.

    The “adomain” attribute can be used to check advertiser block list compliance.
    The “iurl” attribute can provide a link to an image that is representative of the campaign’s
    content (irrespective of whether the campaign may have multiple creatives).
    This enables human review for spotting inappropriate content.
    The “cid” attribute can be used to block ads that were previously identified as inappropriate;
    essentially a safety net beyond the block lists.
    The “crid” attribute can be helpful in reporting creative issues back to bidders.
    Finally, the “attr” array indicates the creative attributes that describe the ad to be served.
    """

    id = Field(str, required=True)
    impid = Field(str, required=True)
    price = Field(Decimal, required=True)
    adid = Field(str)
    nurl = Field(str)
    adm = Field(str)
    adomain = Field(Array(str))
    iurl = Field(str)
    cid = Field(str)
    crid = Field(str)
    attr = Field(Array(constants.CreativeAttribute))
    ext = Field(Object)


class SeatBid(Object):
    u"""
    A bid response can contain multiple “seatbid” objects, each on behalf of a different bidder seat.
    Since a bid request can include multiple impressions,
    each “seatbid” object can contain multiple bids each pertaining to a different impression on behalf of a seat.
    Thus, each “bid” object must include the impression ID to which it pertains as well as the bid price.
    The “group” attribute can be used to specify if a seat is willing to accept
    any impressions that it can win (default) or if it is only interested
    in winning any if it can win them all (i.e., all or nothing).
    """

    bid = Field(Array(Bid), required=True)
    seat = Field(str)
    group = Field(int)


class BidResponse(Object):
    u"""
    The top-level bid response object.
    The “id” attribute is a reflection of the bid request ID for logging purposes.
    Similarly, “bidid” is an optional response tracking ID for bidders.
    If specified, it can be included in the subsequent win notice call if the bidder wins.
    At least one “seatbid” object is required, which contains a bid on at least one impression.
    Other attributes are optional since an exchange may establish default values.
    """

    id = Field(str, required=True)
    seatbid = Field(Array(SeatBid), required=True)
    bidid = Field(str)
    cur = Field(str)
    customdata = Field(str)
    ext = Field(Object)

    @staticmethod
    def minimal(id, bid_id, bid_impid, bid_price):
        return BidResponse(id=id, seatbid=[
            SeatBid(bid=[
                Bid(id=bid_id, impid=bid_impid, price=bid_price)
            ])
        ])

    def first_bid(self):
        return self.seatbid[0].bid[0]

    def get_bid_id(self):
        return self.first_bid().id

    def get_imp_id(self):
        return self.first_bid().impid

    def get_ad_id(self):
        return self.first_bid().adid

    def get_first_price(self):
        return self.first_bid().price
