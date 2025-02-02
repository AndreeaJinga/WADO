import { Routes } from '@angular/router';
import { RegisterComponent } from './components/register/register.component';
import { WelcomeComponent } from './components/welcome/welcome.component';
import { LoginComponent } from './components/login/login.component';
import { ConceptPageComponent } from './components/pages/concept-page/concept-page.component';
import { FrameworkInfoComponent } from './components/pages/framework-info/framework-info.component';
import { InstancesComponent } from './components/pages/instances/instances.component';
import { SparqlQueryComponent } from './components/pages/sparql-query/sparql-query.component';
import { OneConceptPageComponent } from './components/pages/one-concept-page/one-concept-page.component';

export const routes: Routes = [
  { path: '', redirectTo: '/welcome', pathMatch: 'full' }, // Default page
  { path: 'welcome', component: WelcomeComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  { path: 'concept-page', component: ConceptPageComponent },
  { path: 'framework-info', component: FrameworkInfoComponent },
  { path: 'instances', component: InstancesComponent },
  { path: 'sparql-query', component: SparqlQueryComponent },
  { path: 'one-concept-page', component: OneConceptPageComponent },
];
