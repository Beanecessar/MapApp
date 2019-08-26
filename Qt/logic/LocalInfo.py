import geoip2.database
import urllib.request
import re

reader = geoip2.database.Reader("./GeoLite2-City/GeoLite2-City.mmdb")

class LocalInfo(object):
	def __init__(self):
		res = reader.city(self.getIp())
		self.countryName = res.country.name
		self.cityName = res.city.name
		self.latitude = res.location.latitude
		self.longitude = res.location.longitude

	def getIp(self):
		url = urllib.request.urlopen("http://txt.go.sohu.com/ip/soip")
		text = url.read().decode("utf-8")
		ip = re.findall(r'\d+.\d+.\d+.\d+',text)
		return ip[0]