import { Component } from '@angular/core';
import { Router } from '@angular/router';

interface NavItem {
  label: string;
  icon: string;
  route: string;
}

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.html',
  styleUrls: ['./sidebar.scss']
})
export class SidebarComponent {
  navItems: NavItem[] = [
    { label: 'Dashboard', icon: '⊞', route: '/dashboard' },
    { label: 'Students', icon: '👥', route: '/students' },
    { label: 'Grades', icon: '📊', route: '/grades' },
    { label: 'Predictions', icon: '🔮', route: '/predictions' },
    { label: 'Alerts', icon: '🔔', route: '/alerts' },
  ];

  constructor(public router: Router) {}

  isActive(route: string): boolean {
    return this.router.url === route;
  }
}