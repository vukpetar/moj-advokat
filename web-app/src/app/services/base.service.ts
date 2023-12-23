import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';


type valueType = string | number | boolean;
export type ParamType = { [key: string]: valueType | valueType[] } | undefined;
export declare type Nullish = null | undefined;

export class ApiData<T> {
  data: T;
  totalCount?: number;

  constructor(data: T) {
    this.data = data;
  }
}

export abstract class BaseService<T extends object> {

  constructor(
    protected url: string,
    protected http: HttpClient,
  ) {
    this.url = environment.apiURL + url;
  }


  all(data?: ParamType): Observable<ApiData<T>[]> {
    return this.http
      .get<ApiData<T>[]>(this.url, {
        params: data,
      });
  }

  get(id: number, data?: ParamType): Observable<ApiData<T>> {
    return this.http
      .get<ApiData<T>>(`${this.url}/${id}`, {
        params: data,
      });
  }

  save(data: any): Observable<T> {
    return this.http.post<T>(this.url, data);
  }

}
