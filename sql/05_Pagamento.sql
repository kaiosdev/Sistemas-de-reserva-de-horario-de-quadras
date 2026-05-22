USE athletix_db;

-- Cria a tabela financeira final do sistema
CREATE TABLE Pagamento (
    id_pagamento INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    data_pagamento DATE NOT NULL,
    status_pagamento VARCHAR(20) DEFAULT 'Pendente',
    -- Relacionamento com a tabela criada pelo Membro 1 (Construtor Base)
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
);
