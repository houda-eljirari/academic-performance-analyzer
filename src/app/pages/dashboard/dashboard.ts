import { Component, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { ApiService } from '../../core/services/api';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, DatePipe],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.scss']
})
export class DashboardComponent implements OnInit {

  today = new Date();

  // Données statiques par défaut — remplacées par l'API si disponible
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

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    // Appel API — fonctionne quand le backend Django est lancé
    this.api.get<any>('analytics/stats/').subscribe({
      next: (data) => {
        this.stats = {
          totalStudents: data.total_students,
          avgGrade: data.avg_score,
          atRiskStudents: data.at_risk_count,
          pendingAlerts: data.pending_alerts
        };
      },
      error: () => {
        // Backend pas encore lancé → garde les données statiques
        console.log('API non disponible, données statiques utilisées');
      }
    });
  }
}