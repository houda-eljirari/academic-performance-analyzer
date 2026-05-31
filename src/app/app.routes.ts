import { Routes } from '@angular/router';
import { Dashboard } from './pages/dashboard/dashboard';
import { Students } from './pages/students/students';
import { Grades } from './pages/grades/grades';
import { Login } from './pages/login/login';
import { Predictions } from './pages/predictions/predictions';
import { Alerts } from './pages/alerts/alerts';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: Login },
  { path: 'dashboard', component: Dashboard },
  { path: 'students', component: Students },
  { path: 'grades', component: Grades },
  { path: 'predictions', component: Predictions },
  { path: 'alerts', component: Alerts },
];