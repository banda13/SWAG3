import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SwagVideoComponent } from './swag-video.component';

describe('SwagVideoComponent', () => {
  let component: SwagVideoComponent;
  let fixture: ComponentFixture<SwagVideoComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SwagVideoComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SwagVideoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
