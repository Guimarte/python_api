from flask import Flask, make_response, jsonify, request
import bd

app = Flask("api_flask")
app.config['JSONIFY_SORT_KEYS'] = False


@app.route('/produtos', methods=['GET'])
def get_produtos():
    produtos = bd.busca_produtos()
    produtos_json = [produto.to_dict() for produto in produtos]

    # Retornando a lista de produtos serializada em JSON
    return make_response(jsonify(produtos_json))
    


@app.route('/produtos', methods = ['POST'])
def insere_produtos():
    if request.is_json:
        data = request.get_json()  
        descricao = data.get('descricao')
        valor = data.get('valor')
        if descricao is not None and valor is not None:
            bd.add_produto(descricao, valor)  

            return jsonify({"message": "Produtos inseridos com sucesso."}), 201
        else:
            return jsonify({"error": "Dados inválidos no corpo da requisição."}), 400  
    else:
        return jsonify({"error": "Corpo da requisição não contém dados JSON."}), 400 

    
@app.route('/produtos/<id>', methods = ['GET'])
def busca_produto(id):
    produto =  bd.busca_produto(id=id)
    if produto is not None:
        produto_json = produto.to_dict()
        return jsonify(produto_json), 200
    else:
        return jsonify({"error": "Produto não encontrado."}), 404
    
    
@app.route('/produtos/<id>', methods=['PUT'])
def atualiza_produto(id):
    produto = bd.busca_produto(id)
    if produto is not None:
        if request.is_json:
            data = request.get_json()
            descricao = data.get('descricao')
            valor = data.get('valor')

            if descricao is not None:
                produto.descricao = descricao
            if valor is not None:
                produto.valor = valor

            bd.atualiza_produto(produto)

            return jsonify({"message": "Produto atualizado com sucesso."}), 200
        else:
            return jsonify({"error": "Corpo da requisição não contém dados JSON."}), 400
    else:
        return jsonify({"error": "Produto não encontrado."}), 404
    
    
@app.route('/produtos/<id>', methods=['DELETE'])
def deleta_produto(id):
    produto = bd.busca_produto(id)
    if produto is not None:
        bd.deletar_produto(produto)
        return jsonify({"message": "Produto atualizado com sucesso."}), 200
    else:return jsonify({"error": "Produto não encontrado."}), 404
        


    
    




app.run()
