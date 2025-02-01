import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeaderComponent } from './components/header/header.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, HeaderComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  template: `
    <app-header></app-header>
    <router-outlet></router-outlet>
  `,// Renders the active route
  standalone: true,
})
export class AppComponent {
  title = 'wado-frontend-app';
}

