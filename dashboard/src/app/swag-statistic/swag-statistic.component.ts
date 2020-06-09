import { Component, OnInit, Input, SimpleChanges, OnChanges } from '@angular/core';
import { SwagObject } from '../swag-object';
import { stringify } from 'querystring';


@Component({
  selector: 'app-swag-statistic',
  templateUrl: './swag-statistic.component.html',
  styleUrls: ['./swag-statistic.component.css']
})
export class SwagStatisticComponent implements OnInit {

  @Input()
  objects: Array<SwagObject>;

  @Input()
  name: string;

  @Input()
  isLoading: Boolean;

  // params for statics
  public totalCount: number;
  public categories = new Map<string, number>();
  public avgSpeed: number;
  public length = 0;
  public mainDirection = "";

  constructor() { }

  ngOnInit(): void {
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['isLoading'] && changes['isLoading'].currentValue == false) {
      this.prepareStatistic();
    }
  }

  prepareStatistic() {
    this.totalCount = this.objects.length;
    var directions = new Map<string, number>();
    var totalDirections = 0;
    this.avgSpeed = 0.0;
    this.objects.forEach(element => {
      if (!this.categories.has(element.label.toString())) {
        this.categories.set(element.label.toString(), 1);
      }
      else {
        let newValue = this.categories.get(element.label.toString()) + 1;
        this.categories.set(element.label.toString(), newValue);
      }

      if (element.avg_speed) {
        let newValue = (this.avgSpeed + parseFloat(element.avg_speed.toString())) / 2;
        this.avgSpeed = newValue;
      }

      if (element.last_appear > self.length) {
        this.length = element.last_appear;
      }

      if (directions.has(element.direction)) {
        let newValue = directions.get(element.direction) + 1;
        directions.set(element.direction, newValue);
        totalDirections++;
      }
      else {
        directions.set(element.direction, 1);
        totalDirections++;
      }
    });

    directions.forEach((value: number, key: string) => {
      if (value > totalDirections * 0.3 && key != null) {
        if (this.mainDirection == "") {
          this.mainDirection = key;
        }
        else {
          this.mainDirection = this.mainDirection + " | " + key;
        }
      }
    });
    this.avgSpeed = parseFloat(this.avgSpeed.toFixed(2));
  }

}
