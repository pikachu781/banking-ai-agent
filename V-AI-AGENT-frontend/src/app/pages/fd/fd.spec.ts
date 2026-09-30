import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Fd } from './fd';

describe('Fd', () => {
  let component: Fd;
  let fixture: ComponentFixture<Fd>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Fd],
    }).compileComponents();

    fixture = TestBed.createComponent(Fd);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
