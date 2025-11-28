import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Geolocation } from '../shared/geolocation';
import { AqiData } from '../shared/aqiData';




@Injectable({
  providedIn: 'root'
})
export class ApiSimulationService {
getAqiInfo(coords: Geolocation): Observable<AqiData> {
    const mockedData: AqiData = {
      'location': 'Shinjuku',
      'country': 'JP',
      'lon': coords.lng,
      'lat': coords.lat,
      'aqi': 98,
      'co': 158.89,
      'no': 0.03,
      'no2': 28.19,
      'o3': 48.96,
      'so2': 15.65,
      'pm2_5': 8.07,
      'pm10': 14.83,
      'nh3': 0.2,
      'uv_index': 3.21,
      'time': new Date().toISOString(), 
    };
    
    return of(mockedData); 
  }
}
