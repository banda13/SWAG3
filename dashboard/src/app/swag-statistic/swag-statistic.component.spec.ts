import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SwagStatisticComponent } from './swag-statistic.component';

describe('SwagStatisticComponent', () => {
  let component: SwagStatisticComponent;
  let fixture: ComponentFixture<SwagStatisticComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SwagStatisticComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SwagStatisticComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
