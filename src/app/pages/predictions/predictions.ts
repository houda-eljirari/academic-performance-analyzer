import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/services/api';

interface ShapFeature {
  feature: string;
  value: number;
  contribution: number;
  direction: 'positive' | 'negative';
}

interface StudentShap {
  id: number;
  name: string;
  initials: string;
  filiere: string;
  prediction: string;
  predClass: string;
  confidence: number;
  features: ShapFeature[];
}

@Component({
  selector: 'app-predictions',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: '../shap/shap.html',
  styleUrls: ['../shap/shap.scss']
})
export class Predictions implements OnInit {

  selectedStudentId = 0;
  loading = false;

  // Données statiques de fallback
  students: StudentShap[] = [
    {
      id: 0, name: 'Chargement...', initials: '...',
      filiere: '', prediction: '', predClass: '', confidence: 0, features: []
    }
  ];

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    // Charger d'abord la liste des vrais étudiants depuis Django
    this.api.get<any>('students/').subscribe({
      next: (res) => {
        const list = res.results || res;
        if (list && list.length > 0) {
          // Construire la liste depuis la DB
          this.students = list.slice(0, 10).map((s: any) => ({
            id:         s.id,
            name:       `Étudiant ${s.id_student}`,
            initials:   s.gender === 'M' ? 'M' : 'F',
            filiere:    s.module || s.region || 'OULAD',
            prediction: '',
            predClass:  '',
            confidence: 0,
            features:   [],
          }));
          // Charger la prédiction du premier étudiant
          this.selectedStudentId = this.students[0].id;
          this.loadShap(this.selectedStudentId);
        }
      },
      error: () => {
        // Fallback sur données statiques si API indisponible
        this.students = [
          {
            id: 1, name: 'Abdessamad Benhiri', initials: 'AB',
            filiere: 'Informatique', prediction: 'Succès',
            predClass: 'success', confidence: 94,
            features: [
              { feature: 'Moyenne générale',   value: 16.5, contribution: 2.8,  direction: 'positive' },
              { feature: 'Note Algorithmique', value: 18,   contribution: 2.1,  direction: 'positive' },
              { feature: 'Note Mathématiques', value: 17,   contribution: 1.9,  direction: 'positive' },
              { feature: 'Absences',           value: 2,    contribution: 0.8,  direction: 'positive' },
              { feature: 'Note BDD',           value: 16,   contribution: 0.6,  direction: 'positive' },
              { feature: 'Note Anglais',       value: 14,   contribution: -0.3, direction: 'negative' },
            ]
          },
          {
            id: 2, name: 'Aya Benhadi', initials: 'AB',
            filiere: 'Gestion', prediction: 'À risque',
            predClass: 'warning', confidence: 71,
            features: [
              { feature: 'Absences',           value: 7,   contribution: -2.4, direction: 'negative' },
              { feature: 'Note Mathématiques', value: 8,   contribution: -2.1, direction: 'negative' },
              { feature: 'Moyenne générale',   value: 9.2, contribution: -1.8, direction: 'negative' },
              { feature: 'Note Algorithmique', value: 9,   contribution: -1.2, direction: 'negative' },
              { feature: 'Note Anglais',       value: 11,  contribution: 0.4,  direction: 'positive' },
              { feature: 'Note BDD',           value: 9,   contribution: -0.8, direction: 'negative' },
            ]
          },
          {
            id: 4, name: 'Ali Jbira', initials: 'AJ',
            filiere: 'Sciences', prediction: 'Échec',
            predClass: 'danger', confidence: 82,
            features: [
              { feature: 'Moyenne générale',   value: 7.1, contribution: -3.2, direction: 'negative' },
              { feature: 'Absences',           value: 12,  contribution: -2.8, direction: 'negative' },
              { feature: 'Note Mathématiques', value: 6,   contribution: -2.5, direction: 'negative' },
              { feature: 'Note Algorithmique', value: 7,   contribution: -1.9, direction: 'negative' },
              { feature: 'Note BDD',           value: 6,   contribution: -1.5, direction: 'negative' },
              { feature: 'Note Anglais',       value: 9,   contribution: 0.2,  direction: 'positive' },
            ]
          },
        ];
        this.selectedStudentId = this.students[0].id;
        console.log('API indisponible - données statiques utilisées');
      }
    });
  }

  loadShap(studentId: number): void {
    if (!studentId) return;
    this.loading = true;

    this.api.post<any>(`ml/predict/pk/${studentId}/`, {}).subscribe({
      next: (data) => {
        const shapValues = data.shap_values || {};
        const features: ShapFeature[] = Object.entries(shapValues)
          .filter(([k]) => k !== 'error')
          .map(([key, val]: any) => ({
            feature:      key.replace(/_/g, ' '),
            value:        0,
            contribution: val,
            direction:    val >= 0 ? 'positive' : 'negative'
          }));

        const idx = this.students.findIndex(s => s.id === studentId);
        if (idx >= 0) {
          this.students[idx].features   = features;
          this.students[idx].prediction = data.result === 'Pass' ? 'Succès' :
                                          data.result === 'Fail' ? 'Échec' : 'À risque';
          this.students[idx].predClass  = data.result === 'Pass' ? 'success' :
                                          data.result === 'Fail' ? 'danger' : 'warning';
          this.students[idx].confidence = Math.round((data.probability || 0) * 100);
        }
        this.loading = false;
      },
      error: () => {
        console.log('Prédiction API indisponible - données statiques conservées');
        this.loading = false;
      }
    });
  }

  get selectedStudent(): StudentShap {
    return this.students.find(s => s.id === this.selectedStudentId) || this.students[0];
  }

  onStudentChange(id: number): void {
    this.selectedStudentId = +id;
    this.loadShap(this.selectedStudentId);
  }

  getBarWidth(contribution: number): string {
    return (Math.abs(contribution) / 4 * 100) + '%';
  }

  getTotalPositive(): number {
    return this.selectedStudent.features
      .filter(f => f.direction === 'positive')
      .reduce((a, f) => a + f.contribution, 0);
  }

  getTotalNegative(): number {
    return this.selectedStudent.features
      .filter(f => f.direction === 'negative')
      .reduce((a, f) => a + f.contribution, 0);
  }
}