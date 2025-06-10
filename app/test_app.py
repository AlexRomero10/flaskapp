import pytest
import os
from flask import Flask
from app import app  # Importa la app desde tu script principal

def test_inicio(client):
    """Prueba la ruta de inicio y verifica el contador."""
    contador_file = "contador.txt"
    
    # Eliminar el archivo de contador si existe para una prueba limpia
    if os.path.exists(contador_file):
        os.remove(contador_file)
    
    # Simular la primera petición
    response = client.get("/")
    assert response.status_code == 200
    assert "1 visitas" in response.text
    
    # Simular una segunda petición
    response = client.get("/")
    assert response.status_code == 200
    assert "2 visitas" in response.text
    
    # Limpieza después de la prueba
    if os.path.exists(contador_file):
        os.remove(contador_file)

def test_nombre_env(client, monkeypatch):
    """Prueba si la variable de entorno NOMBRE es respetada."""
    monkeypatch.setenv("NOMBRE", "TestUser")
    response = client.get("/")
    assert response.status_code == 200
    assert "App de: TestUser" in response.text
    
@pytest.fixture
def client():
    """Fixture de cliente de prueba para Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
