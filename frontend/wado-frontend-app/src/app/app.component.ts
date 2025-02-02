import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeaderComponent } from './components/header/header.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, HeaderComponent, FontAwesomeModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  template: `
    <app-header></app-header>
    <router-outlet></router-outlet>
  `,// Renders the active route
  standalone: true,
})
export class AppComponent implements OnInit {
  title = 'wado-frontend-app';

  ngOnInit(): void {
    if (this.safeDocumentAccess()) {

      const burger = document.querySelector('.navbar-burger');
      const menu = document.querySelector('.navbar-menu');

      if (burger && menu) {
        burger.addEventListener('click', () => {
          burger.classList.toggle('is-active');
          menu.classList.toggle('is-active');
        });
      }
    }
  }

  safeDocumentAccess() {
    if (typeof document !== 'undefined') {
      // Your code that accesses the document object
      return true;
    }
    return false;
  }

}



