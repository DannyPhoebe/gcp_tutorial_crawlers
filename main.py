import webapp2
import cloudstorage as gcs

import requests
import requests_toolbelt.adapters.appengine
from bs4 import BeautifulSoup

requests_toolbelt.adapters.appengine.monkeypatch()


class Apple_Headline(webapp2.RequestHandler):
    def get(self):
        date = self.request.get("date") #current time
        assert date is not None, "Please enter a date"
        write2file = self.request.get("write2file")
        url = "https://tw.appledaily.com/appledaily/archive/{}".format(date)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        headlines = soup.find_all("article",{"class": "nclns eclnms5"})[0] # headlines
        pair = [item['title'] + '\t' + item['href'] for item in headlines.select('li > a')]
        if write2file == 'yes':
            self.write2gcs('headline_{}.txt'.format(date), '\n'.join(pair))
            self.response.headers['Content-Type'] = 'text/plain'
        else:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('\n'.join(pair))

    def write2gcs(self, filename, msg):
        gcs_file = gcs.open('/prime-basis-152406.appspot.com/' + filename, 'w')
        gcs_file.write(msg.encode('utf-8') + '\n')
        gcs_file.close()
        self.response.write('Written in file %s\n' % filename)

app = webapp2.WSGIApplication([
    ('/', Apple_Headline),
], debug=True)
