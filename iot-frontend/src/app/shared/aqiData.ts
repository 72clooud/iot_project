export interface AqiData {
  location: string;
  country: string;
  lon: number;
  lat: number;
  aqi: number;
  co: number;
  no: number;
  no2: number;
  o3: number;
  so2: number;
  pm2_5: number;
  pm10: number;
  nh3: number;
  uv_index: number;
  timestamp: string;
}