import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface GradeRow {
  studentId: number;
  name: string;
  initials: string;
  filiere: string;
  grades: { [matiere: string]: number };
  average: number;
  status: string;
  statusClass: string;
}

@Component({
  selector: 'app-grades',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './grades.html',
  styleUrls: ['./grades.scss']
})
export class Grades {

  selectedMatiere = '';
  selectedSemestre = 'S1';
  saved = false;

  matieres = ['Maths', 'Algo', 'Réseaux', 'BDD', 'Anglais'];

  gradesData: GradeRow[] = [
    { studentId: 1, name: 'Abdessamad Benhiri', initials: 'AB', filiere: 'Informatique',
      grades: { Maths: 17, Algo: 18, Réseaux: 15, BDD: 16, Anglais: 14 },
      average: 16, status: 'Admis', statusClass: 'success' },
    { studentId: 2, name: 'Aya Benhadi', initials: 'AB', filiere: 'Gestion',
      grades: { Maths: 8, Algo: 9, Réseaux: 10, BDD: 9, Anglais: 11 },
      average: 9.4, status: 'Risque', statusClass: 'warning' },
    { studentId: 3, name: 'Safaa Bennani', initials: 'SB', filiere: 'Droit',
      grades: { Maths: 14, Algo: 15, Réseaux: 13, BDD: 16, Anglais: 15 },
      average: 14.6, status: 'Admis', statusClass: 'success' },
    { studentId: 4, name: 'Ali Jbira', initials: 'AJ', filiere: 'Sciences',
      grades: { Maths: 6, Algo: 7, Réseaux: 8, BDD: 6, Anglais: 9 },
      average: 7.2, status: 'Echec', statusClass: 'danger' },
    { studentId: 5, name: 'Nadia El Fassi', initials: 'NF', filiere: 'Informatique',
      grades: { Maths: 18, Algo: 17, Réseaux: 16, BDD: 19, Anglais: 15 },
      average: 17, status: 'Admis', statusClass: 'success' },
  ];

  updateAverage(row: GradeRow): void {
    const vals = Object.values(row.grades);
    row.average = vals.reduce((a, b) => a + b, 0) / vals.length;
    if (row.average >= 12) { row.status = 'Admis'; row.statusClass = 'success'; }
    else if (row.average >= 10) { row.status = 'Risque'; row.statusClass = 'warning'; }
    else { row.status = 'Echec'; row.statusClass = 'danger'; }
  }

  saveGrades(): void {
    this.saved = true;
    setTimeout(() => this.saved = false, 3000);
  }
}