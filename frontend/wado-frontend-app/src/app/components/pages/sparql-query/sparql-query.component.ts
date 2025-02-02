import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-sparql-query',
  imports: [CommonModule, HttpClientModule, FormsModule],
  templateUrl: './sparql-query.component.html',
  styleUrl: './sparql-query.component.css',
  standalone: true,
})
export class SparqlQueryComponent implements OnInit {
  private http = inject(HttpClient);
  private router = inject(Router);

  query: string = '';
  resultData: { property: string, value: string }[] = [];
  userEmail: string | null = null;
  errorMessage: string = '';

  constructor() {
  }

  ngOnInit() {
    this.checkUser();
  }

  checkUser() {
    if (typeof localStorage !== 'undefined') {
      const token = localStorage.getItem('token');
      if (token) {
        this.userEmail = localStorage.getItem('email') || 'User';
      }
      else {
        this.router.navigate(['/login']);
      }
    }
    else {
      this.router.navigate(['/login']);
    }
  }

  submitQuery(): void {
    if (!this.query.trim()) {
      this.errorMessage = 'Please enter a SPARQL query!';
      return;
    }

    const token = localStorage.getItem('token');
    if (!token) {
      this.errorMessage = 'Authentication token is missing. Please log in.';
      this.router.navigate(['/login']);
      return;
    }

    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);

    this.http.post<{ results: { Framework: string }[] }>(
      'http://127.0.0.1:5000/api/ontology/sparql',
      { query: this.query, email_bool: false },
      { headers }
    ).subscribe({
      next: (response) => {
        if (response.results && response.results.length > 0) {
          this.resultData = response.results.map(item => ({
            property: "Framework",
            value: item.Framework
          }));
        } else {
          this.resultData = [];
        }
        this.errorMessage = '';
      },
      error: () => {
        this.errorMessage = 'Error fetching data. Check your query!';
        this.resultData = [];
      }
    });

  }

  sendEmail(): void {
    if (!this.query.trim()) {
      this.errorMessage = 'Please enter a SPARQL query!';
      return;
    }

    const token = localStorage.getItem('token');
    if (!token) {
      this.errorMessage = 'Authentication token is expired. Please log in.';
      this.router.navigate(['/login']);
      return;
    }

    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);

    this.http.post<{ results: { Framework: string }[] }>(
      'http://127.0.0.1:5000/api/ontology/sparql',
      { query: this.query, email_bool: true },
      { headers }
    ).subscribe({
      next: (response) => {
        if (response.results && response.results.length > 0) {
          this.resultData = response.results.map(item => ({
            property: "Framework",
            value: item.Framework
          }));
        } else {
          this.resultData = [];
        }
        this.errorMessage = '';
      },
      error: () => {
        this.errorMessage = 'Error fetching data. Check your query!';
        this.resultData = [];
      }
    });
  }
}
