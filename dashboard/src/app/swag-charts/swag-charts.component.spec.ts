import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SwagChartsComponent } from './swag-charts.component';

describe('SwagChartsComponent', () => {
  let component: SwagChartsComponent;
  let fixture: ComponentFixture<SwagChartsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SwagChartsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SwagChartsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
