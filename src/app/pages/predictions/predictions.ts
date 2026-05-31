import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Prediction {
  studentId: number;
  name: string;
  initials: string;
  filiere: string;
  currentAvg: number;
  prediction: string;
  predClass: string;
  confidence: number;
  recommendation: string;
}

@Component({
  selector: 'app-predictions',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './predictions.html',
  styleUrls: ['./predictions.scss']
})
export class Predictions {

  accuracy = 87;

  predictions: Prediction[] = [
    { studentId: 1, name: 'Abdessamad Benhiri', initials: 'AB', filiere: 'Informatique',
      currentAvg: 16.5, prediction: 'Succès', predClass: 'success',
      confidence: 94, recommendation: 'Continuer ainsi' },
    { studentId: 2, name: 'Aya Benhadi', initials: 'AB', filiere: 'Gestion',
      currentAvg: 9.2, prediction: 'À risque', predClass: 'warning',
      confidence: 71, recommendation: 'Tutorat recommandé' },
    { studentId: 3, name: 'Safaa Bennani', initials: 'SB', filiere: 'Droit',
      currentAvg: 14.8, prediction: 'Succès', predClass: 'success',
      confidence: 88, recommendation: 'Bon niveau' },
    { studentId: 4, name: 'Ali Jbira', initials: 'AJ', filiere: 'Sciences',
      currentAvg: 7.1, prediction: 'Échec', predClass: 'danger',
      confidence: 82, recommendation: 'Intervention urgente' },
    { studentId: 5, name: 'Nadia El Fassi', initials: 'NF', filiere: 'Informatique',
      currentAvg: 17.2, prediction: 'Succès', predClass: 'success',
      confidence: 97, recommendation: 'Excellence maintenue' },
    { studentId: 6, name: 'Youssef Alami', initials: 'YA', filiere: 'Gestion',
      currentAvg: 11.5, prediction: 'Succès', predClass: 'success',
      confidence: 63, recommendation: 'Surveiller les progrès' },
    { studentId: 7, name: 'Fatima Zahra Idrissi', initials: 'FI', filiere: 'Droit',
      currentAvg: 8.4, prediction: 'À risque', predClass: 'warning',
      confidence: 68, recommendation: 'Soutien scolaire' },
    { studentId: 8, name: 'Omar Chraibi', initials: 'OC', filiere: 'Informatique',
      currentAvg: 15.3, prediction: 'Succès', predClass: 'success',
      confidence: 91, recommendation: 'Très bon niveau' },
  ];

  get successCount(): number {
    return this.predictions.filter(p => p.predClass === 'success').length;
  }

  get riskCount(): number {
    return this.predictions.filter(p => p.predClass === 'warning').length;
  }

  get failCount(): number {
    return this.predictions.filter(p => p.predClass === 'danger').length;
  }

  refresh(): void {
    this.accuracy = Math.floor(Math.random() * 5) + 85;
  }
}