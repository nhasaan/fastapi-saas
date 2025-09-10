# FastAPI SaaS Platform

A microservices-based SaaS platform built with FastAPI, PostgreSQL, and following Domain-Driven Design (DDD) principles.

## Architecture

The platform consists of 4 microservices:

1. **Config Vault Service** - Manages RSA key pairs, tenants, and sites
2. **UAM Service** - User Account Management (users, profiles, roles, permissions)
3. **IAM Service** - Identity and Access Management (JWT authentication)
4. **Content Management Service** - Content management functionality

## Project Structure

```
FastAPI-SaaS/
├── source/                    # Source code for all microservices
│   ├── config-vault/         # Config Vault Service
│   ├── uam/                  # User Account Management Service
│   ├── iam/                  # Identity and Access Management Service
│   └── content-manage/       # Content Management Service
└── orchestrate/              # Orchestration files
    ├── docker-compose.yml    # Docker Compose configuration
    └── k8s/                  # Kubernetes manifests
```

## Config Vault Service

### Features

- **Tenant Management**: Create, read, update, delete tenants
- **Site Management**: Manage sites associated with tenants
- **RSA Key Management**: Generate and manage RSA key pairs for multi-tenant architecture
- **Key Hierarchy**: Support for both tenant-level and site-level keys

### Key Design Decisions

**Key Storage Strategy**: We store RSA keys per tenant with optional site-level keys. This provides:
- Tenant-level keys for general tenant operations
- Site-level keys for specific site operations
- Flexibility to have both or either type

### API Endpoints

#### Tenants
- `POST /config-vault/v1/tenants` - Create tenant
- `GET /config-vault/v1/tenants` - List all tenants
- `GET /config-vault/v1/tenants/{tenant_id}` - Get tenant by ID
- `PUT /config-vault/v1/tenants/{tenant_id}` - Update tenant
- `DELETE /config-vault/v1/tenants/{tenant_id}` - Delete tenant

#### Sites
- `POST /config-vault/v1/sites` - Create site
- `GET /config-vault/v1/sites` - List all sites
- `GET /config-vault/v1/sites/{site_id}` - Get site by ID
- `GET /config-vault/v1/tenants/{tenant_id}/sites` - Get sites by tenant
- `PUT /config-vault/v1/sites/{site_id}` - Update site
- `DELETE /config-vault/v1/sites/{site_id}` - Delete site

#### RSA Keys
- `POST /config-vault/v1/keys` - Create RSA key pair
- `GET /config-vault/v1/keys/{kid}` - Get key by Key ID
- `GET /config-vault/v1/tenants/{tenant_id}/keys` - Get keys by tenant
- `GET /config-vault/v1/sites/{site_id}/keys` - Get keys by site
- `GET /config-vault/v1/tenants/{tenant_id}/keys/active` - Get active keys by tenant
- `GET /config-vault/v1/sites/{site_id}/keys/active` - Get active keys by site
- `POST /config-vault/v1/keys/{key_id}/revoke` - Revoke key
- `POST /config-vault/v1/keys/{key_id}/activate` - Activate key
- `DELETE /config-vault/v1/keys/{key_id}` - Delete key

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+

### Running the Config Vault Service

1. Clone the repository
2. Navigate to the project directory
3. Start the services:

```bash
cd orchestrate
docker-compose up -d
```

The service will be available at `http://localhost:8000`

### API Documentation

Once the service is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Environment Variables

Copy `env.example` to `.env` and configure:

```bash
DATABASE_URL=postgresql://postgres:password@localhost:5432/config_vault
```

## Development

### Project Structure

Each service follows the standard FastAPI backend structure:

```
app/
├── api/                     # API layer
│   ├── api_v1/             # API version 1
│   │   ├── endpoints/      # API endpoints
│   │   └── api.py         # API router
│   └── deps.py            # API dependencies
├── core/                   # Core functionality
│   ├── config.py          # Configuration
│   └── key_generation.py  # Key generation service
├── crud/                   # Database operations
│   ├── base.py            # Base CRUD operations
│   └── crud_*.py          # Specific CRUD operations
├── db/                     # Database configuration
│   ├── base_class.py      # Base class for models
│   ├── base.py           # Database base
│   └── session.py        # Database session
├── models/                 # SQLAlchemy models
├── schemas/                # Pydantic schemas
└── tests/                  # Test files
```

### Database Schema

The Config Vault service uses the following tables with UUID primary keys for security and scalability:

- `tenants` - Tenant information (UUID primary key)
- `sites` - Site information (UUID primary key, linked to tenants)
- `rsa_key_pairs` - RSA key pairs (UUID primary key, linked to tenants and optionally sites)

**UUID Benefits:**
- **Security**: No sequential ID enumeration attacks
- **Privacy**: Harder to guess or predict IDs
- **Scalability**: Better for distributed systems
- **Multi-tenant**: Prevents cross-tenant data leakage

## Next Steps

1. Implement UAM Service
2. Implement IAM Service  
3. Implement Content Management Service
4. Add authentication and authorization
5. Add monitoring and logging
6. Add comprehensive testing
# fastapi-saas
