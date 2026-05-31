import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,  // pour *ngIf
    FormsModule,   // pour [(ngModel)]
  ],
  templateUrl: './login.html',
  styleUrl: './login.scss',
})
export class Login {

  // Les champs du formulaire
  email: string = '';
  password: string = '';
  errorMsg: string = '';

  constructor(private router: Router) {}

  onLogin() {
    // Vérification basique
    if (!this.email || !this.password) {
      this.errorMsg = 'Veuillez remplir tous les champs.';
      return;
    }

    // Pour l'instant on simule la connexion
    // Plus tard on appellera l'API Django de ton binôme
    if (this.email === 'admin@test.com' && this.password === '1234') {
      this.router.navigate(['/dashboard']);
    } else {
      this.errorMsg = 'Email ou mot de passe incorrect.';
    }
  }
}
