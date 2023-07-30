from model.produtos_model import Produto
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser
from sqlalchemy import create_engine
from flask import Flask, jsonify

config = configparser.ConfigParser()
config.read('config.ini')

url = config.get('database','url')

engine = create_engine(url)
Session = sessionmaker(bind=engine)



def busca_produtos():
    Session = sessionmaker(bind=engine)
    session = Session()
    products = session.query(Produto).all()
    return products

def add_produto(descricao,valor):
    Session = sessionmaker(bind=engine)
    session = Session()
    novo_produto = Produto(descricao = descricao, valor = valor)
    session.add(novo_produto)
    session.commit()
    produto_json = novo_produto.to_dict()
    session.close()
    return jsonify(produto_json)

def busca_produto(id):
    session = Session()
    produto = session.query(Produto).filter_by(id=id).first()
    session.close()
    return produto if produto is not None else None

def atualiza_produto(produto):
    try:
        session = Session()
        session.add(produto)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def deletar_produto(produto):
    try: 
        session = Session()
        session.delete(produto)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

