import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../../core/services/api';
import { LucideAngularModule, BrainCircuit, Sparkles, TrendingUp, CheckCircle, Users, AlertTriangle, Loader2 } from 'lucide-angular';

interface StudentPred {
  id:         number;
  name:       string;
  initials:   string;
  region:     string;
  filiere:    string;
  prediction: string;
  predClass:  string;
  confidence: number;
  riskLevel:  string;
  features:   any[];
}

@Component({
  selector:    'app-predictions',
  standalone:  true,
  imports:     [CommonModule, FormsModule, LucideAngularModule],
  templateUrl: './predictions.html',
  styleUrls:   ['./predictions.scss']
})
export class Predictions implements OnInit {
  readonly BrainCircuit  = BrainCircuit;
  readonly Sparkles      = Sparkles;
  readonly TrendingUp    = TrendingUp;
  readonly CheckCircle   = CheckCircle;
  readonly Users         = Users;
  readonly AlertTriangle = AlertTriangle;
  readonly Loader2       = Loader2;

  loading    = false;
  riskFilter = 'all';
  students:  StudentPred[] = [];

  constructor(private api: ApiService, private router: Router) {}

  ngOnInit(): void {
    this.loading = true;
    this.api.get<any>('students/').subscribe({
      next: (res) => {
        const list = res.results || res;
        if (list && list.length > 0) {
          this.students = list.slice(0, 10).map((s: any) => ({
            id:         s.id,
            name:       `Étudiant ${s.id_student || s.id}`,
            initials:   s.gender === 'M' ? 'M' : 'F',
            region:     s.region || 'Unknown Region',
            filiere:    s.course || s.filiere || 'Informatique',
            prediction: 'En cours...', // État d'attente textuel initial
            predClass:  'loading',     // Classe d'attente pour le CSS du badge
            confidence: 0,
            riskLevel:  '—',            // Valeur neutre pendant le chargement
            features:   [],
          }));

          // Déclenchement simultané des prédictions pour toutes les lignes
          this.students.forEach(s => this.loadPrediction(s));
        }
        this.loading = false;
      },
      error: (err) => { 
        console.error("Erreur lors de la récupération de la liste d'étudiants:", err);
        this.loading = false; 
      }
    });
  }

  loadPrediction(student: StudentPred): void {
    this.api.post<any>(`ml/predict/pk/${student.id}/`, {}).subscribe({
      next: (data) => {
        student.prediction = data.result === 'Pass' ? 'Succès' :
                             data.result === 'Fail' ? 'Échec'  : 'À risque';
        student.predClass  = data.result === 'Pass' ? 'success' :
                             data.result === 'Fail' ? 'danger'  : 'warning';
        student.confidence = Math.round((data.probability || 0) * 100);
        student.riskLevel  = data.risk_level || (data.result === 'Fail' ? 'HIGH' : 'LOW');
        student.features   = Object.entries(data.shap_values || {})
          .filter(([k]) => k !== 'error')
          .map(([key, val]: any) => ({
            feature:      key.replace(/_/g, ' '),
            contribution: val,
            direction:    val >= 0 ? 'positive' : 'negative'
          }));
      },
      error: (err) => {
        student.prediction = 'Non disponible';
        student.predClass  = 'unknown';
        student.confidence = 0;
        student.riskLevel  = '—';
        student.features   = [];
      }
    });
  }

  get filteredStudents(): StudentPred[] {
    if (this.riskFilter === 'all')     return this.students;
    if (this.riskFilter === 'success') return this.students.filter(s => s.predClass === 'success');
    if (this.riskFilter === 'danger')  return this.students.filter(s => s.predClass === 'danger');
    return this.students;
  }

  get highRiskCount(): number {
    return this.students.filter(s => s.riskLevel === 'HIGH').length;
  }

  viewShap(id: number): void {
    // Redirige explicitement vers la page externe /shap avec le queryParam
    this.router.navigate(['/shap'], { queryParams: { studentId: id } });
  }
}