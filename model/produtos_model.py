import uuid
from sqlalchemy import Column,String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
url = config.get('database','url')

engine = create_engine(url)

Base = declarative_base()


class Produto(Base):
    __tablename__ = 'products'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    descricao = Column(String)
    valor = Column(String)
    def to_dict(self):
        return {
            'id': str(self.id),
            'descricao': self.descricao,
            'valor': self.valor
        }


    
Base.metadata.create_all(engine)