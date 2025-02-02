import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OneConceptPageComponent } from './one-concept-page.component';

describe('OneConceptPageComponent', () => {
  let component: OneConceptPageComponent;
  let fixture: ComponentFixture<OneConceptPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OneConceptPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OneConceptPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
