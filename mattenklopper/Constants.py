class Constants:
    GENERAL_XPATHS = {"red": """//node[(@cat="cp" or @cat="rel" or @cat="inf") and //node[(@wvorm="pv" or @wvorm="inf") and @begin < ./preceding-sibling::node/node[@wvorm="vd"]/@begin | ./following-sibling::node/node[@wvorm="vd"]/@begin]]""",
                      "green": """//node[(@cat="cp" or @cat="rel" or @cat="inf") and //node[(@wvorm="pv" or @wvorm="inf") and @begin > ./preceding-sibling::node/node[@wvorm="vd"]/@begin | ./following-sibling::node/node[@wvorm="vd"]/@begin]]""",
                      "red_green": """//node[(@cat="cp" or @cat="rel" or @cat="inf") and .//node[(@pt="ww" or @rel="hd")] and .//node[@rel="hd" and @wvorm="vd"]]""",
                      "participles": """//node[@cat="top" and descendant::node[@wvorm="vd" and @pos="verb"]]""",
                      "adjectives": """//node[@cat="top" and descendant::node[@buiging="zonder" and @pos="adj"]]"""}
    SPECIFIC_XPATHS = {"participle": """.//node[@rel="hd" and @wvorm="vd" and @begin $SIGN$ ../../node[@rel="hd" and @pt="ww"]/@begin and not(../../@cat="smain") and ../../../../node[@id="$ID$"]]""",
                       "auxiliary": """.//node[@rel="hd" and @pt="ww" and @begin $SIGN$ ../node/node[@rel="hd" and @wvorm="vd"]/@begin and not(../@cat="smain") and ../../../node[@id="$ID$"]]""",
                       "participles": """//node[@wvorm="vd" and @pos="verb"]""",
                       "adjectives": """//node[@buiging="zonder" and @pos="adj"]"""}
    OPERATORS = {"participle": {"red": ">", "green": "<"},
                 "auxiliary": {"red": "<", "green": ">"}}
