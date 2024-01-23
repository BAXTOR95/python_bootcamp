class MapDrawer:
    def __init__(self, my_coordinates: tuple):
        self.my_coordinates = my_coordinates

    def prepare_map(self, iss_coordinates: tuple):
        iss_map = ""
        my_lat, my_long = self.my_coordinates
        my_y = 11 - int((my_lat + 90) / 15)
        my_x = int((my_long + 180) / 4)
        iss_lat, iss_long = iss_coordinates
        iss_y = 11 - int((iss_lat + 90) / 15)
        iss_x = int((iss_long + 180) / 4)
        is_spot_on = (my_y, my_x) == (iss_y, iss_x)
        for i in range(12):
            for j in range(90):
                if is_spot_on and (i, j) == (my_y, my_x):
                    iss_map += "🥰"
                elif (i, j) == (my_y, my_x):
                    iss_map += "👤"
                elif (i, j) == (iss_y, iss_x):
                    iss_map += "🚀"
                else:
                    iss_map += "o"
            iss_map += "\n"
        return iss_map
