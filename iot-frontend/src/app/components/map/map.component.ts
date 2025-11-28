import { Component, Output } from '@angular/core';
import { ElementRef, ViewChild, inject, AfterViewInit } from '@angular/core';
import * as L from 'leaflet';
import { EventEmitter } from '@angular/core';
import { Geolocation } from '../../shared/geolocation';


@Component({
  selector: 'app-map',
  imports: [],
  templateUrl: './map.component.html',
  styleUrl: './map.component.scss'
})
export class MapComponent implements AfterViewInit{

    @ViewChild('mapElement') mapElement!: ElementRef;
    @Output() hasClicked = new EventEmitter<Geolocation>();

    
    ngAfterViewInit(): void {
    this.initMap();
    }
initMap() {

  
const map = L.map(this.mapElement.nativeElement).setView([52.0, 20.0], 6); 

map.on('click',(e:any)=>{
  const {lat,lng}=e.latlng;
  console.log('Kliknieto',lat,lng)
  this.hasClicked.emit({lat,lng});
})
  
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);
}

}
