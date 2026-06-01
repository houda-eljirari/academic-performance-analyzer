import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

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
  imports: [CommonModule, FormsModule],
  templateUrl: './shap.html',
  styleUrls: ['./shap.scss']
})
export class Shap {

  constructor(private http: HttpClient) {}

  selectedStudentId = 1;

  ngOnInit() {
  this.loadShap(this.selectedStudentId);
}

  loadShap(studentId: number) {

  this.http.post(
    `http://localhost:8000/api/ml/predict/${studentId}/`,
    {}
  ).subscribe({

    next: (response: any) => {
      console.log('Réponse Django:', response);
    },

    error: (err) => {
      console.error('Erreur API:', err);
    }

  });

}
  students: StudentShap[] = [
    {
      id: 1, name: 'Abdessamad Benhiri', initials: 'AB',
      filiere: 'Informatique', prediction: 'Succès', predClass: 'success', confidence: 94,
      features: [
        { feature: 'Moyenne générale',    value: 16.5, contribution: 2.8,  direction: 'positive' },
        { feature: 'Note Algorithmique',  value: 18,   contribution: 2.1,  direction: 'positive' },
        { feature: 'Note Mathématiques',  value: 17,   contribution: 1.9,  direction: 'positive' },
        { feature: 'Absences',            value: 2,    contribution: 0.8,  direction: 'positive' },
        { feature: 'Note BDD',            value: 16,   contribution: 0.6,  direction: 'positive' },
        { feature: 'Note Anglais',        value: 14,   contribution: -0.3, direction: 'negative' },
      ]
    },
    {
      id: 2, name: 'Aya Benhadi', initials: 'AB',
      filiere: 'Gestion', prediction: 'À risque', predClass: 'warning', confidence: 71,
      features: [
        { feature: 'Absences',            value: 7,    contribution: -2.4, direction: 'negative' },
        { feature: 'Note Mathématiques',  value: 8,    contribution: -2.1, direction: 'negative' },
        { feature: 'Moyenne générale',    value: 9.2,  contribution: -1.8, direction: 'negative' },
        { feature: 'Note Algorithmique',  value: 9,    contribution: -1.2, direction: 'negative' },
        { feature: 'Note Anglais',        value: 11,   contribution: 0.4,  direction: 'positive' },
        { feature: 'Note BDD',            value: 9,    contribution: -0.8, direction: 'negative' },
      ]
    },
    {
      id: 4, name: 'Ali Jbira', initials: 'AJ',
      filiere: 'Sciences', prediction: 'Échec', predClass: 'danger', confidence: 82,
      features: [
        { feature: 'Moyenne générale',    value: 7.1,  contribution: -3.2, direction: 'negative' },
        { feature: 'Absences',            value: 12,   contribution: -2.8, direction: 'negative' },
        { feature: 'Note Mathématiques',  value: 6,    contribution: -2.5, direction: 'negative' },
        { feature: 'Note Algorithmique',  value: 7,    contribution: -1.9, direction: 'negative' },
        { feature: 'Note BDD',            value: 6,    contribution: -1.5, direction: 'negative' },
        { feature: 'Note Anglais',        value: 9,    contribution: 0.2,  direction: 'positive' },
      ]
    },
  ];

  get selectedStudent(): StudentShap {
    return this.students.find(s => s.id === this.selectedStudentId) || this.students[0];
  }

  getBarWidth(contribution: number): string {
    const max = 4;
    return (Math.abs(contribution) / max * 100) + '%';
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