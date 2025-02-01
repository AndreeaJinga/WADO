import { Component, OnInit } from '@angular/core';
import { RouterModule, Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-header',
  imports: [CommonModule, RouterModule],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css'],
  standalone: true,
})
export class HeaderComponent implements OnInit {
  userEmail: string | null = null;

  constructor(private router: Router) { }

  ngOnInit(): void {
    this.checkUser();
  }

  checkUser(): void {
    if (typeof localStorage !== 'undefined') {
      const token = localStorage.getItem('token');
      if (token) {
        this.userEmail = localStorage.getItem('email') || 'User';
      }
      else {
        this.userEmail = null;
      }
    }
  }

  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('email');
    this.userEmail = null;
    this.router.navigate(['/welcome']);
  }
}
