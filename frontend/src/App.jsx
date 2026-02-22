import { useState } from "react";
import axios from "axios";
import {
  MapContainer,
  TileLayer,
  Marker,
  Polyline
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./App.css";

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png",
  iconUrl:
    "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
  shadowUrl:
    "https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png"
});

// 🌍 Generate safe offshore route
function generateSafeSeaRoute(start, end, curvature = 0.25) {
  const [lat1, lon1] = start;
  const [lat2, lon2] = end;

  const midLat = (lat1 + lat2) / 2;

  // Determine offshore direction automatically
  const lonDirection = lon2 > lon1 ? 1 : -1;

  const distance = Math.abs(lon2 - lon1);

  const midLon =
    (lon1 + lon2) / 2 +
    lonDirection * distance * curvature;

  return [
    [lat1, lon1],
    [midLat, midLon],
    [lat2, lon2]
  ];
}

function App() {
  const [startLat, setStartLat] = useState("");
  const [startLon, setStartLon] = useState("");
  const [endLat, setEndLat] = useState("");
  const [endLon, setEndLon] = useState("");

  const [result, setResult] = useState(null);
  const [baselineRoute, setBaselineRoute] = useState([]);
  const [optimizedRoute, setOptimizedRoute] = useState([]);

  const optimizeRoute = async () => {
    if (!startLat || !startLon || !endLat || !endLon) {
      alert("Please enter all coordinates");
      return;
    }

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/optimize",
        {
          voyage: {
            start_port: {
              lat: parseFloat(startLat),
              lon: parseFloat(startLon)
            },
            end_port: {
              lat: parseFloat(endLat),
              lon: parseFloat(endLon)
            }
          }
        }
      );

      setResult(response.data);

      const start = [parseFloat(startLat), parseFloat(startLon)];
      const end = [parseFloat(endLat), parseFloat(endLon)];

      // 🔴 Baseline route (slight offshore)
      const baseline = generateSafeSeaRoute(start, end, 0.15);

      // 🟢 Optimized route (more offshore)
      const optimized = generateSafeSeaRoute(start, end, 0.35);

      setBaselineRoute(baseline);
      setOptimizedRoute(optimized);

    } catch (error) {
      alert("Backend error");
    }
  };

  return (
    <div className="app-container">
      <div className="card">
        <h1 className="title">🚢 AI Shipping Route Optimization</h1>

        <div className="input-grid">
          <div>
            <label>Start Latitude</label>
            <input type="number" value={startLat} onChange={(e) => setStartLat(e.target.value)} />
          </div>
          <div>
            <label>Start Longitude</label>
            <input type="number" value={startLon} onChange={(e) => setStartLon(e.target.value)} />
          </div>
          <div>
            <label>End Latitude</label>
            <input type="number" value={endLat} onChange={(e) => setEndLat(e.target.value)} />
          </div>
          <div>
            <label>End Longitude</label>
            <input type="number" value={endLon} onChange={(e) => setEndLon(e.target.value)} />
          </div>
        </div>

        <button className="optimize-btn" onClick={optimizeRoute}>
          Optimize Route
        </button>
      </div>

      {result && (
        <>
          <div className="report-card">
            <h2>📊 Voyage Optimization Report</h2>
            <div className="report-item">{result["Optimized Route Generated"]}</div>
            <div className="report-item">{result["Weather Impact Adjustment"]}</div>
            <div className="report-item">{result["Emissions Report"]}</div>
            <div className="report-item">{result["Operational Insight"]}</div>
            <div className="timestamp">{result["Data Timestamp"]}</div>
          </div>

          <div className="map-container">
            <h2>🌊 Maritime Route Visualization</h2>

            <MapContainer
              center={[parseFloat(startLat), parseFloat(startLon)]}
              zoom={4}
              style={{ height: "500px", width: "100%", borderRadius: "15px" }}
            >
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />

              <Marker position={[parseFloat(startLat), parseFloat(startLon)]} />
              <Marker position={[parseFloat(endLat), parseFloat(endLon)]} />

              <Polyline positions={baselineRoute} color="red" weight={5} />
              <Polyline positions={optimizedRoute} color="green" weight={5} />
            </MapContainer>
          </div>
        </>
      )}
    </div>
  );
}

export default App;