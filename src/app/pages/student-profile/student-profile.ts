import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';

interface StudentDetail {
  id: number;
  name: string;
  initials: string;
  email: string;
  filiere: string;
  niveau: string;
  average: number;
  status: string;
  statusClass: string;
  absences: number;
  grades: { matiere: string; note: number; coeff: number }[];
  evolution: { mois: string; moyenne: number }[];
}

@Component({
  selector: 'app-student-profile',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './student-profile.html',
  styleUrls: ['./student-profile.scss']
})
export class StudentProfile implements OnInit {

  student!: StudentDetail;

  students: StudentDetail[] = [
    {
      id: 1, name: 'Abdessamad Benhiri', initials: 'AB',
      email: 'a.benhiri@univ.ma', filiere: 'Informatique', niveau: 'L2',
      average: 16.5, status: 'Admis', statusClass: 'success', absences: 2,
      grades: [
        { matiere: 'Mathématiques', note: 17, coeff: 3 },
        { matiere: 'Algorithmique', note: 18, coeff: 3 },
        { matiere: 'Réseaux', note: 15, coeff: 2 },
        { matiere: 'BDD', note: 16, coeff: 2 },
        { matiere: 'Anglais', note: 14, coeff: 1 },
      ],
      evolution: [
        { mois: 'Sep', moyenne: 14.2 },
        { mois: 'Oct', moyenne: 15.1 },
        { mois: 'Nov', moyenne: 15.8 },
        { mois: 'Déc', moyenne: 16.0 },
        { mois: 'Jan', moyenne: 16.5 },
      ]
    },
    {
      id: 2, name: 'Aya Benhadi', initials: 'AB',
      email: 'a.benhadi@univ.ma', filiere: 'Gestion', niveau: 'L1',
      average: 9.2, status: 'Risque', statusClass: 'warning', absences: 7,
      grades: [
        { matiere: 'Mathématiques', note: 8, coeff: 3 },
        { matiere: 'Algorithmique', note: 9, coeff: 3 },
        { matiere: 'Réseaux', note: 10, coeff: 2 },
        { matiere: 'BDD', note: 9, coeff: 2 },
        { matiere: 'Anglais', note: 11, coeff: 1 },
      ],
      evolution: [
        { mois: 'Sep', moyenne: 11.0 },
        { mois: 'Oct', moyenne: 10.5 },
        { mois: 'Nov', moyenne: 9.8 },
        { mois: 'Déc', moyenne: 9.5 },
        { mois: 'Jan', moyenne: 9.2 },
      ]
    },
    {
      id: 3, name: 'Safaa Bennani', initials: 'SB',
      email: 's.bennani@univ.ma', filiere: 'Droit', niveau: 'L2',
      average: 14.8, status: 'Admis', statusClass: 'success', absences: 1,
      grades: [
        { matiere: 'Mathématiques', note: 14, coeff: 3 },
        { matiere: 'Algorithmique', note: 15, coeff: 3 },
        { matiere: 'Réseaux', note: 13, coeff: 2 },
        { matiere: 'BDD', note: 16, coeff: 2 },
        { matiere: 'Anglais', note: 15, coeff: 1 },
      ],
      evolution: [
        { mois: 'Sep', moyenne: 13.0 },
        { mois: 'Oct', moyenne: 13.5 },
        { mois: 'Nov', moyenne: 14.0 },
        { mois: 'Déc', moyenne: 14.5 },
        { mois: 'Jan', moyenne: 14.8 },
      ]
    },
    {
      id: 4, name: 'Ali Jbira', initials: 'AJ',
      email: 'a.jbira@univ.ma', filiere: 'Sciences', niveau: 'L1',
      average: 7.1, status: 'Echec', statusClass: 'danger', absences: 12,
      grades: [
        { matiere: 'Mathématiques', note: 6, coeff: 3 },
        { matiere: 'Algorithmique', note: 7, coeff: 3 },
        { matiere: 'Réseaux', note: 8, coeff: 2 },
        { matiere: 'BDD', note: 6, coeff: 2 },
        { matiere: 'Anglais', note: 9, coeff: 1 },
      ],
      evolution: [
        { mois: 'Sep', moyenne: 9.5 },
        { mois: 'Oct', moyenne: 8.8 },
        { mois: 'Nov', moyenne: 8.0 },
        { mois: 'Déc', moyenne: 7.5 },
        { mois: 'Jan', moyenne: 7.1 },
      ]
    },
  ];

  constructor(private route: ActivatedRoute, private router: Router) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.student = this.students.find(s => s.id === id) || this.students[0];
  }

  goBack(): void {
    this.router.navigate(['/students']);
  }

  getBarWidth(note: number): string {
    return (note / 20 * 100) + '%';
  }

  getBarColor(note: number): string {
    if (note >= 14) return '#059669';
    if (note >= 10) return '#d97706';
    return '#dc2626';
  }

  getEvolutionHeight(moyenne: number): string {
    return (moyenne / 20 * 100) + '%';
  }
}
