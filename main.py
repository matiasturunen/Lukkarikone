# ------------------------------------------------------------------------------
# Name:        Main.py
# Purpose:	   Handle all the things!!
#
# Author:      Matias
#
# Created:     25.09.2015
# Copyright:   (c) Matias 2015
# ------------------------------------------------------------------------------
from lib.utilities import links, html, scheludes
from lib.utilities import debug
from lib.models import Link
import re
import os


uniURL = "https://uni.lut.fi"
scheludeListURL = uniURL + "/fi/lukujarjestykset1"


def main():
    local = True    # set False to load scheludes from internet
    if ( local ):
        sche = scheludes.getLocalScheludesHTML()
        scheludes.saveScheludes(sche)
    else:
        sche = scheludes.getScheludes(uniURL, scheludeListURL)

if __name__ == '__main__':
    main()
