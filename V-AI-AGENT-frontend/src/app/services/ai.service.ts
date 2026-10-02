import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../environments/environment';


/* ============================================================
   CHAT REQUEST
============================================================ */

export interface ChatRequest {

  user_id: number;

  message: string;

}


/* ============================================================
   CHAT RESPONSE
============================================================ */

export interface ChatResponse {

  response: string;

  action?: string;

}


/* ============================================================
   AI SERVICE
============================================================ */

@Injectable({
  providedIn: 'root'
})

export class AiService {

  private apiUrl =
    `${environment.apiUrl}/api/ai`;


  constructor(
    private http: HttpClient
  ) {}


  /* ==========================================================
     SEND MESSAGE
  ========================================================== */

  sendMessage(
    request: ChatRequest
  ): Observable<ChatResponse> {

    return this.http.post<ChatResponse>(
      `${this.apiUrl}/chat`,
      request
    );

  }


  /* ==========================================================
     FD CALCULATOR
  ========================================================== */

  calculateFd(data: {
    principal: number;
    rate: number;
    years: number;
  }): Observable<any> {

    return this.http.post<any>(
      `${this.apiUrl}/fd/calculate`,
      data
    );

  }
  /* ==========================================================
   EMI CALCULATOR
========================================================== */

calculateEmi(data: {
  principal: number;
  annual_rate: number;
  years: number;
}): Observable<any> {

  return this.http.post<any>(
    `${this.apiUrl}/emi/calculate`,
    data
  );

}

}