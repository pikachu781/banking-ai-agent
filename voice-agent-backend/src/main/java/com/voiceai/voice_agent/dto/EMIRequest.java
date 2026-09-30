package com.voiceai.voice_agent.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class EMIRequest {

    private Double principal;
    private Double annual_rate;
    private Double years;
}