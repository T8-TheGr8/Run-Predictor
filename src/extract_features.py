import gpxpy 
import numpy as np
import pandas as pd

def extract_features(gpx_path):
  with open(gpx_path, 'r') as f: 
    gpx = gpxpy.parse(f)

    distances = []
    times = []
    elevations = []

    for track in gpx.tracks:
      for segment in track.segments: 
        for i in range(1, len(segment.points)): 
          p1 = segment.points[i-1]
          p2 = segment.points[i]

          distances.append(p1.distance_3d(p2)) # distance in meters

          if p1.time and p2.time: 
            times.append((p2.time - p1.time).total_seconds())

            if p1.elevation and p2.elevation: 
              elevations.append(p2.elevation - p1.elevation)

    total_distance_km = sum(distances) / 1000 
    total_time_min = sum(times) / 60 if sum(times) else 0

    avg_pace = total_time_min / total_distance_km if total_distance_km > 0 else None
    pace_std = np.std([ (times[i]/60) / (distances[i]/1000)
                        for i in range(len(distances)) if distances[i] > 0 ])

    features = {
        "distance_km": total_distance_km,
        "duration_min": total_time_min,
        "avg_pace_min_per_km": avg_pace,
        "pace_std": pace_std,
        "elev_gain_m": sum([e for e in elevations if e > 0]),
    }

    return features

# Test on one file
if __name__ == "__main__":
    test = extract_run_features("data/raw/10-6-easy.gpx")
    print(test)
