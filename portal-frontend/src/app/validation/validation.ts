import { Component, OnInit, Renderer2, Inject } from '@angular/core';
import { CommonModule, DOCUMENT } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-validation',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './validation.html',
  styleUrl: './validation.css',
})
export class Validation implements OnInit {
  isMobileMenuOpen = false;

  assessments = [
    {
      id: 1,
      title: 'Assessment 1: JavaScript Fundamentals',
      icon: 'fa-code',
      duration: '45 minutes',
      difficulty: 'Beginner',
      description: 'Test your knowledge of JavaScript basics including variables, data types, functions, and control structures.',
      link: 'https://karthikeyan-210701111.github.io/Vcodez_student_portal/config.seb',
      status: 'pending'
    },
    {
      id: 2,
      title: 'Assessment 2: Advanced JavaScript',
      icon: 'fa-puzzle-piece',
      duration: '60 minutes',
      difficulty: 'Intermediate',
      description: 'Demonstrate your skills with advanced JavaScript concepts including closures, promises, async/await, and DOM manipulation.',
      link: 'your-assessment2.seb',
      status: 'pending'
    },
    {
      id: 3,
      title: 'Assessment 3: Full-Stack Development',
      icon: 'fa-project-diagram',
      duration: '90 minutes',
      difficulty: 'Advanced',
      description: 'Showcase your ability to build a complete web application with front-end and back-end components.',
      link: 'your-assessment3.seb',
      status: 'pending'
    },
    {
      id: 4,
      title: 'Final Validation: Comprehensive Evaluation',
      icon: 'fa-award',
      duration: '120 minutes',
      difficulty: 'Expert',
      description: 'Complete a comprehensive evaluation that tests all aspects of your development skills. Successful completion will earn you a certified developer certificate.',
      link: 'your-final-validation.seb',
      status: 'final'
    }
  ];

  constructor(private renderer: Renderer2, @Inject(DOCUMENT) private document: Document) {}

  ngOnInit(): void {
    this.initializeParticles();
  }

  toggleMobileMenu() {
    this.isMobileMenuOpen = !this.isMobileMenuOpen;
  }

  initializeParticles() {
    const particlesContainer = this.document.getElementById('particles');
    if (!particlesContainer) return;
    
    // Clear existing particles
    particlesContainer.innerHTML = '';

    const particleCount = 15;
    for (let i = 0; i < particleCount; i++) {
      const particle = this.renderer.createElement('div');
      this.renderer.addClass(particle, 'particle');
      
      const size = Math.random() * 150 + 50 + 'px';
      this.renderer.setStyle(particle, 'width', size);
      this.renderer.setStyle(particle, 'height', size);
      this.renderer.setStyle(particle, 'left', Math.random() * 100 + '%');
      this.renderer.setStyle(particle, 'top', Math.random() * 100 + '%');
      this.renderer.setStyle(particle, 'animation-delay', Math.random() * 5 + 's');
      
      this.renderer.appendChild(particlesContainer, particle);
    }
  }

  logout(event?: Event) {
    if (event) event.preventDefault();
    if (confirm('Are you sure you want to logout?')) {
      window.location.href = '/logout';
    }
  }
}
