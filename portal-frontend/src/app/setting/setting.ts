import { Component, OnInit, Renderer2, Inject } from '@angular/core';
import { CommonModule, DOCUMENT } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-setting',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './setting.html',
  styleUrl: './setting.css',
})
export class Setting implements OnInit {
  activeTab = 'account';
  isMobileMenuOpen = false;

  // Account Settings
  studentData = {
    name: 'John Doe',
    email: 'john.doe@example.com',
    phone: '+1 234 567 8900',
    language: 'english',
    timezone: 'utc-5'
  };

  // Appearance Settings
  appearance = {
    darkMode: false,
    themeColor: 'blue',
    fontSize: 'medium',
    reduceAnimations: false
  };

  // Notification Settings
  notifications = {
    email: true,
    push: true,
    sms: false,
    marketing: false
  };

  // Security Settings
  security = {
    twoFactor: false,
    twoFactorMethod: 'app',
    sessionTimeout: '30'
  };

  themes: any = {
    blue: { primary: '#667eea', primaryLight: '#764ba2' },
    purple: { primary: '#8b5cf6', primaryLight: '#6d28d9' },
    green: { primary: '#10b981', primaryLight: '#047857' },
    red: { primary: '#ef4444', primaryLight: '#b91c1c' },
    orange: { primary: '#f59e0b', primaryLight: '#d97706' }
  };

  constructor(private renderer: Renderer2, @Inject(DOCUMENT) private document: Document) {}

  ngOnInit(): void {
    this.loadSettings();
    this.initializeParticles();
  }

  loadSettings() {
    // Load individual settings from localStorage
    this.appearance.darkMode = localStorage.getItem('dark-mode') === 'enabled';
    this.appearance.themeColor = localStorage.getItem('theme-color') || 'blue';
    this.appearance.fontSize = localStorage.getItem('font-size') || 'medium';
    this.appearance.reduceAnimations = localStorage.getItem('reduce-animations') === 'enabled';

    // Apply active settings
    this.applyAppearance();
  }

  saveSettings() {
    // Save appearance to localStorage
    localStorage.setItem('dark-mode', this.appearance.darkMode ? 'enabled' : 'disabled');
    localStorage.setItem('theme-color', this.appearance.themeColor);
    localStorage.setItem('font-size', this.appearance.fontSize);
    localStorage.setItem('reduce-animations', this.appearance.reduceAnimations ? 'enabled' : 'disabled');

    this.applyAppearance();
    alert('Settings saved successfully!');
  }

  applyAppearance() {
    const body = this.document.body;
    const root = this.document.documentElement;

    // Dark Mode
    if (this.appearance.darkMode) {
      this.renderer.addClass(body, 'dark-mode');
    } else {
      this.renderer.removeClass(body, 'dark-mode');
    }

    // Font Size
    this.renderer.removeClass(body, 'font-small');
    this.renderer.removeClass(body, 'font-medium');
    this.renderer.removeClass(body, 'font-large');
    this.renderer.addClass(body, `font-${this.appearance.fontSize}`);

    // Reduce Animations
    if (this.appearance.reduceAnimations) {
      this.renderer.addClass(body, 'reduce-animations');
    } else {
      this.renderer.removeClass(body, 'reduce-animations');
    }

    // Theme Color
    const theme = this.themes[this.appearance.themeColor];
    if (theme) {
      root.style.setProperty('--primary', theme.primary);
      root.style.setProperty('--primary-light', theme.primaryLight);
    }
  }

  setTab(tab: string) {
    this.activeTab = tab;
  }

  setThemeColor(color: string) {
    this.appearance.themeColor = color;
    this.applyAppearance();
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
