"""color definitions for nicer console output
    USAGE:
        print(col.LT_BLUE + "My text in blue" + col.NC + "My text in default")
""" 
class col:
    RED='\033[0;31m'
    LT_RED='\033[1;31m'
    LT_GREEN='\033[1;32m'
    YELLOW='\033[1;33m'
    LT_BLUE='\033[1;36m'
    NC='\033[0m' # NO COLOR
