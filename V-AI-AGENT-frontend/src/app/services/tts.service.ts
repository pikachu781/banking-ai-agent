import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class TtsService {

  private provider: 'browser' | 'elevenlabs' = 'browser';

  speak(text: string): void {

    if (this.provider === 'browser') {
      this.browserSpeak(text);
    }

    // ElevenLabs will be added here later
  }

  private browserSpeak(text: string): void {

    if (!('speechSynthesis' in window)) {
      console.error('Text-to-Speech is not supported in this browser.');
      return;
    }

    // Stop previous speech
    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);

    speech.lang = 'en-US';
    speech.rate = 1;
    speech.pitch = 1;
    speech.volume = 1;

    speech.onstart = () => {
      console.log('🔊 TTS started');
    };

    speech.onend = () => {
      console.log('🔊 TTS finished');
    };

    speech.onerror = (error) => {
      console.error('TTS error:', error);
    };

    window.speechSynthesis.speak(speech);
  }

  stop(): void {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
  }
}