import httplib, urllib

# Establish first HTTP connection.
http = httplib.HTTPConnection("daftarj.spr.gov.my")
http.request("GET", "/daftarj/")

conn = http.getresponse()

if conn.status != 200:
   print "Error getting DaftarJ - ", conn.status, conn.reason

# Parse the data for hidden key
data = conn.read()
lhtm = data.split("<")

for tag in lhtm:
    if tag.startswith("input") and tag.find("__VIEWSTATE") != -1:
        tag_s = tag.find("value=\"")
        tag_e = tag.find("\"", tag_s + 7)
        vkey = tag[tag_s+7:tag_e]
        print "VKEY", vkey
    elif tag.startswith("input") and tag.find("__EVENTVALIDATION") != -1:
        tag_s = tag.find("value=\"")
        tag_e = tag.find("\"", tag_s + 7)
        ekey = tag[tag_s+7:tag_e]
        print "EKEY", ekey
        

# Assume key found. Proceed with IC check
# Example POST request: __EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwULLTE1ODMwMDk4MDUPZBYCAgEPZBYGAhMPDxYCHgRUZXh0BQgyNzUzMjk2MGRkAhcPZBYCAgMPDxYCHgdWaXNpYmxlaGRkAiEPDxYCHwAFBzIxMzc0NTRkZGQ3ZABOk0gdkLKGDM8EsbMDhqcCmA%3D%3D&txtIC=800312145029&Semak=SEMAK&__EVENTVALIDATION=%2FwEWAwLv186jCgKp%2B5bqDwKztY%2FNDi%2BNpOZAXdjQF%2FCAwA1SgP2JaZP3

params = urllib.urlencode ({"__VIEWSTATE":vkey,
                            "__EVENTVALIDATION":ekey,
                            "__EVENTTARGET":"",
                            "__EVENTARGUMENT":"",
                            "Semak":"SEMAK",
                            "txtIC": "800312145029"})
headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}

post = httplib.HTTPConnection("daftarj.spr.gov.my")
post.request("POST", "/daftarj/daftar.aspx", params, headers)

conn = post.getresponse()

if conn.status != 200:
    print "Error submitting MyKAD - ", conn.status, conn.reason

# Parse results - look for KETERANGAN

data = conn.read()
res = data.find("KETERANGAN")
print res
