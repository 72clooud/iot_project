import { Component } from '@angular/core';
import { MapComponent } from "../../components/map/map.component";
import { DrawerComponent } from "../../components/drawer/drawer.component";
import { AqiData } from '../../shared/aqiData';
import { AirqualityService } from '../../core/airquality.service';
@Component({
  selector: 'app-home',
  imports: [MapComponent, DrawerComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
 drawerVisible: boolean=false;
drawerData: AqiData | null = null;
isLoading: boolean = false;

    constructor(private airQualityService: AirqualityService) {} 
onMapClicked(coords: {lat: number, lng: number}) { 
      this.isLoading = true;
      this.drawerVisible = true;
      
      console.log('Współrzędne z mapy:', coords);

      
      this.airQualityService.getAirQuality(coords.lat, coords.lng).subscribe({
          next: (data) => {
              console.log('--- HOME: Otrzymano dane:', data); 
              this.drawerData = data; 
              this.isLoading = false; 
          },
          error: (err) => {
              console.error("--- HOME: Błąd:", err);
              this.isLoading = false;
              
          }
      });
  }

 openDrawer() {
    this.drawerVisible = true;
    console.log('Szuflada otwarta:', this.drawerVisible);
  }


  closeDrawer() {
    this.drawerVisible = false;
   this.drawerData = null; 
      this.isLoading = false;
  }
}
