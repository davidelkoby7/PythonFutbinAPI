import json
from futbin_api import FutbinAPI

FutbinAPI.CURRENT_PLATFORM = FutbinAPI.Platforms.PC
print (FutbinAPI.get_latest_player_prices_hourly_yesterday("neymar"))

