import { Routes } from '@angular/router';
import { DashboardComponent } from './pages/dashboard/dashboard';
import { LoginComponent } from './pages/login/login';
import { StudentsComponent } from './pages/students/students';
import { StudentProfile } from './pages/student-profile/student-profile';
import { Grades } from './pages/grades/grades';
import { Predictions } from './pages/predictions/predictions';
import { Alerts } from './pages/alerts/alerts';
import { CsvImport } from './pages/csv-import/csv-import';
import { Shap } from './pages/shap/shap';

export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'students', component: StudentsComponent },
  { path: 'students/:id', component: StudentProfile },
  { path: 'grades', component: Grades },
  { path: 'predictions', component: Predictions },
  { path: 'alerts', component: Alerts },
  { path: 'csv-import', component: CsvImport },
  { path: 'shap', component: Shap },
  { path: '**', redirectTo: '/dashboard' }
];