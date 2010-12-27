#!/usr/bin/python
#
# SPR MyKAD Checker - Checks MyKAD against SPR database for registration purpose.
# Copyright (C) 2010 Shawn Tan <shawn.tan@sybreon.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

## HOW TO USE: This script looks for a list of MyKAD numbers in
## "mykad.csv" that must reside in the same directory as the
## script. It will output the results to "result.csv".

import httplib, urllib, csv

def checkMyKAD(mykad):

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
         vkey = tag[tag_s + 7:tag_e]
         #print "VKEY", vkey
      elif tag.startswith("input") and tag.find("__EVENTVALIDATION") != -1:
         tag_s = tag.find("value=\"")
         tag_e = tag.find("\"", tag_s + 7)
         ekey = tag[tag_s + 7:tag_e]
         #print "EKEY", ekey
         
   # Assume key found. Proceed with IC check

   params = urllib.urlencode ({"__VIEWSTATE":vkey,
                               "__EVENTVALIDATION":ekey,
                               "__EVENTTARGET":"",
                               "__EVENTARGUMENT":"",
                               "Semak":"SEMAK",
                               "txtIC": mykad})
   
   # Example POST request: __EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwULLTE1ODMwMDk4MDUPZBYCAgEPZBYGAhMPDxYCHgRUZXh0BQgyNzUzMjk2MGRkAhcPZBYCAgMPDxYCHgdWaXNpYmxlaGRkAiEPDxYCHwAFBzIxMzc0NTRkZGQ3ZABOk0gdkLKGDM8EsbMDhqcCmA%3D%3D&txtIC=800312145029&Semak=SEMAK&__EVENTVALIDATION=%2FwEWAwLv186jCgKp%2B5bqDwKztY%2FNDi%2BNpOZAXdjQF%2FCAwA1SgP2JaZP3

   headers = {"Content-type": "application/x-www-form-urlencoded",
              "Accept": "text/plain"}
   
   # reuse previous HTTP request
   http.request("POST", "/daftarj/daftar.aspx", params, headers)
   conn = http.getresponse()
   
   if conn.status != 200:
      print "Error submitting MyKAD - ", conn.status, conn.reason
      
   # Parse results - look for "KETERANGAN"
      
   data = conn.read()
   res = data.find("KETERANGAN")

   return res != -1

# Parse through mykad.csv file

csvRead = csv.reader(open("mykad.csv", "rb"))
csvWrite = csv.writer(open("result.csv", "wb"))

for row in csvRead:
   #print row[0]
   print "Checking - ", row[0]
   res = checkMyKAD(row[0])
   csvWrite.writerow([row[0], res])

#if checkMyKAD("850725136345"):
