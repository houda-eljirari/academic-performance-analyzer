import { Component, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { ApiService } from '../../core/services/api';
import { LucideAngularModule,
         Users, TrendingUp, AlertTriangle, UserMinus,
         Award, CheckCircle, XCircle, BookOpen,
         Activity, ClipboardList, AlertCircle,
         UserPlus, BrainCircuit } from 'lucide-angular';

@Component({
  selector:    'app-dashboard',
  standalone:  true,
  imports:     [CommonModule, DatePipe, LucideAngularModule],
  templateUrl: './dashboard.html',
  styleUrls:   ['./dashboard.scss']
})
export class DashboardComponent implements OnInit {

  // Icônes Lucide
  readonly Users         = Users;
  readonly TrendingUp    = TrendingUp;
  readonly AlertTriangle = AlertTriangle;
  readonly UserMinus     = UserMinus;
  readonly Award         = Award;
  readonly CheckCircle   = CheckCircle;
  readonly XCircle       = XCircle;
  readonly BookOpen      = BookOpen;
  readonly Activity      = Activity;
  readonly ClipboardList = ClipboardList;
  readonly AlertCircle   = AlertCircle;
  readonly UserPlus      = UserPlus;
  readonly BrainCircuit  = BrainCircuit;

  today   = new Date();
  loading = false;

  stats = {
    totalStudents:    0,
    avgGrade:         0,
    atRiskStudents:   0,
    pendingAlerts:    0,
    passRate:         0,
    failRate:         0,
    withdrawnRate:    0,
    distinctionCount: 0,
    passCount:        0,
    failCount:        0,
    withdrawnCount:   0,
    disabledStudents: 0,
    avgCredits:       0,
  };

  recentActivity = [
    { student: 'Abdessamad Benhiri', action: 'Grade submitted',    subject: 'Mathematics', time: '2 min ago',  type: 'grade'      },
    { student: 'Aya Benhadi',        action: 'At-risk detected',   subject: 'Physics',     time: '15 min ago', type: 'alert'      },
    { student: 'Safaa Bennani',      action: 'New enrollment',     subject: 'CS Dept.',    time: '1h ago',     type: 'student'    },
    { student: 'Ali Jbira',          action: 'Prediction updated', subject: 'Semester 2',  time: '2h ago',     type: 'prediction' },
  ];

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    fetch('http://localhost:8000/api/analytics/stats/')
      .then(r => r.json())
      .then(data => {
        const dist = data.result_distribution || {};
        this.stats = {
          totalStudents:    data.total_students,
          avgGrade:         data.pass_rate,
          atRiskStudents:   dist.Fail        || 0,
          pendingAlerts:    dist.Withdrawn   || 0,
          passRate:         data.pass_rate,
          failRate:         data.fail_rate,
          withdrawnRate:    data.withdrawn_rate,
          distinctionCount: dist.Distinction || 0,
          passCount:        dist.Pass        || 0,
          failCount:        dist.Fail        || 0,
          withdrawnCount:   dist.Withdrawn   || 0,
          disabledStudents: data.disabled_students,
          avgCredits:       data.avg_studied_credits,
        };
      })
      .catch(() => {
        console.log('API indisponible — données statiques');
      });
  }
}