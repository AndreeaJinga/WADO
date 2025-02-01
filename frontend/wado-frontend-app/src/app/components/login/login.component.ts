import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  imports: [CommonModule, ReactiveFormsModule, RouterModule, HttpClientModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  standalone: true,
})
export class LoginComponent {
  loginForm: FormGroup;
  message: string = '';

  constructor(private fb: FormBuilder, private http: HttpClient, private router: Router) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
    });
  }

  onSubmit(): void {
    if (this.loginForm.valid) {
      this.http.post<{ token: string }>('http://127.0.0.1:5000/api/auth/login', this.loginForm.value)
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

