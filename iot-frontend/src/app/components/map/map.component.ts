import { Component, Output } from '@angular/core';
import { ElementRef, ViewChild, inject, AfterViewInit } from '@angular/core';
import * as L from 'leaflet';
import { EventEmitter } from '@angular/core';
import { Geolocation } from '../../shared/geolocation';

import { AutoCompleteModule, AutoCompleteSelectEvent } from 'primeng/autocomplete';
import { AirqualityService } from '../../core/airquality.service';
import { FormsModule } from '@angular/forms';


@Component({
  selector: 'app-map',
  imports: [AutoCompleteModule,FormsModule],
  templateUrl: './map.component.html',
  styleUrl: './map.component.scss'
})
export class MapComponent implements AfterViewInit{

    @ViewChild('mapElement') mapElement!: ElementRef;
    @Output() hasClicked = new EventEmitter<Geolocation>();

    constructor(private airqualityService:AirqualityService){}
    private map!: L.Map;
    selectedCity: any;
    filteredCities: any[] = [];


    ngAfterViewInit(): void {
    this.initMap();
    }
initMap() {

  
this.map = L.map(this.mapElement.nativeElement).setView([52.0, 20.0], 6); 

this.map.on('click',(e:any)=>{
  const {lat,lng}=e.latlng;
  console.log('Kliknieto',lat,lng)
  this.hasClicked.emit({lat,lng});
})
  
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(this.map);
}


search(event:any){
  const query=event.query;
  this.airqualityService.searchLocation(query).subscribe((data)=>this.filteredCities=data);
}

onCitySelect(event: AutoCompleteSelectEvent) {
        const selected = event.value;
        const lat = parseFloat(selected.lat);
        const lon = parseFloat(selected.lon);
        this.map.flyTo([lat, lon], 12); 

      
    }
}
