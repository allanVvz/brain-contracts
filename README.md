# brain-contracts

Current package version: `1.1.0`.

Version 1.1 keeps every 1.0 payload readable and adds provider completion,
prompt-budget and asked-field telemetry to `ConversationObservation`. Consumers
must continue accepting `contract_version="1.0"` throughout the blue/green
window; removing that adapter requires a later release.

Contratos estritos e versionados entre os serviços Brain AI. Este pacote não contém
regra comercial nem acesso ao banco. Serviços devem fixar uma tag exata.

Versão inicial: `1.0.0`. Origem: `b6ee5edc884e233cc0ff41798f4c19239e04fd88`.
