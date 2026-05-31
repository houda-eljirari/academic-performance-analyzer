import { Component, OnInit, computed, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../../core/services/api';

interface Student {
  id: number;
  name: string;
  email: string;
  initials: string;
  filiere: string;
  average: number;
  status: string;
  statusClass: string;
}

@Component({
  selector: 'app-students',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './students.html',
  styleUrls: ['./students.scss']
})
export class StudentsComponent implements OnInit {

  searchTerm = '';
  filterFiliere = '';
  filterStatus = '';

  // Données statiques par défaut
  students: Student[] = [
    { id: 1, name: 'Abdessamad Benhiri', email: 'a.benhiri@univ.ma', initials: 'AB', filiere: 'Informatique', average: 16.5, status: 'Admis', statusClass: 'success' },
    { id: 2, name: 'Aya Benhadi', email: 'a.benhadi@univ.ma', initials: 'AB', filiere: 'Gestion', average: 9.2, status: 'Risque', statusClass: 'warning' },
    { id: 3, name: 'Safaa Bennani', email: 's.bennani@univ.ma', initials: 'SB', filiere: 'Droit', average: 14.8, status: 'Admis', statusClass: 'success' },
    { id: 4, name: 'Ali Jbira', email: 'a.jbira@univ.ma', initials: 'AJ', filiere: 'Sciences', average: 7.1, status: 'Echec', statusClass: 'danger' },
    { id: 5, name: 'Nadia El Fassi', email: 'n.elfassi@univ.ma', initials: 'NF', filiere: 'Informatique', average: 17.2, status: 'Admis', statusClass: 'success' },
    { id: 6, name: 'Youssef Alami', email: 'y.alami@univ.ma', initials: 'YA', filiere: 'Gestion', average: 11.5, status: 'Admis', statusClass: 'success' },
    { id: 7, name: 'Fatima Zahra Idrissi', email: 'f.idrissi@univ.ma', initials: 'FI', filiere: 'Droit', average: 8.4, status: 'Risque', statusClass: 'warning' },
    { id: 8, name: 'Omar Chraibi', email: 'o.chraibi@univ.ma', initials: 'OC', filiere: 'Informatique', average: 15.3, status: 'Admis', statusClass: 'success' },
    { id: 9, name: 'Hajar Tazi', email: 'h.tazi@univ.ma', initials: 'HT', filiere: 'Sciences', average: 12.7, status: 'Admis', statusClass: 'success' },
    { id: 10, name: 'Mehdi Berrada', email: 'm.berrada@univ.ma', initials: 'MB', filiere: 'Gestion', average: 6.8, status: 'Echec', statusClass: 'danger' },
  ];

  constructor(private router: Router, private api: ApiService) {}

  ngOnInit(): void {
    this.api.get<any>('students/').subscribe({
      next: (data) => {
        const results = data.results || data;
        this.students = results.map((s: any) => ({
          id: s.id,
          name: s.full_name || s.name || `${s.first_name} ${s.last_name}`,
          email: s.email || `${s.id}@univ.ma`,
          initials: (s.full_name || s.name || 'XX').split(' ').map((n: string) => n[0]).join('').toUpperCase(),
          filiere: s.module_code || s.filiere || 'N/A',
          average: s.avg_score || s.average || 0,
          status: s.final_result || s.status || 'N/A',
          statusClass: s.final_result === 'Pass' ? 'success' : s.final_result === 'Fail' ? 'danger' : 'warning'
        }));
      },
      error: () => {
        console.log('API non disponible, données statiques utilisées');
      }
    });
  }

  filteredStudents = computed(() => {
    return this.students.filter(s => {
      const matchSearch = s.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
                          s.email.toLowerCase().includes(this.searchTerm.toLowerCase());
      const matchFiliere = this.filterFiliere === '' || s.filiere === this.filterFiliere;
      const matchStatus = this.filterStatus === '' || s.status === this.filterStatus;
      return matchSearch && matchFiliere && matchStatus;
    });
  });

  viewProfile(id: number): void {
    this.router.navigate(['/students', id]);
  }
}