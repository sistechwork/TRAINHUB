import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

interface Topic {
  id: string;
  domain: string;
  title: string;
  description: string;
  label: string;
  link?: string;
}

@Component({
  selector: 'app-learning',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './learning.html',
  styleUrl: './learning.css',
})
export class Learning implements OnInit {
  activeDomain = 'machine-learning';
  searchTerm = '';
  isMobileMenuOpen = false;

  topics: Topic[] = [
    {
      id: 'ml-libs',
      domain: 'machine-learning',
      title: 'ML Libraries',
      description: 'Learn about Python libraries essential for ML: Scikit-learn, TensorFlow, PyTorch, etc.',
      label: 'Beginner',
      link: 'https://drive.google.com/file/d/19MbycgLNLAJfy37qo73rGf_05_DQIWVh/view?usp=sharing'
    },
    {
      id: 'eda',
      domain: 'machine-learning',
      title: 'Exploratory Data Analysis',
      description: 'Master the techniques of data exploration and visualization to understand your datasets.',
      label: 'Intermediate',
      link: 'https://drive.google.com/file/d/14aTPx0Re5Y_HGYRGjD7iRxXcw8DEXdfn/view?usp=sharing'
    },
    {
      id: 'feature-eng',
      domain: 'machine-learning',
      title: 'Feature Engineering',
      description: 'Learn how to transform raw data into features that improve model performance.',
      label: 'Intermediate',
      link: 'https://drive.google.com/file/d/1Un3WAB_-Fu5_G8Xms6VmHFYzVSuWee1x/view?usp=sharing'
    },
    {
      id: 'ml-models',
      domain: 'machine-learning',
      title: 'ML Models',
      description: 'Understand different ML algorithms and when to use them for various problems.',
      label: 'Advanced'
    },
    {
      id: 'deployment',
      domain: 'machine-learning',
      title: 'Model Deployment',
      description: 'Learn to deploy machine learning models to production environments.',
      label: 'Advanced'
    },
    {
      id: 'deep-learning',
      domain: 'machine-learning',
      title: 'Deep Learning',
      description: 'Explore neural networks, CNNs, RNNs, and transformers for complex learning tasks.',
      label: 'Advanced'
    },
    // Data Science Topics
    {
      id: 'data-processing',
      domain: 'data-science',
      title: 'Data Processing',
      description: 'Learn techniques for cleaning, transforming, and preparing data for analysis.',
      label: 'Beginner'
    },
    {
      id: 'stat-analysis',
      domain: 'data-science',
      title: 'Statistical Analysis',
      description: 'Master statistical methods and hypothesis testing for data analysis.',
      label: 'Intermediate'
    },
    {
      id: 'data-viz',
      domain: 'data-science',
      title: 'Data Visualization',
      description: 'Create compelling visual representations of data using Matplotlib, Seaborn, and Plotly.',
      label: 'Intermediate'
    },
    {
      id: 'big-data',
      domain: 'data-science',
      title: 'Big Data Tools',
      description: 'Learn tools like Hadoop, Spark, and distributed computing for large datasets.',
      label: 'Advanced'
    },
    {
      id: 'nlp',
      domain: 'data-science',
      title: 'NLP',
      description: 'Process and analyze text data using natural language processing techniques.',
      label: 'Advanced'
    },
    {
      id: 'time-series',
      domain: 'data-science',
      title: 'Time Series Analysis',
      description: 'Analyze time-dependent data and make forecasts using specialized techniques.',
      label: 'Advanced'
    },
    // Data Analytics Topics
    {
      id: 'sql-fundamentals',
      domain: 'data-analytics',
      title: 'SQL Fundamentals',
      description: 'Master SQL for querying, manipulating, and analyzing data in databases.',
      label: 'Beginner'
    },
    {
      id: 'bi',
      domain: 'data-analytics',
      title: 'Business Intelligence',
      description: 'Learn how to use BI tools to gain insights from data.',
      label: 'Intermediate'
    },
    {
      id: 'excel-analytics',
      domain: 'data-analytics',
      title: 'Excel for Analytics',
      description: 'Advanced Excel techniques for data analysis, including PivotTables and formulas.',
      label: 'Beginner'
    },
    {
      id: 'data-driven-decisions',
      domain: 'data-analytics',
      title: 'Data-Driven Decisions',
      description: 'Learn frameworks for using data to inform business decisions.',
      label: 'Advanced'
    },
    {
      id: 'ab-testing',
      domain: 'data-analytics',
      title: 'A/B Testing',
      description: 'Design and analyze experiments to optimize products and services.',
      label: 'Intermediate'
    }
  ];

  constructor() {}

  ngOnInit(): void {}

  setDomain(domain: string) {
    this.activeDomain = domain;
  }

  toggleMobileMenu() {
    this.isMobileMenuOpen = !this.isMobileMenuOpen;
  }

  get filteredTopics() {
    return this.topics.filter(topic => {
      const matchesSearch = topic.title.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
                           topic.description.toLowerCase().includes(this.searchTerm.toLowerCase());
      const matchesDomain = topic.domain === this.activeDomain;
      return matchesSearch && matchesDomain;
    });
  }

  getDomainDisplayName() {
    return this.activeDomain.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  }

  onTopicClick(topic: Topic) {
    if (topic.link) {
      window.open(topic.link, '_blank');
    } else {
      alert(`You selected: ${topic.title}. This would navigate to the topic page.`);
    }
  }

  logout() {
    if (confirm('Are you sure you want to logout?')) {
      window.location.href = '/logout';
    }
  }
}
