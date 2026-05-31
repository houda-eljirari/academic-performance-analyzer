import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Shap } from './shap';

describe('Shap', () => {
  let component: Shap;
  let fixture: ComponentFixture<Shap>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Shap],
    }).compileComponents();

    fixture = TestBed.createComponent(Shap);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
