package com.voiceai.voice_agent.client;

import com.voiceai.voice_agent.dto.AIChatRequest;
import com.voiceai.voice_agent.dto.AIChatResponse;
import org.springframework.http.client.JdkClientHttpRequestFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;
import com.voiceai.voice_agent.dto.FDRequest;
import com.voiceai.voice_agent.dto.FDResponse;
import com.voiceai.voice_agent.dto.EMIRequest;
import com.voiceai.voice_agent.dto.EMIResponse;
import java.net.http.HttpClient;
import java.time.Duration;

@Component
public class AIServiceClient {

    private final RestClient restClient;

    public AIServiceClient() {

        HttpClient httpClient = HttpClient.newBuilder()
                .version(HttpClient.Version.HTTP_1_1)
                .connectTimeout(Duration.ofSeconds(10))
                .build();

        JdkClientHttpRequestFactory requestFactory =
                new JdkClientHttpRequestFactory(httpClient);

        this.restClient = RestClient.builder()
                .baseUrl("http://127.0.0.1:8000")
                .requestFactory(requestFactory)
                .build();
    }

    public String checkAIService() {

        return restClient.get()
                .uri("/api/health")
                .retrieve()
                .body(String.class);
    }

    public String testFastApi() {

        return restClient.get()
                .uri("/api/test")
                .retrieve()
                .body(String.class);
    }

    public AIChatResponse sendMessage(
            Long userId,
            String message
    ) {

        AIChatRequest request = new AIChatRequest();

        request.setUser_id(userId);
        request.setMessage(message);

        System.out.println(
                "Sending request to FastAPI..."
        );

        System.out.println(
                "URL: http://127.0.0.1:8000/api/ai/chat"
        );

        System.out.println(
                "User ID: " + userId
        );

        System.out.println(
                "Message: " + message
        );

        AIChatResponse response = restClient.post()
                .uri("/api/ai/chat")
                .body(request)
                .retrieve()
                .body(AIChatResponse.class);

        System.out.println(
                "FastAPI response: "
                        + response.getResponse()
        );

        System.out.println(
                "FastAPI action: "
                        + response.getAction()
        );

        return response;
    }
    public FDResponse calculateFD(FDRequest request) {

        System.out.println(
                "========== FD CALCULATION =========="
        );

        System.out.println(
                "Principal: " + request.getPrincipal()
        );

        System.out.println(
                "Rate: " + request.getRate()
        );

        System.out.println(
                "Years: " + request.getYears()
        );

        FDResponse response = restClient.post()
                .uri("/api/ai/fd/calculate")
                .body(request)
                .retrieve()
                .body(FDResponse.class);

        System.out.println(
                "FD Interest: " + response.getInterest()
        );

        System.out.println(
                "FD Maturity: " + response.getMaturity_amount()
        );

        return response;
    }
    // =====================================================
// EMI CALCULATOR
// =====================================================

    public EMIResponse calculateEMI(EMIRequest request) {

        System.out.println(
                "========== EMI CALCULATION =========="
        );

        System.out.println(
                "Principal: " + request.getPrincipal()
        );

        System.out.println(
                "Annual Rate: " + request.getAnnual_rate()
        );

        System.out.println(
                "Years: " + request.getYears()
        );

        EMIResponse response = restClient.post()
                .uri("/api/ai/emi/calculate")
                .body(request)
                .retrieve()
                .body(EMIResponse.class);

        System.out.println(
                "Monthly EMI: " + response.getEmi()
        );

        System.out.println(
                "Total Interest: "
                        + response.getTotal_interest()
        );

        System.out.println(
                "Total Payment: "
                        + response.getTotal_payment()
        );

        return response;
    }
}