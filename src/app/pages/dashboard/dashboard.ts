import { Component, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { ApiService } from '../../core/services/api';

interface DashboardStats {
  totalStudents: number;
  avgGrade: number;
  atRiskStudents: number;
  pendingAlerts: number;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, DatePipe],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.scss']
})
export class DashboardComponent implements OnInit {
  stats: DashboardStats = { totalStudents: 0, avgGrade: 0, atRiskStudents: 0, pendingAlerts: 0 };
  recentActivity: any[] = [];
  loading = true;
  today = new Date();

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    setTimeout(() => {
      this.stats = { totalStudents: 248, avgGrade: 14.3, atRiskStudents: 18, pendingAlerts: 5 };
      this.recentActivity = [
        { student: 'Abdessamad benhiri', action: 'Grade submitted', subject: 'Mathematics', time: '2 min ago', type: 'grade' },
        { student: 'Aya fatih', action: 'At-risk detected', subject: 'Physics', time: '15 min ago', type: 'alert' },
        { student: 'Chaimaa bannani', action: 'New enrollment', subject: 'CS Dept.', time: '1h ago', type: 'student' },
        { student: 'Ahmed bernis', action: 'Prediction updated', subject: 'Semester 2', time: '2h ago', type: 'prediction' },
      ];
      this.loading = false;
    }, 8);
  }
}