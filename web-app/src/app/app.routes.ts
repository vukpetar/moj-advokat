import { Routes } from '@angular/router';

export const routes: Routes = [
    {path: '', loadComponent: () => import('./components/homepage/homepage.component').then(mod => mod.HomepageComponent)},
    {path: 'prijava', loadComponent: () => import('./components/auth/login/login.component').then(mod => mod.LoginComponent)},
    {path: 'registracija', loadComponent: () => import('./components/auth/register/register.component').then(mod => mod.RegisterComponent)},
    {path: 'profil', loadComponent: () => import('./components/user/profile/profile.component').then(mod => mod.ProfileComponent)},
    {path: '**', loadComponent: () => import('./components/homepage/homepage.component').then(mod => mod.HomepageComponent)},
];
