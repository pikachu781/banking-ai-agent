package com.voiceai.voice_agent.controller;

import com.voiceai.voice_agent.client.AIServiceClient;
import com.voiceai.voice_agent.dto.AIChatRequest;
import com.voiceai.voice_agent.dto.AIChatResponse;
import com.voiceai.voice_agent.dto.FDRequest;
import com.voiceai.voice_agent.dto.FDResponse;
import org.springframework.web.bind.annotation.*;
import com.voiceai.voice_agent.dto.EMIRequest;
import com.voiceai.voice_agent.dto.EMIResponse;

@RestController
@RequestMapping("/api/ai")
public class AIController {

    private final AIServiceClient aiServiceClient;

    public AIController(AIServiceClient aiServiceClient) {
        this.aiServiceClient = aiServiceClient;
    }

    @GetMapping("/health")
    public String health() {
        return aiServiceClient.checkAIService();
    }

    @PostMapping("/chat")
    public AIChatResponse chat(
            @RequestBody AIChatRequest request
    ) {

        AIChatResponse response =
                aiServiceClient.sendMessage(
                        request.getUser_id(),
                        request.getMessage()
                );

        return response;
    }

    // =====================================================
    // FD CALCULATOR
    // =====================================================

    @PostMapping("/fd/calculate")
    public FDResponse calculateFD(
            @RequestBody FDRequest request
    ) {

        return aiServiceClient.calculateFD(request);
    }
    // =====================================================
// EMI CALCULATOR
// =====================================================

    @PostMapping("/emi/calculate")
    public EMIResponse calculateEMI(
            @RequestBody EMIRequest request
    ) {

        return aiServiceClient.calculateEMI(request);
    }
}