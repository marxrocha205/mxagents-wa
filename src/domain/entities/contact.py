from sqlalchemy import Column, String, DateTime, Boolean, Integer
from sqlalchemy.sql import func
from src.infrastructure.database.connection import Base

class Contact(Base):
    """
    Representa um cliente/contacto que interagiu com o nosso bot no WhatsApp.
    """
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True) # O nome pode vir do perfil do WhatsApp
    
    # Útil para bloquearmos utilizadores indesejados futuramente
    is_active = Column(Boolean, default=True) 
    
    # Auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Contact(phone_number='{self.phone_number}', name='{self.name}')>"