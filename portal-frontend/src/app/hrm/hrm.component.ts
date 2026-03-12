import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-hrm',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './hrm.component.html',
  styleUrls: ['./hrm.component.css']
})
export class HrmComponent implements OnInit {
  activeTab = 'dashboard';
  studentData: any = { name: 'John Doe', domain: 'ML', college: 'MIT' };
  
  // Dashboard stats
  stats = {
    totalEmployees: 0,
    totalDepartments: 0,
    presentToday: 0,
    pendingLeaves: 0
  };

  // Lists
  departments: any[] = [];
  employees: any[] = [];
  
  // Loaders
  loadingDepartments = false;
  loadingEmployees = false;

  // Forms data
  newDepartment = { name: '' };
  newEmployee = {
    name: '', email: '', department_id: '', position: '', salary: null, phone: '', hire_date: ''
  };
  attendanceData = {
    employee_id: '', date: '', status: '', check_in_time: '', check_out_time: ''
  };

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    // Usually fetch initial dashboard stats here
    this.loadStatsMock();
  }

  setTab(tab: string) {
    this.activeTab = tab;
    if (tab === 'departments' && this.departments.length === 0) {
      this.loadDepartmentsMock();
    } else if (tab === 'employees' && this.employees.length === 0) {
      this.loadEmployeesMock();
    }
  }

  loadStatsMock() {
    this.stats = {
      totalEmployees: 42,
      totalDepartments: 8,
      presentToday: 38,
      pendingLeaves: 3
    };
  }

  loadDepartmentsMock() {
    this.loadingDepartments = true;
    setTimeout(() => {
      this.departments = [
        { id: 1, name: 'Engineering', createdDate: '2025-01-10' },
        { id: 2, name: 'Marketing', createdDate: '2025-02-15' }
      ];
      this.loadingDepartments = false;
    }, 500);
  }

  loadEmployeesMock() {
    this.loadingEmployees = true;
    setTimeout(() => {
      this.employees = [
        { name: 'Alice Smith', email: 'alice@example.com', department: 'Engineering', position: 'Developer', hireDate: '2025-03-01', salary: '85000' },
        { name: 'Bob Jones', email: 'bob@example.com', department: 'Marketing', position: 'Analyst', hireDate: '2025-04-12', salary: '72000' }
      ];
      this.loadingEmployees = false;
    }, 500);
  }

  onAddDepartment() {
    if (!this.newDepartment.name) return;
    this.departments.push({
      id: this.departments.length + 1,
      name: this.newDepartment.name,
      createdDate: new Date().toISOString().split('T')[0]
    });
    this.newDepartment.name = '';
    alert('Department added successfully!');
  }

  onAddEmployee() {
    if (!this.newEmployee.name || !this.newEmployee.email) return;
    this.employees.push({
      name: this.newEmployee.name,
      email: this.newEmployee.email,
      department: 'Assigned', // map id in real app
      position: this.newEmployee.position,
      hireDate: this.newEmployee.hire_date,
      salary: this.newEmployee.salary || 0
    });
    // Reset form
    this.newEmployee = { name: '', email: '', department_id: '', position: '', salary: null, phone: '', hire_date: '' };
    alert('Employee added successfully!');
  }

  onMarkAttendance() {
    if (!this.attendanceData.employee_id || !this.attendanceData.date || !this.attendanceData.status) return;
    alert('Attendance marked successfully!');
  }

  logout() {
    if (confirm('Are you sure you want to logout?')) {
      window.location.href = '/logout';
    }
  }
}
