import { Component, OnInit } from '@angular/core';
import { SwagServiceService } from '../swag-service.service';



@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit {

  APIURL = "http://178.48.246.170:1235/"
  isLoading = true;
  data = [];
  noResult = false;

  constructor(private swagService: SwagServiceService) {
    
   }

  ngOnInit(): void {
    this.getData();
  }

  setData(data): void{
    this.data = data;
    this.isLoading = false;
    console.log(data);
    if(this.data.length == 0){
      this.noResult = true;
    }
  }

  getData(): void{
    this.swagService.getItems().subscribe(data=> this.setData(data));
  }

}
