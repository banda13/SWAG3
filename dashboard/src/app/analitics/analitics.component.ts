import { Component, OnInit, NgModule } from '@angular/core';
import { SwagStatisticComponent } from '../swag-statistic/swag-statistic.component'
import { SwagServiceService } from '../swag-service.service';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { SwagObject } from "../swag-object";

@Component({
  selector: 'app-analitics',
  templateUrl: './analitics.component.html',
  styleUrls: ['./analitics.component.css']
})
export class AnaliticsComponent implements OnInit {

  name = null;
  isLoading = true;
  logLoading = true;
  videoLoading = true;
  objects = [];
  logs = "";
  progress = 0;

  constructor(private route: ActivatedRoute, private swagService: SwagServiceService) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.name = params['name'];
      this.loadData();
      this.loadLogs();
      this.videoLoading = false;
    });
  }

  loadData() {
    this.swagService.getObjectList(this.name)
      .subscribe(objectIds => {
        objectIds = objectIds;
        var i = 0;
        objectIds.forEach(id => {
          this.swagService.getObjectDetails(this.name, id).subscribe(data => {
            i++;
            if (data != null && data != "" ) {
              let d = new SwagObject(data);
              this.objects.push(d);
              this.progress = (i / objectIds.length) * 100;
            }
            else {
              console.log("Oopsie");
            }
            if (objectIds.length == i) {
              this.isLoading = false;
            }
          })
        })
      });
  }

  loadLogs() {
    this.swagService.getLogs(this.name).subscribe(logs => {
      logs.forEach(line => {
        this.logs += line + "\n";
      })
      this.logLoading = false;
    })
  }

}
