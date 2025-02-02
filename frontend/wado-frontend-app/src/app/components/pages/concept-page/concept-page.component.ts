import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { extractName } from '../../../utils/string-utils';

@Component({
  selector: 'app-concept-page',
  imports: [CommonModule, FormsModule, HttpClientModule, RouterModule],
  templateUrl: './concept-page.component.html',
  styleUrls: ['./concept-page.component.css'],
  standalone: true,
})
export class ConceptPageComponent {
  extractName = extractName; // Expose function to the template
  user_url: string = '';
  conceptUri: string = '';
  links: { key: string, value: string }[] = [];
  errorMessage: string = '';  // if any

  constructor(private http: HttpClient) { }

  submitUrl(): void {
    if (!this.user_url.trim()) {
      this.errorMessage = 'Please enter a valid URL!';
      return;
    }

    this.http.get<any>(`http://127.0.0.1:5000/api/ontology/concept?uri=${encodeURIComponent(this.user_url)}`)
      .subscribe({
        next: (response) => {
          this.extractData(response);
          this.errorMessage = '';  // Clear errors
        },
        error: () => {
          this.errorMessage = 'Error processing URL. Try again!';
          this.conceptUri = '';
          this.links = [];
        }
      });
  }

  extractData(data: any): void {
    if (!data || !data.concept_uri || !data.info) {
      this.errorMessage = 'Invalid data format';
      return;
    }

    this.conceptUri = data.concept_uri;

    this.links = Object.entries(data.info)
      .filter(([_, value]) => typeof value === 'string' && value.startsWith('http'))
      .map(([key, value]) => ({ key, value: value as string })); 
  }
}
