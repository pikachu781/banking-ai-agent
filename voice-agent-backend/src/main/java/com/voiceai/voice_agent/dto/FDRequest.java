package com.voiceai.voice_agent.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class FDRequest {

    private Double principal;
    private Double rate;
    private Double years;
}