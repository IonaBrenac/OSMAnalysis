"""Module of globals for plots in BSO data analysis.

"""

__all__ = ['BAR_COLORS_DICT',
           'LEGENDS_DICT',
           'NAMES_DICT',
           'TICKS_FONT_SIZE',
           'TITLES_DICT',
           'YAXIS_DICT',
           'YLABEL_DICT',
          ]


NAMES_DICT = {'pylib'        : "Bibliothèques python",
              'python'       : "Python",
              'matlab'       : "Matlab",
              'free_lang'    : "Languages libres",
              'prop_lang'    : "Languages propriétaires",
              'all_lang'     : "Tous languages",
              'all_python'   : "Python ou ses bibliothèques",
              'soft_articles': "Articles citant un langage de programmation",
              'created'      : "Articles citant un logiciel créé",
              'used'         : "Articles citant un logiciel utilisé",
              'shared'       : "Articles citant un logiciel partagé",
             }


BAR_COLORS_DICT = {'python': 'rgb(21, 96, 189)',
                   'matlab': 'rgb(223, 109, 20)',}


TITLES_DICT = {'fig0' : ("Historique, par type de langage de programmation, de la proportion "
                         "d\'articles citant un langage par rapport aux articles citant un logiciel"),
               'fig1' : ("Historique, par type de langage de programmation, de la proportion "
                         "d\'articles citant un langage par rapport au total des articles"),
               'fig2' : ("Historique, par type de logiciel, de la proportion d\'articles "
                         "citant le logiciel par rapport au total des articles citant des logiciels"),
               'fig3' : ("Répartition des articles citant un language par rapport au total "
                         "des articles citant un langage"),
               'fig8' : "Mots des titres des articles citant un langage de programmation",
               'fig9' : "Mots des titres des articles citant Python ou ses bibliothèques",
               'fig10': "Mots des titres des articles citant Matlab",
               }


YLABEL_DICT = {'fig0' : f'{NAMES_DICT["soft_articles"]} (%)',
               'fig1' : f'{NAMES_DICT["soft_articles"]} (%)',
               'fig2' : "Articles citant des logiciels (%)",
               'fig3' : "Articles citant des langages de programmation (%)",
               'fig4' : "Langages",
               'fig5' : "Classes",
               'fig6' : "Nombre d'articles",
               'fig8' : "Fréquence d'occurence du mot",
               'fig9' : "Fréquence d'occurence du mot",
               'fig10': "Fréquence d'occurence du mot",
              }


TICKS_FONT_SIZE = 20


YAXIS_DICT = {}
for key, label in YLABEL_DICT.items():
    YAXIS_DICT[key] = {'title': {'text': YLABEL_DICT[key],
                                 'font': {'size':20},
                                },
                      }


GO_LEGEND_DICT = {'x'          : 0,
                  'y'          : 1.0,
                  'bgcolor'    : 'rgba(255, 255, 255, 0)',
                  'bordercolor': 'rgba(255, 255, 255, 0)',
                 }


PX_LEGEND_DICT = {'title': {'text': "Légende",},}


LEGENDS_DICT = {'go': GO_LEGEND_DICT,
                'px': PX_LEGEND_DICT,
               }
