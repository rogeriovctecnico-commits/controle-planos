from flask import render_template, redirect, url_for, flash, request, Blueprint
from ...extensions import db
from ...models import PrecoFaixaEtaria, Plano
from ...forms import PrecoFaixaForm
from . import precos_bp

@precos_bp.route("/")
def list_precos():
    page = request.args.get("page", 1, type=int)
    search_term = request.args.get("q", "")

    query = PrecoFaixaEtaria.query.join(Plano)

    if search_term:
        search_term = search_term.strip()
        query = query.filter(Plano.nome_plano.ilike(f"%{search_term}%"))

    precos = query.order_by(PrecoFaixaEtaria.plano_id.desc()).paginate(page=page, per_page=10)
    return render_template("precos_list.html", precos=precos, search_term=search_term)

@precos_bp.route("/create", methods=["GET", "POST"])
def create_preco():
    # --- Parâmetros da URL para pré-preenchimento e foco ---
    plano_id_param = request.args.get('plano_id', type=int)
    focus_param = request.args.get('focus')
    next_idade_min = request.args.get('next_idade_min', type=int)
    next_idade_max = request.args.get('next_idade_max', type=int)
    
    # --- Cria o formulário, pré-preenchendo com os dados da URL ---
    form = PrecoFaixaForm(
        plano_id=plano_id_param,
        idade_min=next_idade_min,
        idade_max=next_idade_max
    )
    
    # --- Define o foco automático no campo solicitado ---
    if focus_param == 'idade_min':
        form.idade_min.render_kw = {"autofocus": True}
    elif focus_param == 'valor':
        form.valor.render_kw = {"autofocus": True}

    if form.validate_on_submit():
        # --- VERIFICAÇÃO DE DUPLICIDADE ---
        # Verifica pelo NOME do plano para evitar duplicatas em planos homônimos
        selected_plano = Plano.query.get(form.plano_id.data)
        existing_preco = None
        if selected_plano:
            existing_preco = PrecoFaixaEtaria.query.join(Plano).filter(
                Plano.nome_plano == selected_plano.nome_plano,
                PrecoFaixaEtaria.idade_min == form.idade_min.data,
                PrecoFaixaEtaria.idade_max == form.idade_max.data
            ).first()

        if existing_preco:
            # Busca o nome do plano para exibir na mensagem de erro, ajudando a identificar confusões de nomes similares
            nome_plano = selected_plano.nome_plano if selected_plano else "selecionado"
            flash(f"Já existe uma faixa de preço ({form.idade_min.data} a {form.idade_max.data} anos) cadastrada para o plano '{nome_plano}'. Verifique se selecionou o plano correto.", "danger")
            return render_template("precos_form.html", form=form, title="Nova Faixa Etária")
        # --- FIM DA VERIFICAÇÃO ---
        
        # --- Salva o novo registro ---
        preco = PrecoFaixaEtaria()
        preco.plano_id=form.plano_id.data
        preco.idade_min=form.idade_min.data
        preco.idade_max=form.idade_max.data
        preco.valor=form.valor.data
        
        db.session.add(preco)
        db.session.commit()
        flash("Faixa etária criada. Continue cadastrando para este plano.", "success")
        
        # --- Lógica para o próximo registro ---
        # Garante que os dados de idade existem antes de calcular a próxima faixa
        if form.idade_min.data is not None and form.idade_max.data is not None:
            # Calcula a próxima idade mínima e máxima
            proxima_idade_min = form.idade_max.data + 1
            
            # Se a próxima faixa for a última (padrão ANS >= 59), sugere até 99 anos
            if proxima_idade_min >= 59:
                proxima_idade_max = 99
            else:
                # Calcula o intervalo da faixa atual
                intervalo = form.idade_max.data - form.idade_min.data
                
                # Ajuste para faixas padrão ANS: se o intervalo for longo (ex: 0-18), sugere intervalo padrão de 5 anos (4)
                if intervalo > 4:
                    intervalo = 4
                
                proxima_idade_max = proxima_idade_min + intervalo
            
            # Redireciona para a mesma tela, com os campos pré-preenchidos e foco no valor
            return redirect(url_for(
                ".create_preco", 
                plano_id=form.plano_id.data, 
                next_idade_min=proxima_idade_min,
                next_idade_max=proxima_idade_max,
                focus='valor'
            ))
        
        # Fallback: se os dados de idade não estiverem disponíveis, redireciona sem preencher a próxima faixa
        return redirect(url_for(".create_preco", plano_id=form.plano_id.data, focus='idade_min'))
    return render_template("precos_form.html", form=form, title="Nova Faixa Etária")

@precos_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_preco(id):
    preco = PrecoFaixaEtaria.query.get_or_404(id)
    form = PrecoFaixaForm(obj=preco)
    if form.validate_on_submit():
        # --- VERIFICAÇÃO DE DUPLICIDADE (AO EDITAR) ---
        # Verifica se existe outra faixa (excluindo a atual) com os mesmos dados
        selected_plano = Plano.query.get(form.plano_id.data)
        existing_preco = None
        if selected_plano:
            existing_preco = PrecoFaixaEtaria.query.join(Plano).filter(
                PrecoFaixaEtaria.id != id,
                Plano.nome_plano == selected_plano.nome_plano,
                PrecoFaixaEtaria.idade_min == form.idade_min.data,
                PrecoFaixaEtaria.idade_max == form.idade_max.data
            ).first()

        if existing_preco:
            nome_plano = selected_plano.nome_plano if selected_plano else "selecionado"
            flash(f"Já existe outra faixa de preço ({form.idade_min.data} a {form.idade_max.data} anos) cadastrada para o plano '{nome_plano}'.", "danger")
            return render_template("precos_form.html", form=form, title="Editar Faixa")
        # --- FIM DA VERIFICAÇÃO ---
        form.populate_obj(preco)
        db.session.commit()
        flash("Faixa atualizada", "success")
        return redirect(url_for(".list_precos"))
    return render_template("precos_form.html", form=form, title="Editar Faixa")

@precos_bp.route("/<int:id>/delete", methods=["POST"])
def delete_preco(id):
    preco = PrecoFaixaEtaria.query.get_or_404(id)
    db.session.delete(preco)
    db.session.commit()
    flash("Faixa removida", "warning")
    return redirect(url_for(".list_precos"))
