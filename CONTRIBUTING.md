# Guia de Contribuição - Spacial GAME

Agradecemos o interesse em contribuir com o **Spacial GAME**!

## Como Contribuir

1. **Fork o repositório** para a sua conta no GitHub.
2. **Crie uma branch** para a sua funcionalidade ou correção:
   ```bash
   git checkout -b feature/minha-melhoria
   ```
3. **Instale as dependências** em um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # ou .venv\Scripts\activate no Windows
   pip install -r requirements.txt
   ```
4. **Valide seu código**:
   - Garanta conformidade com a PEP 8.
   - Verifique que os caminhos para arquivos e fontes utilizem `pathlib.Path` ou referências relativas, garantindo portabilidade entre Windows, Linux e macOS.
5. **Abra um Pull Request** detalhando as alterações propostas.
