import { Component, OnDestroy, OnInit } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';
import { ActivatedRoute, Router } from '@angular/router';
import { Subject, filter, take, takeUntil } from 'rxjs';
import { AuthService } from '../../../services/auth.service';
import { FormsModule, NgForm } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-activate',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatIconModule,
    MatButtonModule,
    MatInputModule,
    MatFormFieldModule,
    FormsModule
  ],
  templateUrl: './activate.component.html',
  styleUrl: './activate.component.css'
})
export class ActivateComponent implements OnInit, OnDestroy {
  public activateValid = true;
  public email = '';
  public activation_code = '';
  
  private _destroySub$ = new Subject<void>();
  private readonly returnUrl: string;

  constructor(
    private _route: ActivatedRoute,
    private _router: Router,
    private _authService: AuthService
  ) {
    this.returnUrl = this._route.snapshot.queryParams['returnUrl'] || '/';
  }

  public ngOnInit(): void {
    this._route.queryParams.subscribe(params => {
      if (params["email"] !== undefined) {
        this.email = params["email"];
      }
      
    })
    this._authService.isAuthenticated$.pipe(
      filter((isAuthenticated: boolean) => isAuthenticated),
      takeUntil(this._destroySub$)
    ).subscribe(_ => this._router.navigateByUrl(this.returnUrl));
  }

  public ngOnDestroy(): void {
    this._destroySub$.next();
  }

  public onSubmit(loginForm: NgForm): void {
    this.activateValid = true;
    
    this._authService.activate(this.email, this.activation_code).pipe(
      take(1)
    ).subscribe({
      next: _ => {
        this.activateValid = true;
        this._router.navigateByUrl('/');
      },
      error: _ => this.activateValid = false
    });
  }
}