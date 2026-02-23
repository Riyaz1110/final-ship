// import { MapPin } from "lucide-react";

// interface MapSectionProps {
//   startCoords: { lat: number; lon: number } | null;
//   endCoords: { lat: number; lon: number } | null;
//   visible: boolean;
// }

// const MapSection = ({ startCoords, endCoords, visible }: MapSectionProps) => {
//   return (
//     <section className="py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
//       <div
//         className={`glass-card overflow-hidden ${visible ? "" : "opacity-0"}`}
//         style={{
//           animation: visible ? "fadeInUp 0.6s ease-out 0.3s both" : "none",
//         }}
//       >
//         <div className="p-5 border-b border-border/50 flex items-center justify-between">
//           <div className="flex items-center gap-2">
//             <MapPin className="w-4 h-4 text-primary" />
//             <span className="text-sm font-semibold text-foreground">Route Visualization</span>
//           </div>
//           {startCoords && endCoords && (
//             <span className="text-xs text-muted-foreground">
//               {startCoords.lat.toFixed(2)}°, {startCoords.lon.toFixed(2)}° → {endCoords.lat.toFixed(2)}°, {endCoords.lon.toFixed(2)}°
//             </span>
//           )}
//         </div>

//         {/* Map placeholder — ready for Leaflet integration */}
//         <div className="relative w-full aspect-[21/9] min-h-[320px] bg-secondary/30 flex items-center justify-center">
//           {/* Grid overlay for visual effect */}
//           <div
//             className="absolute inset-0 opacity-[0.04]"
//             style={{
//               backgroundImage:
//                 "linear-gradient(hsl(var(--foreground)) 1px, transparent 1px), linear-gradient(90deg, hsl(var(--foreground)) 1px, transparent 1px)",
//               backgroundSize: "60px 60px",
//             }}
//           />

//           {visible && startCoords && endCoords ? (
//             <div className="relative z-10 flex flex-col items-center gap-4">
//               <div className="flex items-center gap-8">
//                 <div className="flex flex-col items-center gap-1.5">
//                   <div className="w-3 h-3 rounded-full bg-primary shadow-lg shadow-primary/40" />
//                   <span className="text-xs text-muted-foreground">Start</span>
//                 </div>
//                 <div className="w-32 sm:w-48 h-px bg-gradient-to-r from-primary via-primary/50 to-accent relative">
//                   <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-primary/60 animate-subtle-pulse" />
//                 </div>
//                 <div className="flex flex-col items-center gap-1.5">
//                   <div className="w-3 h-3 rounded-full bg-accent shadow-lg shadow-accent/40" />
//                   <span className="text-xs text-muted-foreground">End</span>
//                 </div>
//               </div>
//               <p className="text-xs text-muted-foreground mt-2">Leaflet map integration ready</p>
//             </div>
//           ) : (
//             <p className="text-sm text-muted-foreground z-10">
//               Run optimization to visualize the route
//             </p>
//           )}
//         </div>
//       </div>
//     </section>
//   );
// };

// export default MapSection;
// import { MapPin } from "lucide-react";
// // import { MapContainer, TileLayer, Marker, Polyline, Popup } from "react-leaflet";
// import L from "leaflet";
// import "leaflet/dist/leaflet.css";
// import { MapContainer, TileLayer, Marker, Polyline, Popup } from "react-leaflet";

// interface RoutePoint {
//   lat: number;
//   lon: number;
// }

// interface MapSectionProps {
//   baselineRoute?: RoutePoint[];
//   optimizedRoute?: RoutePoint[];
//   visible: boolean;
// }
// // interface MapSectionProps {
// //   startCoords: { lat: number; lon: number } | null;
// //   endCoords: { lat: number; lon: number } | null;
// //   visible: boolean;
// // }

// const startIcon = new L.Icon({
//   iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
//   shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
//   iconSize: [25, 41],
//   iconAnchor: [12, 41],
// });

// const MapSection = ({ startCoords, endCoords, visible }: MapSectionProps) => {
//   if (!visible || !startCoords || !endCoords) {
//     return (
//       <section className="py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
//         <div className="glass-card p-6 text-center text-muted-foreground">
//           Run optimization to visualize the route
//         </div>
//       </section>
//     );
//   }

//   const center = [
//     (startCoords.lat + endCoords.lat) / 2,
//     (startCoords.lon + endCoords.lon) / 2,
//   ];

//   const routePositions: [number, number][] = [
//     [startCoords.lat, startCoords.lon],
//     [endCoords.lat, endCoords.lon],
//   ];

//   return (
//     <section className="py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
//       <div className="glass-card overflow-hidden">
//         <div className="p-5 border-b border-border/50 flex items-center justify-between">
//           <div className="flex items-center gap-2">
//             <MapPin className="w-4 h-4 text-primary" />
//             <span className="text-sm font-semibold text-foreground">
//               Route Visualization
//             </span>
//           </div>
//           <span className="text-xs text-muted-foreground">
//             {startCoords.lat.toFixed(2)}°, {startCoords.lon.toFixed(2)}° →{" "}
//             {endCoords.lat.toFixed(2)}°, {endCoords.lon.toFixed(2)}°
//           </span>
//         </div>

//         <div className="w-full aspect-[21/9] min-h-[400px]">
//           <MapContainer
//             center={center as [number, number]}
//             zoom={4}
//             style={{ height: "100%", width: "100%" }}
//             scrollWheelZoom={true}
//           >
//             <TileLayer
//               attribution="&copy; OpenStreetMap contributors"
//               url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
//             />

//             <Marker position={[startCoords.lat, startCoords.lon]} icon={startIcon}>
//               <Popup>Start Port</Popup>
//             </Marker>

//             <Marker position={[endCoords.lat, endCoords.lon]} icon={startIcon}>
//               <Popup>End Port</Popup>
//             </Marker>

//             <Polyline
//               positions={routePositions}
//               pathOptions={{ color: "#22d3ee", weight: 4 }}
//             />
//           </MapContainer>
//         </div>
//       </div>
//     </section>
//   );
// };

// export default MapSection;

import { MapPin } from "lucide-react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { MapContainer, TileLayer, Marker, Polyline, Popup } from "react-leaflet";

interface RoutePoint {
  lat: number;
  lon: number;
}

interface MapSectionProps {
  baselineRoute?: RoutePoint[];
  optimizedRoute?: RoutePoint[];
  visible: boolean;
}

const icon = new L.Icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

const MapSection = ({ baselineRoute, optimizedRoute, visible }: MapSectionProps) => {
  if (!visible || !baselineRoute || baselineRoute.length === 0) {
    return (
      <section className="py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="glass-card p-6 text-center text-muted-foreground">
          Run optimization to visualize the route
        </div>
      </section>
    );
  }

  const baselinePositions = baselineRoute.map(p => [p.lat, p.lon]) as [number, number][];
  const optimizedPositions = optimizedRoute?.map(p => [p.lat, p.lon]) as [number, number][];

  const center = baselinePositions[0];

  return (
    <section className="py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <div className="glass-card overflow-hidden">
        <div className="p-5 border-b border-border/50 flex items-center gap-2">
          <MapPin className="w-4 h-4 text-primary" />
          <span className="text-sm font-semibold text-foreground">
            Maritime Route Visualization
          </span>
        </div>

        <div className="w-full aspect-[21/9] min-h-[450px]">
          <MapContainer
            center={center}
            zoom={5}
            style={{ height: "100%", width: "100%" }}
            scrollWheelZoom={true}
          >
            {/* 🌊 Ocean Themed Dark Map */}
            <TileLayer
              url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
              attribution="&copy; OpenStreetMap & CartoDB"
            />

            {/* Start Marker */}
            <Marker position={baselinePositions[0]} icon={icon}>
              <Popup>Start Port</Popup>
            </Marker>

            {/* End Marker */}
            <Marker position={baselinePositions[baselinePositions.length - 1]} icon={icon}>
              <Popup>End Port</Popup>
            </Marker>

            {/* 🔴 Baseline Route */}
            <Polyline
              positions={baselinePositions}
              pathOptions={{ color: "#ef4444", weight: 4 }}
            />

            {/* 🟢 Optimized Route */}
            {optimizedPositions && (
              <Polyline
                positions={optimizedPositions}
                pathOptions={{ color: "#22c55e", weight: 5 }}
              />
            )}
          </MapContainer>
        </div>
      </div>
    </section>
  );
};

export default MapSection;