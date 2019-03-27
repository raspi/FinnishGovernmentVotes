import logging
import os
import sys
import re
import json
import argparse
import datetime
import csv


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        #level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s',
    )

    log = logging.getLogger(__name__)

    # Read all JSON files
    filelist = []

    for i in os.listdir("."):
        if os.path.isfile(i):
            extension = os.path.splitext(i)[1]
            if '.json' in extension:
                filelist.append(i)

    # Get list of all voter names
    voters = []

    for fname in filelist:
        with open(fname, 'r', encoding='utf8') as f:
            d = json.load(f)

            for idx in d:
                for x in idx['votes']:
                    if x not in voters:
                        voters.append(x)


    # Get votes
    votes = []

    for fname in filelist:
        with open(fname, 'r', encoding='utf8') as f:
            d = json.load(f)

            for idx in d:
                vote = {
                    "main": idx['main'],
                    "title": idx['title'],
                    "speaker": idx['speaker'],
                    "ref": idx['ref'],
                    "presenter": idx['presenter'],
                }

                # Map votes by voter name
                for voterName in voters:
                    if voterName in idx['votes']:
                        vote[voterName] = idx['votes'][voterName]
                    else:
                        vote[voterName] = ""

                votes.append(vote)

    # Generate CSV file
    with open("res.csv", "w", encoding="utf8") as f:
        fieldnames = ['main', 'title', 'speaker', 'ref', 'presenter', ]

        for voterName in voters:
            fieldnames.append(voterName)

        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        for i in votes:
            row = {
                'main': i['main'],
                'title': i['title'],
                'speaker': i['speaker'],
                'ref': i['ref'],
                'presenter': i['presenter'],
            }

            for voterName in voters:
                row[voterName] = i[voterName]


            writer.writerow(row)
