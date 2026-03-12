import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminStudentEdit } from './admin-student-edit';

describe('AdminStudentEdit', () => {
  let component: AdminStudentEdit;
  let fixture: ComponentFixture<AdminStudentEdit>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AdminStudentEdit],
    }).compileComponents();

    fixture = TestBed.createComponent(AdminStudentEdit);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
