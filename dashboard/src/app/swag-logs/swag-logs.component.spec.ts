import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SwagLogsComponent } from './swag-logs.component';

describe('SwagLogsComponent', () => {
  let component: SwagLogsComponent;
  let fixture: ComponentFixture<SwagLogsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SwagLogsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SwagLogsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
