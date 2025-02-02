import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';
import { Router, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { extractName, BASE_URL } from '../../../utils/string-utils';

@Component({
  selector: 'app-sparql-query',
  imports: [CommonModule, HttpClientModule, FormsModule, RouterModule],
  templateUrl: './sparql-query.component.html',
  styleUrl: './sparql-query.component.css',
  standalone: true,
})
export class SparqlQueryComponent implements OnInit {
  private http = inject(HttpClient);
  private router = inject(Router);

  query: string = '';
  resultData: { object:string, property: string, value: string }[] = [];
  userEmail: string | null = null;
  errorMessage: string = '';
  extractName = extractName; // Expose function to the template

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

    this.http.post<{ results: { object: string, property: string, value: string }[] }>(
      `${BASE_URL}/ontology/sparql`,
      { query: this.query, email_bool: false },
      { headers }
    ).subscribe({
      next: (response) => {
        if (response.results && response.results.length > 0) {
          this.resultData = response.results.map(item => ({
            object: item.object,
            property: item.property,
            value: item.value,
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

    this.http.post<{ results: { object: string, property: string, value: string }[] }>(
      `${BASE_URL}/ontology/sparql`,
      { query: this.query, email_bool: true },
      { headers }
    ).subscribe({
      next: (response) => {
        if (response.results && response.results.length > 0) {
          this.resultData = response.results.map(item => ({
            object: item.object,
            property: item.property,
            value: item.value,
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
