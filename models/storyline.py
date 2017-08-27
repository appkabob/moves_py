import uuid
from pprint import pprint

import constants
from database import Database
from lib.PyMoves.moves import Moves


class Storyline:
    def __init__(self, date, segments, summary, lastUpdate=None, id=None, _id=None):
        self.date = date
        self.lastUpdate = lastUpdate
        self.segments = segments
        self.summary = summary
        self.id = uuid.uuid4().hex if id is None else id

    def __repr__(self):
        return "<Storyline {}>".format(self.date)

    @classmethod
    def fetch_by_date_range(cls, on_or_after, on_or_before):
        m = Moves(constants.CLIENT_ID, constants.CLIENT_SECRET, constants.CALLBACK_URL, constants.API_URL)
        storylines = m.get_range(constants.ACCESS_TOKEN, '/user/storyline/daily', on_or_after, on_or_before)
        return [cls(**storyline) for storyline in storylines]

    def save_to_mongo(self):
        Database.insert(collection='storylines', data=self.json())

    def json(self):
        return {
            'date': self.date,
            'lastUpdate': self.lastUpdate,
            'segments': self.segments,
            'summary': self.summary,
            'id': self.id
        }

    @classmethod
    def from_mongo(cls, date):
        return [cls(**storyline) for storyline in Database.find_one(collection='storylines', query={'date': date})]

    @classmethod
    def all_from_mongo(cls):
        storylines = Database.find(collection='storylines', query={})
        return [cls(**storyline) for storyline in storylines]

    def trackpoints(self, activity_type=None):
        trackpoints = []
        if not self.segments: return []
        for segment in self.segments:
            if not 'activities' in segment: segment['activities'] = []
            for activity in segment['activities']:
                if activity_type:
                    if activity_type == activity['activity']:
                        activity_trackpoints = []
                        for trackpoint in activity['trackPoints']:
                            activity_trackpoints.append(tuple([trackpoint['lat'], trackpoint['lon']]))
                        trackpoints.append(activity_trackpoints)
                else:
                    trackpoints.append(tuple([trackpoint['lat'], trackpoint['lon']]))
        return trackpoints
