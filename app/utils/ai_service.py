"""
Serviço de integração com Ollama para geração de feedback usando IA
"""
import httpx
import json
from typing import List, Dict, Any
from datetime import datetime


class OllamaService:
    """Cliente para comunicação com Ollama"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2"):
        self.base_url = base_url
        self.model = model
        self.timeout = 120.0  # 2 minutos para geração
    
    async def generate_feedback(
        self, 
        errors_list: List[Dict[str, Any]], 
        improvements_list: List[Dict[str, Any]],
        user_context: Dict[str, Any]
    ) -> str:
        """
        Gera feedback personalizado baseado nos erros e melhorias observados
        
        Args:
            errors_list: Lista de erros das sessões
            improvements_list: Lista de melhorias observadas
            user_context: Contexto do usuário (idioma nativo, alvo, nível)
        
        Returns:
            Feedback em markdown gerado pela IA
        """
        
        # Construir prompt com contexto
        prompt = self._build_feedback_prompt(errors_list, improvements_list, user_context)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "top_p": 0.9,
                        }
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "")
                else:
                    raise Exception(f"Ollama error: {response.status_code} - {response.text}")
                    
        except httpx.ConnectError:
            raise Exception(
                "Não foi possível conectar ao Ollama. Certifique-se de que o Ollama está rodando "
                "(execute: ollama serve)"
            )
        except httpx.TimeoutException:
            raise Exception("Timeout ao gerar feedback. Tente novamente.")
    
    def _build_feedback_prompt(
        self, 
        errors_list: List[Dict[str, Any]], 
        improvements_list: List[Dict[str, Any]],
        user_context: Dict[str, Any]
    ) -> str:
        """Constrói o prompt para a IA"""
        
        native_lang = user_context.get("native_language", "Unknown")
        target_lang = user_context.get("target_language", "Unknown")
        level = user_context.get("current_level", "Unknown")
        
        # Agregar erros por tipo
        error_summary = {}
        for error in errors_list:
            error_type = error.get("type", "other")
            if error_type not in error_summary:
                error_summary[error_type] = []
            error_summary[error_type].append(error)
        
        # Construir prompt
        prompt = f"""Você é um professor de idiomas experiente. Analise os dados de prática de um aluno e gere um feedback construtivo e motivador.

**Contexto do Aluno:**
- Idioma Nativo: {native_lang}
- Idioma Alvo: {target_lang}
- Nível Atual: {level}

**Erros Observados nas Sessões Recentes:**
"""
        
        if error_summary:
            for error_type, errors in error_summary.items():
                prompt += f"\n### {error_type.replace('_', ' ').title()} ({len(errors)} ocorrências)\n"
                for i, error in enumerate(errors[:3], 1):  # Máximo 3 exemplos por tipo
                    example = error.get("example", error.get("description", "N/A"))
                    prompt += f"{i}. {example}\n"
        else:
            prompt += "\n✅ Nenhum erro significativo detectado!\n"
        
        prompt += "\n**Melhorias Observadas:**\n"
        if improvements_list:
            for i, improvement in enumerate(improvements_list[:5], 1):
                desc = improvement.get("description", improvement.get("area", "N/A"))
                prompt += f"{i}. {desc}\n"
        else:
            prompt += "Ainda coletando dados...\n"
        
        prompt += """
**Tarefa:**
Gere um feedback em português (mesmo que o idioma alvo seja outro) no formato markdown com:

1. **Resumo do Progresso** (2-3 linhas)
2. **Pontos Fortes** (lista com 2-3 itens)
3. **Áreas de Atenção** (lista com os principais erros e como corrigi-los)
4. **Recomendações Práticas** (3-4 sugestões específicas de estudo)
5. **Mensagem Motivacional** (1-2 linhas)

Seja específico, construtivo e encorajador. Use emojis quando apropriado. Foque no aprendizado prático.
"""
        
        return prompt
    
    async def check_connection(self) -> bool:
        """Verifica se o Ollama está acessível"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except:
            return False


# Instância global do serviço
ollama_service = OllamaService()
