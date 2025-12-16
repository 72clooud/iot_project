import numpy as np
import pandas as pd
import os

class SpatialSelector:
    def __init__(self, input_path: str = "../data/polish_cities_with_coordinates.parquet"):
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"File not found: {input_path}")
        self.path = input_path
        self.data = pd.read_parquet(self.path)

    def select_spatial_fillers(self, threshold: int = 200, n_to_add: int = 250):

        selected = self.data.head(threshold).copy()
        candidates = self.data.iloc[threshold:].copy().reset_index(drop=True)
        
        candidates_coords = candidates[['Lat', 'Lon']].values.astype(float)
        selected_coords = selected[['Lat', 'Lon']].values.astype(float)

        lon_scale = 0.6
        candidates_coords[:, 1] *= lon_scale
        selected_coords[:, 1] *= lon_scale
        
        min_dists = np.full(len(candidates), np.inf)
        
        for s_lat, s_lon in selected_coords:
            dist_sq = (candidates_coords[:, 0] - s_lat)**2 + (candidates_coords[:, 1] - s_lon)**2
            min_dists = np.minimum(min_dists, dist_sq)

        newly_selected_indices = []

        for i in range(n_to_add):

            best_candidate_idx = np.argmax(min_dists)
            newly_selected_indices.append(best_candidate_idx)

            new_city_coords = candidates_coords[best_candidate_idx]
            min_dists[best_candidate_idx] = -1.0

            dist_sq_new = (candidates_coords[:, 0] - new_city_coords[0])**2 + (candidates_coords[:, 1] - new_city_coords[1])**2

            min_dists = np.minimum(min_dists, dist_sq_new)

        fillers = candidates.iloc[newly_selected_indices]

        self.final_data = pd.concat([selected, fillers], ignore_index=True)
    
    def save_to_parquet(self, file_path: str) -> None:
        if self.final_data is not None:
            self.final_data.to_parquet(file_path, index=False)


if __name__ == "__main__":
    selector = SpatialSelector()
    selector.select_spatial_fillers()
    selector.save_to_parquet("../data/polish_cities_spatially_selected.parquet")
