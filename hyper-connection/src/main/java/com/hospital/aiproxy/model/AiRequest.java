package com.hospital.aiproxy.model;

// Importante: classes de DTOs são apenas estruturas de dados, não precisam de anotações do Spring
public class AiRequest {

    private String prompt;

    // Construtor vazio (necessário para o Jackson/Spring desserializar o JSON)
    public AiRequest() {}

    // Getters e Setters (métodos para acessar e modificar o campo 'prompt')
    public String getPrompt() {
        return prompt;
    }

    public void setPrompt(String prompt) {
        this.prompt = prompt;
    }
}