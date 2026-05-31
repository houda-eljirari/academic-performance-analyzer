import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';

interface NavItem {
  label: string;
  icon: string;
  route: string;
}

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './sidebar.html',
  styleUrls: ['./sidebar.scss']
})
export class SidebarComponent {

  navItems: NavItem[] = [
    { label: 'Dashboard',   icon: '⊞', route: '/dashboard'   },
    { label: 'Students',    icon: '👥', route: '/students'    },
    { label: 'Grades',      icon: '📊', route: '/grades'      },
    { label: 'Predictions', icon: '🔮', route: '/predictions' },
    { label: 'Alerts',      icon: '🔔', route: '/alerts'      },
    { label: 'Import CSV',  icon: '📂', route: '/csv-import'  },
      { label: 'SHAP',        icon: '🧠', route: '/shap'      },
  ];

  constructor(public router: Router) {}

  isActive(route: string): boolean {
    return this.router.url === route;
  }

  navigate(route: string): void {
    this.router.navigate([route]);
  }
}