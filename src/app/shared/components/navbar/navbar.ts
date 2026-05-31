import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService, AuthUser } from '../../../core/services/auth';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.html',
  styleUrls: ['./navbar.scss']
})
export class NavbarComponent implements OnInit {
  user: AuthUser | null = null;
  currentTime = new Date();

  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit(): void {
    this.authService.currentUser$.subscribe(u => (this.user = u));
    setInterval(() => (this.currentTime = new Date()), 60000);
  }

  logout(): void {
    this.authService.logout();
  }
}