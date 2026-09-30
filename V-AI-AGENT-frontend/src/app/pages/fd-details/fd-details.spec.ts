import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FdDetails } from './fd-details';

describe('FdDetails', () => {
  let component: FdDetails;
  let fixture: ComponentFixture<FdDetails>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FdDetails],
    }).compileComponents();

    fixture = TestBed.createComponent(FdDetails);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
