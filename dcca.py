# Author: V. David Zvenyach
# Date created:2014-02-21

import time
from datetime import date
from datetime import datetime
from lxml import html

from juriscraper.GenericSite import GenericSite
from juriscraper.lib.string_utils import titlecase


class Site(GenericSite):
    def __init__(self):
        super(Site, self).__init__()
        self.court_id = self.__module__
        self.url = 'http://www.dccourts.gov/internet/opinionlocator.jsf'

# tr.class="opinionTR1" or "opinionTR2"
# <tr class="opinionTR1"><td class="opinionC1"><a href="/internet/documents/13-BG-955.pdf" target="13-BG-955.pdf">13-BG-955</a></td><td class="opinionC2">In re: Scott B. Gilly</td><td class="opinionC3">Nov 7, 2013</td><td class="opinionC4"></td><td class="opinionC5"></td></tr>

    #.opinionC1/a[@href] ('http://www.dccourts.gov/' + opinionC1 (e.g., http://www.dccourts.gov/internet/documents/13-BG-955.pdf)
    def _get_download_urls(self):
        path = '//td[@class="opinionC1"]/a/@href'
        return [t for t in self.html.xpath(path)]

    #.opinionC2
    def _get_case_names(self):
        path = '//td[@class="opinionC2"]//text()'
        return [titlecase(t.upper()) for t in self.html.xpath(path)]

    #.opinionC3 (e.g., Nov 7, 2013)
    def _get_case_dates(self):
        path = '//td[@class="opinionC3"]//text()'
        return [date.fromtimestamp(time.mktime(time.strptime(date_string, '%b %d, %Y')))
                    for date_string in self.html.xpath(path)]

    def _get_precedential_statuses(self):
        return ["Published"] * len(self.case_names)

    #.opinionC1 value (e.g., 13-BG-955)
    def _get_docket_numbers(self):
        path = '//td[@class="opinionC1"]//text()'
        return [t for t in self.html.xpath(path)]

site = Site()
site.parse()
print str(site)