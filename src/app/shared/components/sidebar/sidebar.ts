import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { LucideAngularModule, 
         LayoutDashboard,
         Users,
         GraduationCap,
         BrainCircuit,
         Bell,
         FileUp,
         Sparkles } from 'lucide-angular';

interface NavItem {
  label: string;
  icon:  any;
  route: string;
}

@Component({
  selector:    'app-sidebar',
  standalone:  true,
  imports:     [CommonModule, RouterModule, LucideAngularModule],
  templateUrl: './sidebar.html',
  styleUrls:   ['./sidebar.scss']
})
export class SidebarComponent {

  readonly LayoutDashboard = LayoutDashboard;
  readonly Users           = Users;
  readonly GraduationCap   = GraduationCap;
  readonly BrainCircuit    = BrainCircuit;
  readonly Bell            = Bell;
  readonly FileUp          = FileUp;
  readonly Sparkles        = Sparkles;

  navItems: NavItem[] = [
    { label: 'Dashboard',   icon: LayoutDashboard, route: '/dashboard'   },
    { label: 'Students',    icon: Users,           route: '/students'    },
    { label: 'Grades',      icon: GraduationCap,   route: '/grades'      },
    { label: 'Predictions', icon: BrainCircuit,    route: '/predictions' },
    { label: 'Alerts',      icon: Bell,            route: '/alerts'      },
    { label: 'Import CSV',  icon: FileUp,          route: '/csv-import'  },
    { label: 'SHAP',        icon: Sparkles,        route: '/shap'        },
  ];

  constructor(public router: Router) {}

  isActive(route: string): boolean {
    return this.router.url === route;
  }

  navigate(route: string): void {
    this.router.navigate([route]);
  }
}