"""Module of globals used for BSO analysis.

"""

__all__ = ['BSO_NAME',
           'USE_COLS',
           'SW_NAME',
           'WF_NAME',
          ]


WF_NAME = 'BSOA_Files'

BSO_NAME = 'bso-publications-UGA.csv'

SW_NAME= 'stopwords-fr.txt'

USE_COLS=['year',
          'software_mentions',
          'software_created',
          'software_used',
          'software_shared',
          'bso_classification',
          'title',
         ]
