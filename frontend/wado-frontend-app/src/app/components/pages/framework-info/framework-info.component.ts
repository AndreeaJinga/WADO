import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { extractName, BASE_URL } from '../../../utils/string-utils';

@Component({
  selector: 'app-framework-info',
  imports: [CommonModule, FormsModule, HttpClientModule, RouterModule],
  templateUrl: './framework-info.component.html',
  styleUrl: './framework-info.component.css',
  standalone: true,
})
export class FrameworkInfoComponent {
  extractName = extractName; // Expose function to the template
  keywords: string[] = [];
  keyword_links: string[] = [];
  selectedKeyword: string = '';
  jsonResponse: string[] = [];
  errorMessage: string = ''; // if any
  current_chosen_keyword: string = '';

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.fetchKeywords();
  }


  fetchKeywords(): void {
    this.http.get<{ languages: string[] }>(`${BASE_URL}/ontology/languages`)
      .subscribe({
        next: (response) => {
          this.keyword_links = response.languages;
          this.keywords = response.languages.map(link => link.split('#')[1]); // Extract names
        },
        error: () => {
          this.errorMessage = 'Error fetching keywords. Try again!';
        }
      });
  }

  searchLanguage(): void {
    if (!this.selectedKeyword) {
      this.errorMessage = 'Please enter a language!';
      return;
    }

    this.http.get<{ frameworks: any }>(`${BASE_URL}/ontology/frameworks?language=${this.selectedKeyword}`)
      .subscribe({
        next: (response) => {
          this.current_chosen_keyword = this.selectedKeyword;
          this.jsonResponse = response.frameworks || 'No result found';
          this.errorMessage = ''; // Clear errors
        },
        error: () => {
          this.errorMessage = 'Error fetching data. Try again!';
          this.jsonResponse = [];
        }
      });
  }
}
