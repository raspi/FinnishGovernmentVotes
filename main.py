import logging
import os
import sys
import re
import json
import argparse
import datetime

# 3rd party
from bs4 import BeautifulSoup
import requests
import requests_cache

__VERSION__ = "1.0.0"
__AUTHOR__ = u"Pekka Järvinen"
__YEAR__ = 2019
__DESCRIPTION__ = u"Get Finnish government vote results. Version {0}.".format(__VERSION__)
__EPILOG__ = u"%(prog)s v{0} (c) {1} {2}-".format(__VERSION__, __AUTHOR__, __YEAR__)

__EXAMPLES__ = [
    u'',
    u'-' * 60,
    u'%(prog)s --year 2018 --number 181',
    u'-' * 60,
]

VOTES = {
    r'Ei': 'E',
    r'Jaa': 'J',
    r'Tyhjää': 'T',
    r'Poissa': 'P',
}

def stripSpaces(s:str) -> str:
    return re.sub(r" +", ' ', s)

def getVotes(istunto:int, vuosi:int) -> object:
    ses = requests.session()

    main_url_page = "https://www.eduskunta.fi/FI/Vaski/sivut/aanestys.aspx?istuntonro={}&vuosi={}".format(istunto, vuosi)

    log.info("Getting '{}'".format(main_url_page))
    req = ses.get(main_url_page)

    if req.status_code != 200:
        log.info("Error getting '{}'".format(main_url_page))
        return {}

    soup = BeautifulSoup(req.content, "html.parser")

    allVoteResults = soup.find("ul", {"class": "voteResults"})

    votes = []

    log.info("Parsing vote results..")
    for vResult in allVoteResults.find_all("li", {"class": "expand", "id": True, "onclick": True}):
        vote = {}

        divheader = vResult.find("div", {"class": "header"})
        vote['main'] = stripSpaces(divheader.text.strip())
        log.info("Parsing vote result '{}'..".format(vote['main']))

        divcontent = vResult.find("div", {"class": "content"})

        yhtveto = divcontent.find("div", {"class": "yhtvetoTeksti"})

        lines = []

        for p in yhtveto.find_all("p"):
            lines.append(stripSpaces(p.text.strip()))

        lines[0] = lines[0].replace("Puhemies ei osallistu äänestykseen.", "")
        lines[0] = lines[0].replace("Puhemiehenä toimi", "")

        m = re.findall(r"puhemies ([^.]+).", lines[0])
        vote['speaker'] = m[0].strip()

        vote['phase'] = lines[1]
        vote['ref'] = lines[2].replace("Valtiopäiväasia", "").strip()
        vote['presenter'] = lines[3]

        asia = yhtveto.find("h4")
        vote['title'] = asia.text.strip()
        log.info("  -'{}'..".format(vote['title']))

        # Voter names with vote
        log.info("  Parsing voters..")
        for votec in divcontent.find_all("ul"):
            for x in votec.find_all("li", {"class": "expand"}):
                txtheader = x.find("div", {"class": "header"}).text.strip()

                if txtheader != "Kansanedustajittain":
                    continue

                txtcontent = x.find("div", {"class": "content"})

                v = {}

                for voteName in txtcontent.find_all("tr"):
                    voterWithVote = voteName.find_all("td")
                    v[voterWithVote[0].text.strip()] = VOTES[voterWithVote[1].text.strip()]

                vote['votes'] = v


        votes.append(vote)

    return votes


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        #level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s',
    )

    log = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(
        description=__DESCRIPTION__,
        epilog=__EPILOG__,
        usage=os.linesep.join(__EXAMPLES__),
    )

    parser.add_argument('--year', '-y', type=int, default=datetime.datetime.now().year, dest='year', help='Year')
    parser.add_argument('--number', '-n', type=int, dest='number', required=True, help='Session number')
    parser.add_argument('--output <file.json>', '-o', type=argparse.FileType('w+', encoding='utf8'), dest='file',
                        required=False, help='JSON output file. Always overwritten.', default="output.json")
    parser.add_argument('--verbose', '-v', action='count', required=False, default=0, dest='verbose',
                        help="Be verbose. -vvv.. Be more verbose.")


    args = parser.parse_args()

    if int(args.verbose) > 0:
        logging.getLogger().setLevel(logging.DEBUG)
        log.info("Being verbose")


    requests_cache.install_cache("cache")

    log.info("Downloading HTML..")
    votes = getVotes(args.number, args.year)

    log.info("Writing JSON file..")
    with args.file as f:
        json.dump(votes, f, )

