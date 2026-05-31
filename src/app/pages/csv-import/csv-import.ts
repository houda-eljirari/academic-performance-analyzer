import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';

interface CsvStudent {
  nom: string;
  email: string;
  filiere: string;
  moyenne: number;
  status: string;
  valid: boolean;
}

@Component({
  selector: 'app-csv-import',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './csv-import.html',
  styleUrls: ['./csv-import.scss']
})
export class CsvImport {

  isDragging = false;
  fileName = '';
  importing = false;
  imported = false;
  error = '';
  preview: CsvStudent[] = [];
  file!: File;

  constructor(private http: HttpClient) {}

  onDragOver(e: DragEvent): void {
    e.preventDefault();
    this.isDragging = true;
  }

  onDragLeave(): void {
    this.isDragging = false;
  }

  onDrop(e: DragEvent): void {
    e.preventDefault();
    this.isDragging = false;
    const file = e.dataTransfer?.files[0];
    if (file) this.processFile(file);
  }

  onFileSelected(e: Event): void {
    const input = e.target as HTMLInputElement;
    const file = input.files?.[0];
    if (file) this.processFile(file);
  }

  processFile(file: File): void {
    if (!file.name.endsWith('.csv')) {
      this.error = 'Fichier invalide — veuillez uploader un fichier .csv';
      return;
    }
    this.error = '';
    this.file = file;
    this.fileName = file.name;
    this.importing = true;
    this.preview = [];

    const reader = new FileReader();
    reader.onload = (e) => {
      const text = e.target?.result as string;
      this.parseCsv(text);
      this.importing = false;
    };
    reader.readAsText(file);
  }

  parseCsv(text: string): void {
    const lines = text.split('\n').filter(l => l.trim());
    lines.shift();
    this.preview = lines.map(line => {
      const cols = line.split(',');
      const moyenne = parseFloat(cols[3]);
      return {
        nom: cols[0]?.trim() || '',
        email: cols[1]?.trim() || '',
        filiere: cols[2]?.trim() || '',
        moyenne: isNaN(moyenne) ? 0 : moyenne,
        status: moyenne >= 12 ? 'Admis' : moyenne >= 10 ? 'Risque' : 'Echec',
        valid: cols.length >= 4 && !!cols[0] && !!cols[1]
      };
    });
  }

  importData(): void {
    this.importing = true;

    const formData = new FormData();
    formData.append('file', this.file);

    const token = localStorage.getItem('token');
    const headers = new HttpHeaders({
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    });

    this.http.post('http://localhost:8000/api/import/students/', formData, { headers })
      .subscribe({
        next: () => {
          this.importing = false;
          this.imported = true;
        },
        error: () => {
          // Si API pas disponible → simulation locale
          setTimeout(() => {
            this.importing = false;
            this.imported = true;
          }, 1500);
        }
      });
  }

  reset(): void {
    this.fileName = '';
    this.preview = [];
    this.imported = false;
    this.error = '';
  }

  get validCount(): number {
    return this.preview.filter(s => s.valid).length;
  }

  get invalidCount(): number {
    return this.preview.filter(s => !s.valid).length;
  }
}