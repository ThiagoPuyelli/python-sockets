from abc import ABC, abstractmethod

class IConexion(ABC):
    @abstractmethod
    def conectar(self):
        """Establece la conexión con la base de datos"""
        pass

    @abstractmethod
    def desconectar(self):
        """Cierra la conexión con la base de datos"""
        pass

    @abstractmethod
    def ejecutarConsulta(self, consulta: str) -> str:
        """Ejecuta la consulta que llega por parametro"""
        pass

    @abstractmethod
    def bdRegistradas(self) -> list:
        """Lista las bases de datos registradas en un determinado motor."""
        pass

    @abstractmethod
    def listaDeTablas(self) -> list:
        """Lista las tablas de una determinada BD."""
        pass

    @abstractmethod
    def seleccionarBD(self, bd: str) -> bool:
        """Permite seleccionar la base de datos de un determinado motor."""
        pass