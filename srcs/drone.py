from zone import Zone


class Drone:
    def __init__(self, id: int) -> None:
        """Create a drone with an identifier and initial movement state."""
        self.id = id
        self.status: str = "move"
        self.waiting_turn: int = 0
        self.path: list[Zone] = []

    @staticmethod
    def create_drones(nb_of_drones: int = 1) -> list[Drone]:
        """Generate a list of drones with sequential ids."""
        drones: list[Drone] = []

        for i in range(0, nb_of_drones):
            drones.append(Drone(i))

        return drones

    @staticmethod
    def remove_drones_in_order(nb_of_drones: int, drones: list[Drone]) -> None:
        """Remove the first N drones from an ordered drone list."""
        new_drones = drones[nb_of_drones:]
        drones.clear()
        drones.extend(new_drones)

    def __str__(self) -> str:
        """Return a readable string representation of the drone."""
        return f"drone_id: {self.id}"
