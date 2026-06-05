import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
// 1. Importer le module Lucide
import { LucideAngularModule } from 'lucide-angular';

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
  selector: 'app-shap',
  standalone: true,
  // 2. Ajouter LucideAngularModule aux imports du composant
  imports: [CommonModule, FormsModule, LucideAngularModule],
  templateUrl: './shap.html',
  styleUrls: ['./shap.scss']
})
export class Shap implements OnInit {

  constructor(private http: HttpClient) {}

  selectedStudentId = 0;
  loading = false;
  students: StudentShap[] = [];

  private fallbackStudents: StudentShap[] = [
    {
      id: 1, name: 'Abdessamad Benhiri', initials: 'AB',
      filiere: 'Informatique', prediction: 'Succès', predClass: 'success', confidence: 94,
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
      filiere: 'Gestion', prediction: 'À risque', predClass: 'warning', confidence: 71,
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
      filiere: 'Sciences', prediction: 'Échec', predClass: 'danger', confidence: 82,
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

  ngOnInit(): void {
    this.http.get<any>('http://localhost:8000/api/students/')
      .subscribe({
        next: (res) => {
          const list = res.results || res;
          if (list && list.length > 0) {
            this.students = list.slice(0, 10).map((s: any) => ({
              id:         s.id,
              name:       `Étudiant ${s.id_student}`,
              initials:   s.gender || 'ET',
              filiere:    s.region || 'OULAD',
              prediction: '',
              predClass:  '',
              confidence: 0,
              features:   [],
            }));
            this.selectedStudentId = this.students[0].id;
            this.loadShap(this.selectedStudentId);
          } else {
            this.useFallback();
          }
        },
        error: () => this.useFallback()
      });
  }

  private useFallback(): void {
    this.students = this.fallbackStudents;
    this.selectedStudentId = this.students[0].id;
    console.log('API indisponible - données statiques utilisées');
  }

  onStudentChange(newId: any): void {
    const id = parseInt(newId, 10);
    console.log('Changement étudiant → ID:', id);

    if (!id || id === this.selectedStudentId) return;

    this.selectedStudentId = id;

    const existing = this.students.find(s => s.id === id);
    if (existing && existing.features.length > 0) {
      console.log('Données en cache pour étudiant', id);
      return;
    }

    this.loadShap(id);
  }

  loadShap(studentId: number): void {
    if (!studentId) return;
    this.loading = true;

    this.http.post<any>(
      `http://localhost:8000/api/ml/predict/pk/${studentId}/`, {}
    ).subscribe({
      next: (response: any) => {
        console.log('Réponse Django:', response);
        const shapValues = response.shap_values || {};
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
          this.students[idx].prediction = response.result === 'Pass' ? 'Succès' :
                                          response.result === 'Fail' ? 'Échec' : 'À risque';
          this.students[idx].predClass  = response.result === 'Pass' ? 'success' :
                                          response.result === 'Fail' ? 'danger' : 'warning';
          this.students[idx].confidence = Math.round((response.probability || 0) * 100);
        }
        this.loading = false;
      },
      error: (err) => {
        console.error('Erreur prédiction API:', err);
        this.loading = false;
      }
    });
  }

  get selectedStudent(): StudentShap {
    return this.students.find(s => s.id === this.selectedStudentId) || this.students[0];
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