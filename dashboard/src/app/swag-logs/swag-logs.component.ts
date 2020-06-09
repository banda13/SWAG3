import { Component, OnInit, Input, SimpleChanges, OnChanges, NgZone, ViewChild } from '@angular/core';
import {CdkTextareaAutosize} from '@angular/cdk/text-field';
import {take} from 'rxjs/operators';

@Component({
  selector: 'app-swag-logs',
  templateUrl: './swag-logs.component.html',
  styleUrls: ['./swag-logs.component.css']
})
export class SwagLogsComponent implements OnInit {

  @Input()
  logtext: String

  @Input()
  isLoading: Boolean;


  @ViewChild('autosize') autosize: CdkTextareaAutosize;

  constructor(private _ngZone: NgZone) { }
  
  triggerResize() {
    // Wait for changes to be applied, then trigger textarea resize.
    this._ngZone.onStable.pipe(take(1))
        .subscribe(() => this.autosize.resizeToFitContent(true));
  }

  ngOnInit(): void {
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['isLoading'] && changes['isLoading'].currentValue == false) {
      this.prepare();
    }
  }

  prepare() {
   
  }
}
