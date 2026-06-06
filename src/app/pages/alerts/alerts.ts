import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LucideAngularModule } from 'lucide-angular';
import { ApiService } from '../../core/services/api';

interface Alert {
  id:       number;
  type:     'danger' | 'warning' | 'info';
  icon:     string;
  title:    string;
  message:  string;
  student:  string;
  time:     string;
  resolved: boolean;
}

@Component({
  selector:    'app-alerts',
  standalone:  true,
  imports:     [CommonModule, LucideAngularModule],
  templateUrl: './alerts.html',
  styleUrls:   ['./alerts.scss']
})
export class Alerts implements OnInit {

  activeFilter  = 'all';
  resolvedCount = 0;

  alerts: Alert[] = [];

  private fallbackAlerts: Alert[] = [
    { id: 1, type: 'danger',  icon: 'bell-ring',      title: 'Note critique',
      message: 'Note de 4.5/20 en Mathématiques — en dessous du seuil critique',
      student: 'Ali Jbira',            time: 'il y a 10 min', resolved: false },
    { id: 2, type: 'danger',  icon: 'bell-ring',      title: 'Absences répétées',
      message: '5 absences consécutives en Algorithmique ce mois',
      student: 'Aya Benhadi',          time: 'il y a 25 min', resolved: false },
    { id: 3, type: 'warning', icon: 'alert-triangle', title: 'Baisse de moyenne',
      message: 'Moyenne en baisse de 3.2 points par rapport au semestre précédent',
      student: 'Fatima Zahra Idrissi', time: 'il y a 1h',     resolved: false },
    { id: 4, type: 'warning', icon: 'alert-triangle', title: "Risque d'échec prédit",
      message: "Le modèle IA prédit un risque d'échec à 68% pour ce semestre",
      student: 'Mehdi Berrada',        time: 'il y a 2h',     resolved: false },
    { id: 5, type: 'info',    icon: 'clipboard-list', title: 'Nouveau dossier',
      message: "Un nouveau dossier d'inscription a été soumis pour validation",
      student: 'Omar Chraibi',         time: 'il y a 3h',     resolved: false },
    { id: 6, type: 'info',    icon: 'bar-chart-3',    title: 'Rapport disponible',
      message: 'Le rapport de performance du semestre 1 est disponible',
      student: 'Système',              time: 'il y a 5h',     resolved: false },
  ];

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.api.get<any>('analytics/alerts/').subscribe({
      next: (data) => {
        const rawAlerts = data.alerts || [];
        if (rawAlerts.length === 0) {
          this.alerts = [...this.fallbackAlerts];
          return;
        }
        this.alerts = rawAlerts.map((a: any, index: number) => ({
          id:       index + 1,
          type:     a.type === 'critique'      ? 'danger'  :
                    a.type === 'avertissement' ? 'warning' : 'info',
          icon:     a.icon === 'alert'   ? 'bell-ring'      :
                    a.icon === 'warning' ? 'alert-triangle' : 'info',
          title:    a.title,
          message:  a.description,
          student:  a.student,
          time:     a.time,
          resolved: false,
        }));
      },
      error: () => {
        this.alerts = [...this.fallbackAlerts];
      }
    });
  }

  // ← getter au lieu de computed() — détecté automatiquement par Angular
  get filteredAlerts(): Alert[] {
    return this.alerts.filter(a => {
      if (this.activeFilter === 'all') return !a.resolved;
      const typeMap: any = { danger: 'danger', warning: 'warning', info: 'info' };
      return a.type === typeMap[this.activeFilter] && !a.resolved;
    });
  }

  get dangerCount():  number { return this.alerts.filter(a => a.type === 'danger'  && !a.resolved).length; }
  get warningCount(): number { return this.alerts.filter(a => a.type === 'warning' && !a.resolved).length; }
  get infoCount():    number { return this.alerts.filter(a => a.type === 'info'    && !a.resolved).length; }

  setFilter(filter: string): void { this.activeFilter = filter; }

  resolve(id: number): void {
    const alert = this.alerts.find(a => a.id === id);
    if (alert) { alert.resolved = true; this.resolvedCount++; }
  }

  clearAll(): void {
    this.alerts.forEach(a => a.resolved = true);
    this.resolvedCount = this.alerts.length;
  }
}