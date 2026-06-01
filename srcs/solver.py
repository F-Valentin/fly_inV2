from zone import Zone, ZoneState


class Solver:
    def __init__(self) -> None:
        """Create a solver instance (unused; static methods are provided)."""
        pass

    @staticmethod
    def _dfs_rec(source: Zone, dest: Zone,
                 path: list[Zone], visited_zone: set[str],
                 all_paths: list[list[Zone]]
                 ) -> None:

        path.append(source)

        if source.metadata.state == ZoneState.BLOCKED:
            return

        if source.name == dest.name:
            all_paths.append(path.copy())
            return

        visited_zone.add(source.name)
        for connection in source.connections:
            if connection.dest.name not in visited_zone:
                Solver._dfs_rec(
                    connection.dest,
                    dest,
                    path,
                    visited_zone,
                    all_paths)
                path.pop()
        visited_zone.remove(source.name)

    @staticmethod
    def dfs(start: Zone, dest: Zone) -> list[list[Zone]]:
        """Find all valid paths from start to dest using DFS."""
        visited_zone: set[str] = set()
        all_paths: list[list[Zone]] = []

        Solver._dfs_rec(start, dest, [], visited_zone, all_paths)
        return all_paths
