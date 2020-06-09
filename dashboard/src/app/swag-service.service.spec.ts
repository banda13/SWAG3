import { TestBed } from '@angular/core/testing';

import { SwagServiceService } from './swag-service.service';

describe('SwagServiceService', () => {
  let service: SwagServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SwagServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
