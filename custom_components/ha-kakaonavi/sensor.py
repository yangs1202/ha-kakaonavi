import requests
import logging
import hashlib
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)



class Priority:
    RECOMMEND = "RECOMMEND"
    TIME = "TIME"
    DISTANCE = "DISTANCE"


class KakaoNaviApiClient:
    def __init__(self, token: str):
        self.rs = requests.Session()
        self.host = "https://apis-navi.kakaomobility.com"
        self.rs.headers.update({
            "Authorization": f"KakaoAK {token}"
        })
        self._cache = {}

    def direction(self, start: str, end: str, waypoint: str = None, priority: Priority = Priority.TIME):
        start_point = self.address(start)
        _start = f"{start_point.get('x')},{start_point.get('y')}"
        end_point = self.address(end)
        _end = f"{end_point.get('x')},{end_point.get('y')}"
        _waypoint = None
        if waypoint is not None:
            waypoint_point = self.address(waypoint)
            _waypoint = f"{waypoint_point.get('x')},{waypoint_point.get('y')}"

        resp = self.rs.get(f"{self.host}/v1/directions", params={
            "origin": _start,
            "destination": _end,
            "waypoints": _waypoint,
            "priority": str(priority),
            "summary": True
        })
        if resp.status_code != 200:
            return None
        return resp.json()

    def address(self, query):
        if self._cache.get(query) is not None:
            return self._cache.get(query)
        resp = self.rs.get("https://dapi.kakao.com/v2/local/search/address.json", params={
            "query": query,
            "analyze_type": "exact"
        })
        if resp.status_code != 200 or len(resp.json().get("documents", [])) == 0:
            return None
        result = resp.json().get("documents", [])[0].get("address")
        self._cache[query] = result
        return result




def setup_platform(hass, config, add_entities, discovery_info=None):
    apikey = config["apikey"]
    start = config["start"]
    end = config["end"]
    waypoint = config.get("waypoint")


    add_entities([
        KakaoNaviEta(apikey, start, end, waypoint)
    ])



class KakaoNaviEta(Entity):
    def __init__(self, apikey, start, end ,waypoint):
        self._name = f"{start}-{end}-{waypoint}"
        self.device_id = hashlib.md5(f"{start}-{end}-{waypoint}".encode("UTF-8")).hexdigest()
        self.rs = requests.Session()
        self.apikey = apikey
        self.start = start
        self.end = end
        self.waypoint = waypoint
        self._value = 0.0
        self._data = {}
        try:
            self.update()
        except Exception as e:
            _LOGGER.exception(e)

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self.device_id

    @property
    def state(self):
        return round(self._value, 2)

    @property
    def extra_state_attributes(self):
        return self._data

    @property
    def available(self):
        """Could the device be accessed during the last update call."""
        return True
    
    @property
    def state_class(self):
        return "measurement"

    @property
    def device_class(self):
        return "pm25"

    def update(self):
        data = KakaoNaviApiClient(self.apikey).direction(self.start, self.end, self.waypoint).get("routes")[0]
        self._data = data.get("summary")
        self._value = data.get("summary").get("duration") / 60
        
