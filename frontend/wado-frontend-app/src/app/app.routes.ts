import { Routes } from '@angular/router';
import { RegisterComponent } from './components/register/register.component';
import { WelcomeComponent } from './components/welcome/welcome.component';
import { LoginComponent } from './components/login/login.component';
import { ConceptPageComponent } from './components/pages/concept-page/concept-page.component';

export const routes: Routes = [
  { path: '', redirectTo: '/welcome', pathMatch: 'full' }, // Default page
  { path: 'welcome', component: WelcomeComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  { path: 'concept-page', component: ConceptPageComponent },
];
