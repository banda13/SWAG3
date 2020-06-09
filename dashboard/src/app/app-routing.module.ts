import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MenuComponent} from './menu/menu.component';
import { AnaliticsComponent } from './analitics/analitics.component';
import { SwagLogsComponent } from './swag-logs/swag-logs.component';
import { SwagStatisticComponent } from './swag-statistic/swag-statistic.component';


const routes: Routes = [
  {
    path: '',
    component: MenuComponent
  },
  {
    path: 'anal',
    component: AnaliticsComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
