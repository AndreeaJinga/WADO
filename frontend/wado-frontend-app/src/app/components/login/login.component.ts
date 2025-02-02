import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule, FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { BASE_URL, extractName } from '../../utils/string-utils';

@Component({
  selector: 'app-login',
  imports: [CommonModule, ReactiveFormsModule, RouterModule, HttpClientModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  standalone: true,
})
export class LoginComponent {
  loginForm: FormGroup;
  message: string = '';
email: any;
password: any;

  constructor(private fb: FormBuilder, private http: HttpClient, private router: Router) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
    });
  }

  onSubmit(): void {
    if (this.loginForm.valid) {
      this.http.post<{ token: string }>(`${BASE_URL}/auth/login`, this.loginForm.value)
        .subscribe({
          next: (response) => {
            localStorage.setItem('token', response.token); // Store token
            this.message = 'Login successful!';
            this.router.navigate(['/welcome']); // Redirect to welcome page
          },
          error: () => {
            this.message = 'Invalid email or password!';
          },
        });
    }
  }
}

