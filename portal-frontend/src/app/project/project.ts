import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-project',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './project.html',
  styleUrl: './project.css',
})
export class Project implements OnInit {
  name: string = '';
  project_title: string = '';
  loading: boolean = true;
  studentData: any = { name: 'John Doe' };

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    // Attempt to fetch user details from the backend
    this.http.get<any>('/api/me').subscribe({
      next: (res) => {
        if (res.success && res.details) {
          this.name = res.details.name;
          this.project_title = res.details.project_title || 'N/A';
        } else {
          this.loadMockData();
        }
        this.loading = false;
      },
      error: () => {
        this.loadMockData();
        this.loading = false;
      }
    });
  }

  loadMockData() {
    this.name = 'John Doe';
    this.project_title = 'Predictive Analytics Model';
  }

  logout(event?: Event) {
    if (event) event.preventDefault();
    if (confirm('Are you sure you want to logout?')) {
      window.location.href = '/logout';
    }
  }
}
