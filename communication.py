class CommunicationModel:
    def __init__(self, vehicles):
        self.vehicles = vehicles

    def send_alert(self, vehicle):
        print(f"Alert: Emergency vehicle {vehicle.id} is approaching.")

    def update_traffic_lights(self):
        print("Adjusting traffic lights for emergency clearance...")
