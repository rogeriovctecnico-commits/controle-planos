from flask import render_template, request, redirect, url_for, flash
from ...extensions import db
from ...models import Administradora
from ...forms import AdministradoraForm
from . import administradoras_bp

# Listar administradoras
@administradoras_bp.route("/")
def list_administradoras():
    page = request.args.get("page", 1, type=int)
    search_term = request.args.get("q", "")

    query = Administradora.query

    if search_term:
        search_term = search_term.strip()
        query = query.filter(Administradora.nome_administradora.ilike(f"%{search_term}%"))

    administradoras = query.order_by(Administradora.created_at.desc()).paginate(page=page, per_page=10)
    return render_template("administradora_list.html", administradoras=administradoras, search_term=search_term)

# Criar administradora
@administradoras_bp.route("/create", methods=["GET", "POST"])
def create_administradora():
    form = AdministradoraForm()
    if form.validate_on_submit():
        
        nova = Administradora(nome_administradora=form.nome_administradora.data) # type: ignore
        db.session.add(nova)
        db.session.commit()
        flash("Administradora criada com sucesso!", "success")
        return redirect(url_for("administradoras.list_administradoras"))
    return render_template("administradora_form.html", form=form, title="Nova Administradora")

# Editar administradora
@administradoras_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_administradora(id):
    administradora = Administradora.query.get_or_404(id)
    form = AdministradoraForm(obj=administradora)
    if form.validate_on_submit():
        form.populate_obj(administradora)
        db.session.commit()
        flash("Administradora atualizada com sucesso!", "success")
        return redirect(url_for("administradoras.list_administradoras"))
    return render_template("administradora_form.html", form=form, title="Editar Administradora")

# Deletar administradora
@administradoras_bp.route("/<int:id>/delete", methods=["POST"])
def delete_administradora(id):
    administradora = Administradora.query.get_or_404(id)
    db.session.delete(administradora)
    db.session.commit()
    flash("Administradora removida com sucesso!", "warning")
    return redirect(url_for("administradoras.list_administradoras"))