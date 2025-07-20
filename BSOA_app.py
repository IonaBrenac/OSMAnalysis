#%% Imports

# Standard Library imports
from pathlib import Path

# 3rd party imports
import pandas as pd
import plotly.io as pio

# Local imports
import bso_analysis.bsoa_functs as bsof
import bso_analysis.bsoa_globals as bsog
import bso_analysis.plot_utils as pl
import bso_analysis.print_utils as pr
import bso_analysis.regexp_globals as rg

#%% openning plotly in browser
pio.renderers.default='browser'

#%% Setting paths

# Specific paths to user (user root and working root)
user_root = Path.home()
wr_path = user_root / Path('Documents') / Path('Iona')

# Work paths
wf_path = wr_path / Path(bsog.WF_NAME)
bso_path = wf_path / Path(bsog.BSO_NAME)
sw_path = wf_path / Path(bsog.SW_NAME)

print("\nRun completed")

#%% Getting BSO data
bso_data = bsof.read_bso_data(bso_path)

print("BSO data columns:" bso_data.columns)

#%% clean year column to have int values, no strings like "unknown"
# (2 occurences) and no date from the future (years >2024 not representative)
period = (2013, 2023)
years = bsof.set_years_list(bso_data, period)

print("Analysis years:", years)

print("\nRun completed")

#%%
###########################
##### Annual analysis #####
###########################

#%% Computing mentions numbers of softwares and languages 
# using 'year' column and regular expressions on 'software_mentions' column

mentions_dict = {}
for key, pattern in rg.PATTERN_DICT.items():
    mentions_dict[key] = bsof.build_mentions_nbs(bso_data, years=years,
                                                 patterns_list=[pattern])
mentions_dict['all_python'] = mentions_dict['pylib'] + mentions_dict['python']

all_articles_nbs, soft_articles_nbs = bsof.build_articles_nbs(bso_data, years)

#%% error bars
soft_errors_y_dict = {}
all_errors_y_dict = {}
for key, mentions_nbs in mentions_dict.items():
    soft_errors_y_dict[key] = bsof.compute_errors(mentions_nbs, soft_articles_nbs)
    all_errors_y_dict[key] = bsof.compute_errors(mentions_nbs, all_articles_nbs)

pr.print_mentions_dict(years, mentions_dict, soft_articles_nbs, all_articles_nbs)
pl.plot_nbs_dict('fig0', years, mentions_dict, soft_articles_nbs, soft_errors_y_dict)
pl.plot_nbs_dict('fig1', years, mentions_dict, all_articles_nbs, all_errors_y_dict,
                 mentions_add_tup=(soft_articles_nbs, 'soft_articles'))

print("\nRun completed")

#%% Computing data for softwares creation vs utilisation vs sharing
# using 'year', 'software_created', 'software_used' and 'software_shared' columns

softwares_dict = bsof.build_softwares_nbs(bso_data, years)

pr.print_softwares_dict(years, softwares_dict)
pl.plot_nbs_dict('fig2', years, softwares_dict, soft_articles_nbs)

print("\nRun completed")

#%% Create dataframe of language per years count nb of mentions per softwares per years 
# using 'year' column and regular expressions on 'software_mentions' column

lang_mentions_per_years_df = bsof.build_lang_mentions_data(bso_data, years)

pl.plot_bar_df('fig4', lang_mentions_per_years_df, "years")

print("\nRun completed")

#%%
###############################
##### All period analysis #####
###############################

#%% Computing part of each programming languages in softwares mentions
# using  regular expressions on 'software_mentions' column

lang_mentions = bsof.build_mentions_nbs(bso_data, patterns_list=rg.ALL_LANG_PATTERN_LIST)
Lang_mentions_dict = dict(zip(rg.ALL_LANGUAGES_LIST, lang_mentions))

#%% Create dataframe of languge and filter them when mentionned 100 times or less
lang_df = pd.DataFrame({'languages':rg.ALL_LANGUAGES_LIST, 'languages_mentions':lang_mentions})
big_lang_df = lang_df[lang_df['languages_mentions'] > 100]

pr.print_lang_mentions(Lang_mentions_dict, big_lang_df)
pl.plot_pie_df('fig3', big_lang_df, ['languages', 'languages_mentions'])

print("\nRun completed")

#%% Analysing words of titles for articles mentioning softwares
# statistics and wordcloud

base_sw, french_sw, more_sw_dict = bsof.set_stopwords_info(sw_path)

titles_kw_dict = {}
wordcloud_dict = {}
for sw_key, pattern_keys_list in rg.PATTERN_KEYS_DICT.items():
    all_sw = bsof.set_upd_sw(base_sw, french_sw, more_sw_dict[sw_key])
    titles_str = bsof.build_titles_str(bso_data, pattern_keys_list)
    titles_kw_dict[sw_key] = bsof.build_titles_kw(titles_str, base_sw, all_sw)
    wordcloud_dict[sw_key] = bsof.build_word_cloud(titles_str, base_sw, all_sw)    

pl.show_wordcloud_dict(wordcloud_dict)

#%% Scatter chart of all titles keywords after base_sw remove
freq_max = 1000
key = 'all'
titles_kw_tup = titles_kw_dict[key]
full_titles_kw_df = titles_kw_tup[1]
pl.plot_pareto_df('fig8', full_titles_kw_df, 'count', freq_max)

print("\nRun completed")

#%% Scatter chart of Python titles keywords after all_sw remove
freq_max = 10
key = 'python'
titles_kw_tup = titles_kw_dict[key]
full_titles_kw_df = titles_kw_tup[1]
pl.plot_pareto_df('fig9', full_titles_kw_df, 'count', freq_max)

print("\nRun completed")

#%% Scatter chart of  python titles keywords after all_sw remove
freq_max = 5
key = 'matlab'
titles_kw_tup = titles_kw_dict[key]
full_titles_kw_df = titles_kw_tup[1]
pl.plot_pareto_df('fig10', full_titles_kw_df, 'count', freq_max)

print("\nRun completed")

#%% Analysing classifications of articles mentioning softwares

classes_dict = {}
for sw_key, pattern_keys_list in rg.PATTERN_KEYS_DICT.items():
    classes_dict[sw_key] = bsof.build_bso_classes(bso_data, pattern_keys_list)

pl.plot_pie_df('fig5', classes_dict['all'], ['bso_classification', 'count'])
pl.plot_bar_nbs_dict('fig6', classes_dict, ['matlab', 'python'], ['bso_classification', 'count'])

print("\nRun completed")
