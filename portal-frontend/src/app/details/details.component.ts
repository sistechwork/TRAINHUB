import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-details',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './details.component.html',
  styleUrls: ['./details.component.css']
})
export class DetailsComponent implements OnInit {
  studentData: any = {};
  activeTab: string = 'personal';

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    // Attempt to fetch user details from the backend
    this.http.get<any>('/api/me').subscribe({
      next: (res) => {
        if (res.success) {
          this.studentData = res.details;
        } else {
          // If not logged in or endpoint fails, fallback to mocked data or redirect
          this.loadMockData();
        }
      },
      error: () => {
        this.loadMockData();
      }
    });
  }

  loadMockData() {
    this.studentData = {
      name: 'John Doe',
      email: 'john.doe@example.com',
      phone: '+1 234 567 8900',
      domain: 'Data Science',
      mentor: 'Jane Smith',
      college: 'Tech University',
      dept: 'Computer Science',
      mode: 'Online',
      time: '10:00 AM - 1:00 PM',
      days: 'Mon - Fri',
      batch: 'B1',
      project_title: 'Predictive Analytics Model',
      assessment1: 8,
      assessment2: 9,
      task: 9,
      project_mark: 10,
      final_validation: 8,
      total_mark: 44,
      registration_date: 'January 15, 2026',
      start_date: 'February 1, 2026',
      end_date: 'May 1, 2026',
      stipend_eligibility: 'Eligible',
      stipend_reason: 'Excellent Performance',
      per: 92,
      attendance_percentage: 92
    };
  }

  setTab(tab: string) {
    this.activeTab = tab;
  }

  logout(event?: Event) {
    if (event) event.preventDefault();
    if (confirm('Are you sure you want to logout?')) {
      window.location.href = '/logout';
    }
  }
}
