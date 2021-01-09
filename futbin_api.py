import requests
import datetime

class FutbinAPI:
    FIFA_YEAR = "21"
    FUTBIN_BASE_URL = "https://www.futbin.com/"
    XBOX_PLATFORM = "xbox"
    PLAYSTATION_PLATFORM = "ps"
    PC_PLATFORM = "pc"
    CURRENT_PLATFORM = PLAYSTATION_PLATFORM

    @staticmethod
    def get_players_cards_data(player_name):
        """
        Will return an array with data about all of the cards a certain player has.
        Each item of the array will have the info of a card of this player. The dict will be of the form:
            {
                "rating": "92",
                "position": "CM",
                "club_image": "https:\/\/cdn.futbin.com\/content\/fifa21\/img\/clubs\/10.png",
                "image": "https:\/\/cdn.futbin.com\/content\/fifa21\/img\/players\/192985.png?v=22",
                "rare_type": "70",
                "full_name": "Kevin De Bruyne",
                "url_name": "Kevin De Bruyne",
                "name": "De Bruyne",
                "id": "26796",
                "nation_image": "https:\/\/cdn.futbin.com\/content\/fifa21\/img\/nation\/7.png",
                "rare": "1",
                "version": "TOTGS"
            }
        """
        player_cards_data = requests.get("{}/search?year={}&term={}".format(FutbinAPI.FUTBIN_BASE_URL, FutbinAPI.FIFA_YEAR, player_name))
        return player_cards_data.json()

    @staticmethod
    def get_player_url_id(player_name, rare_type = 1):
        rare_type = str(rare_type)
        players_data = FutbinAPI.get_players_cards_data(player_name)
        wanted_card_data = [x for x in players_data if x["rare_type"] == rare_type][0]
        return wanted_card_data["id"]

    @staticmethod
    def get_players_main_html(player_name, rare_type = 1):
        player_url_id = FutbinAPI.get_player_url_id(player_name, rare_type)
        player_html_page = requests.get("{}/{}/player/{}".format(FutbinAPI.FUTBIN_BASE_URL, FutbinAPI.FIFA_YEAR, player_url_id)).text
        return player_html_page

    @staticmethod
    def get_player_db_id(player_name, rare_type = 1):
        player_html = FutbinAPI.get_players_main_html(player_name, rare_type)
        db_id_line = [x for x in player_html.split() if "data-player-resource=" in x][0]
        player_db_id = db_id_line.split("data-player-resource=")[-1][1:-1]
        return player_db_id

    @staticmethod
    def get_current_player_price(player_name, rare_type = 1):
        player_db_id = FutbinAPI.get_player_db_id(player_name, rare_type)
        player_price_info = requests.get("{}/{}/playerPrices?player={}".format(FutbinAPI.FUTBIN_BASE_URL, FutbinAPI.FIFA_YEAR, player_db_id)).json()
        player_price = player_price_info[player_db_id]["prices"][FutbinAPI.CURRENT_PLATFORM]["LCPrice"]
        return player_price

    @staticmethod
    def get_latest_player_prices(player_name, search_type, rare_type = 1):
        player_db_id = FutbinAPI.get_player_db_id(player_name, rare_type)
        player_price_info = requests.get("{}/{}/playerGraph?type={}&year={}&player={}".format(FutbinAPI.FUTBIN_BASE_URL, FutbinAPI.FIFA_YEAR, search_type, player_db_id, player_db_id)).json()
        player_prices = player_price_info[FutbinAPI.CURRENT_PLATFORM]

        # Converting the arrays into something easier to work with
        for i in range(len(player_prices)):
            data_point_dict = {}
            data_point_dict["price"] = player_prices[i][1]
            data_point_dict["timestamp"] = player_prices[i][0]
            data_point_dict["date_time"] = datetime.datetime.fromtimestamp(player_prices[i][0] / 1e3)
            data_point_dict["date_time"] = data_point_dict["date_time"].strftime("%D_%H:%M:%S")
            player_prices[i] = data_point_dict

        return player_prices

    @staticmethod
    def get_latest_player_prices_daily(player_name, rare_type = 1):
        return FutbinAPI.get_latest_player_prices(player_name, search_type = "daily_graph", rare_type = rare_type)

    @staticmethod
    def get_latest_player_prices_hourly_today(player_name, rare_type = 1):
        return FutbinAPI.get_latest_player_prices(player_name, search_type = "today", rare_type = rare_type)

    @staticmethod
    def get_latest_player_prices_hourly_yesterday(player_name, rare_type = 1):
        return FutbinAPI.get_latest_player_prices(player_name, search_type = "yesterday", rare_type = rare_type)

