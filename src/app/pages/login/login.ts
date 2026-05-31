import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.html',
  styleUrls: ['./login.scss']
})
export class LoginComponent {
  email = '';
  password = '';
  loading = false;
  error = '';

  constructor(private router: Router) {}

  onSubmit(): void {
    if (!this.email || !this.password) {
      this.error = 'Please fill in all fields';
      return;
    }

    this.loading = true;
    this.error = '';

    // Simulation connexion — à remplacer par l'API Django plus tard
    setTimeout(() => {
      if (this.email === 'admin@test.com' && this.password === '1234') {
        localStorage.setItem('token', 'fake-token-123');
        localStorage.setItem('user', JSON.stringify({
          id: 1,
          email: this.email,
          name: 'Admin',
          role: 'admin',
          token: 'fake-token-123'
        }));
        this.router.navigate(['/dashboard']);
      } else {
        this.error = 'Email ou mot de passe incorrect';
        this.loading = false;
      }
    }, 1000);
  }
}