import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MenuComponent } from './menu/menu.component';
import { AnaliticsComponent } from './analitics/analitics.component';
import { HeaderComponent } from './header/header.component';

import { MatToolbarModule } from '@angular/material/toolbar';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatCardModule} from '@angular/material/card';
import {MatListModule} from '@angular/material/list';
import { SwagLogsComponent } from './swag-logs/swag-logs.component';
import { SwagTableComponent } from './swag-table/swag-table.component';
import { SwagVideoComponent } from './swag-video/swag-video.component';
import { SwagChartsComponent } from './swag-charts/swag-charts.component';
import { SwagStatisticComponent } from './swag-statistic/swag-statistic.component';
import {MatGridListModule} from '@angular/material/grid-list';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ChartsModule } from 'ng2-charts';
import {TextFieldModule} from '@angular/cdk/text-field';
import { MatTableModule } from '@angular/material/table';
import { MatInputModule } from '@angular/material/input';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatButtonModule } from '@angular/material/button';
import { MatSortModule } from '@angular/material/sort';
import {MatProgressBarModule} from '@angular/material/progress-bar';

@NgModule({
  declarations: [
    AppComponent,
    MenuComponent,
    AnaliticsComponent,
    HeaderComponent,
    SwagLogsComponent,
    SwagTableComponent,
    SwagVideoComponent,
    SwagChartsComponent,
    SwagStatisticComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatToolbarModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MatCardModule,
    MatListModule,
    MatGridListModule,
    MatProgressSpinnerModule,
    ChartsModule,
    TextFieldModule,
    MatInputModule,
    MatTableModule,
    MatPaginatorModule,
    MatSortModule,
    MatButtonModule,
    MatProgressBarModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
