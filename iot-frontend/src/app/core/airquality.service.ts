import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AqiData } from '../shared/aqiData';

@Injectable({
  providedIn: 'root'
})
export class AirqualityService {

  private apiUrl = "http://127.0.0.1:8000/telemetry";

  constructor(private http: HttpClient) { }

  getAirQuality(lat: number, lng: number): Observable<AqiData> {

    const params = new HttpParams()
      .set('lat', lat.toString())
      .set('lon', lng.toString());

    return this.http.get<AqiData>(this.apiUrl, { params });
  }
}
