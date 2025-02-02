import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { extractName, BASE_URL } from '../../../utils/string-utils';

@Component({
  selector: 'app-instances',
  imports: [CommonModule, FormsModule, HttpClientModule, RouterModule],
  templateUrl: './instances.component.html',
  styleUrl: './instances.component.css',
  standalone: true,
})
export class InstancesComponent {
  extractName = extractName; // Expose function to the template
  keywords: string[] = [];
  keyword_links: string[] = [];
  selectedKeyword: string = '';
  jsonResponse: string[] = [];
  errorMessage: string = ''; // if any

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.fetchKeywords();
  }

  fetchKeywords(): void {
    this.http.get<string[]>(`${BASE_URL}/ontology/classes`)
      .subscribe({
        next: (response: string[]) => {
          this.keyword_links = response;
          this.keywords = response.map(link => {
            const parts = link.split('/');
            return parts[parts.length - 1] || ''; 
          });
        },
        error: () => {
          this.errorMessage = 'Error fetching classes. Try again!';
        }
      });
  }

  searchInstances(): void {
    if (!this.selectedKeyword) {
      this.errorMessage = 'Please enter a class type!';
      return;
    }

  const selectedLink = this.keyword_links[this.keywords.indexOf(this.selectedKeyword)];

  if (!selectedLink) {
    this.errorMessage = 'Invalid selection!';
    return;
  }

  const encodedLink = encodeURIComponent(selectedLink);

    this.http.get<{instances: string[]}>(`${BASE_URL}/ontology/class/${encodedLink}/instances`)
      .subscribe({
        next: (response) => {
          this.jsonResponse = response.instances || 'No result found';
          this.errorMessage = ''; // Clear errors
        },
        error: () => {
          this.errorMessage = 'Error fetching data. Try again!';
          this.jsonResponse = [];
        }
      });
  }
}
