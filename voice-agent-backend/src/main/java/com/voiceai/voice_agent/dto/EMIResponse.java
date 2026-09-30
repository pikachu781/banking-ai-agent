package com.voiceai.voice_agent.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class EMIResponse {

    private Double principal;
    private Double annual_rate;
    private Double years;
    private Integer months;
    private Double emi;
    private Double total_interest;
    private Double total_payment;
}