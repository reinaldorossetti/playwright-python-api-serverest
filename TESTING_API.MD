# Documentação da API ServeRest (resumo)

Esta API de testes utiliza o **ServeRest**, uma API pública que simula uma loja virtual.

- Documentação oficial (Swagger): https://serverest.dev/?lang=pt-BR  
- Swagger JSON: https://serverest.dev/swagger.json?lang=pt-BR

> Sempre consulte o Swagger oficial para detalhes completos de request/response, exemplos e códigos de erro. Abaixo está apenas um resumo das rotas principais para facilitar os testes automatizados deste projeto.

---

## Base URL

Ambiente público do ServeRest:

```text
https://serverest.dev
```

Todas as rotas abaixo são relativas a essa URL.

---

## Autenticação (Login)

Autentica um usuário previamente cadastrado e retorna um token de acesso.

| Método | Caminho    | Descrição         |
|--------|-----------|-------------------|
| POST   | `/login`  | Realizar login    |

- Corpo da requisição: credenciais de usuário (e-mail e senha).
- Resposta de sucesso: token JWT para ser usado nas rotas que exigem autenticação/administrador.

---

## Usuários

Gerenciamento de usuários do sistema (inclusive administradores).

| Método | Caminho            | Descrição                     |
|--------|--------------------|-------------------------------|
| GET    | `/usuarios`        | Listar usuários cadastrados   |
| POST   | `/usuarios`        | Cadastrar novo usuário        |
| GET    | `/usuarios/{_id}`  | Buscar usuário por ID         |
| PUT    | `/usuarios/{_id}`  | Editar usuário existente      |
| DELETE | `/usuarios/{_id}`  | Excluir usuário por ID        |

Observações gerais:

- Alguns cenários exigem usuário **administrador** (ver campo `administrador` no cadastro e o Swagger para regras exatas).
- Erros comuns: e-mail já utilizado, usuário com carrinho ativo que não pode ser excluído etc.

---

## Produtos

Consulta e gerenciamento dos produtos da loja. Operações de escrita normalmente exigem usuário administrador autenticado.

| Método | Caminho             | Descrição                     |
|--------|---------------------|-------------------------------|
| GET    | `/produtos`         | Listar produtos cadastrados   |
| POST   | `/produtos`         | Cadastrar novo produto        |
| GET    | `/produtos/{_id}`   | Buscar produto por ID         |
| PUT    | `/produtos/{_id}`   | Editar produto existente      |
| DELETE | `/produtos/{_id}`   | Excluir produto por ID        |

Observações gerais:

- Nome do produto deve ser único (conferir mensagens de erro no Swagger).
- Estoque e preço são campos importantes para cenários de carrinho.

---

## Carrinhos

Permite criar e gerenciar carrinhos de compras vinculados a um usuário.

| Método | Caminho                          | Descrição                                      |
|--------|-----------------------------------|------------------------------------------------|
| GET    | `/carrinhos`                      | Listar carrinhos cadastrados                   |
| POST   | `/carrinhos`                      | Cadastrar novo carrinho                        |
| GET    | `/carrinhos/{_id}`                | Buscar carrinho por ID                         |
| DELETE | `/carrinhos/concluir-compra`      | Concluir compra (remove carrinho)              |
| DELETE | `/carrinhos/cancelar-compra`      | Cancelar compra e devolver produtos ao estoque |

Observações gerais:

- É necessário estar autenticado para criar carrinho para um usuário.
- Conclusão e cancelamento de compra têm regras específicas de negócio (ver Swagger para detalhes de mensagens e códigos de resposta).

---

## Schemas e exemplos de payloads

O Swagger oficial descreve os principais schemas utilizados, por exemplo:

- `requestBodyUsuarios` – estrutura para cadastro/edição de usuários.
- `requestBodyLogin` – corpo de login.
- `requestBodyProduto` – estrutura de cadastro/edição de produtos.
- `requestBodyCarrinho` – estrutura de criação de carrinho.

Para montar os cenários de teste automatizado (Karate), utilize os exemplos de request/response diretamente do Swagger em https://serverest.dev/?lang=pt-BR.

---

## Testes automatizados (Karate)

Os testes deste projeto são escritos em **Karate** e estão localizados em `src/test/java`. As suítes principais validam autenticação, usuários, produtos e carrinhos da API ServeRest.

### Visão geral das suítes

| Suíte / Funcionalidade | Arquivo                                   | Qtde. de cenários | Criticidade média da suíte | Tags principais                    |
|------------------------|-------------------------------------------|-------------------|---------------------------|------------------------------------|
| Login                  | `serverest/login/Login.feature`           | 5                 | Alta                      | `@login`, `@smoke`, `@regression`  |
| Usuários               | `serverest/usuarios/Users.feature`        | 14                | Alta                      | `@users`, `@smoke`, `@regression`  |
| Produtos               | `serverest/produtos/Products.feature`     | 13                | Alta                      | `@products`, `@smoke`, `@regression` |
| Carrinhos              | `serverest/carrinhos/Carts.feature`       | 8                 | Alta                      | `@carts`, `@regression`            |

Total de cenários automatizados: **40** (5 Login + 14 Usuários + 13 Produtos + 8 Carrinhos).

> As tags `@smoke` identificam cenários de verificação rápida (happy path). A tag `@regression` cobre a bateria completa de testes funcionais e de validação. A criticidade considera impacto no fluxo principal de uso da API (autenticação, CRUD de usuários e produtos).

### Login – autenticação de usuários

Arquivo: `src/test/java/serverest/login/Login.feature`

- **CT01 – Login válido e validação de token**  
	- Tags: `@regression @smoke @login-success`  
	- Tipo: teste positivo, smoke, autenticação básica com geração de token JWT.  
	- Criticidade: **Alta** (login bem-sucedido é o fluxo principal de autenticação).
- **CT02 – Login com credenciais inválidas**  
	- Tags: `@regression`  
	- Tipo: teste negativo, valida mensagem de erro e ausência de token.  
	- Criticidade: **Alta** (garante segurança ao rejeitar credenciais inválidas).
- **CT03 – Campos obrigatórios de login (Scenario Outline)**  
	- Tags: `@regression`  
	- Tipo: validação de obrigatoriedade de `email` e `password` (combinações faltantes, status 400).  
	- Criticidade: **Média** (regras de validação importantes, porém complementares ao fluxo principal).
- **CT04 – Login e acesso a recurso protegido**  
	- Tags: `@regression`  
	- Tipo: integração login + produtos; usa o token para criar um produto autenticado.  
	- Criticidade: **Alta** (valida fim a fim autenticação + autorização em rota protegida).
- **CT05 – Formato inválido de e-mail no login (Scenario Outline)**  
	- Tags: `@regression`  
	- Tipo: teste negativo de validação de formato de e-mail.  
	- Criticidade: **Média** (melhora robustez de validação de entrada).

### Usuários – gestão de usuários

Arquivo: `src/test/java/serverest/usuarios/Users.feature`

- **CT01 – Listar usuários e validar estrutura JSON**  
	- Tags: `@list @smoke @regression`  
	- Tipo: teste positivo/smoke de listagem, com validações estruturais e de conteúdo (quantidade, formato de e-mail, campos obrigatórios).  
	- Criticidade: **Alta** (visualização de usuários e contrato da resposta).
- **CT02 – Buscar usuário específico por ID**  
	- Tags: `@get-by-id @regression`  
	- Tipo: teste positivo de consulta por ID, validando campos retornados.  
	- Criticidade: **Alta** (consulta direta por ID é core do CRUD).
- **CT03 – Criar novo usuário com validações completas**  
	- Tags: `@create @smoke @regression`  
	- Tipo: teste positivo/smoke de criação, seguido de consulta para garantir persistência.  
	- Criticidade: **Alta** (criação de usuário é fluxo crítico da API).
- **CT04 – Validações avançadas com filtros JSON**  
	- Tags: `@advanced-validations @regression`  
	- Tipo: regressão focada em filtros (admins, jsonPath, listas de e-mails).  
	- Criticidade: **Média** (validações avançadas de resposta e filtros).
- **CT05 – Erro ao criar usuário com e-mail duplicado**  
	- Tags: `@error-validation @regression`  
	- Tipo: teste negativo de regra de unicidade de e-mail.  
	- Criticidade: **Alta** (evita inconsistências por duplicidade de e-mail).
- **CT06 – Fuzzy matching para usuários administradores**  
	- Tags: `@fuzzy-validation @regression`  
	- Tipo: validação de usuários com `administrador = true` usando fuzzy matching.  
	- Criticidade: **Média** (garante consistência dos dados de administradores).
- **CT07 – Validações condicionais**  
	- Tags: `@conditional-validation @regression`  
	- Tipo: regressão com validações condicionais com base no campo `administrador`.  
	- Criticidade: **Média** (auxilia no reforço de regras de negócio por perfil).
- **CT08 – Validação com expressões regulares**  
	- Tags: `@regex-validation @regression`  
	- Tipo: validação de formato de e-mail, nome e `_id` usando regex.  
	- Criticidade: **Média** (foco em qualidade de dados e formato).
- **CT09 – Garantir ausência de campos indesejados**  
	- Tags: `@negative-validation @regression`  
	- Tipo: teste negativo que assegura que campos como `error`, `cpf`, `phone` não estejam presentes.  
	- Criticidade: **Baixa/Média** (assegura limpeza de contrato, menor impacto funcional direto).
- **CT10 – Uso de variáveis para validações dinâmicas**  
	- Tags: `@variable-validation @regression`  
	- Tipo: criação e consulta por e-mail dinâmico, garantindo consistência dos dados.  
	- Criticidade: **Média** (reafirma o fluxo de criação + consulta com dados dinâmicos).
- **CT11 – Validação de resposta em criação complexa**  
	- Tags: `@nested-json-validation @regression`  
	- Tipo: criação de usuário com dados "complexos" e validação detalhada da resposta.  
	- Criticidade: **Média** (aprofundamento nas validações de criação).
- **CT12 – Criação de usuário a partir de JSON fixo**  
	- Tags: `@create-from-json @regression`  
	- Tipo: criação baseada em payload fixo (`userPayload.json`), com ajuste de e-mail para evitar duplicidade.  
	- Criticidade: **Média** (garante que payloads fixos usados em testes funcionem corretamente).
- **CT13 – Criar e excluir usuário baseado em payload JSON**  
	- Tags: `@create-and-delete @regression`  
	- Tipo: fluxo completo de criação, exclusão e verificação de inexistência posterior.  
	- Criticidade: **Alta** (fluxo completo de ciclo de vida do usuário).

- **CT14 – Impedir exclusão de usuário com carrinho cadastrado**  
	- Tags: `@delete-with-cart @regression`  
	- Tipo: teste negativo de regra de negócio que impede excluir usuário que possui carrinho associado.  
	- Criticidade: **Alta** (previne perda de vínculo entre usuário e carrinho ativo).

### Produtos – gestão de produtos (necessita admin)

Arquivo: `src/test/java/serverest/produtos/Products.feature`

- **CT01 – Listar produtos e validar estrutura JSON**  
	- Tags: `@list-products @smoke @regression`  
	- Tipo: teste positivo/smoke de listagem com validações estruturais e de campos de preço/quantidade.  
	- Criticidade: **Alta** (consulta básica e contrato de produtos).
- **CT02 – Criar novo produto como administrador**  
	- Tags: `@create-product @smoke @regression`  
	- Tipo: fluxo completo de criação de produto com token admin + consulta por ID.  
	- Criticidade: **Alta** (criação de produto é fluxo core da API de loja).
- **CT03 – Erro ao criar produto com nome duplicado**  
	- Tags: `@duplicate-product @regression`  
	- Tipo: teste negativo de unicidade de nome de produto.  
	- Criticidade: **Alta** (evita inconsistências de catálogo com nomes duplicados).
- **CT04 – Busca de produtos com filtros (query params)**  
	- Tags: `@search-with-filters @regression`  
	- Tipo: regressão que exercita filtros por `nome` e `preco`.  
	- Criticidade: **Média** (importante para usabilidade, mas não bloqueia CRUD básico).
- **CT05 – Atualizar informações de um produto existente**  
	- Tags: `@update-product @regression`  
	- Tipo: fluxo de atualização (PUT) com validação de mensagem e dados atualizados.  
	- Criticidade: **Alta** (atualização de produto é parte do CRUD principal).
- **CT06 – Validações numéricas de preço**  
	- Tags: `@price-validation @regression`  
	- Tipo: análises de máximo, mínimo, média e limites de preço.  
	- Criticidade: **Média** (reforça regras e limites de preço).
- **CT07 – Tentativa de criar produto sem token**  
	- Tags: `@unauthorized @regression`  
	- Tipo: teste negativo de autenticação (401, mensagem de token ausente/inválido).  
	- Criticidade: **Alta** (garante segurança e necessidade de autenticação para escrita).
- **CT08 – Campos obrigatórios na criação de produto (Scenario Outline)**  
	- Tags: `@field-validation @regression`  
	- Tipo: validação de obrigatoriedade/consistência (nome vazio, preço negativo, descrição vazia, quantidade negativa).  
	- Criticidade: **Média** (assegura integridade dos dados cadastrados).
- **CT09 – Agrupamento de produtos por faixa de preço**  
	- Tags: `@complex-json @regression`  
	- Tipo: manipulação de JSON complexo, agrupando em barato/médio/caro.  
	- Criticidade: **Baixa/Média** (cenário exploratório/analítico de dados já existentes).
- **CT10 – Excluir produto existente**  
	- Tags: `@delete-product @regression`  
	- Tipo: fluxo de criação + exclusão + validação de não-encontrado posteriormente.  
	- Criticidade: **Alta** (controle do ciclo de vida do produto).
- **CT11 – Criar produto a partir de JSON fixo**  
	- Tags: `@create-product-from-json @regression`  
	- Tipo: criação baseada em payload fixo (`productPayload.json`) com validação de sucesso.  
	- Criticidade: **Média** (garante que payloads fixos usados em testes funcionem corretamente).

- **CT12 – Impedir exclusão de produto que faz parte de carrinho**  
	- Tags: `@delete-product-in-cart @regression`  
	- Tipo: teste negativo de negócio que impede excluir produto associado a um ou mais carrinhos.  
	- Criticidade: **Alta** (mantém consistência entre catálogo e carrinhos abertos).
- **CT13 – Restringir criação de produto a administradores**  
	- Tags: `@admin-only-route @regression`  
	- Tipo: teste negativo de autorização que valida rota exclusiva para administradores (`administrador = true`).  
	- Criticidade: **Alta** (protege operações críticas de escrita apenas para perfis autorizados).

### Carrinhos – gestão de carrinhos

Arquivo: `src/test/java/serverest/carrinhos/Carts.feature`

- **CT01 – Ciclo completo de carrinho para usuário autenticado**  
	- Tags: `@carts @regression`  
	- Tipo: fluxo fim a fim que cria produto, cria carrinho, busca por ID e conclui compra.  
	- Criticidade: **Alta** (fluxo principal de compra da API).
- **CT02 – Cancelar compra e retornar produtos ao estoque**  
	- Tags: `@carts @regression`  
	- Tipo: fluxo de cancelamento de compra com remoção de carrinho e reabastecimento implícito de estoque.  
	- Criticidade: **Alta** (controle correto do ciclo de vida do carrinho e do estoque).
- **CT03 – Impedir criação de carrinho sem token**  
	- Tags: `@carts @regression`  
	- Tipo: teste negativo de autenticação em `/carrinhos` (401 com mensagem de token ausente/inválido/expirado).  
	- Criticidade: **Alta** (garante que apenas usuários autenticados possam criar carrinho).
- **CT04 – Impedir mais de um carrinho por usuário**  
	- Tags: `@carts @regression`  
	- Tipo: teste negativo de regra de negócio que restringe um único carrinho por usuário.  
	- Criticidade: **Alta** (evita estados inconsistentes de múltiplos carrinhos por usuário).
- **CT05 – Carrinho não encontrado por ID**  
	- Tags: `@carts @regression`  
	- Tipo: teste negativo de consulta com ID inválido, validando mensagem de erro sobre o formato/quantidade de caracteres do ID (16 caracteres alfanuméricos).  
	- Criticidade: **Média** (tratamento de erro de validação de identificador).
- **CT06 – Impedir criação de carrinho com estoque insuficiente**  
	- Tags: `@carts @regression`  
	- Tipo: teste negativo que tenta adicionar ao carrinho quantidade maior que o estoque disponível, validando mensagem de erro.  
	- Criticidade: **Alta** (protege consistência de estoque e regras de venda).
- **CT07 – Impedir carrinho com produtos duplicados**  
	- Tags: `@carts @regression`  
	- Tipo: teste negativo que tenta criar um carrinho contendo o mesmo produto repetido mais de uma vez na lista, esperando mensagem de erro sobre produto duplicado.  
	- Criticidade: **Alta** (evita inconsistências na composição do carrinho e duplicidade de itens).
- **CT08 – Impedir criação de carrinho com produto inexistente**  
	- Tags: `@carts @regression`  
	- Tipo: teste negativo que tenta criar carrinho com um `idProduto` inexistente, validando mensagem de "Produto não encontrado".  
	- Criticidade: **Alta** (garante que apenas produtos válidos sejam associados a carrinhos).

### Classificação geral dos testes

- **Smoke tests**: subset mínimo para checagem rápida da API (`Login CT01`, `Usuários CT01 e CT03`, `Produtos CT01 e CT02`).  
- **Testes de regressão funcionais**: toda a bateria marcada com `@regression`, cobrindo fluxos de CRUD, autenticação, filtros e validações de contrato.  
- **Testes positivos (happy path)**: criação, listagem, consulta, atualização e fluxo de compra bem-sucedidos (por exemplo, CT01/CT03 de Usuários, CT01/CT02/CT05 de Produtos, CT01/CT04 de Login, CT01/CT02 de Carrinhos).  
- **Testes negativos/validação de regras**: credenciais inválidas, campos obrigatórios, formato de e-mail, e-mail duplicado, nome de produto duplicado, criação sem token, valores inválidos, regras de carrinho e autorização de administrador (cenários CT02/CT03/CT05 de Login, CT05/CT14 de Usuários, CT03/CT07/CT08/CT12/CT13 de Produtos, CT03/CT04/CT05/CT06 de Carrinhos).


