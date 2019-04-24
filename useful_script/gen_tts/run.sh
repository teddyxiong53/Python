#!/bin/sh

# ./gen_tts.py 0 spd6-pit6 6 6 
# ./gen_tts.py 0 spd6-pit7 6 7 
# ./gen_tts.py 0 spd7-pit6 7 6 
# ./gen_tts.py 0 spd7-pit7 7 7

# ./gen_tts.py 0 spd5-pit6 5 6 
# ./gen_tts.py 0 spd6-pit5 6 5 

rm ./appresources -rf
mkdir -p ./appresources/gome

./gen_tts.py 4 appresources/ 5 5 

#rm appresources/gome/response*
