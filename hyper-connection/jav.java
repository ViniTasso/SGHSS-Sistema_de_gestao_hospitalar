// AiRequest.java
public class AiRequest {
    private String prompt;

    // Construtor, Getters e Setters (O Lombok ajuda a gerar isso)
    // Para simplificar, vou omitir getters/setters e assumir que você os adicionou ou usou Lombok.

    public String getPrompt() { return prompt; }
    public void setPrompt(String prompt) { this.prompt = prompt; }
}

// AiResponse.java
public class AiResponse {
    private String response;

    // Construtor, Getters e Setters
    public String getResponse() { return response; }
    public void setResponse(String response) { this.response = response; }
}