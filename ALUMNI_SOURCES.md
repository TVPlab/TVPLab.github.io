# Alumni migration — 22 September 2026

Source: https://www.tvplab-cambridge.com/our-people, Former TVPLab Members, plus the featured Elizabeth Figueroa-Juarez and Eunyoung Lee cards confirmed in the supplied screenshot. All 20 people included in source order. Short research descriptions for the two featured members derive from /is and /el respectively. Portrait source URLs and profile links are recorded in data/alumni.json. Portraits are copied locally and resized without cropping.

Affiliations are explicitly labelled as records from the original site, not newly verified current appointments. The source places Basel in Germany; the copied card retains Basel and omits the inconsistent country. Names otherwise follow the directory, including Marc Slawic.

Rebuild: python scripts/build_alumni.py, python scripts/build_navigation.py, python scripts/build_zh.py. Names intentionally remain in English. Alumni are hidden in initial HTML and only revealed by their filter or direct link; they are not homepage cards. People menu links to people.html#role-alumni.

Checked EN/ZH: 18 current members initially; 20 alumni upon selection; category switching; individual deep links; language links retain selection; all portrait files exist; no alumni cards on either homepage.
