
# Practica Hospital APHC

Script de automatización para gestión hospitalaria.

Este repositorio contiene el archivo `PracticaHospitalAPHC.py` con funciones desarrolladas para el control de insumos médicos como camas doctores residentes. 
Se manejan protocolos especiales para casos de emergencia.
Todo se basa en un sistema de Hospital de la Mujer.

el sistema simula un sistema hospitalario inteligente enfocado en la atención de pacientes obstétricos y ginecológicos. Integra procesamiento asincrónico, asignación dinámica de recursos, predicción con inteligencia artificial y gestión automatizada de camas y personal médico, todo en un entorno concurrente y realista.

Características principales
Diagnóstico asistido por IA: Utiliza un modelo de RandomForestClassifier para predecir diagnósticos a partir de síntomas simulados.

Asignación de recursos médicos: Gestión automática de camas, médicos y residentes según el turno y el tipo de emergencia.

Procesamiento asincrónico y concurrente: Usa asyncio, concurrent.futures y multiprocessing para mejorar la eficiencia en el procesamiento de múltiples pacientes.

Simulación de protocolos de emergencia: Incluye manejo especial para casos críticos como emergencias obstétricas (MATER) y pérdidas fetales (MARIPOSA).

Interacción con servicios simulados: Emula una API para determinar si se requiere atención psicológica en ciertos diagnósticos sensibles.

Gestión de altas y seguimiento clínico: Simula el seguimiento hospitalario diario y libera los recursos al alta.

Tecnologías utilizadas
asyncio y concurrent.futures para concurrencia y asincronía

multiprocessing.Semaphore y threading.Lock para sincronización de recursos

scikit-learn para el modelo predictivo

aiohttp (placeholder para simulación de servicios externos)

Estructura del código
Paciente: Clase que representa a cada paciente con sus atributos clínicos y administrativos.

ModeloIA: Encapsula la lógica de predicción de diagnósticos médicos.

GestorDeRecursos: Encargado de la asignación y liberación de camas, médicos y residentes.

proceso_paciente: Orquesta el flujo completo desde el ingreso hasta el alta hospitalaria.

seguimiento_y_alta: Simula la estancia hospitalaria y gestiona el alta médica.

consultar_api_psicologo: Simula la evaluación de necesidad de atención psicológica.

Casos de uso cubiertos
Atención rutinaria, emergencias obstétricas y eventos de duelo.

Priorización de pacientes por protocolo.

Asignación óptima de recursos limitados.

Evaluación del impacto psicológico de diagnósticos complejos.

Seguimiento de pacientes durante su estancia hospitalari
