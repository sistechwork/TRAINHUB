import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-admin-student-edit',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './admin-student-edit.html',
  styleUrl: './admin-student-edit.css',
})
export class AdminStudentEdit implements OnInit {
  studentEmail: string | null = null;
  studentData: any = {};
  isLoading = true;
  message = { text: '', type: '' };

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.studentEmail = params['email'];
      if (this.studentEmail) {
        this.loadStudentData();
      } else {
        this.message = { text: 'No student email provided', type: 'error' };
        this.isLoading = false;
      }
    });
  }

  loadStudentData() {
    this.isLoading = true;
    // Mocking data loading
    setTimeout(() => {
      this.studentData = {
        name: 'John Doe',
        email: this.studentEmail,
        phone: '1234567890',
        college: 'ABC Engineering',
        dept: 'CSE',
        domain: 'ML',
        mode: 'ONLINE',
        mentor: 'Mentor Alpha',
        batch: 'B1',
        session_timings: '6:30 to 8 PM',
        days: 'T,T,S',
        registration_date: '2025-01-10',
        session_start_date: '2025-02-01',
        session_end_date: '2025-05-01',
        attendance_count: '28/30',
        stipend_eligibility: 'YES',
        stipend_reason: 'Excellent performance',
        project_title: 'Predictive Maintenance using ML',
        assessment_1: '85',
        assessment_2: '90',
        task: 'Completed',
        project_marks: '95',
        final_validation: 'Pass',
        total_marks: '270',
        program: 'ML'
      };
      this.isLoading = false;
    }, 1000);
  }

  saveStudent() {
    this.message = { text: '✓ Student data updated successfully! (Mock Action)', type: 'success' };
    setTimeout(() => {
      this.router.navigate(['/admin-dashboard']);
    }, 1500);
  }

  showMessage(text: string, type: string) {
    this.message = { text, type };
  }
}
