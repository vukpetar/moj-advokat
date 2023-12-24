import { HttpClient } from '@angular/common/http';
import { Injectable, OnDestroy } from '@angular/core';
import { BaseService } from './base.service';
import { User } from '../models/user.model';
import { environment } from '../../environments/environment';
import { BehaviorSubject, Observable, take, tap } from 'rxjs';
import { StorageService } from './storage.service';


export class Token {
  access_token!: string;
  token_type!: string;
}
@Injectable({
  providedIn: 'root'
})
export class AuthService extends BaseService<User> implements OnDestroy {

  private _authSub$: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  public get isAuthenticated$(): Observable<boolean> {
    return this._authSub$.asObservable();
  }

  constructor(
    protected httpClient: HttpClient,
    private storageService: StorageService
  ) {
    super('/users', httpClient);
  }

  public ngOnDestroy(): void {
    this._authSub$.next(false);
    this._authSub$.complete();
  }

  public login(email: string | null, password: string | null): Observable<any> {
    const formData = new FormData();
    formData.append("grant_type", "");
    formData.append("username", email?? "");
    formData.append("password", password?? "");
    formData.append("scope", "");
    formData.append("client_id", "");
    formData.append("client_secret", "");

    return this.httpClient.post<Token>(`${environment.apiURL}/token`, formData).pipe(
      tap(res => {
        this._authSub$.next(true);
        this.storageService.setItem("accessToken", res.access_token);
    }));
  }

  public activate(email: string, activation_code: string): Observable<any> {
    const formData = new FormData();
    formData.append("email", email);
    formData.append("activation_code", activation_code);

    return this.httpClient.post<Token>(`${environment.apiURL}/users/activate`, formData).pipe(
      tap(res => {
        this._authSub$.next(true);
        this.storageService.setItem("accessToken", res.access_token);
      })
    );
  }

  public refresh_token() {
    return this.httpClient.post<Token>(`${environment.apiURL}/refresh-token`, {}).pipe(
      tap(res => {
        this._authSub$.next(true);
        this.storageService.setItem("accessToken", res.access_token);
      }),
      take(1)
    );
  }

}
