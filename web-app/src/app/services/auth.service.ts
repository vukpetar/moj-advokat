import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BaseService } from './base.service';
import { User } from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService extends BaseService<User> {

  constructor(
    protected httpClient: HttpClient,
  ) {
    super('/users', httpClient);
  }
}
