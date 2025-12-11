import { Component,Input,Output,EventEmitter } from '@angular/core';
import { DrawerModule } from 'primeng/drawer';
import { CardModule } from 'primeng/card';
import { FieldsetModule } from 'primeng/fieldset';
import { BadgeModule } from 'primeng/badge';
import { DividerModule } from 'primeng/divider';
import { MessageModule } from 'primeng/message';
import { PanelModule } from 'primeng/panel';
import { ButtonModule } from 'primeng/button';
import { AqiData } from '../../shared/aqiData';
import { DecimalPipe,CommonModule } from '@angular/common';
import { DatePipe } from '@angular/common';
import { NgIf } from '@angular/common';
import { AqiStatus } from '../../shared/aqi-status';
import { SimpleChanges, OnChanges } from '@angular/core';
import { TagModule } from 'primeng/tag';
import { ProgressBarModule } from 'primeng/progressbar';


@Component({
  selector: 'app-drawer',
  imports: [DrawerModule,ButtonModule,CardModule,FieldsetModule,BadgeModule,DividerModule,MessageModule,PanelModule,DecimalPipe,NgIf,DatePipe,TagModule,CommonModule,ProgressBarModule],
  templateUrl: './drawer.component.html',
  styleUrl: './drawer.component.scss'
})
export class DrawerComponent {
 @Input() visible = false;
    @Input() data: AqiData | null = null; 
    @Input() isLoading: boolean = false; 
    @Output() closed = new EventEmitter<void>();


    aqiStatus: AqiStatus = { text: '', severity: '', color: '' };
    progressValue:number=0;

    ngOnChanges(changes: SimpleChanges): void {
        if (changes['data'] && this.data) {
            this.aqiStatus = this.getAqiStatus(this.data.aqi); 
            
             this.progressValue = Math.min(this.data.aqi*20 , 100);
        }
    }

    getAqiStatus(aqiValue: number): AqiStatus {
    if (aqiValue <= 1) {
        return { text: 'Bardzo Dobra', severity: 'success', color: '#4CAF50' }; 
    } else if (aqiValue <= 2) {
        return { text: 'Umiarkowana', severity: 'warning', color: '#BDB76B' }; 
    } else if (aqiValue <= 3) {
        return { text: 'Niezdrowa dla Wrażliwych', severity: 'danger', color: '#FF9800' }; 
    } else if (aqiValue <= 4) {
        return { text: 'Niezdrowa', severity: 'danger', color: '#F44336' };
    } else if (aqiValue <= 5) {
        return { text: 'Bardzo Niezdrowa', severity: 'danger', color: '#9C27B0' };
    } else {
        return { text: 'NIEBEZPIECZNA (Alarm)', severity: 'danger', color: '#795548' }; 
    }
}


  onClose(){
    this.closed.emit();
  }
}
