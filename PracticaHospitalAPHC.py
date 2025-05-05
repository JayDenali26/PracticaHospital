import asyncio
import random
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import Semaphore
from threading import Lock
from enum import Enum, auto
from typing import Optional, List, Dict
import aiohttp
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Definimos lo de Enums
class Turno(Enum):
    MATUTINO = auto()
    VESPERTINO = auto()
    NOCTURNO = auto()

class TipoCama(Enum):
    OBSTETRICA = auto()
    GINECOLOGICA = auto()
    UCI = auto()
    DUELO = auto()

class TipoEmergencia(Enum):
    RUTINA = auto()
    MATER = auto()
    MARIPOSA = auto()

# Clase Paciente
class Paciente:
    def __init__(self, id_paciente, nombre, edad, sintomas, turno_ingreso):
        self.id_paciente = id_paciente
        self.nombre = nombre
        self.edad = edad
        self.sintomas = sintomas
        self.turno_ingreso = turno_ingreso
        self.diagnostico = None
        self.prioridad = False
        self.protocolo = TipoEmergencia.RUTINA
        self.cama = None
        self.medico = None
        self.residente = None
        self.necesita_psicologo = False
        self.dias_estancia = 0
        self.dado_de_alta = False

# Modelo de  IA
class ModeloIA:
    def __init__(self):
        self.model = RandomForestClassifier()
        X = np.random.rand(100, 5)
        y = np.random.randint(0, 10, 100)
        self.model.fit(X, y)

    def predecir_diagnostico(self, sintomas):
        time.sleep(random.uniform(0.1, 0.5))
        diagnosticos = list(diagnosticos_posibles.keys())
        pesos = [1.0] * len(diagnosticos)
        pesos[0] = 2.0  # Parto natural
        pesos[1] = 1.5  # Cesárea
        return random.choices(diagnosticos, weights=pesos)[0]

# Diagnosticos posibles con días de estancia
diagnosticos_posibles = {
    "Parto natural exitoso": 2,
    "Cesárea programada": 4,
    "Emergencia obstétrica (MATER)": 6,
    "Pérdida fetal (MARIPOSA)": 3,
    "Complicación postparto": 5,
    "Aborto espontáneo": 2,
    "Control prenatal normal": 1,
    "Cirugía ginecológica (miomectomía)": 4,
    "Cirugía ginecológica (histerectomía)": 5,
    "Revisión ginecológica rutinaria": 1
}

# Gestor de Recursos de asignacion
class GestorDeRecursos:
    def __init__(self):
        self.configuracion_camas = {
            TipoCama.OBSTETRICA: 10,
            TipoCama.GINECOLOGICA: 5,
            TipoCama.UCI: 3,
            TipoCama.DUELO: 2,
        }
        
        self.camas = {
            tipo: Semaphore(cantidad) 
            for tipo, cantidad in self.configuracion_camas.items()
        }
        
        self.medicos_turno = {
            Turno.MATUTINO: ["Dra. Esquivel", "Dr. Uriostegui"],
            Turno.VESPERTINO: ["Dra. Connor", "Dr. Sanchéz"],
            Turno.NOCTURNO: ["Dra. Gamez", "Dr. Herrera"]
        }
        
        self.residentes = [
            "Residente1 García", "Residente2 Lerin",
            "Residente3 Murillo", "Residente4 Añorve"
        ]
        
        self.lock = Lock()
        self.camas_ocupadas = {tipo: 0 for tipo in TipoCama}
        self.camas_disponibles = self.configuracion_camas.copy()

    async def asignar_recursos(self, paciente: Paciente):
        try:
            if paciente.protocolo == TipoEmergencia.MARIPOSA:
                tipo_cama = TipoCama.DUELO
            elif paciente.protocolo == TipoEmergencia.MATER:
                tipo_cama = TipoCama.UCI
            else:
                tipo_cama = random.choice([
                    TipoCama.OBSTETRICA, TipoCama.GINECOLOGICA
                ])
            
            if not await self._adquirir_cama_con_timeout(tipo_cama, timeout=30):
                alternativas = [t for t in TipoCama if t != tipo_cama]
                for alternativa in alternativas:
                    if await self._adquirir_cama_con_timeout(alternativa, timeout=10):
                        tipo_cama = alternativa
                        break
                else:
                    raise Exception(f"No hay camas disponibles para {paciente.nombre}")
            
            with self.lock:
                paciente.cama = tipo_cama
                self.camas_ocupadas[tipo_cama] += 1
                self.camas_disponibles[tipo_cama] -= 1
                paciente.medico = random.choice(self.medicos_turno[paciente.turno_ingreso])
                paciente.residente = random.choice(self.residentes)
                print(f"[Asignación] {paciente.nombre} asignada a {paciente.medico} y {paciente.residente} en cama {paciente.cama.name}.")
        except Exception as e:
            print(f"Error al asignar recursos: {e}")
            raise

    async def _adquirir_cama_con_timeout(self, tipo_cama: TipoCama, timeout: int) -> bool:
        try:
            await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: self.camas[tipo_cama].acquire(timeout=timeout)
                ),
                timeout=timeout
            )
            return True
        except (asyncio.TimeoutError, TimeoutError):
            return False

    def liberar_cama(self, tipo_cama: TipoCama):
        with self.lock:
            self.camas[tipo_cama].release()
            self.camas_ocupadas[tipo_cama] -= 1
            self.camas_disponibles[tipo_cama] += 1

    def estado_camas(self) -> str:
        with self.lock:
            reporte = []
            for tipo in TipoCama:
                total = self.configuracion_camas[tipo]
                ocupadas = self.camas_ocupadas[tipo]
                disponibles = self.camas_disponibles[tipo]
                reporte.append(
                    f"{tipo.name}: {ocupadas} ocupadas | {disponibles} disponibles | {total} total"
                )
            return "\n".join(reporte)

# Funciones de operación
async def consultar_api_psicologo(paciente: Paciente, intentos_maximos=3) -> bool:
    """
    Versión simulada de la API de psicólogo que no requiere conexión real
    """
    diagnosticos_que_requieren_psicologo = {
        "Pérdida fetal (MARIPOSA)",
        "Aborto espontáneo",
        "Emergencia obstétrica (MATER)",
        "Complicación postparto"
    }
    
    try:
        
        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        
        paciente.necesita_psicologo = (
            paciente.protocolo == TipoEmergencia.MARIPOSA or
            paciente.diagnostico in diagnosticos_que_requieren_psicologo or
            random.random() < 0.3  # probabilidad de un 30% a que ocurra
        )
        
        print(f"[API Psicólogo Simulada] {paciente.nombre}: Necesita psicólogo: {paciente.necesita_psicologo}")
        return True
        
    except Exception as e:
        print(f"Error en API psicólogo simulada: {e}")
        paciente.necesita_psicologo = False
        return False

def diagnostico_con_ia(paciente: Paciente):
    try:
        print(f"[IA] Procesando diagnóstico para {paciente.nombre}...")
        modelo = ModeloIA()
        paciente.diagnostico = modelo.predecir_diagnostico(paciente.sintomas)
        paciente.dias_estancia = diagnosticos_posibles.get(paciente.diagnostico, 1)
        
        if "MATER" in paciente.diagnostico:
            paciente.protocolo = TipoEmergencia.MATER
            paciente.prioridad = True
        elif "MARIPOSA" in paciente.diagnostico:
            paciente.protocolo = TipoEmergencia.MARIPOSA
        
        print(f"[Diagnóstico IA] {paciente.nombre}: {paciente.diagnostico} (Estancia: {paciente.dias_estancia} días)")
        return paciente
    except Exception as e:
        print(f"Error en diagnóstico IA para {paciente.nombre}: {e}")
        paciente.diagnostico = "Revisión ginecológica rutinaria"
        paciente.dias_estancia = 1
        return paciente

async def seguimiento_y_alta(paciente: Paciente, gestor: GestorDeRecursos):
    try:
        print(f"[Seguimiento] {paciente.nombre} hospitalizada ({paciente.diagnostico}).")
        
        for dia in range(1, paciente.dias_estancia + 1):
            await asyncio.sleep(0.5)
            print(f"[Seguimiento] Día {dia} para {paciente.nombre}.")
        
        if paciente.protocolo == TipoEmergencia.MARIPOSA or "pérdida" in paciente.diagnostico.lower():
            await consultar_api_psicologo(paciente)
        
        paciente.dado_de_alta = True
        print(f"[Alta] {paciente.nombre} fue dada de alta.")
        return paciente
    except Exception as e:
        print(f"Error en seguimiento para {paciente.nombre}: {e}")
        raise
    finally:
        if paciente.cama and not paciente.dado_de_alta:
            gestor.liberar_cama(paciente.cama)
            print(f"[Limpieza] Cama liberada para {paciente.nombre} por error")

async def proceso_paciente(id_paciente, nombre, edad, sintomas, turno_ingreso, gestor, process_pool):
    paciente = Paciente(id_paciente, nombre, edad, sintomas, turno_ingreso)
    try:
        print(f"\n[Registro] Iniciando proceso para {nombre}, edad {edad}, turno {turno_ingreso.name}.")
        
        paciente = await asyncio.get_event_loop().run_in_executor(
            process_pool, diagnostico_con_ia, paciente
        )
        
        await gestor.asignar_recursos(paciente)
        
        paciente = await seguimiento_y_alta(paciente, gestor)
        
        if paciente.cama:
            gestor.liberar_cama(paciente.cama)
        
        return paciente
    except Exception as e:
        print(f"Error en proceso de {nombre}: {e}")
        if paciente.cama and not paciente.dado_de_alta:
            gestor.liberar_cama(paciente.cama)
        return paciente

# Función principal
async def main():
    print("=== INICIO DEL SISTEMA DE GESTIÓN HOSPITALARIA ===")
    gestor = GestorDeRecursos()
    
    nombres = [f"Paciente {i}" for i in range(1, 16)]
    edades = [random.randint(18, 80) for _ in range(15)]
    sintomas_lista = [
        ["contracciones", "rotura de fuente"],
        ["dolor abdominal intenso"],
        ["sangrado vaginal abundante"],
        ["presión alta", "visión borrosa"],
        ["fiebre alta", "malestar general"],
        ["mareos", "debilidad"],
        ["dolor pélvico crónico"],
        ["seguimiento postparto"],
        ["control prenatal"],
        ["sospecha de embarazo ectópico"]
    ]
    turnos = list(Turno)
    
    with ProcessPoolExecutor(max_workers=4) as process_pool, \
         ThreadPoolExecutor(max_workers=8) as thread_pool:
        
        tareas = []
        for i in range(15):
            nombre = nombres[i]
            edad = edades[i]
            sintomas = random.choice(sintomas_lista)
            turno_ingreso = random.choice(turnos)
            
            tarea = asyncio.create_task(
                proceso_paciente(
                    i + 1, nombre, edad, sintomas, turno_ingreso, 
                    gestor, process_pool
                )
            )
            tareas.append(tarea)
        
        resultados = await asyncio.gather(*tareas, return_exceptions=True)
        
        pacientes_exitosos = [r for r in resultados if isinstance(r, Paciente) and r.dado_de_alta]
        pacientes_fallidos = [r for r in resultados if not (isinstance(r, Paciente) and r.dado_de_alta)]
        
        print("\n=== RESUMEN FINAL ===")
        print(f"\nPacientes atendidos exitosamente: {len(pacientes_exitosos)}")
        for paciente in pacientes_exitosos:
            print(f"- {paciente.nombre}: {paciente.diagnostico} (Estancia: {paciente.dias_estancia} días)")
        
        if pacientes_fallidos:
            print(f"\nPacientes con problemas: {len(pacientes_fallidos)}")
            for paciente in pacientes_fallidos:
                if isinstance(paciente, Paciente):
                    print(f"- {paciente.nombre}: Proceso incompleto")
                else:
                    print(f"- Error: {str(paciente)}")
        
        print("\nEstado final de camas:")
        print(gestor.estado_camas())
        print("\n=== SISTEMA CERRADO ===")

if __name__ == "__main__":
    try:
        asyncio.run(asyncio.wait_for(main(), timeout=300.0))
    except asyncio.TimeoutError:
        print("\n¡Atención! El sistema fue detenido después de 5 minutos.")
    except KeyboardInterrupt:
        print("\n¡Atención! El sistema fue interrumpido manualmente.")
    except Exception as e:
        print(f"\nError crítico en el sistema: {e}")
    finally:
        print("Proceso finalizado.")