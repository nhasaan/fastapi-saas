#!/usr/bin/env python3
"""
Simple test script to verify the config-vault service is working
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code} - {response.json()}")

def test_tenant_operations():
    """Test tenant CRUD operations"""
    print("\n=== Testing Tenant Operations ===")
    
    # Create tenant
    tenant_data = {
        "name": "Test Tenant",
        "domain": "test-tenant.com"
    }
    response = requests.post(f"{BASE_URL}/config-vault/v1/tenants", json=tenant_data)
    print(f"Create tenant: {response.status_code}")
    if response.status_code == 200:
        tenant = response.json()
        tenant_id = tenant["id"]
        print(f"Created tenant with ID: {tenant_id}")
        
        # Get tenant
        response = requests.get(f"{BASE_URL}/config-vault/v1/tenants/{tenant_id}")
        print(f"Get tenant: {response.status_code}")
        
        # Create site
        site_data = {
            "name": "Test Site",
            "domain": "test-site.com",
            "tenant_id": tenant_id
        }
        response = requests.post(f"{BASE_URL}/config-vault/v1/sites", json=site_data)
        print(f"Create site: {response.status_code}")
        if response.status_code == 200:
            site = response.json()
            site_id = site["id"]
            print(f"Created site with ID: {site_id}")
            
            # Create tenant key
            key_data = {
                "tenant_id": tenant_id,
                "expires_in_days": 365
            }
            response = requests.post(f"{BASE_URL}/config-vault/v1/keys", json=key_data)
            print(f"Create tenant key: {response.status_code}")
            if response.status_code == 200:
                key = response.json()
                print(f"Created key with KID: {key['kid']}")
            
            # Create site key
            key_data = {
                "tenant_id": tenant_id,
                "site_id": site_id,
                "expires_in_days": 365
            }
            response = requests.post(f"{BASE_URL}/config-vault/v1/keys", json=key_data)
            print(f"Create site key: {response.status_code}")
            if response.status_code == 200:
                key = response.json()
                print(f"Created site key with KID: {key['kid']}")
        
        return tenant_id

def test_key_operations(tenant_id):
    """Test key operations"""
    print("\n=== Testing Key Operations ===")
    
    # Get keys by tenant
    response = requests.get(f"{BASE_URL}/config-vault/v1/keys/tenant/{tenant_id}")
    print(f"Get keys by tenant: {response.status_code}")
    if response.status_code == 200:
        keys = response.json()
        print(f"Found {len(keys)} keys for tenant")
        
        if keys:
            kid = keys[0]["kid"]
            # Get key by KID
            response = requests.get(f"{BASE_URL}/config-vault/v1/keys/{kid}")
            print(f"Get key by KID: {response.status_code}")

if __name__ == "__main__":
    try:
        test_health()
        tenant_id = test_tenant_operations()
        if tenant_id:
            test_key_operations(tenant_id)
        print("\n=== All tests completed ===")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the service. Make sure it's running on localhost:8000")
    except Exception as e:
        print(f"Error: {e}")