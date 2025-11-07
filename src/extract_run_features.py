import gpxpy
import numpy as np

def extract_run_features(gpx_path):
    with open(gpx_path, 'r') as f:
        gpx = gpxpy.parse(f)

    distances = []
    times = []

    for track in gpx.tracks:
        for segment in track.segments:
            for i in range(1, len(segment.points)):
                p1, p2 = segment.points[i-1], segment.points[i]

                # Distance in meters
                d = p1.distance_3d(p2)
                distances.append(d)

                # Time in seconds
                if p1.time and p2.time:
                    t = (p2.time - p1.time).total_seconds()
                    times.append(t)


    total_distance_km = sum(distances) / 1000 if distances else 0
    total_time_min = sum(times) / 60 if times else 0
    avg_pace = total_time_min / total_distance_km if total_distance_km else None


    paces = []
    for dist, time in zip(distances, times):
        if dist > 0:
            pace = (time / 60) / (dist / 1000) 
            if 2 < pace < 15:           
                paces.append(pace)

    pace_std = np.std(paces) if paces else None
    max_effort_pace = np.min(paces) if paces else None 
    top5_pace = np.percentile(paces, 5) if paces else None 

    return {
        "distance_km": total_distance_km,
        "duration_min": total_time_min,
        "avg_pace": avg_pace,
        "pace_std": pace_std,
        "max_pace": max_effort_pace,
        "top5_pace": top5_pace,
    }

# Debug test
if __name__ == "__main__":
    print(extract_run_features("data/raw/<your_file>.gpx"))
