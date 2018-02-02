import webapp2
import requests
import requests_toolbelt.adapters.appengine
from bs4 import BeautifulSoup

requests_toolbelt.adapters.appengine.monkeypatch()


class Apple_Headline(webapp2.RequestHandler):
    def get(self):
        date = self.request.get(date, ) #current time
        url = "https://tw.appledaily.com/appledaily/archive/{}".format(date)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        headlines = soup.find_all("article",{"class": "nclns eclnms5"})[0] # headlines
        pair = [item['title'] + '\t' + item['href'] for item in headlines.select('li > a')]
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('\n'.join(pair))


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
