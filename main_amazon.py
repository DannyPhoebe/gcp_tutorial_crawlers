import webapp2
import cloudstorage as gcs
import logging

from bs4 import BeautifulSoup
import requests
import requests_toolbelt.adapters.appengine

requests_toolbelt.adapters.appengine.monkeypatch()


class Amazon_Tracker(webapp2.RequestHandler):
    def get(self):
        for line in gcs.open("/bucket/url2track.csv"):
            prod_url, threshold = line.split(" ")
            logging.info(prod_url)
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'}
            attempt = 0
            while attempt < 5:
                res = requests.get(prod_url, headers=headers)
                if res.status_code == 200:
                    break
            soup = BeautifulSoup(res.text, 'lxml')
            price = soup.find('span',{'id': 'priceblock_ourprice'})
            if price == None:
                price = soup.find('span',{'id': 'priceblock_saleprice'})
            if price == None:
                price = soup.find('span',{'id': 'priceblock_dealprice'})
            price = float(price.text[2:].replace(',', ''))
            if price <= float(threshold) and self.request.get("notify") == 'yes':
                self.lineNotify("your token", "price reached the threshold: {}".format(prod_url.encode('utf-8')))
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write("{}\n".format(price))

    def write2gcs(self, msg):
        gcs_file = gcs.open('/bucket/url2track.csv', 'a')
        gcs_file.write(msg + '\n')
        gcs_file.close()
        self.response.write('Registered')

    def lineNotify(self, token, msg):
        url = "https://notify-api.line.me/api/notify"
        headers = {
            "Authorization": "Bearer " + token, 
            "Content-Type" : "application/x-www-form-urlencoded"
        }    
                
        payload = {'message': msg}
        r = requests.post(url, headers=headers, params=payload)
        return r.status_code


app = webapp2.WSGIApplication([
    ('/track', Amazon_Tracker),
], debug=True)
