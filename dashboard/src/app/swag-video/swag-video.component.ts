import { Component, OnInit, Input, SimpleChanges, OnChanges } from '@angular/core';

@Component({
  selector: 'app-swag-video',
  templateUrl: './swag-video.component.html',
  styleUrls: ['./swag-video.component.css']
})
export class SwagVideoComponent implements OnInit {

  @Input()
  name: String;

  @Input()
  isLoading: Boolean;

  apiUrl = "http://localhost/"
  videoURL : String;

  constructor() { }

  ngOnInit(): void {
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['name'] && changes['name'] != null) {
      this.videoURL = this.apiUrl + "static/" + this.name + "/output.mp4";
    }
  }

}
