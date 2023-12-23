import { isPlatformBrowser } from '@angular/common';
import { Inject, Injectable, PLATFORM_ID } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class StorageService {

  constructor(
    @Inject(PLATFORM_ID) private platformId: object
  ) { }

  public setItem<T>(key: string, value: T | string): void {
    if (!isPlatformBrowser(this.platformId)) {
      return;
    }
    if (typeof value === 'string') {
      localStorage.setItem(this.getKey(key), value);
    } else {
      localStorage.setItem(this.getKey(key), JSON.stringify(value));
    }
  }

  public getItem(key: string): any | null {
    if (!isPlatformBrowser(this.platformId)) {
      return null;
    }
    const item = localStorage.getItem(this.getKey(key));
    
    if (!item) {
      return null;
    }
    try {
      return JSON.parse(item);
    } catch (e) {
      return item;
    }
  }

  removeItem(key: string): void {
    if (!isPlatformBrowser(this.platformId)) {
      return;
    }
    const item = localStorage.getItem(this.getKey(key));
    if (item) {
      localStorage.removeItem(this.getKey(key));
    }
  }

  private getKey(key: string): string {
    return `mojadvokat.${key}`;
  }
}
