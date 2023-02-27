class Constants:
    GENERAL_XPATHS = {"red": """//node[@cat="cp" and node[@rel="cmp" and @pt="vg" and number(@begin) < ../node[@rel="body" and @cat="ssub"]/node[@rel="su" and @pt="vnw"]/number(@begin)] and node[@rel="body" and @cat="ssub" and node[@rel="su" and @pt="vnw" and number(@begin) < ../node[@rel="hd" and @pt="ww"]/number(@begin)] and node[@rel="hd" and @pt="ww" and number(@begin) < ../node[@rel="vc" and @cat="ppart"]/node[@rel="hd" and @pt="ww"]/number(@begin)] and node[@rel="vc" and @cat="ppart" and node[@rel="hd" and @pt="ww"]]]]""",
                      "green": """//node[@cat="cp" and node[@rel="cmp" and @pt="vg" and number(@begin) < ../node[@rel="body" and @cat="ssub"]/node[@rel="su" and @pt="vnw"]/number(@begin)] and node[@rel="body" and @cat="ssub" and node[@rel="su" and @pt="vnw" and number(@begin) < ../node[@rel="vc" and @cat="ppart"]/node[@rel="hd" and @pt="ww"]/number(@begin)] and node[@rel="vc" and @cat="ppart" and node[@rel="hd" and @pt="ww" and number(@begin) < ../../node[@rel="hd" and @pt="ww"]/number(@begin)]] and node[@rel="hd" and @pt="ww"]]]""",
                      "participles": """//node[@cat="top" and descendant::node[@wvorm="vd" and @pos="verb"]]""",
                      "adjectives": """//node[@cat="top" and descendant::node[@buiging="zonder" and @pos="adj"]]"""}
    SPECIFIC_XPATHS = {"participle": """//node[@wvorm="vd" and @begin $SIGN$ ../following-sibling::node[@wvorm="pv"]/@begin | ../preceding-sibling::node[@wvorm="pv"]/@begin]""",
                       "auxiliary": """//node[@wvorm="pv" and @begin $SIGN$ ./preceding-sibling::node/node[@wvorm="vd"]/@begin | ./following-sibling::node/node[@wvorm="vd"]/@begin]""",
                       "participles": """//node[@wvorm="vd" and @pos="verb"]""",
                       "adjectives": """//node[@buiging="zonder" and @pos="adj"]"""}
    OPERATORS = {"participle": {"red": ">", "green": "<"},
                 "auxiliary": {"red": "<", "green": ">"}}
