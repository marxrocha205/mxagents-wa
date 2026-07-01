import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.domain.entities.contact import Contact

logger = logging.getLogger(__name__)

class ContactRepository:
    """
    Abstrai as operações de base de dados para a entidade Contact.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, phone_number: str, push_name: str = None) -> Contact:
        """
        Procura o contacto pelo número. Se não existir, cria um novo registo.
        Se existir, atualiza o nome (caso o utilizador o tenha alterado no WhatsApp).
        """
        # Procura o utilizador na base de dados
        result = await self.session.execute(
            select(Contact).where(Contact.phone_number == phone_number)
        )
        contact = result.scalars().first()

        if not contact:
            logger.info(f"Novo contacto detetado: {phone_number}. A guardar na base de dados...")
            contact = Contact(phone_number=phone_number, name=push_name)
            self.session.add(contact)
            await self.session.commit()
            await self.session.refresh(contact)
        else:
            # Se já existe mas o nome no WhatsApp mudou, atualizamos
            if push_name and contact.name != push_name:
                contact.name = push_name
                await self.session.commit()
                await self.session.refresh(contact)

        return contact