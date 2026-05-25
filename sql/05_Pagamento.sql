USE athletix_db;

CREATE TABLE Pagamento (
    id_pagamento INT AUTO_INCREMENT PRIMARY KEY,
    valor_total DECIMAL(10, 2) NOT NULL,
    forma_pagamento VARCHAR(50) NOT NULL,
    status ENUM('Pendente', 'Pago', 'Cancelado') DEFAULT 'Pendente',
    id_agendamento INT UNIQUE NOT NULL,
    FOREIGN KEY (id_agendamento) REFERENCES Agendamento(id_agendamento) ON DELETE CASCADE
);