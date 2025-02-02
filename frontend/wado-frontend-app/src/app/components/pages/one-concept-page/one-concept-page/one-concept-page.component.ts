import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { extractName } from '../../../utils/string-utils';

@Component({
  selector: 'app-one-concept-page',
  imports: [CommonModule, HttpClientModule, RouterModule],
  templateUrl: './one-concept-page.component.html',
  styleUrls: ['./one-concept-page.component.css'],
  standalone: true,
})
export class OneConceptPageComponent implements OnInit {
  private http = inject(HttpClient);
  private route = inject(ActivatedRoute);

  conceptUri: string = '';
  conceptData: { property: string, value: string }[] = [];
  errorMessage: string = '';  // if any
  extractName = extractName; // Expose function to the template
  links: { key: string, value: string }[] = [];


  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.conceptUri = params['uri'];
      if (this.conceptUri) {
        this.fetchConceptDetails();
      } else {
        this.errorMessage = 'No concept URI provided!';
      }
    });
  }

  fetchConceptDetails(): void {
    this.http.get<any>(`http://127.0.0.1:5000/api/ontology/concept?uri=${encodeURIComponent(this.conceptUri)}`)
      .subscribe({
        next: (response) => {
          this.extractData(response);
          this.errorMessage = '';
        },
        error: () => {
          this.errorMessage = 'Error fetching data. Check the concept URI!';
          this.conceptData = [];
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

