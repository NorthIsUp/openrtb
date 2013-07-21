# -*- coding: utf-8 -*-

from decimal import Decimal

from . import constants
from .base import Object, Array, Field


class Publisher(Object):
    u"""
    The publisher object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    """

    id = Field(str)
    name = Field(str)
    cat = Field(Array(str))
    domain = Field(str)


class Producer(Object):
    u"""
    The producer is useful when content where the ad is shown is syndicated,
    and may appear on a completely different publisher.
    The producer object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    This object is optional, but useful if the content producer is different from the site publisher.
    """

    id = Field(str)
    name = Field(str)
    cat = Field(Array(str))
    domain = Field(str)


class Geo(Object):
    u"""
    The geo object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    Note that the Geo Object may appear in one or both the Device Object and the User Object.
    This is intentional, since the information may be derived from either a device-oriented
    source (such as IP geo lookup), or by user registration information (for example
    provided to a publisher through a user registration).
    If the information is in conflict, it’s up to the bidder to determine which information to use.
    """

    lat = Field(float)
    lon = Field(float)
    country = Field(str)
    region = Field(str)
    regionfips104 = Field(str)
    metro = Field(str)
    city = Field(str)
    zip = Field(str)
    type = Field(constants.LocationType)

    def loc(self):
        if self.lat and self.lon:
            return self.lat, self.lon


class Segment(Object):
    u"""
    The data and segment objects together allow data about the user to be passed to bidders in the bid request.
    Segment objects convey specific units of information from the provider identified in the parent data object.
    The segment object itself and all of its parameters are optional, so default values are not provided;
    if an optional parameter is not specified, it should be considered unknown.
    """

    id = Field(str)
    name = Field(str)
    value = Field(str)


class Data(Object):
    u"""
    The data and segment objects together allow data about the user to be passed to bidders in the bid request.
    This data may be from multiple sources (e.g., the exchange itself, third party providers)
    as specified by the data object ID field. A bid request can mix data objects from multiple providers.
    The data object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    """

    id = Field(str)
    name = Field(str)
    segment = Field(Array(Segment))


class User(Object):
    u"""
    The “user” object contains information known or derived about the human user of the device.
    Note that the user ID is an exchange artifact (refer to the “device” object for hardware or platform derived IDs)
    and may be subject to rotation policies.
    However, this user ID must be stable long enough to serve reasonably as the basis for frequency capping.
    The user object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    If device ID is used as a proxy for unique user ID, use the device object.
    """

    id = Field(str)
    buyerid = Field(str)
    yob = Field(int)
    gender = Field(str)
    keywords = Field(str)
    customdata = Field(str)
    geo = Field(Geo)
    data = Field(Array(Data))


class Device(Object):
    u"""
    The “device” object provides information pertaining to the device including
    its hardware, platform, location, and carrier.
    This device can refer to a mobile handset, a desktop computer, set top box or other digital device.
    The device object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    In general, the most essential fields are either the IP address (to enable geo-lookup for the bidder),
    or providing geo information directly in the geo object.
    """

    dnt = Field(int)
    ua = Field(str)
    ip = Field(str)
    geo = Field(Geo, default=Geo())
    didsha1 = Field(str)
    didmd5 = Field(str)
    dpidsha1 = Field(str)
    dpidmd5 = Field(str)
    ipv6 = Field(str)
    carrier = Field(str)
    language = Field(str)
    make = Field(str)
    model = Field(str)
    os = Field(str)
    osv = Field(str)
    js = Field(int)
    connectiontype = Field(constants.ConnectionType)
    devicetype = Field(constants.DeviceType)
    flashver = Field(str)

    def is_on_cellular(self):
        return self.connectiontype and self.connectiontype.is_cellular()


class Content(Object):
    u"""
    The content object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    This object describes the content in which the impression will appear (may be syndicated or non-syndicated content).
    This object may be useful in the situation where syndicated content contains impressions
    and does not necessarily match the publisher’s general content.
    The exchange might or might not have knowledge of the page where the content is running,
    as a result of the syndication method.
    (For example, video impressions embedded in an iframe on an unknown web property or device.)
    """

    id = Field(str)
    episode = Field(int)
    title = Field(str)
    series = Field(str)
    season = Field(str)
    url = Field(str)
    cat = Field(Array(str))
    videoquality = Field(constants.VideoQuality)
    keywords = Field(str)
    contentrating = Field(str)
    userrating = Field(str)
    context = Field(str)
    livestream = Field(int)
    sourcerelationship = Field(int)
    producer = Field(Producer)
    len = Field(int)


class Site(Object):
    u"""
    A site object should be included if the ad supported content is part of a website (as opposed to an application).
    A bid request must not contain both a site object and an app object.
    The site object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    At a minimum, it’s useful to provide a page URL or a site ID, but this is not strictly required.
    """

    id = Field(str)
    name = Field(str)
    domain = Field(str)
    cat = Field(Array(str))
    sectioncat = Field(Array(str))
    pagecat = Field(Array(str))
    page = Field(str)
    privacypolicy = Field(int)
    ref = Field(str)
    search = Field(str)
    publisher = Field(Publisher)
    content = Field(Content)
    keywords = Field(str)


class App(Object):
    u"""
    An “app” object should be included if the ad supported content is part of a mobile
    application (as opposed to a mobile website).
    A bid request must not contain both an “app” object and a “site” object.
    The app object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    At a minimum, it’s useful to provide an App ID or bundle, but this is not strictly required.
    """

    id = Field(str)
    name = Field(str)
    domain = Field(str)
    cat = Field(Array(str))
    sectioncat = Field(Array(str))
    pagecat = Field(Array(str))
    ver = Field(str)
    bundle = Field(str)
    privacypolicy = Field(int)
    paid = Field(int)
    publisher = Field(Publisher)
    content = Field(Content)
    keywords = Field(str)


class Banner(Object):
    u"""
    The “banner” object must be included directly in the impression object
    if the impression offered for auction is display or rich media,
    or it may be optionally embedded in the video object to describe
    the companion banners available for the linear or non-linear video ad.
    The banner object may include a unique identifier; this can be useful
    if these IDs can be leveraged in the VAST response
    to dictate placement of the companion creatives when multiple
    companion ad opportunities of the same size are available on a page.
    """

    w = Field(int)
    h = Field(int)
    id = Field(str)
    pos = Field(constants.AdPosition)
    btype = Field(Array(constants.BannerType))
    battr = Field(Array(constants.CreativeAttribute))
    mimes = Field(Array(str))
    topframe = Field(int)
    expdir = Field(Array(constants.ExpandableDirection))
    api = Field(Array(constants.APIFramework))

    def blocked_types(self):
        return set(self.btype or [])

    def size(self):
        if self.w and self.h:
            return self.w, self.h


class Video(Object):
    u"""
    The “video” object must be included directly in the impression object if the impression offered
    for auction is an in-stream video ad opportunity.
    Note that for the video object, many of the fields are non-essential for a minimally viable exchange interfaces.
    These parameters do not necessarily need to be specified to the bidder,
    if they are always the same for all impression,
    or if the exchange chooses not to supply the additional information to the bidder.
    """

    mimes = Field(Array(str), required=True)
    linearity = Field(constants.VideoLinearity, required=True)
    minduration = Field(int, required=True)
    maxduration = Field(int, required=True)
    protocol = Field(constants.VideoProtocol, required=True)
    w = Field(int)
    h = Field(int)
    startdelay = Field(int)
    sequence = Field(int, 1)
    battr = Field(Array(constants.CreativeAttribute))
    maxextended = Field(int)
    minbitrate = Field(int)
    maxbitrate = Field(int)
    boxingallowed = Field(int)
    playbackmethod = Field(Array(constants.VideoPlaybackMethod))
    delivery = Field(Array(constants.ContentDeliveryMethod))
    pos = Field(constants.AdPosition)
    companionad = Field(Array(Banner))
    api = Field(Array(constants.APIFramework))


class Impression(Object):
    u"""
    The “imp” object describes the ad position or impression being auctioned.
    A single bid request can include multiple “imp” objects,
    a use case for which might be an exchange that supports selling all ad positions on a given page as a bundle.
    Each “imp” object has a required ID so that bids can reference them individually.
    """

    id = Field(str, required=True)
    banner = Field(Banner)
    video = Field(Video)
    displaymanager = Field(str)
    instl = Field(int)
    tagid = Field(str)
    bidfloor = Field(Decimal)
    bidfloorcur = Field(str, default='USD')
    iframebuster = Field(Array(str))
    ext = Field(Object)


class BidRequest(Object):
    u"""
    The top-level bid request object contains a globally unique bid request or auction ID.
    This “id” attribute is required as is at least one “imp” (i.e., impression) object.
    Other attributes are optional since an exchange may establish default values.
    """

    id = Field(str, required=True)
    imp = Field(Array(Impression), required=True)
    site = Field(Site, default=Site())
    app = Field(App, default=App())
    device = Field(Device, default=Device())
    user = Field(User, default=User())
    at = Field(constants.AuctionType, default=constants.AuctionType.SECOND_PRICE)
    tmax = Field(int)
    wseat = Field(Array(str))
    allimpd = Field(int)
    cur = Field(Array(str))
    bcat = Field(Array(str))
    badv = Field(Array(str))
    ext = Field(Object)

    @staticmethod
    def minimal(id, imp_id):
        return BidRequest(id=id, imp=[Impression(id=imp_id, banner=Banner())])
