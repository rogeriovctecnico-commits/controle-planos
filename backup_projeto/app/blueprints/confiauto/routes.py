from flask import render_template, redirect, url_for, flash, request, Blueprint
from . import confiauto_bp
from ...extensions import db
from ...models import Confiauto, ClienteConfiauto
from ...forms import ConfiautoForm
from sqlalchemy import or_

@confiauto_bp.route("/")
def list_confiauto():
    page = request.args.get("page", 1, type=int)
    search_term = request.args.get("q", "")

    query = Confiauto.query.join(ClienteConfiauto)

    if search_term:
        search_term = search_term.strip()
        query = query.filter(or_(
            ClienteConfiauto.nome.ilike(f"%{search_term}%"),
            Confiauto.veiculo_marca.ilike(f"%{search_term}%"),
            Confiauto.veiculo_modelo.ilike(f"%{search_term}%"),
            Confiauto.veiculo_placa.ilike(f"%{search_term}%")
        ))

    confiautos = query.order_by(Confiauto.created_at.desc()).paginate(page=page, per_page=10)
    return render_template("confiauto_list.html", confiautos=confiautos, search_term=search_term)

@confiauto_bp.route("/create", methods=["GET", "POST"])
def create_confiauto():
    form = ConfiautoForm()
    form.cliente_confiauto_id.choices = [(c.id, c.nome) for c in ClienteConfiauto.query.order_by(ClienteConfiauto.nome).all()]
    if form.validate_on_submit():
        c = Confiauto()
        c.cliente_confiauto_id = form.cliente_confiauto_id.data
        c.veiculo_marca = form.veiculo_marca.data
        c.veiculo_modelo = form.veiculo_modelo.data
        c.veiculo_ano = form.veiculo_ano.data
        c.veiculo_placa = form.veiculo_placa.data
        c.veiculo_chassi = form.veiculo_chassi.data
        c.valor_veiculo = form.valor_veiculo.data
        c.valor_protecao = form.valor_protecao.data
        c.valor_ativacao = form.valor_ativacao.data
        c.data_contratacao = form.data_contratacao.data
        c.data_vigencia = form.data_vigencia.data
        c.status = form.status.data
        c.observacoes = form.observacoes.data
        db.session.add(c)
        db.session.commit()
        flash("Confiauto criado", "success")
        return redirect(url_for("confiauto.list_confiauto"))
    return render_template("confiauto_form.html", form=form, title="Novo Confiauto")

@confiauto_bp.route("/<int:id>")
def detail_confiauto(id):
    c = Confiauto.query.get_or_404(id)
    return render_template("confiauto_detail.html", confiauto=c)

@confiauto_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_confiauto(id):
    c = Confiauto.query.get_or_404(id)
    form = ConfiautoForm(obj=c)
    form.cliente_confiauto_id.choices = [(cl.id, cl.nome) for cl in ClienteConfiauto.query.order_by(ClienteConfiauto.nome).all()]
    if form.validate_on_submit():
        c.cliente_confiauto_id = form.cliente_confiauto_id.data
        c.veiculo_marca = form.veiculo_marca.data
        c.veiculo_modelo = form.veiculo_modelo.data
        c.veiculo_ano = form.veiculo_ano.data
        c.veiculo_placa = form.veiculo_placa.data
        c.veiculo_chassi = form.veiculo_chassi.data
        c.valor_veiculo = form.valor_veiculo.data
        c.valor_protecao = form.valor_protecao.data
        c.valor_ativacao = form.valor_ativacao.data
        c.data_contratacao = form.data_contratacao.data
        c.data_vigencia = form.data_vigencia.data
        c.status = form.status.data
        c.observacoes = form.observacoes.data
        db.session.commit()
        flash("Confiauto atualizado", "success")
        return redirect(url_for("confiauto.list_confiauto"))
    return render_template("confiauto_form.html", form=form, title="Editar Confiauto")

@confiauto_bp.route("/<int:id>/delete", methods=["POST"])
def delete_confiauto(id):
    c = Confiauto.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    flash("Confiauto removido", "warning")
    return redirect(url_for("confiauto.list_confiauto"))
