# 🚀 Dodge The Triangles — Juego en Pygame

Dodge The Triangles es un juego arcade en 2D desarrollado con **Python** y **Pygame**.  
El jugador controla un círculo rojo que debe moverse libremente por la pantalla mientras esquiva múltiples enemigos con forma de triángulo.

Es un proyecto ideal para aprender:

- Movimiento y física simple en Pygame
- Estados del juego (menú, jugando, pausa, game over)
- Dibujo de sprites mediante primitivas
- Organización modular de un proyecto de videojuegos

---

## 🎮 Descripción del Juego

El objetivo es **sobrevivir el mayor tiempo posible** evitando chocar contra los triángulos enemigos.  
A medida que pasa el tiempo, tu **puntaje aumenta automáticamente**, y puedes competir por tu mejor score.

Características principales:

- Movimiento fluido usando **WASD**
- Enemigos con movimiento autónomo y rebotes en las paredes
- Pantalla de menú inicial
- Pausa en cualquier momento
- Pantalla de Game Over con reinicio
- Puntaje basado en tiempo sobrevivido

---

## 🛠️ Requisitos

Antes de ejecutar el juego necesitas:

- Python **3.10 o superior**
- Pygame (incluido en `requirements.txt`)

---

## ▶️ Cómo Ejecutar el Juego

A continuación se explica cómo crear un entorno virtual en Python, activarlo e instalar las dependencias usando `requirements.txt`.

### 1. Crear entorno virtual

**Windows:**
```bash
python -m venv venv
```

**Linux/Mac:**
```bash
python -m venv venv
```

### 2. Ejecutar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar depenendcias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar

```bash
python main.py
```