package com.hospital.aiproxy.controller;

import com.hospital.aiproxy.model.AiRequest;
import com.hospital.aiproxy.model.AiResponse;
import com.hospital.aiproxy.service.AiProxyService;
import org.springframework.web.bind.annotation.*;

@RestController // Indica que esta classe lida com requisições REST/JSON
@RequestMapping("/api/v1/ai-proxy") // Define o prefixo de URL para todos os métodos
public class AiProxyController {

    private final AiProxyService aiProxyService;

    // Injeção de Dependência (Spring cria o objeto AiProxyService e o passa aqui)
    public AiProxyController(AiProxyService aiProxyService) {
        this.aiProxyService = aiProxyService;
    }

    // Mapeia a requisição POST para a URL: /api/v1/ai-proxy/chat
    @PostMapping("/chat")
    public AiResponse chatWithAi(@RequestBody AiRequest request) {
        
        // 1. O Spring automaticamente converte o JSON do monolito para o objeto 'request'
        
        // 2. Chama a lógica de serviço
        AiResponse response = aiProxyService.getAiResponseFromExternalService(request);

        // 3. O Spring automaticamente converte o objeto 'response' de volta para JSON
        // e o envia como resposta HTTP para o monolito.
        return response;
    }
}