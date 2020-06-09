import { Component, OnInit, Input, SimpleChanges, OnChanges } from '@angular/core';
import { SwagObject } from "../swag-object";
import { stringify } from 'querystring';

@Component({
  selector: 'app-swag-charts',
  templateUrl: './swag-charts.component.html',
  styleUrls: ['./swag-charts.component.css']
})
export class SwagChartsComponent implements OnInit {

  @Input()
  objects: Array<SwagObject>;

  @Input()
  name: String;

  @Input()
  isLoading: Boolean;

  constructor() { }

  ngOnInit(): void {
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['isLoading'] && changes['isLoading'].currentValue == false) {
      this.createPieChart();
      this.createBarChart();
    }
  }

  public pieChartLabels = [];
  public pieChartData = [];
  public pieChartType = 'pie';


  public barChartLabels = [];
  public barChartType = 'bar';
  public barChartLegend = true;
  public barChartData = [
    { data: [], label: 'Average Precisions per classes' }
  ];
  public barChartOptions = {
    scaleShowVerticalLines: false,
    responsive: true
  };


  public lineChartType = "line";
  public lineChartData = [10, 20, 10, 40, 0, 10];
  public lineChartLabels = ["a", "b", "c", "d", "e", "f"];

  public createPieChart() {
    this.objects.forEach(element => {
      let idx = this.pieChartLabels.indexOf(element.label.toString());
      if (idx == -1) {
        this.pieChartLabels.push(element.label.toString());
        this.pieChartData.push(1);
      }
      else {
        this.pieChartData[idx]++;
      }
    });
  }

  public createBarChart() {
    var valueList = [];
    this.objects.forEach(element => {
      var p = element.precision.valueOf();
      if(typeof(p) == typeof("")){
        p = parseFloat(p.toString());
      }
      if (p > 0.0) {
        let idx = this.barChartLabels.indexOf(element.label.toString());
        if (idx == -1) {
          this.barChartLabels.push(element.label.toString());
          valueList.push(p);
        }
        else {
          let newValue = ((valueList[idx] + p) / 2);
          valueList[idx] = newValue;
        }
      }
    });
    this.barChartData[0]["data"] = valueList;
  }
}
