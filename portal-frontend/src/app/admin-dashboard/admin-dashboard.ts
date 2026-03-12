import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

interface Stats {
  total: number;
  ml: number;
  ds: number;
  da: number;
}

interface Student {
  name: string;
  email: string;
  phone: string;
  college: string;
  dept: string;
  domain: string;
  batch: string;
  trainer: string;
  mode: string;
  attendance_summary: string;
  total_marks: any;
  dataset_type: string;
}

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-dashboard.html',
  styleUrl: './admin-dashboard.css',
})
export class AdminDashboard implements OnInit {
  statistics: Stats = { total: 0, ml: 0, ds: 0, da: 0 };
  students: Student[] = [];
  filteredStudents: Student[] = [];
  
  filters = {
    search: '',
    domain: 'all',
    batch: ''
  };

  showAddModal = false;
  showImportModal = false;

  isAddCandidateModalOpen = false;
  isBulkImportModalOpen = false;
  bulkImportStep = 1;
  bulkImportFileName: string = 'No file selected';
  selectedFile: File | null = null;
  validationReport: any = null;
  canImport: boolean = false;

  newCandidate = {
    name: '',
    email: '',
    phone_number: '',
    college: '',
    dept: '',
    domain: '',
    mode: '',
    trainer: '',
    batch: '',
    session_timings: '',
    days: '',
    registration_date: '',
    session_start_date: '',
    session_end_date: '',
    attendance_count: 0,
    stipend_eligibility: '',
    stipend_reason: '',
    project_title: '',
    assessment_1: 0,
    assessment_2: 0,
    task: 0,
    project_marks: 0,
    final_validation: 0,
    total_marks: 0
  };

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    this.fetchData();
  }

  fetchData() {
    this.statistics = {
      total: 156,
      ml: 64,
      ds: 42,
      da: 50
    };

    this.students = [
      {
        name: 'John Doe',
        email: 'john@example.com',
        phone: '1234567890',
        college: 'ABC Engineering',
        dept: 'CSE',
        domain: 'ML',
        batch: 'B1',
        trainer: 'Mentor Alpha',
        mode: 'ONLINE',
        attendance_summary: '28/30',
        total_marks: 285,
        dataset_type: 'ML'
      },
      {
        name: 'Jane Smith',
        email: 'jane@example.com',
        phone: '0987654321',
        college: 'XYZ Tech',
        dept: 'IT',
        domain: 'DS',
        batch: 'B2',
        trainer: 'Mentor Beta',
        mode: 'OFFLINE',
        attendance_summary: '25/30',
        total_marks: 270,
        dataset_type: 'DS'
      }
    ];
    this.filteredStudents = [...this.students];
  }

  applyFilters() {
    this.filteredStudents = this.students.filter(s => {
      const matchesSearch = !this.filters.search || 
                           s.name.toLowerCase().includes(this.filters.search.toLowerCase()) ||
                           s.email.toLowerCase().includes(this.filters.search.toLowerCase()) ||
                           s.phone.includes(this.filters.search);
      
      const matchesDomain = this.filters.domain === 'all' || s.domain === this.filters.domain;
      const matchesBatch = !this.filters.batch || s.batch.toLowerCase().includes(this.filters.batch.toLowerCase());
      
      return matchesSearch && matchesDomain && matchesBatch;
    });
  }

  resetFilters() {
    this.filters = {
      search: '',
      domain: 'all',
      batch: ''
    };
    this.applyFilters();
  }

  downloadCSV() {
    const headers = ['Name', 'Email', 'Phone', 'College', 'Dept', 'Domain', 'Batch', 'Mentor', 'Mode', 'Attendance', 'Total Marks', 'Program'];
    const csvRows = [headers.join(',')];

    for (const student of this.filteredStudents) {
      const row = [
        student.name,
        student.email,
        student.phone,
        student.college,
        student.dept,
        student.domain,
        student.batch,
        student.trainer,
        student.mode,
        student.attendance_summary,
        student.total_marks,
        student.dataset_type
      ].map(val => `"${val}"`).join(',');
      csvRows.push(row);
    }

    const csvContent = "data:text/csv;charset=utf-8," + csvRows.join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `students_export_${new Date().getTime()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  showAddCandidateModal() {
    this.showAddModal = true;
  }

  showBulkImportModal() {
    this.showImportModal = true;
    this.bulkImportStep = 1;
  }

  hideModals() {
    this.showAddModal = false;
    this.showImportModal = false;
  }

  handleAddCandidate() {
    console.log('Adding candidate:', this.newCandidate);
    alert('✓ Candidate added successfully! (Mock Action)');
    this.showAddModal = false;
  }

  closeBulkImportModal() {
    this.showImportModal = false;
  }

  onFileSelected(event: any) {
    if (event.target.files && event.target.files[0]) {
      this.selectedFile = event.target.files[0];
      this.bulkImportFileName = '✓ ' + this.selectedFile!.name;
    }
  }

  validateBulkImport() {
    if (!this.selectedFile) {
      alert('Please select a file');
      return;
    }
    // Mocking validation
    this.bulkImportStep = 2;
    this.validationReport = {
      total_rows: 10,
      valid_rows: 10,
      missing_required_fields: [],
      duplicate_emails_in_file: [],
      duplicate_emails_in_db: []
    };
    this.canImport = true;
  }

  processImport() {
    alert('✓ Successfully imported data! (Mock Action)');
    this.closeBulkImportModal();
  }

  goBackToUpload() {
    this.bulkImportStep = 1;
  }

  editStudent(email: string) {
    this.router.navigate(['/admin-student-edit'], { queryParams: { email: email } });
  }

  logout() {
    if (confirm('Are you sure you want to logout?')) {
      window.location.href = '/admin-logout';
    }
  }
}
