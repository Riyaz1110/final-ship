// import { useState, useCallback } from "react";
// import Navbar from "@/components/Navbar";
// import Footer from "@/components/Footer";
// import HeroSection, { RouteInput } from "@/components/HeroSection";
// import KPICards from "@/components/KPICards";
// import MapSection from "@/components/MapSection";
// import AISummaryPanel from "@/components/AISummaryPanel";

// interface OptimizationResult {
//   fuelSaved: number;
//   co2Reduction: number;
//   timeSaved: number;
//   distanceRerouted: number;
//   summary: string;
// }

// const Index = () => {
//   const [result, setResult] = useState<OptimizationResult | null>(null);
//   const [isOptimizing, setIsOptimizing] = useState(false);
//   const [coords, setCoords] = useState<{
//     start: { lat: number; lon: number };
//     end: { lat: number; lon: number };
//   } | null>(null);

//   const handleOptimize = useCallback(async (input: RouteInput) => {
//     setIsOptimizing(true);
//     setResult(null);

//     const start = { lat: parseFloat(input.startLat), lon: parseFloat(input.startLon) };
//     const end = { lat: parseFloat(input.endLat), lon: parseFloat(input.endLon) };
//     setCoords({ start, end });

//     // Prepare payload for future API integration
//     const _payload = {
//       voyage: {
//         start_port: { lat: start.lat, lon: start.lon },
//         end_port: { lat: end.lat, lon: end.lon },
//       },
//     };

//     // Simulate API call — replace with POST /optimize
//     await new Promise((resolve) => setTimeout(resolve, 2200));

//     // Simulated result — replace with API response
//     const latDiff = Math.abs(start.lat - end.lat);
//     const lonDiff = Math.abs(start.lon - end.lon);
//     const distance = Math.sqrt(latDiff ** 2 + lonDiff ** 2) * 60;

//     setResult({
//       fuelSaved: 8.2 + Math.random() * 6,
//       co2Reduction: 12.5 + distance * 0.15,
//       timeSaved: 2.4 + Math.random() * 3,
//       distanceRerouted: Math.round(distance * 0.12 + Math.random() * 20),
//       summary: `AI rerouted the vessel from ${start.lat.toFixed(2)}°N, ${start.lon.toFixed(2)}°E to ${end.lat.toFixed(2)}°N, ${end.lon.toFixed(2)}°E, avoiding a high-pressure weather system. The optimized path reduces fuel consumption by leveraging favorable ocean currents while maintaining arrival schedule stability. Wind resistance along the original corridor was 23% above threshold, prompting a ${Math.round(distance * 0.12)}nm diversion through calmer waters.`,
//     });

//     setIsOptimizing(false);
//   }, []);

//   return (
//     <div className="min-h-screen ocean-gradient flex flex-col">
//       <Navbar />
//       <main className="flex-1">
//         <HeroSection onOptimize={handleOptimize} isOptimizing={isOptimizing} />
//         <div className="section-divider max-w-7xl mx-auto" />
//         <KPICards
//           data={result ? {
//             fuelSaved: result.fuelSaved,
//             co2Reduction: result.co2Reduction,
//             timeSaved: result.timeSaved,
//             distanceRerouted: result.distanceRerouted,
//           } : null}
//           visible={!!result}
//         />
//         <MapSection
//           startCoords={coords?.start ?? null}
//           endCoords={coords?.end ?? null}
//           visible={!!result}
//         />
//         <AISummaryPanel summary={result?.summary ?? null} visible={!!result} />
//       </main>
//       <Footer />
//     </div>
//   );
// };

// export default Index;


// import { useState, useCallback } from "react";
// import axios from "axios";
// import Navbar from "@/components/Navbar";
// import Footer from "@/components/Footer";
// import HeroSection, { RouteInput } from "@/components/HeroSection";
// import KPICards from "@/components/KPICards";
// import MapSection from "@/components/MapSection";
// import AISummaryPanel from "@/components/AISummaryPanel";

// interface OptimizationResult {
//   fuelSaved: number;
//   co2Reduction: number;
//   timeSaved: number;
//   distanceRerouted: number;
//   summary: string;
// }

// const Index = () => {
//   const [result, setResult] = useState<OptimizationResult | null>(null);
//   const [isOptimizing, setIsOptimizing] = useState(false);
//   const [coords, setCoords] = useState<{
//     start: { lat: number; lon: number };
//     end: { lat: number; lon: number };
//   } | null>(null);

//   const handleOptimize = useCallback(async (input: RouteInput) => {
//     try {
//       setIsOptimizing(true);
//       setResult(null);

//       const start = {
//         lat: parseFloat(input.startLat),
//         lon: parseFloat(input.startLon),
//       };

//       const end = {
//         lat: parseFloat(input.endLat),
//         lon: parseFloat(input.endLon),
//       };

//       setCoords({ start, end });

//       const response = await axios.post("http://localhost:8000/optimize", {
//         voyage: {
//           start_port: { lat: start.lat, lon: start.lon },
//           end_port: { lat: end.lat, lon: end.lon },
//         },
//       });

//       const data = response.data;

//       setResult({
//         fuelSaved: parseFloat(
//           data["Optimized Route Generated"].match(/([\d.]+)%/)?.[1] || "0"
//         ),
//         co2Reduction: parseFloat(
//           data["Emissions Report"].match(/([\d.]+)/)?.[1] || "0"
//         ),
//         timeSaved: parseFloat(
//           data["Operational Insight"].match(/±([\d.]+)/)?.[1] || "0"
//         ),
//         distanceRerouted: parseFloat(
//           data["Weather Impact Adjustment"].match(/([\d.]+) nautical/)?.[1] ||
//             "0"
//         ),
//         summary:
//           data["Optimized Route Generated"] +
//           " " +
//           data["Weather Impact Adjustment"] +
//           " " +
//           data["Emissions Report"] +
//           " " +
//           data["Operational Insight"],
//       });
//     } catch (error) {
//       console.error("Optimization failed:", error);
//       alert("Backend connection failed. Make sure FastAPI is running.");
//     } finally {
//       setIsOptimizing(false);
//     }
//   }, []);

//   return (
//     <div className="min-h-screen ocean-gradient flex flex-col">
//       <Navbar />
//       <main className="flex-1">
//         <HeroSection onOptimize={handleOptimize} isOptimizing={isOptimizing} />
//         <div className="section-divider max-w-7xl mx-auto" />
//         <KPICards
//           data={
//             result
//               ? {
//                   fuelSaved: result.fuelSaved,
//                   co2Reduction: result.co2Reduction,
//                   timeSaved: result.timeSaved,
//                   distanceRerouted: result.distanceRerouted,
//                 }
//               : null
//           }
//           visible={!!result}
//         />
//         <MapSection
//           startCoords={coords?.start ?? null}
//           endCoords={coords?.end ?? null}
//           visible={!!result}
//         />
//         <AISummaryPanel summary={result?.summary ?? null} visible={!!result} />
//       </main>
//       <Footer />
//     </div>
//   );
// };

// export default Index;






// import { useState, useCallback } from "react";
// import axios from "axios";
// import Navbar from "@/components/Navbar";
// import Footer from "@/components/Footer";
// import HeroSection, { RouteInput } from "@/components/HeroSection";
// import KPICards from "@/components/KPICards";
// import MapSection from "@/components/MapSection";
// import AISummaryPanel from "@/components/AISummaryPanel";
// import { useOptimization } from "@/context/OptimizationContext";
// interface OptimizationResult {
//   fuelSaved: number;
//   co2Reduction: number;
//   timeSaved: number;
//   distanceRerouted: number;
//   summary: string;
// }

// const Index = () => {
//   const [result, setResult] = useState<OptimizationResult | null>(null);
//   const [isOptimizing, setIsOptimizing] = useState(false);
//   const { setData } = useOptimization();
//   const [coords, setCoords] = useState<{
//     start: { lat: number; lon: number };
//     end: { lat: number; lon: number };
//   } | null>(null);

//   // const handleOptimize = useCallback(async (input: RouteInput) => {
//   //   try {
//   //     setIsOptimizing(true);
//   //     setResult(null);

//   //     const start = {
//   //       lat: parseFloat(input.startLat),
//   //       lon: parseFloat(input.startLon),
//   //     };

//   //     const end = {
//   //       lat: parseFloat(input.endLat),
//   //       lon: parseFloat(input.endLon),
//   //     };

//   //     setCoords({ start, end });

//   //     // const response = await axios.post("http://localhost:8000/optimize", {
//   //     axios.post(`${import.meta.env.VITE_API_URL}/optimize`, {
//   //       voyage: {
//   //         start_port: { lat: start.lat, lon: start.lon },
//   //         end_port: { lat: end.lat, lon: end.lon },
//   //       },
//   //     });

//   //     const data = response.data;

//   //     setResult({
//   //       fuelSaved: data.fuel_reduction_percent,
//   //       co2Reduction: data.co2_reduction_tons,
//   //       timeSaved: data.time_difference_hours,
//   //       distanceRerouted: data.rerouted_distance_nm,
//   //       summary: `Baseline Distance: ${data.baseline_distance_nm} nm | Optimized Distance: ${data.optimized_distance_nm} nm`,
//   //     });
//   //   } catch (error) {
//   //     console.error(error);
//   //     alert("Backend connection failed.");
//   //   } finally {
//   //     setIsOptimizing(false);
//   //   }
//   // }, []);
//   const handleOptimize = useCallback(async (input: RouteInput) => {
//   try {
//     setIsOptimizing(true);
//     setResult(null);

//     const start = {
//       lat: parseFloat(input.startLat),
//       lon: parseFloat(input.startLon),
//     };

//     const end = {
//       lat: parseFloat(input.endLat),
//       lon: parseFloat(input.endLon),
//     };

//     setCoords({ start, end });

//     const response = await axios.post(
//       `${import.meta.env.VITE_API_URL}/optimize`,
//       {
//         voyage: {
//           start_port: { lat: start.lat, lon: start.lon },
//           end_port: { lat: end.lat, lon: end.lon },
//         },
//       }
//     );

//     const data = response.data;

//     setData({
//   fuelSaved: data.fuel_reduction_percent,
//   co2Reduction: data.co2_reduction_tons,
//   timeSaved: data.time_difference_hours,
//   distanceRerouted: data.rerouted_distance_nm,
//   baselineDistance: data.baseline_distance_nm,
//   optimizedDistance: data.optimized_distance_nm,
//   start,
//   end,
// });
//   } catch (error) {
//     console.error(error);
//     alert("Backend connection failed.");
//   } finally {
//     setIsOptimizing(false);
//   }
// }, []);

//   return (
//     <div className="min-h-screen ocean-gradient flex flex-col">
//       <Navbar />
//       <main className="flex-1">
//         <HeroSection onOptimize={handleOptimize} isOptimizing={isOptimizing} />
//         <div className="section-divider max-w-7xl mx-auto" />
//         <KPICards
//           data={result ? {
//             fuelSaved: result.fuelSaved,
//             co2Reduction: result.co2Reduction,
//             timeSaved: result.timeSaved,
//             distanceRerouted: result.distanceRerouted,
//           } : null}
//           visible={!!result}
//         />
//         <MapSection
//           startCoords={coords?.start ?? null}
//           endCoords={coords?.end ?? null}
//           visible={!!result}
//         />
//         <AISummaryPanel summary={result?.summary ?? null} visible={!!result} />
//       </main>
//       <Footer />
//     </div>
//   );
// };

// export default Index;
// import { useState, useCallback } from "react";
// import axios from "axios";
// import Navbar from "@/components/Navbar";
// import Footer from "@/components/Footer";
// import HeroSection, { RouteInput } from "@/components/HeroSection";
// import KPICards from "@/components/KPICards";
// import MapSection from "@/components/MapSection";
// import AISummaryPanel from "@/components/AISummaryPanel";
// import { useOptimization } from "@/context/OptimizationContext";

// const Index = () => {
//   const [isOptimizing, setIsOptimizing] = useState(false);
//   const { data, setData } = useOptimization();

//   const handleOptimize = useCallback(async (input: RouteInput) => {
//     try {
//       setIsOptimizing(true);

//       const start = {
//         lat: parseFloat(input.startLat),
//         lon: parseFloat(input.startLon),
//       };

//       const end = {
//         lat: parseFloat(input.endLat),
//         lon: parseFloat(input.endLon),
//       };

//       const response = await axios.post(
//         `${import.meta.env.VITE_API_URL}/optimize`,
//         {
//           voyage: {
//             start_port: start,
//             end_port: end,
//           },
//         }
//       );

//       const res = response.data;

//       setData({
//         fuelSaved: res.fuel_reduction_percent,
//         co2Reduction: res.co2_reduction_tons,
//         timeSaved: res.time_difference_hours,
//         distanceRerouted: res.rerouted_distance_nm,
//         baselineDistance: res.baseline_distance_nm,
//         optimizedDistance: res.optimized_distance_nm,
//         start,
//         end,
//       });

//     } catch (error) {
//       console.error(error);
//       alert("Backend connection failed.");
//     } finally {
//       setIsOptimizing(false);
//     }
//   }, []);

//   return (
//     <div className="min-h-screen ocean-gradient flex flex-col">
//       <Navbar />
//       <main className="flex-1">
//         <HeroSection onOptimize={handleOptimize} isOptimizing={isOptimizing} />

//         <div className="section-divider max-w-7xl mx-auto" />

//         <KPICards
//           data={data}
//           visible={!!data}
//         />

//         <MapSection
//           startCoords={data?.start ?? null}
//           endCoords={data?.end ?? null}
//           visible={!!data}
//         />

//         <AISummaryPanel
//           summary={
//             data
//               ? `Baseline Distance: ${data.baselineDistance} nm | Optimized Distance: ${data.optimizedDistance} nm`
//               : null
//           }
//           visible={!!data}
//         />
//       </main>
//       <Footer />
//     </div>
//   );
// };

// export default Index;
// import { useState, useCallback, useEffect } from "react";
// import axios from "axios";
// import Navbar from "@/components/Navbar";
// import Footer from "@/components/Footer";
// import HeroSection, { RouteInput } from "@/components/HeroSection";
// import KPICards from "@/components/KPICards";
// import MapSection from "@/components/MapSection";
// import AISummaryPanel from "@/components/AISummaryPanel";
// import { useOptimization } from "@/context/OptimizationContext";

// const Index = () => {
//   const [isOptimizing, setIsOptimizing] = useState(false);
//   const { data, setData } = useOptimization();

//   // ✅ OPTION 2: Clear stored optimization ONLY when Home loads
//   useEffect(() => {
//     localStorage.removeItem("optimizationData");
//   }, []);

//   const handleOptimize = useCallback(
//     async (input: RouteInput) => {
//       try {
//         setIsOptimizing(true);

//         const start = {
//           lat: parseFloat(input.startLat),
//           lon: parseFloat(input.startLon),
//         };

//         const end = {
//           lat: parseFloat(input.endLat),
//           lon: parseFloat(input.endLon),
//         };

//         const response = await axios.post(
//           `${import.meta.env.VITE_API_URL}/optimize`,
//           {
//             voyage: {
//               start_port: start,
//               end_port: end,
//             },
//           }
//         );

//         const res = response.data;

//         setData({
//           fuelSaved: res.fuel_reduction_percent,
//           co2Reduction: res.co2_reduction_tons,
//           timeSaved: res.time_difference_hours,
//           distanceRerouted: res.rerouted_distance_nm,
//           baselineDistance: res.baseline_distance_nm,
//           optimizedDistance: res.optimized_distance_nm,
//           start,
//           end,
//         });
//       } catch (error) {
//         console.error(error);
//         alert("Backend connection failed.");
//       } finally {
//         setIsOptimizing(false);
//       }
//     },
//     [setData]
//   );

//   return (
//     <div className="min-h-screen ocean-gradient flex flex-col">
//       <Navbar />
//       <main className="flex-1">
//         <HeroSection onOptimize={handleOptimize} isOptimizing={isOptimizing} />

//         <div className="section-divider max-w-7xl mx-auto" />

//         <KPICards data={data} visible={!!data} />

//         <MapSection
//           startCoords={data?.start ?? null}
//           endCoords={data?.end ?? null}
//           visible={!!data}
//         />

//         <AISummaryPanel
//           summary={
//             data
//               ? `Baseline Distance: ${data.baselineDistance} nm | Optimized Distance: ${data.optimizedDistance} nm`
//               : null
//           }
//           visible={!!data}
//         />
//       </main>
//       <Footer />
//     </div>
//   );
// };

// export default Index;
// import { useState, useCallback } from "react";
// import axios from "axios";
// import Navbar from "@/components/Navbar";
// import Footer from "@/components/Footer";
// import HeroSection, { RouteInput } from "@/components/HeroSection";
// import KPICards from "@/components/KPICards";
// import MapSection from "@/components/MapSection";
// import AISummaryPanel from "@/components/AISummaryPanel";
// import { useOptimization } from "@/context/OptimizationContext";

// const Index = () => {
//   const [isOptimizing, setIsOptimizing] = useState(false);
//   const { data, setData } = useOptimization();

//   const handleOptimize = useCallback(
//     async (input: RouteInput) => {
//       try {
//         setIsOptimizing(true);

//         const start = {
//           lat: parseFloat(input.startLat),
//           lon: parseFloat(input.startLon),
//         };

//         const end = {
//           lat: parseFloat(input.endLat),
//           lon: parseFloat(input.endLon),
//         };

//         const response = await axios.post(
//           `${import.meta.env.VITE_API_URL}/optimize`,
//           {
//             voyage: {
//               start_port: start,
//               end_port: end,
//             },
//           }
//         );

//         const res = response.data;

//         // 🔥 Correct mapping for NEW backend keys
//         setData({
//           fuelSaved: res["Fuel Reduction (%)"],
//           co2Reduction: res["CO2 Reduction (tons)"],
//           timeSaved: res["Time Difference (hours)"],
//           distanceRerouted: res["Route Adjustment (NM)"],
//           baselineDistance: res["Baseline Distance (NM)"],
//           optimizedDistance: res["Optimized Distance (NM)"],
//           start,
//           end,
//         });

//       } catch (error) {
//         console.error(error);
//         alert("Backend connection failed.");
//       } finally {
//         setIsOptimizing(false);
//       }
//     },
//     [setData]
//   );

//   return (
//     <div className="min-h-screen ocean-gradient flex flex-col">
//       <Navbar />
//       <main className="flex-1">
//         <HeroSection onOptimize={handleOptimize} isOptimizing={isOptimizing} />

//         <div className="section-divider max-w-7xl mx-auto" />

//         <KPICards data={data} visible={!!data} />

//         <MapSection
//           startCoords={data?.start ?? null}
//           endCoords={data?.end ?? null}
//           visible={!!data}
//         />

//         <AISummaryPanel
//           summary={
//             data
//               ? `Baseline Distance: ${data.baselineDistance} nm | Optimized Distance: ${data.optimizedDistance} nm`
//               : null
//           }
//           visible={!!data}
//         />
//       </main>
//       <Footer />
//     </div>
//   );
// };

// export default Index;
import { useState, useCallback } from "react";
import axios from "axios";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import HeroSection, { RouteInput } from "@/components/HeroSection";
import KPICards from "@/components/KPICards";
import MapSection from "@/components/MapSection";
import AISummaryPanel from "@/components/AISummaryPanel";
import { useOptimization } from "@/context/OptimizationContext";

const Index = () => {
  const [isOptimizing, setIsOptimizing] = useState(false);
  const { data, setData } = useOptimization();

  const handleOptimize = useCallback(
    async (input: RouteInput) => {
      try {
        setIsOptimizing(true);

        const start = {
          lat: parseFloat(input.startLat),
          lon: parseFloat(input.startLon),
        };

        const end = {
          lat: parseFloat(input.endLat),
          lon: parseFloat(input.endLon),
        };

        const response = await axios.post(
          `${import.meta.env.VITE_API_URL}/optimize`,
          {
            voyage: {
              start_port: start,
              end_port: end,
            },
          }
        );

        const res = response.data;

        // ✅ CORRECT mapping for snake_case backend
        setData({
          fuelSaved: res.fuel_reduction_percent,
          co2Reduction: res.co2_reduction_tons,
          timeSaved: res.time_difference_hours,
          distanceRerouted: res.rerouted_distance_nm,
          baselineDistance: res.baseline_distance_nm,
          optimizedDistance: res.optimized_distance_nm,
          baselineRoute: res.baseline_route,
          optimizedRoute: res.optimized_route,
        });

      } catch (error) {
        console.error(error);
        alert("Backend connection failed.");
      } finally {
        setIsOptimizing(false);
      }
    },
    [setData]
  );

  return (
    <div className="min-h-screen ocean-gradient flex flex-col">
      <Navbar />
      <main className="flex-1">
        <HeroSection onOptimize={handleOptimize} isOptimizing={isOptimizing} />

        <div className="section-divider max-w-7xl mx-auto" />

        <KPICards data={data} visible={!!data} />

        <MapSection
        baselineRoute={data?.baselineRoute}
        optimizedRoute={data?.optimizedRoute}
        visible={!!data}
      />
        <AISummaryPanel
          summary={
            data
              ? `Baseline Distance: ${data.baselineDistance} nm | Optimized Distance: ${data.optimizedDistance} nm`
              : null
          }
          visible={!!data}
        />
      </main>
      <Footer />
    </div>
  );
};

export default Index;