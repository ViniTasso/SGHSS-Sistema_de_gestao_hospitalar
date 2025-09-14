-- Cria a tabela de usuários e roles para o monolito
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS sghss_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    role_id INTEGER REFERENCES roles(id)
);

-- Insere as roles básicas
INSERT INTO roles (nome) VALUES ('administrador') ON CONFLICT (nome) DO NOTHING;
INSERT INTO roles (nome) VALUES ('paciente') ON CONFLICT (nome) DO NOTHING;
INSERT INTO roles (nome) VALUES ('profissional') ON CONFLICT (nome) DO NOTHING;

-- Tabela de Pacientes
CREATE TABLE IF NOT EXISTS patients (
    user_id UUID PRIMARY KEY REFERENCES sghss_users(id),
    cpf VARCHAR(14) UNIQUE NOT NULL,
    nome_completo VARCHAR(255) NOT NULL,
    data_nascimento DATE,
    telefone VARCHAR(20)
);

-- Tabela de Prontuários Médicos
CREATE TABLE IF NOT EXISTS medical_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID UNIQUE REFERENCES patients(user_id)
);

-- Tabela de Profissionais de Saúde
CREATE TABLE IF NOT EXISTS healthcare_professionals (
    user_id UUID PRIMARY KEY REFERENCES sghss_users(id),
    crm VARCHAR(50) UNIQUE,
    especialidade VARCHAR(100)
);
