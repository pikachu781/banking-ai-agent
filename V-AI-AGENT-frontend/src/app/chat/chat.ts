import { CommonModule } from '@angular/common';

import {
  ChangeDetectorRef,
  Component,
  ElementRef,
  ViewChild,
  inject
} from '@angular/core';
import { Router } from '@angular/router';

import { FormsModule } from '@angular/forms';

import {
  AiService,
  ChatResponse
} from '../services/ai.service';

import { AuthService } from '../services/auth.service';

import { TtsService } from '../services/tts.service';


interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}


@Component({
  selector: 'app-chat',
  standalone: true,

  imports: [
    CommonModule,
    FormsModule
  ],

  templateUrl: './chat.html',
  styleUrl: './chat.css'
})


export class ChatComponent {

  // =====================================================
  // SERVICES
  // =====================================================

  private aiService = inject(AiService);

  

  private authService = inject(AuthService);

  private cdr = inject(ChangeDetectorRef);

  private router = inject(Router);

  private ttsService = inject(TtsService);


  // =====================================================
  // CHAT CONTAINER
  // =====================================================

  @ViewChild('chatContainer')
  chatContainer!: ElementRef;


  // =====================================================
  // USER
  // =====================================================

  userId: number = 0;


  // =====================================================
  // CHAT
  // =====================================================

  message = '';

  messages: ChatMessage[] = [];

  loading = false;
// =====================================================
// FD CALCULATOR
// =====================================================

showFdCalculator = false;

fdAmount: number | null = null;

fdRate: number | null = null;

fdTenure: number | null = null;

fdTenureUnit: 'years' | 'months' = 'years';

fdCalculating = false;

fdResult: any = null;


// ==========================================================
// EMI CALCULATOR
// ==========================================================

showEmiCalculator = false;

emiAmount: number | null = null;

emiRate: number | null = null;

emiTenure: number | null = null;

emiTenureUnit: 'years' | 'months' = 'years';

emiCalculating = false;

emiResult: any = null;

  // =====================================================
  // VOICE INPUT
  // =====================================================

  isListening = false;

  private recognition: any = null;


  // =====================================================
  // TEXT TO SPEECH
  // =====================================================

  isSpeaking = false;


  // =====================================================
  // CONSTRUCTOR
  // =====================================================

  constructor() {

    const id = this.authService.getUserId();

    if (id) {

      this.userId = Number(id);

    }

  }


  // =====================================================
  // SEND MESSAGE
  // =====================================================

  sendMessage(): void {

    const text = this.message.trim();


    if (!text || this.loading) {
      return;
    }


    // ===================================================
    // LOGIN CHECK
    // ===================================================

    if (!this.userId) {

      console.error('User is not logged in');

      return;
    }


    // ===================================================
    // STOP CURRENT SPEECH
    // ===================================================

    this.stopSpeaking();


    // ===================================================
    // ADD USER MESSAGE
    // ===================================================

    this.messages.push({

      role: 'user',

      content: text

    });


    // ===================================================
    // CLEAR INPUT
    // ===================================================

    this.message = '';


    // ===================================================
    // START LOADING
    // ===================================================

    this.loading = true;

    this.cdr.detectChanges();

    this.scrollToBottom();


    // ===================================================
    // CALL AI API
    // ===================================================

    this.aiService

      .sendMessage({

        user_id: this.userId,

        message: text

      })

      .subscribe({

        // =================================================
        // SUCCESS
        // =================================================

        next: (response: ChatResponse) => {

          console.log(
            'Angular received:',
            response
          );
       // ===============================================
       // CHECK BACKEND ACTION
     // ===============================================

     if (response.action === 'OPEN_FD_CALCULATOR') {

  console.log(
    'Opening manual FD calculator'
  );

  this.showFdCalculator = true;

  this.fdResult = null;

}

if (response.action === 'OPEN_EMI_CALCULATOR') {

  console.log(
    'Opening manual EMI calculator'
  );

  this.showEmiCalculator = true;

  this.emiResult = null;

}

// ===============================================
// AI PAGE NAVIGATION
// ===============================================

if (
  response.action &&
  response.action.startsWith('/')
) {

  console.log(
    'AI navigation action:',
    response.action
  );

  this.router.navigateByUrl(
    response.action
  );

}
          // ===============================================
          // ADD AI MESSAGE
          // ===============================================

          this.messages.push({

            role: 'assistant',

            content: response.response

          });


          // ===============================================
          // STOP LOADING
          // ===============================================

          this.loading = false;


          // ===============================================
          // UPDATE UI
          // ===============================================

          this.cdr.detectChanges();

          this.scrollToBottom();


          // ===============================================
          // SPEAK AI RESPONSE
          // ===============================================

          this.speakResponse(
            response.response
          );

        },


        // =================================================
        // ERROR
        // =================================================

        error: (error) => {

          console.error(
            'AI chat error:',
            error
          );


          this.messages.push({

            role: 'assistant',

            content:
              'Sorry, something went wrong. Please try again.'

          });


          this.loading = false;


          // ===============================================
          // UPDATE UI
          // ===============================================

          this.cdr.detectChanges();

          this.scrollToBottom();

        }

      });

  }
  // =====================================================
// OPEN FD CALCULATOR
// =====================================================

openFdCalculator(): void {

  this.showFdCalculator = true;

  this.fdResult = null;

}


// =====================================================
// CLOSE FD CALCULATOR
// =====================================================

closeFdCalculator(): void {

  this.showFdCalculator = false;

  this.fdResult = null;

}


// =====================================================
// CALCULATE FD
// =====================================================

calculateFd(): void {

  console.log('========== FD CALCULATION ==========');

  // =====================================================
  // VALIDATION
  // =====================================================

  if (
    this.fdAmount === null ||
    this.fdRate === null ||
    this.fdTenure === null
  ) {

    alert(
      'Please enter amount, interest rate and tenure.'
    );

    return;
  }


  if (
    this.fdAmount <= 0 ||
    this.fdRate <= 0 ||
    this.fdTenure <= 0
  ) {

    alert(
      'Please enter valid positive values.'
    );

    return;
  }


  // =====================================================
  // CONVERT TENURE TO YEARS
  // =====================================================

  let years = this.fdTenure;

  if (this.fdTenureUnit === 'months') {

    years = this.fdTenure / 12;

  }


  // =====================================================
  // START CALCULATION
  // =====================================================

  this.fdCalculating = true;

  this.fdResult = null;

  this.cdr.detectChanges();


  console.log('Sending FD data to backend...');

  console.log({
    principal: this.fdAmount,
    rate: this.fdRate,
    years: years
  });


  // =====================================================
  // CALL BACKEND
  // =====================================================

  this.aiService.calculateFd({

    principal: this.fdAmount,

    rate: this.fdRate,

    years: years

  }).subscribe({

    // ===================================================
    // SUCCESS
    // ===================================================

    next: (result) => {

      console.log(
        'FD backend result:',
        result
      );


      this.fdResult = {

        principal: result.principal,

        rate: result.rate,

        years: result.years,

        interest: result.interest,

        maturityAmount:
          result.maturity_amount

      };


      this.fdCalculating = false;

      this.cdr.detectChanges();


      console.log(
        'FD calculation completed successfully'
      );

    },


    // ===================================================
    // ERROR
    // ===================================================

    error: (error) => {

      console.error(
        'FD calculation error:',
        error
      );


      this.fdCalculating = false;

      this.fdResult = null;

      this.cdr.detectChanges();


      alert(
        'Unable to calculate FD. Please try again.'
      );

    }

  });

}
// =====================================================
// RESET FD CALCULATOR
// =====================================================

resetFdCalculator(): void {

  console.log('========== FD RESET ==========');

  this.fdAmount = null;
  this.fdRate = null;
  this.fdTenure = null;
  this.fdTenureUnit = 'years';

  // Remove previous calculation result
  this.fdResult = null;

  // Force UI update
  this.cdr.detectChanges();

  console.log('FD calculator reset successfully');
}

  // =====================================================
  // TEXT TO SPEECH
  // =====================================================

  speakResponse(text: string): void {

    if (!text) {
      return;
    }


    // Stop previous speech

    this.ttsService.stop();


    // Update UI

    this.isSpeaking = true;

    this.cdr.detectChanges();


    // Start speech

    this.ttsService.speak(text);


    /*
     * Estimate speech duration.
     *
     * Browser SpeechSynthesis does not provide
     * a reliable Angular-friendly completion event.
     */

    const estimatedTime =
      Math.max(
        2000,
        text.length * 55
      );


    setTimeout(() => {

      this.isSpeaking = false;

      this.cdr.detectChanges();

    }, estimatedTime);

  }


  // =====================================================
  // SPEAK MESSAGE
  // =====================================================

  speakMessage(text: string): void {

    this.stopSpeaking();

    this.speakResponse(text);

  }


  // =====================================================
  // STOP SPEAKING
  // =====================================================

  stopSpeaking(): void {

    this.ttsService.stop();

    this.isSpeaking = false;

    this.cdr.detectChanges();

  }


  // =====================================================
  // START VOICE INPUT
  // =====================================================

  startVoiceInput(): void {

    const SpeechRecognition =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;


    // ===================================================
    // BROWSER SUPPORT
    // ===================================================

    if (!SpeechRecognition) {

      alert(
        'Speech recognition is not supported in this browser. Please use Google Chrome.'
      );

      return;
    }


    // ===================================================
    // STOP IF ALREADY LISTENING
    // ===================================================

    if (this.isListening) {

      this.stopVoiceInput();

      return;
    }


    // ===================================================
    // CREATE RECOGNITION
    // ===================================================

    this.recognition =
      new SpeechRecognition();


    // ===================================================
    // SETTINGS
    // ===================================================

    this.recognition.lang = 'en-IN';

    this.recognition.continuous = false;

    this.recognition.interimResults = true;


    // ===================================================
    // START LISTENING
    // ===================================================

    this.isListening = true;

    this.cdr.detectChanges();


    this.recognition.start();


    // ===================================================
    // SPEECH RESULT
    // ===================================================

    this.recognition.onresult =
      (event: any) => {

        let transcript = '';


        for (
          let i = event.resultIndex;
          i < event.results.length;
          i++
        ) {

          transcript +=
            event.results[i][0].transcript;

        }


        // Update input

        this.message = transcript;


        // IMPORTANT:
        // SpeechRecognition is a browser API.
        // Force Angular UI update.

        this.cdr.detectChanges();

      };


    // ===================================================
    // SPEECH ERROR
    // ===================================================

    this.recognition.onerror =
      (event: any) => {

        console.error(
          'Speech recognition error:',
          event.error
        );


        this.isListening = false;


        // IMPORTANT

        this.cdr.detectChanges();

      };


    // ===================================================
    // SPEECH END
    // =====================================================

    this.recognition.onend =
      () => {

        this.isListening = false;

        this.recognition = null;


        // IMPORTANT

        this.cdr.detectChanges();

      };

  }


  // =====================================================
  // STOP VOICE INPUT
  // =====================================================

  stopVoiceInput(): void {

    if (this.recognition) {

      this.recognition.stop();

      this.recognition = null;

    }


    this.isListening = false;


    this.cdr.detectChanges();

  }


  // =====================================================
  // ENTER KEY
  // =====================================================

  onEnter(event: Event): void {

    const keyboardEvent =
      event as KeyboardEvent;


    if (!keyboardEvent.shiftKey) {

      keyboardEvent.preventDefault();

      this.sendMessage();

    }

  }


  // =====================================================
  // AUTO SCROLL
  // =====================================================

  private scrollToBottom(): void {

    setTimeout(() => {

      if (!this.chatContainer) {
        return;
      }


      const element =
        this.chatContainer.nativeElement;


      element.scrollTop =
        element.scrollHeight;

    }, 100);

  }
  // ==========================================================
// CALCULATE EMI
// ==========================================================

calculateEmi(): void {

  console.log('========== EMI CALCULATION ==========');

  if (
    this.emiAmount === null ||
    this.emiRate === null ||
    this.emiTenure === null
  ) {

    alert(
      'Please enter loan amount, interest rate and tenure.'
    );

    return;
  }

  if (
    this.emiAmount <= 0 ||
    this.emiRate <= 0 ||
    this.emiTenure <= 0
  ) {

    alert(
      'Please enter valid positive values.'
    );

    return;
  }

  let years = this.emiTenure;

  if (this.emiTenureUnit === 'months') {

    years = this.emiTenure / 12;

  }

  this.emiCalculating = true;

  this.emiResult = null;

  this.cdr.detectChanges();

  console.log('Sending EMI data to backend...');

  console.log({
    principal: this.emiAmount,
    annual_rate: this.emiRate,
    years: years
  });

  this.aiService.calculateEmi({

    principal: this.emiAmount,

    annual_rate: this.emiRate,

    years: years

  }).subscribe({

    next: (result) => {

      console.log(
        'EMI backend result:',
        result
      );

      this.emiResult = {

        principal: result.principal,

        annualRate: result.annual_rate,

        years: result.years,

        months: result.months,

        emi: result.emi,

        totalInterest:
          result.total_interest,

        totalPayment:
          result.total_payment

      };

      this.emiCalculating = false;

      this.cdr.detectChanges();

      console.log(
        'EMI calculation completed successfully'
      );

    },

    error: (error) => {

      console.error(
        'EMI calculation error:',
        error
      );

      this.emiCalculating = false;

      this.emiResult = null;

      this.cdr.detectChanges();

      alert(
        'Unable to calculate EMI. Please try again.'
      );

    }

  });

}
// ==========================================================
// RESET EMI CALCULATOR
// ==========================================================

resetEmiCalculator(): void {

  console.log('========== EMI RESET ==========');

  this.emiAmount = null;

  this.emiRate = null;

  this.emiTenure = null;

  this.emiTenureUnit = 'years';

  this.emiResult = null;

  this.cdr.detectChanges();

  console.log(
    'EMI calculator reset successfully'
  );

}
 

}