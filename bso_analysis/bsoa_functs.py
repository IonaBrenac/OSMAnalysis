"""Module of functions for BSO data analysis.

ToDo: Wright functions docstrings.
"""

__all__ = ['build_articles_nbs',
           'build_bso_classes',
           'build_lang_mentions_data',
           'build_mentions_nbs',
           'build_softwares_nbs',
           'build_titles_kw',
           'build_titles_str',
           'build_word_cloud',
           'compute_errors',
           'read_bso_data',
           'set_stopwords_info',
           'set_upd_sw',
           'set_years_list',
          ]

# Standard Library imports
import re

# 3rd party imports
import numpy as np
import pandas as pd
from wordcloud import WordCloud, STOPWORDS

# local imports
import bso_analysis.bsoa_globals as bsog
import bso_analysis.regexp_globals as rg


def read_bso_data(bso_path):
    bso_data = pd.read_csv(bso_path, sep=",", usecols=bsog.USE_COLS)
    return bso_data


def set_years_list(bso_data, period):
    first_year, last_year = period
    bso_data.year = bso_data.year.replace(np.nan, 0).replace("unknown", 0).astype('int')
    years = np.sort(bso_data.year.unique())
    years = np.delete(years, np.where((years==0) | (years>last_year)))
    years = [int(year) for year in years]
    first_year_idx = years.index(first_year) 
    years = years[first_year_idx:]
    return years


def _try_search(p, x):
    try:
        return bool(p.search(x))
    except TypeError:
        return False


def _build_re_sub_data(data, pattern_re, col):
    sub_data = data[[_try_search(pattern_re, x)
                     for x in data[col]]]
    return sub_data


def _build_col_sub_data(data, col, status=None):
    if status:
        sub_data = data[data[col]==status]
    else:
        sub_data = data[data[col].notna()]
    return sub_data


def _build_year_sub_data(data, year):
    sub_data = data[data['year']==year]
    return sub_data


def build_mentions_nbs(bso_data, years=None, patterns_list=None, flatten=True):
    mentions_nbs = []
    if not years:
        for pattern in patterns_list:
            pattern_re = re.compile(pattern, flags=re.IGNORECASE)
            soft_bso_data = _build_re_sub_data(bso_data, pattern_re,
                                               'software_mentions')
            mentions_nbs.append(soft_bso_data['software_mentions'].size)
    else:
        for year in years:
            year_bso_data = _build_year_sub_data(bso_data, year)
            tmp = []
            for pattern in patterns_list:
                pattern_re = re.compile(pattern, flags=re.IGNORECASE)
                soft_bso_data = _build_re_sub_data(year_bso_data, pattern_re,
                                                   'software_mentions')
                tmp.append(soft_bso_data['software_mentions'].size)
            mentions_nbs.append(tmp)
        if flatten:
            mentions_nbs = sum(mentions_nbs, [])
    mentions_nbs = np.asarray(mentions_nbs)            
    return mentions_nbs


def compute_errors(mentions_nbs, articles_nbs):
    item_mean = np.mean(mentions_nbs*100/articles_nbs)
    item_max = np.max(mentions_nbs*100/articles_nbs)
    item_min = np.min(mentions_nbs*100/articles_nbs)
    item_error_max = item_max-item_mean
    item_error_min = item_mean-item_min
    item_error_y_dict = {'type'      :'percent',
                         'symmetric' : False,
                         'value'     : item_error_max,
                         'valueminus': item_error_min,
                        }    
    return item_error_y_dict


def build_articles_nbs(bso_data, years):
    all_articles_nbs = []
    soft_articles_nbs = [] # pour recevoir tous les articles citant des logiciels
    for year in years :
        year_bso_data = _build_year_sub_data(bso_data, year)
        all_articles_nbs.append(year_bso_data['year'].size)
        notna_bso_data = _build_col_sub_data(year_bso_data, 'software_mentions')
        soft_articles_nbs.append(notna_bso_data['software_mentions'].size)
    all_articles_nbs = np.asarray(all_articles_nbs)
    soft_articles_nbs = np.asarray(soft_articles_nbs)
    return all_articles_nbs, soft_articles_nbs


def build_softwares_nbs(bso_data, years):
    softwares_dict = {'created': [],
                      'used'   : [],
                      'shared' : [],
                     }
    for year in years:
        year_bso_data = _build_year_sub_data(bso_data, year)
        for key in softwares_dict.keys():
            key_col = 'software_' + key
            key_bso_data = _build_col_sub_data(year_bso_data, key_col, status=True)
            softwares_dict[key].append(key_bso_data[key_col].size)
    for key, softwares_nbs in softwares_dict.items():
        softwares_dict[key] = np.asarray(softwares_nbs)
    return softwares_dict


def build_lang_mentions_data(bso_data, years):
    lang_mentions_per_years = build_mentions_nbs(bso_data, years=years,
                                                 patterns_list=rg.ALL_LANG_PATTERN_LIST,
                                                 flatten=False)
    init_lang_mentions_per_years_df = pd.DataFrame(lang_mentions_per_years,
                                                   columns=rg.ALL_LANGUAGES_LIST)
    count_per_year_serie = np.sum(init_lang_mentions_per_years_df[rg.ALL_LANGUAGES_LIST], axis=1)
    init_temp_df = init_lang_mentions_per_years_df.T    
    temp_df = np.divide(init_temp_df, count_per_year_serie)
    lang_mentions_per_years_df = pd.DataFrame(temp_df.T,
                                              columns=rg.ALL_LANGUAGES_LIST)
    lang_mentions_per_years_df['years'] = years
    lang_mentions_per_years_df.sort_values(by=0, axis=1, ascending=False, inplace=True)
    return lang_mentions_per_years_df


def set_stopwords_info(sw_path):
    file = open(sw_path, 'r', encoding='utf-8')
    french_sw = file.read().replace('\n', ',')
    french_sw = list(french_sw.split(','))

    more_sw_dict = {'python': ["based", "using"],
                    'matlab': ["based", "using"],
                    'all'   : ["based", "using"],
                   }
    base_sw = list(STOPWORDS)
    return base_sw, french_sw, more_sw_dict


def set_upd_sw(base_sw, french_sw, more_sw_list):
    add_sw = sum([french_sw, more_sw_list],[])
    all_sw = base_sw + add_sw
    return all_sw


def _built_soft_bso_data(bso_data, pattern_keys_list):
    patterns_list = [rg.PATTERN_DICT[key] for key in pattern_keys_list]   
    soft_bso_data_list = []
    for pattern in patterns_list:
        pattern_re = re.compile(pattern, flags=re.IGNORECASE)
        soft_bso_data_list.append(_build_re_sub_data(bso_data, pattern_re,
                                                    'software_mentions'))
    soft_bso_data = pd.concat(soft_bso_data_list).drop_duplicates()
    return soft_bso_data


def build_bso_classes(bso_data, pattern_keys_list):
    # Selecting classes from BSO data for articles mentioning softwares
    if pattern_keys_list:
        soft_bso_data = _built_soft_bso_data(bso_data, pattern_keys_list)    
    else:
        soft_bso_data = _build_col_sub_data(bso_data, 'software_mentions')    
    soft_bso_class = soft_bso_data['bso_classification']
    soft_bso_class_serie = soft_bso_class.value_counts()
    soft_bso_class_df = soft_bso_class_serie.to_frame()
    soft_bso_class_df = soft_bso_class_serie.reset_index()
    return soft_bso_class_df


def build_titles_str(bso_data, pattern_keys_list):
    # Selecting titles from BSO data for articles mentioning softwares
    if pattern_keys_list:
        sub_bso_data = _built_soft_bso_data(bso_data, pattern_keys_list)
    else:
        sub_bso_data = bso_data.copy()   
    titles = sub_bso_data['title'].values.astype("str")
    titles_str = " ".join(titles).lower()
    return titles_str


def build_word_cloud(titles_str, base_sw, all_sw):    
    # Building wordclouds
    base_wordcloud = WordCloud(stopwords=base_sw, collocations=False,
                               background_color="white").generate(titles_str)   
    clean_wordcloud = WordCloud(stopwords=all_sw, collocations=False,
                                background_color="white").generate(titles_str)
    return base_wordcloud, clean_wordcloud

    
def build_titles_kw(titles_str, base_sw, all_sw):
    # Building titles keywords lists
    title_words_list = re.findall('[a-zA-Z]+', titles_str)    
    base_tkw = [word for word in title_words_list if word not in base_sw]
    base_tkw_df = pd.Series(base_tkw).value_counts().to_frame()    
    clean_tkw = [word for word in title_words_list if word not in all_sw]
    clean_tkw_df = pd.Series(clean_tkw).value_counts().to_frame()
    return base_tkw_df, clean_tkw_df
