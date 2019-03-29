This project has been discontinued. See: 

* http://avoindata.eduskunta.fi/ 
* http://avoindata.eduskunta.fi/api/v1/tables/SaliDBAanestys/rows?perPage=10&page=0
* http://avoindata.eduskunta.fi/api/v1/tables/SaliDBAanestysEdustaja/rows?perPage=10&page=0

# FinnishGovernmentVotes
Convert Finnish government votes to more parsable JSON.

Votes are available at:

https://www.eduskunta.fi/FI/lakiensaataminen/taysistunnon_verkkolahetykset/Sivut/Aanestykset.aspx

https://www.eduskunta.fi/FI/Vaski/sivut/aanestys.aspx?aanestysnro=N&istuntonro=S&vuosi=Y

Where 
* N is voting number
* S is session number
* Y is year

This can be also used as https://www.eduskunta.fi/FI/Vaski/sivut/aanestys.aspx?istuntonro=S&vuosi=Y

# Usage

    python main.py --help

For help.

    python main.py --year 2018 --number 181

This will write `output.json`.

As of writing this README you can get all votes with:

    ./get_year.sh 2015 85
    ./get_year.sh 2016 139
    ./get_year.sh 2017 147
    ./get_year.sh 2018 181
   
# Requirements
* Python 3.6+
* Requests
* Requests cache
* Beautiful soup 4
