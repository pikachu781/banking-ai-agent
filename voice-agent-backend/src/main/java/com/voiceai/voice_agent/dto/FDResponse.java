package com.voiceai.voice_agent.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class FDResponse {

    private Double principal;
    private Double rate;
    private Double years;
    private Double interest;

    private Double maturity_amount;
}