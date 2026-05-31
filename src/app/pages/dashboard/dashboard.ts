import { Component } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, DatePipe],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.scss']
})
export class DashboardComponent {

  today = new Date();

  stats = {
    totalStudents: 248,
    avgGrade: 14.3,
    atRiskStudents: 18,
    pendingAlerts: 5
  };

  recentActivity = [
    { student: 'Abdessamad Benhiri', action: 'Grade submitted', subject: 'Mathematics', time: '2 min ago', type: 'grade' },
    { student: 'Aya Benhadi', action: 'At-risk detected', subject: 'Physics', time: '15 min ago', type: 'alert' },
    { student: 'Safaa Bennani', action: 'New enrollment', subject: 'CS Dept.', time: '1h ago', type: 'student' },
    { student: 'Ali Jbira', action: 'Prediction updated', subject: 'Semester 2', time: '2h ago', type: 'prediction' },
  ];
}