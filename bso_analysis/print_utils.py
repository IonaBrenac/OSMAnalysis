"""Module of functions for control prints of results of BSO data analysis.

ToDo: Wright functions docstrings.
"""

__all__ = ['print_lang_mentions',
           'print_mentions_dict',
           'print_softwares_dict',
          ]


def print_mentions_dict(years, mentions_dict, soft_articles_nbs, all_articles_nbs):
    # Prints for control of mentions dict
    print("\nYears:", years)
    for key, mentions_nbs in mentions_dict.items():
        print(f"Number of {key} mentions per year:", mentions_nbs)

    print("total of articles mentionning softwares:", soft_articles_nbs)
    print("total of all articles:", all_articles_nbs)


def print_softwares_dict(years, softwares_dict):
    print("\nYears:", years)
    for key, softwares_nbs in softwares_dict.items():
        print(f"Number of {key} softwares per year:", softwares_nbs)


def print_lang_mentions(Lang_mentions_dict, big_lang_df):
    # Prints for control of language mentions
    for key, Lang_mentions_nbs in Lang_mentions_dict.items():
        print(f"Number of mentions of {key} language:", Lang_mentions_nbs)
    print()    
    print(big_lang_df['languages'])
