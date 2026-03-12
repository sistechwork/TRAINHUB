import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class LoginComponent {
  loginData = {
    email: '',
    phone: '',
    password: ''
  };

  isAdmin = false;
  isLoading = false;
  message = { text: '', type: '' };

  constructor(private http: HttpClient, private router: Router) { }

  toggleAdmin() {
    this.isAdmin = !this.isAdmin;
    this.message = { text: '', type: '' };
  }

  handleLogin() {
    this.message = { text: '', type: '' };

    if (!this.loginData.email) {
      this.message = { text: 'Email is required', type: 'error' };
      return;
    }

    if (this.isAdmin && !this.loginData.password) {
      this.message = { text: 'Password is required for admin', type: 'error' };
      return;
    }

    if (!this.isAdmin && !this.loginData.phone) {
      this.message = { text: 'Phone number is required', type: 'error' };
      return;
    }

    this.isLoading = true;
    
    const payload: any = {
      email: this.loginData.email
    };

    if (this.isAdmin) {
      payload.password = this.loginData.password;
    } else {
      payload.phone = this.loginData.phone;
    }

    // Call the Flask backend API
    this.http.post<any>('/login', payload).subscribe({
      next: (data) => {
        this.isLoading = false;
        if (data.success) {
          this.message = { text: 'Login successful! Redirecting...', type: 'success' };
          
          if (data.type === 'admin') {
            this.router.navigate(['/admin-dashboard']);
          } else {
            this.router.navigate(['/details']);
          }
        } else {
          this.message = { text: data.message || 'Invalid credentials', type: 'error' };
        }
      },
      error: (err) => {
        this.isLoading = false;
        this.message = { text: 'Connection error. Please ensure the backend is running.', type: 'error' };
        console.error('Login error:', err);
      }
    });
  }
}
