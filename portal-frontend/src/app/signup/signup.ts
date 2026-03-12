import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './signup.html',
  styleUrl: './signup.css'
})
export class Signup {
  signupData = {
    name: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: ''
  };
  
  message = { text: '', type: '' };

  constructor(private http: HttpClient, private router: Router) {}

  handleSignup() {
    if (this.signupData.password !== this.signupData.confirmPassword) {
      this.message = { text: 'Passwords do not match', type: 'error' };
      return;
    }
    
    // In a real app, this would call the Flask API
    console.log('Signup Attempt:', this.signupData);
    this.message = { text: '✓ Account created successfully! (Mock Action)', type: 'success' };
    
    setTimeout(() => {
      this.router.navigate(['/']);
    }, 2000);
  }
}
