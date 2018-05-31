#!/bin/sh

# To be placed in ~/.local/share/nautilus/scripts/

# Flatten a directory so convert this:
# .
# └── Dire Straits - Alchemy
#     ├── CD1
#     │   ├── 01_Once_Upon_A_Time_in_The_West (2).ogg
#     │   ├── 02_Expresso_Love (2).ogg
#     │   ├── 03_Romeo_And_Juliet (2).ogg
#     │   ├── 04_Love_over_Gold (2).ogg
#     │   ├── 05_Private_Investigations (2).ogg
#     │   ├── 06_Sultans_Of_swing (2).ogg
#     │   ├── Cover1.jpg
#     │   └── Cover2.jpg
#     └── CD2
#         ├── 01_Two_Young_Lovers_(Intro-_The_Carousel_Waltz) (2).ogg
#         ├── 02_Tunnel_Of_Love (2).ogg
#         ├── 03_Telegraph_Road (2).ogg
#         ├── 04_Solid_Rock (2).ogg
#         ├── 05_Going_Home_-_Theme_from_Local_Hero (2).ogg
#         ├── Cover1.jpg
#         └── Cover2.jpg
# into this:
# .
# ├── Dire Straits - Alchemy_CD1_01_Once_Upon_A_Time_in_The_West (2).ogg
# ├── Dire Straits - Alchemy_CD1_02_Expresso_Love (2).ogg
# ├── Dire Straits - Alchemy_CD1_03_Romeo_And_Juliet (2).ogg
# ├── Dire Straits - Alchemy_CD1_04_Love_over_Gold (2).ogg
# ├── Dire Straits - Alchemy_CD1_05_Private_Investigations (2).ogg
# ├── Dire Straits - Alchemy_CD1_06_Sultans_Of_swing (2).ogg
# ├── Dire Straits - Alchemy_CD1_Cover1.jpg
# ├── Dire Straits - Alchemy_CD1_Cover2.jpg
# ├── Dire Straits - Alchemy_CD2_01_Two_Young_Lovers_(Intro-_The_Carousel_Waltz) (2).ogg
# ├── Dire Straits - Alchemy_CD2_02_Tunnel_Of_Love (2).ogg
# ├── Dire Straits - Alchemy_CD2_03_Telegraph_Road (2).ogg
# ├── Dire Straits - Alchemy_CD2_04_Solid_Rock (2).ogg
# ├── Dire Straits - Alchemy_CD2_05_Going_Home_-_Theme_from_Local_Hero (2).ogg
# ├── Dire Straits - Alchemy_CD2_Cover1.jpg
# └── Dire Straits - Alchemy_CD2_Cover2.jpg

for folder in "$@"; do
    cd "$folder"
    find */ -type f -exec bash -c 'file=${1#./}; mv "$file" "${file//\//_}"' _ '{}' \;
    find */ -depth -type d -exec rmdir '{}' \;
done
