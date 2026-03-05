from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, TextAreaField, BooleanField, SelectField, DateField, DateTimeField, SubmitField, ValidationError, FloatField
from wtforms.validators import DataRequired, Optional, Length, NumberRange
from flask import request
from .models import Cliente, Usuario, Plano, Operadora

class ClienteForm(FlaskForm):
    def __init__(self, original_cpf=None, original_email=None, *args, **kwargs):
        # Adiciona o construtor para aceitar o objeto 'obj' e popular o formulário
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.original_cpf = original_cpf
        self.original_email = original_email

    nome = StringField("Nome", validators=[DataRequired()])
    cpf = StringField("CPF", validators=[Optional()], filters=[lambda x: x or None])
    email = StringField("Email", validators=[DataRequired()], filters=[lambda x: x or None])
    telefone = StringField("Telefone", validators=[Optional()])
    endereco = StringField("Endereço", validators=[Optional()])
    data_nascimento = DateField("Data de Nascimento", validators=[Optional()])
    #data_aniversario_contrato = DateField("Aniversário do Contrato", validators=[Optional()])
    cnpj = StringField("CNPJ", validators=[Optional()])
    responsavel = StringField("Responsável", validators=[Optional()])
    status = SelectField('Status', choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo')

    submit = SubmitField("Salvar")

    def validate_cpf(self, cpf):
        # Se o campo estiver vazio, não faz nada
        if not cpf.data:
            return
        # Se o CPF não mudou durante a edição, não precisamos validar
        if self.original_cpf and self.original_cpf == cpf.data:
            return
        cliente = Cliente.query.filter_by(cpf=cpf.data).first()
        if cliente:
            raise ValidationError('Este CPF já está cadastrado. Por favor, utilize outro.')

    def validate_email(self, email):
        # Se o email não mudou durante a edição, não precisamos validar
        if hasattr(self, 'original_email') and self.original_email and self.original_email == email.data:
            return
        cliente = Cliente.query.filter_by(email=email.data).first()
        if cliente:
            raise ValidationError('Este email já está cadastrado. Por favor, utilize outro.')

class PlanoForm(FlaskForm):
    def __init__(self, original_nome_plano=None, *args, **kwargs):
        super(PlanoForm, self).__init__(*args, **kwargs)
        self.original_nome_plano = original_nome_plano

    nome_plano = StringField("Nome do Plano", validators=[DataRequired(), Length(max=100)])
    descricao = TextAreaField("Descrição", validators=[Optional()])
    valor_base = DecimalField("Valor Base", validators=[DataRequired()])
    cobertura = TextAreaField("Cobertura", validators=[Optional()])
    tipo_plano = StringField("Tipo de Plano", validators=[Optional(), Length(max=50)])
    ativo = BooleanField("Ativo", default=True)
    operadora_id = SelectField("Operadora", coerce=int, validators=[DataRequired()])
    regiao = StringField("Região", validators=[Optional(), Length(max=100)])
    acomodacao = StringField("Acomodação", validators=[Optional(), Length(max=50)])
    administradora = StringField("Administradora", validators=[Optional(), Length(max=100)])
    entidade = StringField("Entidade", validators=[Optional(), Length(max=100)])
    beneficios = TextAreaField("Benefícios", validators=[Optional()])
    data_vigencia = DateField("Data de Vigência", validators=[Optional()])
    created_by_username = StringField("Criado por", validators=[Optional(), Length(max=100)])
    submit = SubmitField("Salvar")

    def validate_nome_plano(self, nome_plano):
        if not nome_plano.data:
            return
        if self.original_nome_plano and self.original_nome_plano == nome_plano.data:
            return
        plano = Plano.query.filter_by(nome_plano=nome_plano.data).first()
        if plano:
            raise ValidationError('Este nome de plano já está cadastrado. Por favor, utilize outro.')

class PrecoFaixaForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(PrecoFaixaForm, self).__init__(*args, **kwargs)
        # Popula a lista de planos em ordem decrescente de ID
        self.plano_id.choices = [
            (p.id, p.nome_plano) for p in Plano.query.order_by(Plano.id.desc()).all()
        ]

    plano_id = SelectField("Plano", coerce=int, validators=[DataRequired()])
    idade_min = IntegerField("Idade Mínima", validators=[DataRequired()])
    idade_max = IntegerField("Idade Máxima", validators=[DataRequired()])
    valor = DecimalField("Valor", validators=[DataRequired()])
    submit = SubmitField("Salvar")

class VendaForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(VendaForm, self).__init__(*args, **kwargs)
        # Popula a lista de planos exibindo "Plano - Operadora"
        self.plano_id.choices = [
            (p.id, f"{p.nome_plano} - {p.operadora.nome_operadora}")
            for p in Plano.query.join(Operadora).order_by(Plano.nome_plano).all()
        ]
        # Garante a lista de clientes para validação
        self.cliente_id.choices = [(c.id, c.nome) for c in Cliente.query.order_by(Cliente.nome).all()]

        # Verifica se é edição e se o status é cancelado
        obj = kwargs.get('obj')
        is_cancelado = obj and hasattr(obj, 'status') and obj.status == 'cancelado'

        # Todos os campos são opcionais por padrão, validação customizada no método validate
        self.cliente_id.validators = [Optional()]
        self.plano_id.validators = [Optional()]
        self.data_venda.validators = [Optional()]
        self.data_vigencia.validators = [Optional()]
        self.origem.validators = [Optional()]
        self.natureza.validators = [Optional()]
        self.promocao.validators = [Optional()]
        self.valor_venda.validators = [Optional()]
        self.numeros_vida.validators = [Optional()]
        self.comissao.validators = [Optional()]
        self.premiacao.validators = [Optional()]
        self.desconto.validators = [Optional()]
        self.valor_final.validators = [Optional()]
        self.tipo_plano.validators = [Optional()]
        self.administradora.validators = [Optional()]
        self.observacoes.validators = [Optional()]

    def validate(self, extra_validators=None):
        # Chama a validação padrão
        if not super().validate():
            return False

        # Se o status for 'cancelado', permite salvar sem validar campos obrigatórios
        if self.status.data == 'cancelado':
            if not self.observacoes.data:
                self.observacoes.errors = list(self.observacoes.errors) + ['Observações são obrigatórias ao cancelar uma venda.']
                return False
            return True

        # Caso contrário, valida os campos obrigatórios
        has_error = False
        if not self.cliente_id.data:
            self.cliente_id.errors = list(self.cliente_id.errors) + ['Cliente é obrigatório.']
            has_error = True
        if not self.plano_id.data:
            self.plano_id.errors = list(self.plano_id.errors) + ['Plano é obrigatório.']
            has_error = True
        if not self.data_venda.data:
            self.data_venda.errors = list(self.data_venda.errors) + ['Data da Venda é obrigatória.']
            has_error = True
        if not self.data_vigencia.data:
            self.data_vigencia.errors = list(self.data_vigencia.errors) + ['Data de Vigência é obrigatória.']
            has_error = True
        if not self.origem.data:
            self.origem.errors = list(self.origem.errors) + ['Origem é obrigatória.']
            has_error = True
        if not self.natureza.data:
            self.natureza.errors = list(self.natureza.errors) + ['Natureza é obrigatória.']
            has_error = True
        if not self.valor_venda.data:
            self.valor_venda.errors = list(self.valor_venda.errors) + ['Valor da Venda é obrigatório.']
            has_error = True

        if has_error:
            return False
        return True

    cliente_id = SelectField("cliente_id", coerce=int)
    plano_id = SelectField("plano_id", coerce=int)
    data_venda = DateTimeField("Data da Venda", format="%Y-%m-%dT%H:%M")
    data_vigencia = DateField("data_vigencia")
    origem = StringField("origem")
    natureza = StringField("natureza")
    promocao = StringField("promocao")
    numeros_vida = IntegerField("numeros_vida", validators=[Optional()])
    comissao = DecimalField("Comissão", validators=[Optional()])
    premiacao = DecimalField("Premiação", validators=[Optional()])
    premiacao_paga = BooleanField("premiacao_paga")
    comissao_paga = BooleanField("comissao_paga")
    valor_venda = DecimalField("valor_venda")
    desconto = DecimalField("desconto", validators=[Optional()])
    valor_final = DecimalField("valor_final", validators=[Optional()])
    status = SelectField("Status", choices=[('ativo', 'ATIVO'), ('cancelado', 'CANCELADO')], validators=[Optional()])
    tipo_plano = StringField("Tipo de Plano", validators=[Optional()])
    administradora = StringField("Administradora", validators=[Optional()])
    observacoes = TextAreaField("observacoes", validators=[Optional()])
    submit = SubmitField("Salvar")

class AdministradoraForm(FlaskForm):
    nome_administradora = StringField("nome_administradora", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Salvar")

class OperadoraForm(FlaskForm):
    nome_operadora = StringField("nome_operadora", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Salvar")
