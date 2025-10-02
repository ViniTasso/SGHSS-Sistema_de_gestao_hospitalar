package com.hospital.aiproxy.service;

import com.hospital.aiproxy.model.AiRequest;
import com.hospital.aiproxy.model.AiResponse;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service // Marca a classe como um 'Service' (Componente de Negócio) do Spring
public class AiProxyService {

    // URL do Microsserviço de IA (Python)
    private final String AI_SERVICE_URL = "http://ai-service:8002/api/ai/chat";
    
    // Ferramenta do Spring para fazer chamadas HTTP sincronas
    private final RestTemplate restTemplate = new RestTemplate(); 

    /**
     * Função que recebe o prompt, chama o microsserviço de IA e retorna a resposta.
     */
    public AiResponse getAiResponseFromExternalService(AiRequest request) {
        
        // Faz a chamada POST: 
        // 1. URL de destino
        // 2. Objeto de requisição (que será convertido para JSON pelo RestTemplate)
        // 3. Tipo da classe que o JSON de retorno deve ser convertido
        
        AiResponse response = restTemplate.postForObject(
            AI_SERVICE_URL, 
            request, 
            AiResponse.class // O Spring/Jackson fará a conversão do JSON para AiResponse
        );

        // Se a chamada for bem sucedida, 'response' terá o objeto pronto
        return response;
    }
}