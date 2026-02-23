# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import numpy as np
# import requests
# import math
# import joblib
# import os
# from datetime import datetime
# from sklearn.linear_model import LinearRegression

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# EMISSION_FACTOR = 3.114
# SPEED_KNOTS = 20
# MODEL_PATH = "fuel_model.pkl"

# # -------------------------
# # Request Models
# # -------------------------

# class Port(BaseModel):
#     lat: float
#     lon: float

# class Voyage(BaseModel):
#     start_port: Port
#     end_port: Port

# class OptimizationRequest(BaseModel):
#     voyage: Voyage

# # -------------------------
# # Haversine Distance
# # -------------------------

# def haversine(lat1, lon1, lat2, lon2):
#     R = 6371
#     phi1 = math.radians(lat1)
#     phi2 = math.radians(lat2)
#     dphi = math.radians(lat2 - lat1)
#     dlambda = math.radians(lon2 - lon1)

#     a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

#     distance_km = R * c
#     return distance_km * 0.539957

# # -------------------------
# # Live Weather Fetch
# # -------------------------

# def fetch_live_wind(lat, lon):
#     try:
#         url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
#         response = requests.get(url, timeout=5)
#         data = response.json()
#         return data["current_weather"]["windspeed"]
#     except:
#         return 12

# def fetch_wave_height():
#     return float(np.random.uniform(1, 4))

# def fetch_ocean_current():
#     return float(np.random.uniform(0.5, 2.0))

# # -------------------------
# # ML Model
# # -------------------------

# def train_model():
#     np.random.seed(42)
#     samples = 600

#     distance = np.random.uniform(100, 5000, samples)
#     wind = np.random.uniform(0, 25, samples)
#     current = np.random.uniform(0, 3, samples)
#     wave = np.random.uniform(0, 6, samples)
#     time = distance / 20

#     fuel = (
#         0.04 * distance +
#         0.7 * wind -
#         0.5 * current +
#         0.8 * wave +
#         0.02 * time +
#         np.random.normal(0, 5, samples)
#     )

#     X = np.column_stack((distance, wind, current, wave, time))
#     y = fuel

#     model = LinearRegression()
#     model.fit(X, y)

#     joblib.dump(model, MODEL_PATH)

# def load_model():
#     if not os.path.exists(MODEL_PATH):
#         train_model()
#     return joblib.load(MODEL_PATH)

# def predict_fuel(distance_nm, wind, current, wave):
#     model = load_model()
#     voyage_hours = distance_nm / SPEED_KNOTS
#     X = np.array([[distance_nm, wind, current, wave, voyage_hours]])
#     fuel = float(model.predict(X)[0])
#     if fuel < 0:
#         fuel = abs(fuel)
#     co2 = fuel * EMISSION_FACTOR
#     return fuel, co2, voyage_hours

# # -------------------------
# # Optimization Endpoint
# # -------------------------

# @app.post("/optimize")
# def optimize_route(data: OptimizationRequest):

#     lat1 = data.voyage.start_port.lat
#     lon1 = data.voyage.start_port.lon
#     lat2 = data.voyage.end_port.lat
#     lon2 = data.voyage.end_port.lon

#     baseline_distance = haversine(lat1, lon1, lat2, lon2)

#     wind = fetch_live_wind(lat1, lon1)
#     current = fetch_ocean_current()
#     wave = fetch_wave_height()

#     safety_penalty = 0.05 if wave > 3 else 0

#     optimized_distance = baseline_distance * (
#         1 + safety_penalty + (wave * 0.02) - (current * 0.03)
#     )

#     fuel_base, co2_base, time_base = predict_fuel(baseline_distance, wind, current, wave)
#     fuel_opt, co2_opt, time_opt = predict_fuel(optimized_distance, wind, current, wave)

#     fuel_reduction = ((fuel_base - fuel_opt) / fuel_base) * 100
#     co2_reduction = co2_base - co2_opt
#     time_diff = abs(time_base - time_opt)
#     reroute_nm = abs(baseline_distance - optimized_distance)

#     return {
#         "Optimized Route Generated":
#             f"Fuel consumption reduced by {round(fuel_reduction,2)}% compared to shortest-path navigation.",
#         "Weather Impact Adjustment":
#             f"Strong headwinds avoided by rerouting {round(reroute_nm,1)} nautical miles south.",
#         "Emissions Report":
#             f"Estimated CO2 reduction — {round(co2_reduction,2)} tons for this voyage.",
#         "Operational Insight":
#             f"Arrival time maintained within ±{round(time_diff,2)} hours while improving fuel efficiency.",
#         "Data Timestamp": str(datetime.utcnow())
#     }
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import numpy as np
# import requests
# import math
# import joblib
# import os
# from datetime import datetime
# from sklearn.linear_model import LinearRegression

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# EMISSION_FACTOR = 3.114
# SPEED_KNOTS = 20
# MODEL_PATH = "fuel_model.pkl"

# class Port(BaseModel):
#     lat: float
#     lon: float

# class Voyage(BaseModel):
#     start_port: Port
#     end_port: Port

# class OptimizationRequest(BaseModel):
#     voyage: Voyage

# def haversine(lat1, lon1, lat2, lon2):
#     R = 6371
#     phi1 = math.radians(lat1)
#     phi2 = math.radians(lat2)
#     dphi = math.radians(lat2 - lat1)
#     dlambda = math.radians(lon2 - lon1)
#     a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#     distance_km = R * c
#     return distance_km * 0.539957

# def fetch_live_wind(lat, lon):
#     try:
#         url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
#         response = requests.get(url, timeout=5)
#         data = response.json()
#         return data["current_weather"]["windspeed"]
#     except:
#         return 12

# # def fetch_wave_height():
# #     return float(np.random.uniform(1, 4))

# # def fetch_ocean_current():
# #     return float(np.random.uniform(0.5, 2.0))
# def fetch_wave_height(lat, lon):
#     return round(abs(math.sin(lat)) * 2 + 1.5, 2)

# def fetch_ocean_current(lat, lon):
#     return round(abs(math.cos(lon)) * 1.5 + 0.5, 2)

# def train_model():
#     np.random.seed(42)
#     samples = 600
#     distance = np.random.uniform(100, 5000, samples)
#     wind = np.random.uniform(0, 25, samples)
#     current = np.random.uniform(0, 3, samples)
#     wave = np.random.uniform(0, 6, samples)
#     time = distance / 20

#     fuel = (
#         0.04 * distance +
#         0.7 * wind -
#         0.5 * current +
#         0.8 * wave +
#         0.02 * time +
#         np.random.normal(0, 5, samples)
#     )

#     X = np.column_stack((distance, wind, current, wave, time))
#     y = fuel

#     model = LinearRegression()
#     model.fit(X, y)
#     joblib.dump(model, MODEL_PATH)

# def load_model():
#     if not os.path.exists(MODEL_PATH):
#         train_model()
#     return joblib.load(MODEL_PATH)

# def predict_fuel(distance_nm, wind, current, wave):
#     model = load_model()
#     voyage_hours = distance_nm / SPEED_KNOTS
#     X = np.array([[distance_nm, wind, current, wave, voyage_hours]])
#     fuel = float(model.predict(X)[0])
#     fuel = abs(fuel)
#     co2 = fuel * EMISSION_FACTOR
#     return fuel, co2, voyage_hours

# @app.post("/optimize")
# def optimize_route(data: OptimizationRequest):

#     lat1 = data.voyage.start_port.lat
#     lon1 = data.voyage.start_port.lon
#     lat2 = data.voyage.end_port.lat
#     lon2 = data.voyage.end_port.lon

#     baseline_distance = haversine(lat1, lon1, lat2, lon2)

#     wind = fetch_live_wind(lat1, lon1)
#     current = fetch_ocean_current(lat1, lon1)
#     wave = fetch_wave_height(lat1, lon1)

#     safety_penalty = 0.05 if wave > 3 else 0

#     optimized_distance = baseline_distance * (
#         1 + safety_penalty + (wave * 0.02) - (current * 0.03)
#     )

#     fuel_base, co2_base, time_base = predict_fuel(baseline_distance, wind, current, wave)
#     fuel_opt, co2_opt, time_opt = predict_fuel(optimized_distance, wind, current, wave)

#     fuel_difference = fuel_base - fuel_opt
#     co2_difference = co2_base - co2_opt

#     fuel_reduction_percent = (fuel_difference / fuel_base) * 100

#     return {
#         "baseline_distance_nm": round(baseline_distance, 2),
#         "optimized_distance_nm": round(optimized_distance, 2),
#         "rerouted_distance_nm": round(abs(baseline_distance - optimized_distance), 2),
#         "fuel_reduction_percent": round(fuel_reduction_percent, 2),
#         "co2_reduction_tons": round(co2_difference, 2),
#         "time_difference_hours": round(abs(time_base - time_opt), 2),
#         "timestamp": str(datetime.utcnow())
#     }
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import numpy as np
# import requests
# import math
# import joblib
# import os
# from datetime import datetime
# from sklearn.linear_model import LinearRegression

# app = FastAPI(title="AI Marine Route Optimizer - Real Time")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # -------------------------
# # Constants
# # -------------------------

# EMISSION_FACTOR = 3.114
# SPEED_KNOTS = 20
# MODEL_PATH = "fuel_model.pkl"

# # -------------------------
# # Request Models
# # -------------------------

# class Port(BaseModel):
#     lat: float
#     lon: float

# class Voyage(BaseModel):
#     start_port: Port
#     end_port: Port

# class OptimizationRequest(BaseModel):
#     voyage: Voyage

# # -------------------------
# # Distance Calculation
# # -------------------------

# def haversine(lat1, lon1, lat2, lon2):
#     R = 6371
#     phi1 = math.radians(lat1)
#     phi2 = math.radians(lat2)
#     dphi = math.radians(lat2 - lat1)
#     dlambda = math.radians(lon2 - lon1)

#     a = math.sin(dphi / 2)**2 + \
#         math.cos(phi1) * math.cos(phi2) * \
#         math.sin(dlambda / 2)**2

#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#     return R * c * 0.539957  # nautical miles

# # -------------------------
# # Route Sampling
# # -------------------------

# def interpolate_points(lat1, lon1, lat2, lon2, steps=6):
#     lats = np.linspace(lat1, lat2, steps)
#     lons = np.linspace(lon1, lon2, steps)
#     return list(zip(lats, lons))

# # -------------------------
# # Safe Float
# # -------------------------

# def safe_float(value, default=0.0):
#     try:
#         if value is None:
#             return default
#         return float(value)
#     except:
#         return default

# # -------------------------
# # Real Marine Weather (Robust)
# # -------------------------

# def fetch_marine_weather(lat, lon):
#     try:
#         # Wind API
#         weather_url = (
#             f"https://api.open-meteo.com/v1/forecast"
#             f"?latitude={lat}&longitude={lon}&current_weather=true"
#         )

#         weather_res = requests.get(weather_url, timeout=8)
#         weather_res.raise_for_status()
#         weather_data = weather_res.json()

#         wind = weather_data.get("current_weather", {}).get("windspeed", 0)

#         # Marine API
#         marine_url = (
#             f"https://marine-api.open-meteo.com/v1/marine"
#             f"?latitude={lat}&longitude={lon}"
#             f"&hourly=wave_height,ocean_current_velocity"
#         )

#         marine_res = requests.get(marine_url, timeout=8)
#         marine_res.raise_for_status()
#         marine_data = marine_res.json()

#         hourly = marine_data.get("hourly", {})

#         wave = safe_float(hourly.get("wave_height", [0])[0])
#         current = safe_float(hourly.get("ocean_current_velocity", [0])[0])
#         wind = safe_float(wind)

#         return wind, current, wave

#     except requests.exceptions.Timeout:
#         return 5.0, 0.2, 0.5  # fallback safe values

#     except Exception:
#         return 5.0, 0.2, 0.5  # fallback safe values

# # -------------------------
# # ML Model Training
# # -------------------------

# def train_model():
#     np.random.seed(42)
#     samples = 800

#     distance = np.random.uniform(100, 6000, samples)
#     wind = np.random.uniform(0, 30, samples)
#     current = np.random.uniform(0, 3, samples)
#     wave = np.random.uniform(0, 6, samples)
#     time = distance / SPEED_KNOTS

#     fuel = (
#         0.045 * distance +
#         0.9 * wind +
#         1.2 * wave -
#         0.6 * current +
#         0.03 * time +
#         np.random.normal(0, 8, samples)
#     )

#     X = np.column_stack((distance, wind, current, wave, time))
#     y = fuel

#     model = LinearRegression()
#     model.fit(X, y)
#     joblib.dump(model, MODEL_PATH)

# if not os.path.exists(MODEL_PATH):
#     train_model()

# model = joblib.load(MODEL_PATH)

# def predict_fuel(distance_nm, wind, current, wave):
#     voyage_hours = distance_nm / SPEED_KNOTS
#     X = np.array([[distance_nm, wind, current, wave, voyage_hours]])
#     fuel = abs(float(model.predict(X)[0]))
#     co2 = fuel * EMISSION_FACTOR
#     return fuel, co2, voyage_hours

# # -------------------------
# # Optimization Endpoint
# # -------------------------

# @app.post("/optimize")
# async def optimize_route(data: OptimizationRequest):

#     lat1 = data.voyage.start_port.lat
#     lon1 = data.voyage.start_port.lon
#     lat2 = data.voyage.end_port.lat
#     lon2 = data.voyage.end_port.lon

#     baseline_distance = haversine(lat1, lon1, lat2, lon2)

#     route_points = interpolate_points(lat1, lon1, lat2, lon2)

#     winds, currents, waves = [], [], []

#     for lat, lon in route_points:
#         wind, current, wave = fetch_marine_weather(lat, lon)
#         winds.append(wind)
#         currents.append(current)
#         waves.append(wave)

#     avg_wind = float(np.mean(winds))
#     avg_current = float(np.mean(currents))
#     avg_wave = float(np.mean(waves))

#     # SMART rerouting logic
#     if avg_wave > 2.5 or avg_wind > 20:
#         weather_factor = (
#             1 +
#             (avg_wave * 0.04) +
#             (avg_wind * 0.005) -
#             (avg_current * 0.03)
#         )
#     else:
#         weather_factor = 1  # calm sea → no reroute

#     optimized_distance = baseline_distance * weather_factor

#     fuel_base, co2_base, time_base = predict_fuel(
#         baseline_distance, avg_wind, avg_current, avg_wave
#     )

#     fuel_opt, co2_opt, time_opt = predict_fuel(
#         optimized_distance, avg_wind, avg_current, avg_wave
#     )

#     fuel_reduction = (
#         ((fuel_base - fuel_opt) / fuel_base) * 100
#         if fuel_base != 0 else 0
#     )
#     # Prevent worse deployment
#     # if fuel_opt > fuel_base:
#     #     optimized_distance = baseline_distance
#     #     fuel_opt = fuel_base
#     #     co2_opt = co2_base
#     #     time_opt = time_base
#     #     fuel_reduction = 0

#     return {
#         "Baseline Distance (NM)": round(baseline_distance, 2),
#         "Optimized Distance (NM)": round(optimized_distance, 2),
#         "Fuel Reduction (%)": round(fuel_reduction, 2),
#         "CO2 Reduction (tons)": round(co2_base - co2_opt, 2),
#         "Time Difference (hours)": round(abs(time_base - time_opt), 2),
#         "Route Adjustment (NM)": round(abs(optimized_distance - baseline_distance), 2),
#         "Live Weather Summary": {
#             "Average Wind (km/h)": round(avg_wind, 2),
#             "Average Wave Height (m)": round(avg_wave, 2),
#             "Average Current (m/s)": round(avg_current, 2)
#         },
#         "Weather Condition":
#             "Rerouted (Rough Sea)" if weather_factor != 1 else "Direct Route (Calm Sea)",
#         "Timestamp (UTC)": datetime.utcnow().isoformat()
#     }
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import numpy as np
# import requests
# import math
# import joblib
# import os
# from datetime import datetime
# from sklearn.linear_model import LinearRegression

# app = FastAPI(title="AI Marine Route Optimizer - Real Time")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # -------------------------
# # Constants
# # -------------------------

# EMISSION_FACTOR = 3.114
# SPEED_KNOTS = 20
# MODEL_PATH = "fuel_model.pkl"

# # -------------------------
# # Request Models
# # -------------------------

# class Port(BaseModel):
#     lat: float
#     lon: float

# class Voyage(BaseModel):
#     start_port: Port
#     end_port: Port

# class OptimizationRequest(BaseModel):
#     voyage: Voyage

# # -------------------------
# # Distance Calculation
# # -------------------------

# def haversine(lat1, lon1, lat2, lon2):
#     R = 6371
#     phi1 = math.radians(lat1)
#     phi2 = math.radians(lat2)
#     dphi = math.radians(lat2 - lat1)
#     dlambda = math.radians(lon2 - lon1)

#     a = math.sin(dphi / 2)**2 + \
#         math.cos(phi1) * math.cos(phi2) * \
#         math.sin(dlambda / 2)**2

#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#     return R * c * 0.539957  # nautical miles

# # -------------------------
# # Route Sampling
# # -------------------------

# def interpolate_points(lat1, lon1, lat2, lon2, steps=6):
#     lats = np.linspace(lat1, lat2, steps)
#     lons = np.linspace(lon1, lon2, steps)
#     return list(zip(lats, lons))

# # -------------------------
# # Safe Float
# # -------------------------

# def safe_float(value, default=0.0):
#     try:
#         if value is None:
#             return default
#         return float(value)
#     except:
#         return default

# # -------------------------
# # Real Marine Weather (Robust)
# # -------------------------

# def fetch_marine_weather(lat, lon):
#     try:
#         # Wind API
#         weather_url = (
#             f"https://api.open-meteo.com/v1/forecast"
#             f"?latitude={lat}&longitude={lon}&current_weather=true"
#         )

#         weather_res = requests.get(weather_url, timeout=8)
#         weather_res.raise_for_status()
#         weather_data = weather_res.json()

#         wind = weather_data.get("current_weather", {}).get("windspeed", 0)

#         # Marine API
#         marine_url = (
#             f"https://marine-api.open-meteo.com/v1/marine"
#             f"?latitude={lat}&longitude={lon}"
#             f"&hourly=wave_height,ocean_current_velocity"
#         )

#         marine_res = requests.get(marine_url, timeout=8)
#         marine_res.raise_for_status()
#         marine_data = marine_res.json()

#         hourly = marine_data.get("hourly", {})

#         wave = safe_float(hourly.get("wave_height", [0])[0])
#         current = safe_float(hourly.get("ocean_current_velocity", [0])[0])
#         wind = safe_float(wind)

#         return wind, current, wave

#     except requests.exceptions.Timeout:
#         return 5.0, 0.2, 0.5  # fallback safe values

#     except Exception:
#         return 5.0, 0.2, 0.5  # fallback safe values

# # -------------------------
# # ML Model Training
# # -------------------------

# def train_model():
#     np.random.seed(42)
#     samples = 800

#     distance = np.random.uniform(100, 6000, samples)
#     wind = np.random.uniform(0, 30, samples)
#     current = np.random.uniform(0, 3, samples)
#     wave = np.random.uniform(0, 6, samples)
#     time = distance / SPEED_KNOTS

#     fuel = (
#         0.045 * distance +
#         0.9 * wind +
#         1.2 * wave -
#         0.6 * current +
#         0.03 * time +
#         np.random.normal(0, 8, samples)
#     )

#     X = np.column_stack((distance, wind, current, wave, time))
#     y = fuel

#     model = LinearRegression()
#     model.fit(X, y)
#     joblib.dump(model, MODEL_PATH)

# if not os.path.exists(MODEL_PATH):
#     train_model()

# model = joblib.load(MODEL_PATH)

# def predict_fuel(distance_nm, wind, current, wave):
#     voyage_hours = distance_nm / SPEED_KNOTS
#     X = np.array([[distance_nm, wind, current, wave, voyage_hours]])
#     fuel = abs(float(model.predict(X)[0]))
#     co2 = fuel * EMISSION_FACTOR
#     return fuel, co2, voyage_hours

# # -------------------------
# # Optimization Endpoint
# # -------------------------

# @app.post("/optimize")
# async def optimize_route(data: OptimizationRequest):

#     lat1 = data.voyage.start_port.lat
#     lon1 = data.voyage.start_port.lon
#     lat2 = data.voyage.end_port.lat
#     lon2 = data.voyage.end_port.lon

#     baseline_distance = haversine(lat1, lon1, lat2, lon2)

#     route_points = interpolate_points(lat1, lon1, lat2, lon2)

#     winds, currents, waves = [], [], []

#     for lat, lon in route_points:
#         wind, current, wave = fetch_marine_weather(lat, lon)
#         winds.append(wind)
#         currents.append(current)
#         waves.append(wave)

#     avg_wind = float(np.mean(winds))
#     avg_current = float(np.mean(currents))
#     avg_wave = float(np.mean(waves))

#     # SMART rerouting logic
#     if avg_wave > 2.5 or avg_wind > 20:
#         weather_factor = (
#             1 +
#             (avg_wave * 0.04) +
#             (avg_wind * 0.005) -
#             (avg_current * 0.03)
#         )
#     else:
#         weather_factor = 1  # calm sea → no reroute

#     optimized_distance = baseline_distance * weather_factor

#     fuel_base, co2_base, time_base = predict_fuel(
#         baseline_distance, avg_wind, avg_current, avg_wave
#     )

#     fuel_opt, co2_opt, time_opt = predict_fuel(
#         optimized_distance, avg_wind, avg_current, avg_wave
#     )

#     fuel_reduction = (
#         ((fuel_base - fuel_opt) / fuel_base) * 100
#         if fuel_base != 0 else 0
#     )
#     # Prevent worse deployment
#     # if fuel_opt > fuel_base:
#     #     optimized_distance = baseline_distance
#     #     fuel_opt = fuel_base
#     #     co2_opt = co2_base
#     #     time_opt = time_base
#     #     fuel_reduction = 0

#     return {
#         "Baseline Distance (NM)": round(baseline_distance, 2),
#         "Optimized Distance (NM)": round(optimized_distance, 2),
#         "Fuel Reduction (%)": round(fuel_reduction, 2),
#         "CO2 Reduction (tons)": round(co2_base - co2_opt, 2),
#         "Time Difference (hours)": round(abs(time_base - time_opt), 2),
#         "Route Adjustment (NM)": round(abs(optimized_distance - baseline_distance), 2),
#         "Live Weather Summary": {
#             "Average Wind (km/h)": round(avg_wind, 2),
#             "Average Wave Height (m)": round(avg_wave, 2),
#             "Average Current (m/s)": round(avg_current, 2)
#         },
#         "Weather Condition":
#             "Rerouted (Rough Sea)" if weather_factor != 1 else "Direct Route (Calm Sea)",
#         "Timestamp (UTC)": datetime.utcnow().isoformat()
#     }
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import numpy as np
# import requests
# import math
# import joblib
# import os
# from datetime import datetime
# from sklearn.linear_model import LinearRegression

# app = FastAPI(title="AI Marine Route Optimizer - Real Time")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # -------------------------
# # Constants
# # -------------------------

# EMISSION_FACTOR = 3.114
# SPEED_KNOTS = 20
# MODEL_PATH = "fuel_model.pkl"

# # -------------------------
# # Request Models
# # -------------------------

# class Port(BaseModel):
#     lat: float
#     lon: float

# class Voyage(BaseModel):
#     start_port: Port
#     end_port: Port

# class OptimizationRequest(BaseModel):
#     voyage: Voyage

# # -------------------------
# # Distance Calculation
# # -------------------------

# def haversine(lat1, lon1, lat2, lon2):
#     R = 6371
#     phi1 = math.radians(lat1)
#     phi2 = math.radians(lat2)
#     dphi = math.radians(lat2 - lat1)
#     dlambda = math.radians(lon2 - lon1)

#     a = math.sin(dphi / 2)**2 + \
#         math.cos(phi1) * math.cos(phi2) * \
#         math.sin(dlambda / 2)**2

#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#     return R * c * 0.539957  # nautical miles

# # -------------------------
# # Route Sampling
# # -------------------------

# def interpolate_points(lat1, lon1, lat2, lon2, steps=6):
#     lats = np.linspace(lat1, lat2, steps)
#     lons = np.linspace(lon1, lon2, steps)
#     return list(zip(lats, lons))

# # -------------------------
# # Safe Float
# # -------------------------

# def safe_float(value, default=0.0):
#     try:
#         if value is None:
#             return default
#         return float(value)
#     except:
#         return default

# # -------------------------
# # Real Marine Weather (Robust)
# # -------------------------

# def fetch_marine_weather(lat, lon):
#     try:
#         # Wind API
#         weather_url = (
#             f"https://api.open-meteo.com/v1/forecast"
#             f"?latitude={lat}&longitude={lon}&current_weather=true"
#         )

#         weather_res = requests.get(weather_url, timeout=8)
#         weather_res.raise_for_status()
#         weather_data = weather_res.json()

#         wind = weather_data.get("current_weather", {}).get("windspeed", 0)

#         # Marine API
#         marine_url = (
#             f"https://marine-api.open-meteo.com/v1/marine"
#             f"?latitude={lat}&longitude={lon}"
#             f"&hourly=wave_height,ocean_current_velocity"
#         )

#         marine_res = requests.get(marine_url, timeout=8)
#         marine_res.raise_for_status()
#         marine_data = marine_res.json()

#         hourly = marine_data.get("hourly", {})

#         wave = safe_float(hourly.get("wave_height", [0])[0])
#         current = safe_float(hourly.get("ocean_current_velocity", [0])[0])
#         wind = safe_float(wind)

#         return wind, current, wave

#     except requests.exceptions.Timeout:
#         return 5.0, 0.2, 0.5  # fallback safe values

#     except Exception:
#         return 5.0, 0.2, 0.5  # fallback safe values

# # -------------------------
# # ML Model Training
# # -------------------------

# def train_model():
#     np.random.seed(42)
#     samples = 800

#     distance = np.random.uniform(100, 6000, samples)
#     wind = np.random.uniform(0, 30, samples)
#     current = np.random.uniform(0, 3, samples)
#     wave = np.random.uniform(0, 6, samples)
#     time = distance / SPEED_KNOTS

#     fuel = (
#         0.045 * distance +
#         0.9 * wind +
#         1.2 * wave -
#         0.6 * current +
#         0.03 * time +
#         np.random.normal(0, 8, samples)
#     )

#     X = np.column_stack((distance, wind, current, wave, time))
#     y = fuel

#     model = LinearRegression()
#     model.fit(X, y)
#     joblib.dump(model, MODEL_PATH)

# if not os.path.exists(MODEL_PATH):
#     train_model()

# model = joblib.load(MODEL_PATH)

# def predict_fuel(distance_nm, wind, current, wave):
#     voyage_hours = distance_nm / SPEED_KNOTS
#     X = np.array([[distance_nm, wind, current, wave, voyage_hours]])
#     fuel = abs(float(model.predict(X)[0]))
#     co2 = fuel * EMISSION_FACTOR
#     return fuel, co2, voyage_hours

# # -------------------------
# # Optimization Endpoint
# # -------------------------

# @app.post("/optimize")
# async def optimize_route(data: OptimizationRequest):

#     lat1 = data.voyage.start_port.lat
#     lon1 = data.voyage.start_port.lon
#     lat2 = data.voyage.end_port.lat
#     lon2 = data.voyage.end_port.lon

#     baseline_distance = haversine(lat1, lon1, lat2, lon2)

#     route_points = interpolate_points(lat1, lon1, lat2, lon2)

#     winds, currents, waves = [], [], []

#     for lat, lon in route_points:
#         wind, current, wave = fetch_marine_weather(lat, lon)
#         winds.append(wind)
#         currents.append(current)
#         waves.append(wave)

#     avg_wind = float(np.mean(winds))
#     avg_current = float(np.mean(currents))
#     avg_wave = float(np.mean(waves))

#     # SMART rerouting logic
#     if avg_wave > 2.5 or avg_wind > 20:
#         weather_factor = (
#             1 +
#             (avg_wave * 0.04) +
#             (avg_wind * 0.005) -
#             (avg_current * 0.03)
#         )
#     else:
#         weather_factor = 1  # calm sea → no reroute

#     optimized_distance = baseline_distance * weather_factor

#     fuel_base, co2_base, time_base = predict_fuel(
#         baseline_distance, avg_wind, avg_current, avg_wave
#     )

#     fuel_opt, co2_opt, time_opt = predict_fuel(
#         optimized_distance, avg_wind, avg_current, avg_wave
#     )

#     fuel_reduction = (
#         ((fuel_base - fuel_opt) / fuel_base) * 100
#         if fuel_base != 0 else 0
#     )
#     # Prevent worse deployment
#     # if fuel_opt > fuel_base:
#     #     optimized_distance = baseline_distance
#     #     fuel_opt = fuel_base
#     #     co2_opt = co2_base
#     #     time_opt = time_base
#     #     fuel_reduction = 0
#     baseline_route = [
#         {"lat": lat1, "lon": lon1},
#         {"lat": lat2, "lon": lon2}
#     ]

#     optimized_route = [
#         {"lat": lat1, "lon": lon1},
#         {
#             "lat": lat2,
#             "lon": lon2 + (avg_wave * 0.3 if weather_factor != 1 else 0)
#         }
#     ]

#     return {
#     "baseline_distance_nm": round(baseline_distance, 2),
#     "optimized_distance_nm": round(optimized_distance, 2),
#     "fuel_reduction_percent": round(fuel_reduction, 2),
#     "co2_reduction_tons": round(co2_base - co2_opt, 2),
#     "time_difference_hours": round(abs(time_base - time_opt), 2),
#     "rerouted_distance_nm": round(abs(optimized_distance - baseline_distance), 2),

#     "baseline_route": baseline_route,
#     "optimized_route": optimized_route,

#     "weather": {
#         "avg_wind_kmh": round(avg_wind, 2),
#         "avg_wave_m": round(avg_wave, 2),
#         "avg_current_ms": round(avg_current, 2),
#         "condition": "rough" if weather_factor != 1 else "calm"
#     },
#     "timestamp": datetime.utcnow().isoformat()

# }
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import numpy as np
# import requests
# import math
# import joblib
# import os
# from datetime import datetime
# from sklearn.linear_model import LinearRegression

# app = FastAPI(title="AI Marine Route Optimizer - Real Time")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# EMISSION_FACTOR = 3.114
# SPEED_KNOTS = 20
# MODEL_PATH = "fuel_model.pkl"

# # -------------------------
# # Request Models
# # -------------------------

# class Port(BaseModel):
#     lat: float
#     lon: float

# class Voyage(BaseModel):
#     start_port: Port
#     end_port: Port

# class OptimizationRequest(BaseModel):
#     voyage: Voyage

# # -------------------------
# # Distance Calculation
# # -------------------------

# def haversine(lat1, lon1, lat2, lon2):
#     R = 6371
#     phi1 = math.radians(lat1)
#     phi2 = math.radians(lat2)
#     dphi = math.radians(lat2 - lat1)
#     dlambda = math.radians(lon2 - lon1)

#     a = math.sin(dphi / 2)**2 + \
#         math.cos(phi1) * math.cos(phi2) * \
#         math.sin(dlambda / 2)**2

#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#     return R * c * 0.539957

# # -------------------------
# # Smooth Maritime Curve
# # -------------------------

# # def generate_curve(lat1, lon1, lat2, lon2, curvature=0):
# #     points = []
# #     steps = 25
# #     for i in range(steps + 1):
# #         t = i / steps
# #         lat = lat1 + (lat2 - lat1) * t
# #         lon = lon1 + (lon2 - lon1) * t
# #         lon += curvature * math.sin(math.pi * t)
# #         points.append({"lat": lat, "lon": lon})
# #     return points
# def generate_curved_route(lat1, lon1, lat2, lon2, curvature=0.5, points=25):
#     route = []
#     for i in range(points + 1):
#         t = i / points

#         lat = lat1 + (lat2 - lat1) * t
#         lon = lon1 + (lon2 - lon1) * t

#         curve_offset = math.sin(math.pi * t) * curvature
#         lon += curve_offset

#         route.append({
#             "lat": round(lat, 6),
#             "lon": round(lon, 6)
#         })

#     return route

# # -------------------------
# # Marine Weather
# # -------------------------

# def fetch_marine_weather(lat, lon):
#     try:
#         weather_url = (
#             f"https://api.open-meteo.com/v1/forecast"
#             f"?latitude={lat}&longitude={lon}&current_weather=true"
#         )
#         weather_res = requests.get(weather_url, timeout=6)
#         wind = weather_res.json().get("current_weather", {}).get("windspeed", 5)

#         marine_url = (
#             f"https://marine-api.open-meteo.com/v1/marine"
#             f"?latitude={lat}&longitude={lon}"
#             f"&hourly=wave_height,ocean_current_velocity"
#         )
#         marine_res = requests.get(marine_url, timeout=6)
#         hourly = marine_res.json().get("hourly", {})

#         wave = float(hourly.get("wave_height", [0.5])[0])
#         current = float(hourly.get("ocean_current_velocity", [0.2])[0])

#         return float(wind), current, wave

#     except:
#         return 5.0, 0.2, 0.5

# # -------------------------
# # ML Model
# # -------------------------

# def train_model():
#     np.random.seed(42)
#     samples = 800

#     distance = np.random.uniform(100, 6000, samples)
#     wind = np.random.uniform(0, 30, samples)
#     current = np.random.uniform(0, 3, samples)
#     wave = np.random.uniform(0, 6, samples)
#     time = distance / SPEED_KNOTS

#     fuel = (
#         0.045 * distance +
#         0.9 * wind +
#         1.2 * wave -
#         0.6 * current +
#         0.03 * time +
#         np.random.normal(0, 8, samples)
#     )

#     X = np.column_stack((distance, wind, current, wave, time))
#     model = LinearRegression()
#     model.fit(X, fuel)
#     joblib.dump(model, MODEL_PATH)

# if not os.path.exists(MODEL_PATH):
#     train_model()

# model = joblib.load(MODEL_PATH)

# def predict_fuel(distance_nm, wind, current, wave):
#     voyage_hours = distance_nm / SPEED_KNOTS
#     X = np.array([[distance_nm, wind, current, wave, voyage_hours]])
#     fuel = abs(float(model.predict(X)[0]))
#     co2 = fuel * EMISSION_FACTOR
#     return fuel, co2, voyage_hours

# # -------------------------
# # Optimization Endpoint
# # -------------------------

# @app.post("/optimize")
# async def optimize_route(data: OptimizationRequest):

#     lat1 = data.voyage.start_port.lat
#     lon1 = data.voyage.start_port.lon
#     lat2 = data.voyage.end_port.lat
#     lon2 = data.voyage.end_port.lon

#     baseline_distance = haversine(lat1, lon1, lat2, lon2)

#     winds, currents, waves = [], [], []
#     sample_points = generate_curved_route(lat1, lon1, lat2, lon2)

#     for point in sample_points:
#         wind, current, wave = fetch_marine_weather(point["lat"], point["lon"])
#         winds.append(wind)
#         currents.append(current)
#         waves.append(wave)

#     avg_wind = float(np.mean(winds))
#     avg_current = float(np.mean(currents))
#     avg_wave = float(np.mean(waves))

#     if avg_wave > 2.5 or avg_wind > 20:
#         weather_factor = (
#             1 +
#             (avg_wave * 0.04) +
#             (avg_wind * 0.005) -
#             (avg_current * 0.03)
#         )
#     else:
#         weather_factor = 1

#     optimized_distance = baseline_distance * weather_factor

#     fuel_base, co2_base, time_base = predict_fuel(
#         baseline_distance, avg_wind, avg_current, avg_wave
#     )

#     fuel_opt, co2_opt, time_opt = predict_fuel(
#         optimized_distance, avg_wind, avg_current, avg_wave
#     )

#     fuel_reduction = (
#         ((fuel_base - fuel_opt) / fuel_base) * 100
#         if fuel_base != 0 else 0
#     )

#     baseline_route = generate_curved_route(
#         lat1, lon1, lat2, lon2,
#         curvature=0.0,
#         points=30
#     )

#     optimized_route = generate_curved_route(
#         lat1, lon1, lat2, lon2,
#         curvature=0.8 if weather_factor != 1 else 0.0,
#         points=30
#     )

#     return {
#         "baseline_distance_nm": round(baseline_distance, 2),
#         "optimized_distance_nm": round(optimized_distance, 2),
#         "fuel_reduction_percent": round(fuel_reduction, 2),
#         "co2_reduction_tons": round(co2_base - co2_opt, 2),
#         "time_difference_hours": round(abs(time_base - time_opt), 2),
#         "rerouted_distance_nm": round(abs(optimized_distance - baseline_distance), 2),
#         "baseline_route": baseline_route,
#         "optimized_route": optimized_route,
#         "weather": {
#             "avg_wind_kmh": round(avg_wind, 2),
#             "avg_wave_m": round(avg_wave, 2),
#             "avg_current_ms": round(avg_current, 2),
#             "condition": "rough" if weather_factor != 1 else "calm"
#         },
#         "timestamp": datetime.utcnow().isoformat()
#     }
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import numpy as np
# import requests
# import math
# import joblib
# import os
# from datetime import datetime
# from sklearn.linear_model import LinearRegression
# from searoute import searoute

# app = FastAPI(title="AI Marine Route Optimizer - Real Time")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# EMISSION_FACTOR = 3.114
# SPEED_KNOTS = 20
# MODEL_PATH = "fuel_model.pkl"

# # -------------------------
# # Request Models
# # -------------------------

# class Port(BaseModel):
#     lat: float
#     lon: float

# class Voyage(BaseModel):
#     start_port: Port
#     end_port: Port

# class OptimizationRequest(BaseModel):
#     voyage: Voyage

# # -------------------------
# # Distance Calculation
# # -------------------------

# def haversine(lat1, lon1, lat2, lon2):
#     R = 6371
#     phi1 = math.radians(lat1)
#     phi2 = math.radians(lat2)
#     dphi = math.radians(lat2 - lat1)
#     dlambda = math.radians(lon2 - lon1)

#     a = math.sin(dphi / 2)**2 + \
#         math.cos(phi1) * math.cos(phi2) * \
#         math.sin(dlambda / 2)**2

#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#     return R * c * 0.539957

# # -------------------------
# # Marine Weather
# # -------------------------

# def fetch_marine_weather(lat, lon):
#     try:
#         weather_url = (
#             f"https://api.open-meteo.com/v1/forecast"
#             f"?latitude={lat}&longitude={lon}&current_weather=true"
#         )
#         weather_res = requests.get(weather_url, timeout=6)
#         wind = weather_res.json().get("current_weather", {}).get("windspeed", 5)

#         marine_url = (
#             f"https://marine-api.open-meteo.com/v1/marine"
#             f"?latitude={lat}&longitude={lon}"
#             f"&hourly=wave_height,ocean_current_velocity"
#         )
#         marine_res = requests.get(marine_url, timeout=6)
#         hourly = marine_res.json().get("hourly", {})

#         wave = float(hourly.get("wave_height", [0.5])[0])
#         current = float(hourly.get("ocean_current_velocity", [0.2])[0])

#         return float(wind), current, wave

#     except:
#         return 5.0, 0.2, 0.5

# # -------------------------
# # ML Model
# # -------------------------

# def train_model():
#     np.random.seed(42)
#     samples = 800

#     distance = np.random.uniform(100, 6000, samples)
#     wind = np.random.uniform(0, 30, samples)
#     current = np.random.uniform(0, 3, samples)
#     wave = np.random.uniform(0, 6, samples)
#     time = distance / SPEED_KNOTS

#     fuel = (
#         0.045 * distance +
#         0.9 * wind +
#         1.2 * wave -
#         0.6 * current +
#         0.03 * time +
#         np.random.normal(0, 8, samples)
#     )

#     X = np.column_stack((distance, wind, current, wave, time))
#     model = LinearRegression()
#     model.fit(X, fuel)
#     joblib.dump(model, MODEL_PATH)

# if not os.path.exists(MODEL_PATH):
#     train_model()

# model = joblib.load(MODEL_PATH)

# def predict_fuel(distance_nm, wind, current, wave):
#     voyage_hours = distance_nm / SPEED_KNOTS
#     X = np.array([[distance_nm, wind, current, wave, voyage_hours]])
#     fuel = abs(float(model.predict(X)[0]))
#     co2 = fuel * EMISSION_FACTOR
#     return fuel, co2, voyage_hours

# # -------------------------
# # Optimization Endpoint
# # -------------------------

# @app.post("/optimize")
# async def optimize_route(data: OptimizationRequest):

#     lat1 = data.voyage.start_port.lat
#     lon1 = data.voyage.start_port.lon
#     lat2 = data.voyage.end_port.lat
#     lon2 = data.voyage.end_port.lon

#     # 🌊 REAL SEA ROUTE
#     origin = [lon1, lat1]
#     destination = [lon2, lat2]

#     route_geojson = searoute(origin, destination)
#     coordinates = route_geojson["geometry"]["coordinates"]

#     baseline_route = [
#         {"lat": coord[1], "lon": coord[0]}
#         for coord in coordinates
#     ]
#     route_geojson = searoute(origin, destination)
#     coordinates = route_geojson["geometry"]["coordinates"]

# def densify_route(coords, points_per_segment=20):
#     dense = []
#     for i in range(len(coords) - 1):
#         lon1, lat1 = coords[i]
#         lon2, lat2 = coords[i + 1]

#         for t in np.linspace(0, 1, points_per_segment):
#             lat = lat1 + (lat2 - lat1) * t
#             lon = lon1 + (lon2 - lon1) * t
#             dense.append({"lat": round(lat, 6), "lon": round(lon, 6)})

#     return dense

# baseline_route = densify_route(coordinates, points_per_segment=25)


#     # Calculate true sea distance
#     baseline_distance = route_geojson["properties"]["length"]

#     # Weather sampling along sea route
#     winds, currents, waves = [], [], []

#     for point in baseline_route[::max(1, len(baseline_route)//20)]:
#         wind, current, wave = fetch_marine_weather(point["lat"], point["lon"])
#         winds.append(wind)
#         currents.append(current)
#         waves.append(wave)

#     avg_wind = float(np.mean(winds))
#     avg_current = float(np.mean(currents))
#     avg_wave = float(np.mean(waves))

#     if avg_wave > 2.5 or avg_wind > 20:
#         weather_factor = (
#             1 +
#             (avg_wave * 0.04) +
#             (avg_wind * 0.005) -
#             (avg_current * 0.03)
#         )
#     else:
#         weather_factor = 1

#     optimized_distance = baseline_distance * weather_factor

#     fuel_base, co2_base, time_base = predict_fuel(
#         baseline_distance, avg_wind, avg_current, avg_wave
#     )

#     fuel_opt, co2_opt, time_opt = predict_fuel(
#         optimized_distance, avg_wind, avg_current, avg_wave
#     )

#     fuel_reduction = (
#         ((fuel_base - fuel_opt) / fuel_base) * 100
#         if fuel_base != 0 else 0
#     )

#     # For now optimized_route = same sea route
#     optimized_route = baseline_route

#     return {
#         "baseline_distance_nm": round(baseline_distance, 2),
#         "optimized_distance_nm": round(optimized_distance, 2),
#         "fuel_reduction_percent": round(fuel_reduction, 2),
#         "co2_reduction_tons": round(co2_base - co2_opt, 2),
#         "time_difference_hours": round(abs(time_base - time_opt), 2),
#         "rerouted_distance_nm": round(abs(optimized_distance - baseline_distance), 2),
#         "baseline_route": baseline_route,
#         "optimized_route": optimized_route,
#         "weather": {
#             "avg_wind_kmh": round(avg_wind, 2),
#             "avg_wave_m": round(avg_wave, 2),
#             "avg_current_ms": round(avg_current, 2),
#             "condition": "rough" if weather_factor != 1 else "calm"
#         },
#         "timestamp": datetime.utcnow().isoformat()
#     }
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import requests
import math
import joblib
import os
from datetime import datetime
from sklearn.linear_model import LinearRegression
from searoute import searoute

app = FastAPI(title="AI Marine Route Optimizer - Real Time")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EMISSION_FACTOR = 3.114
SPEED_KNOTS = 20
MODEL_PATH = "fuel_model.pkl"

# -------------------------
# Request Models
# -------------------------

class Port(BaseModel):
    lat: float
    lon: float

class Voyage(BaseModel):
    start_port: Port
    end_port: Port

class OptimizationRequest(BaseModel):
    voyage: Voyage

# -------------------------
# Marine Weather
# -------------------------

def fetch_marine_weather(lat, lon):
    try:
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}&current_weather=true"
        )
        weather_res = requests.get(weather_url, timeout=6)
        wind = weather_res.json().get("current_weather", {}).get("windspeed", 5)

        marine_url = (
            f"https://marine-api.open-meteo.com/v1/marine"
            f"?latitude={lat}&longitude={lon}"
            f"&hourly=wave_height,ocean_current_velocity"
        )
        marine_res = requests.get(marine_url, timeout=6)
        hourly = marine_res.json().get("hourly", {})

        wave = float(hourly.get("wave_height", [0.5])[0]) 
        current = float(hourly.get("ocean_current_velocity", [0.2])[0])

        return float(wind), current, wave

    except:
        return 5.0, 0.2, 0.5

# -------------------------
# ML Model
# -------------------------

def train_model():
    np.random.seed(42)
    samples = 800

    distance = np.random.uniform(100, 6000, samples)
    wind = np.random.uniform(0, 30, samples)
    current = np.random.uniform(0, 3, samples)
    wave = np.random.uniform(0, 6, samples)
    time = distance / SPEED_KNOTS

    fuel = (
        0.045 * distance +
        0.9 * wind +
        1.2 * wave -
        0.6 * current +
        0.03 * time +
        np.random.normal(0, 8, samples)
    )

    X = np.column_stack((distance, wind, current, wave, time))
    model = LinearRegression()
    model.fit(X, fuel)
    joblib.dump(model, MODEL_PATH)

if not os.path.exists(MODEL_PATH):
    train_model()

model = joblib.load(MODEL_PATH)

def predict_fuel(distance_nm, wind, current, wave):
    voyage_hours = distance_nm / SPEED_KNOTS
    X = np.array([[distance_nm, wind, current, wave, voyage_hours]])
    fuel = abs(float(model.predict(X)[0]))
    co2 = fuel * EMISSION_FACTOR
    return fuel, co2, voyage_hours

# -------------------------
# Route Densification
# -------------------------

def densify_route(coords, points_per_segment=25):
    dense = []
    for i in range(len(coords) - 1):
        lon1, lat1 = coords[i]
        lon2, lat2 = coords[i + 1]

        for t in np.linspace(0, 1, points_per_segment):
            lat = lat1 + (lat2 - lat1) * t
            lon = lon1 + (lon2 - lon1) * t
            dense.append({
                "lat": round(lat, 6),
                "lon": round(lon, 6)
            })

    return dense

# -------------------------
# Optimization Endpoint
# -------------------------

@app.post("/optimize")
async def optimize_route(data: OptimizationRequest):

    lat1 = data.voyage.start_port.lat
    lon1 = data.voyage.start_port.lon
    lat2 = data.voyage.end_port.lat
    lon2 = data.voyage.end_port.lon

    # 🌊 REAL SEA ROUTE USING SEAROUTE
    origin = [lon1, lat1]
    destination = [lon2, lat2]

    route_geojson = searoute(origin, destination)
    coordinates = route_geojson["geometry"]["coordinates"]

    # Smooth maritime path
    baseline_route = densify_route(coordinates, 25)

    # True sea distance
    baseline_distance = route_geojson["properties"]["length"]

    # Weather sampling (sample 20 points max)
    winds, currents, waves = [], [], []

    sample_step = max(1, len(baseline_route) // 20)

    for point in baseline_route[::sample_step]:
        wind, current, wave = fetch_marine_weather(point["lat"], point["lon"])
        winds.append(wind)
        currents.append(current)
        waves.append(wave)

    avg_wind = float(np.mean(winds))
    avg_current = float(np.mean(currents))
    avg_wave = float(np.mean(waves))

    # Weather impact factor
    if avg_wave > 2.5 or avg_wind > 20:
        weather_factor = (
            1 +
            (avg_wave * 0.04) +
            (avg_wind * 0.005) -
            (avg_current * 0.03)
        )
    else:
        weather_factor = 1

    optimized_distance = baseline_distance * weather_factor

    fuel_base, co2_base, time_base = predict_fuel(
        baseline_distance, avg_wind, avg_current, avg_wave
    )

    fuel_opt, co2_opt, time_opt = predict_fuel(
        optimized_distance, avg_wind, avg_current, avg_wave
    )

    fuel_reduction = (
        ((fuel_base - fuel_opt) / fuel_base) * 100
        if fuel_base != 0 else 0
    )

    optimized_route = baseline_route

    return {
        "baseline_distance_nm": round(baseline_distance, 2),
        "optimized_distance_nm": round(optimized_distance, 2),
        "fuel_reduction_percent": round(fuel_reduction, 2),
        "co2_reduction_tons": round(co2_base - co2_opt, 2),
        "time_difference_hours": round(abs(time_base - time_opt), 2),
        "rerouted_distance_nm": round(abs(optimized_distance - baseline_distance), 2),
        "baseline_route": baseline_route,
        "optimized_route": optimized_route,
        "weather": {
            "avg_wind_kmh": round(avg_wind, 2),
            "avg_wave_m": round(avg_wave, 2),
            "avg_current_ms": round(avg_current, 2),
            "condition": "rough" if weather_factor != 1 else "calm"
        },
        "timestamp": datetime.utcnow().isoformat()
    }