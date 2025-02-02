import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-framework-info',
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './framework-info.component.html',
  styleUrl: './framework-info.component.css',
  standalone: true,
})
export class FrameworkInfoComponent {
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
    this.http.get<{languages: string[]}>('http://127.0.0.1:5000/api/ontology/languages')
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

    this.http.get<{frameworks: string[]}>(`http://127.0.0.1:5000/api/ontology/frameworks?language=${this.selectedKeyword}`)
      .subscribe({
        next: (response) => {
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
