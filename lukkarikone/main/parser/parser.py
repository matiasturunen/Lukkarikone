from . import scheludes


def fetchScheludes():
    sche = scheludes.getScheludes("https://uni.lut.fi", "https://uni.lut.fi/fi/lukujarjestykset1")
    
    if (sche):
        return True
    return False