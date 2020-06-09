import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SwagTableComponent } from './swag-table.component';

describe('SwagTableComponent', () => {
  let component: SwagTableComponent;
  let fixture: ComponentFixture<SwagTableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SwagTableComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SwagTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
