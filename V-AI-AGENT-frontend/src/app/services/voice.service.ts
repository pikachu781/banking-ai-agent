import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class VoiceService {

  constructor(private http: HttpClient) {}

  speak(text: string): Observable<Blob> {
    return this.http.post(
      `${environment.apiUrl}/api/voice/speak`,
      { text },
      { responseType: 'blob' }
    );
  }
}