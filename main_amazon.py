import webapp2
import cloudstorage as gcs

from bs4 import BeautifulSoup
import requests
import requests_toolbelt.adapters.appengine

requests_toolbelt.adapters.appengine.monkeypatch()


class Amazon_Tracker(webapp2.RequestHandler):
    def get(self):
        for prod_url in read2gcs("prime-basis-152406.appspot.com/url2track.csv")
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'}
            res = requests.get(prod_url, headers=headers)
            soup = BeautifulSoup(res.text, 'lxml')
            price = soup.find('span',{'id':'priceblock_ourprice'})
                     'priceblock_saleprice'
            check_price = price.text if price is not None else soup.find('span',{'id':'priceblock_dealprice'}).text
            price = float(check_price[2:].replace(',',''))
        if price <= threshold:
            lineNotify(, "price reached the threshold!")
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(200)

    def post(self):
        prod_url = self.request.get("prod_url")
        threshold = self.request.get("threshold")
        msg = prod_url + threshold + '\n'
        write2gcs(filename)
        self.response.write("Success")

    def write2gcs(filenamem msg):
        self.response.write('Creating file %s\n' % filename)
        gcs_file = gcs.open(filename, 'w')
        gcs_file.write(msg + '\n')
        gcs_file.close()

        def lineNotify(token, msg):
            url = "https://notify-api.line.me/api/notify"
            headers = {
                "Authorization": "Bearer " + token, 
                "Content-Type" : "application/x-www-form-urlencoded"
            }    
                
            payload = {'message': msg}
            #payload = {'message': msg,"stickerPackageId": 2, 'stickerId': 38}
            r = requests.post(url, headers = headers, params = payload)
            return r.status_code

    def read2gcs(filenamem):
        gcs_file = gcs.open(filename)
        wait2crawl = gcs_file.readlines()
        gcs_file.close()
        return w


app = webapp2.WSGIApplication([
    ('/tracking', Amazon_Tracker),
], debug=True)
