import sqlite3
import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMainWindow, \
    QApplication, QMessageBox


class CadastroCliente(QMainWindow):
    def __init__(self):
        super().__init__()


        #Configurações da janela principal
        self.setWindowTitle('Cadastro de clientes')
        self.setGeometry(100, 100, 400, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        #Widgets do layout
        self.label_nome = QLabel('Nome')
        self.texto_nome = QLineEdit()
        self.label_sobrenome = QLabel('Sobrenome')
        self.texto_sobrenome = QLineEdit()
        self.label_email = QLabel('E-mail')
        self.texto_email = QLineEdit()
        self.label_telefone = QLabel('Telefone')
        self.texto_telefone = QLineEdit()


        #definindo as cores dos botões
        self.botao_salvar = QPushButton('Adicionar Contato')
        self.botao_salvar.setStyleSheet("background-color: lightgreen; "
                                 "border-radius: 5px; "
                                 "border: 2px solid green; "
                              )
        self.botao_editar = QPushButton('Editar Contato')
        self.botao_editar.setStyleSheet("background-color: #f1eb9c; "
                              "border-radius: 5px; "
                              "border: 2px solid orange; "
                              )
        self.botao_remover = QPushButton('Excluir Contato')
        self.botao_remover.setStyleSheet("background-color: #ff6961; "
                                "border-radius: 5px; "
                                "border: 2px solid red; "
                                )

        self.botao_limpar = QPushButton('Limpar Campos')
        self.botao_limpar.setStyleSheet("background-color: #5353ec ; "
                                "border-radius: 5px; "
                                "border: 2px solid blue; "
                                )

        #Widget de lista para demonstrar os clintes ja cadastrados
        self.lista_clientes = QListWidget()
        self.lista_clientes.itemClicked.connect(self.selecionar_cliente)

        #Adiciona widgets ao layout
        self.layout.addWidget(self.label_nome)
        self.layout.addWidget(self.texto_nome)
        self.layout.addWidget(self.label_sobrenome)
        self.layout.addWidget(self.texto_sobrenome)
        self.layout.addWidget(self.label_email)
        self.layout.addWidget(self.texto_email)
        self.layout.addWidget(self.label_telefone)
        self.layout.addWidget(self.texto_telefone)
        self.layout.addWidget(self.lista_clientes)
        self.layout.addWidget(self.botao_salvar)
        self.layout.addWidget(self.botao_editar)
        self.layout.addWidget(self.botao_remover)
        self.layout.addWidget(self.botao_limpar)

        self.criar_banco()

        self.carregar_clientes()

        self.cliente_selecionado = None

        self.botao_salvar.clicked.connect(self.salvar_cliente)
        self.botao_editar.clicked.connect(self.editar_cliente)
        self.botao_remover.clicked.connect(self.validar_remocao)
        self.botao_limpar.clicked.connect(self.limpar_campos)

    def criar_banco(self):
        conexao = sqlite3.connect('contatos.db')
        cursor = conexao.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                sobrenome TEXT,
                email TEXT,
                telefone TEXT
                )
        ''')
        conexao.close()

    def salvar_cliente(self):
        nome = self.texto_nome.text()
        sobrenome = self.texto_sobrenome.text()
        email = self.texto_email.text()
        telefone = self.texto_telefone.text()

        if self.botao_salvar.text() == 'Atualizar Contato':
            self.botao_salvar.setText('Adicionar Contato')

        if self.botao_editar.text() == 'Cancelar':
            self.botao_editar.setText('Editar Contato')

        if nome and sobrenome and email and telefone:
            conexao = sqlite3.connect('contatos.db')
            cursor = conexao.cursor()


            if self.cliente_selecionado is None:
                cursor.execute(''' 
                INSERT INTO clientes(nome, sobrenome, email, telefone)
                VALUES(?, ?, ?, ?)
            ''',(nome, sobrenome, email, telefone))

            else:
                cursor.execute('''
                    UPDATE clientes 
                    SET nome = ?,  sobrenome = ?,  email = ?, telefone = ?
                    WHERE ID = ?
                ''',(nome, sobrenome, email, telefone, self.cliente_selecionado['id']))

            conexao.commit()
            conexao.close()

            self.texto_nome.clear()
            self.texto_sobrenome.clear()
            self.texto_email.clear()
            self.texto_telefone.clear()
            self.cliente_selecionado = None
            self.carregar_clientes()


        else:
            QMessageBox.warning(self,'Aviso', 'Preencha todos os dados')

    def carregar_clientes(self):
        self.lista_clientes.clear()
        conexao = sqlite3.connect('contatos.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT id, nome, sobrenome, email, telefone FROM clientes')
        clientes = cursor.fetchall()
        conexao.close()

        for cliente in clientes:
            id_cliente, nome, sobrenome, email, telefone = cliente
            self.lista_clientes.addItem(f'{id_cliente} | {nome} {sobrenome} | {email} | {telefone}')


    def selecionar_cliente(self, item):
        self.cliente_selecionado = {
            'id': item.text().split()[0],
            'nome': self.texto_nome.text(),
            'sobrenome': self.texto_sobrenome.text(),
            'email': self.texto_email.text(),
            'telefone': self.texto_telefone.text()
        }

    def editar_cliente(self):
        if self.botao_editar.text() == 'Editar Contato':
            if self.cliente_selecionado is not None:
                conexao = sqlite3.connect('contatos.db')
                cursor = conexao.cursor()
                cursor.execute('SELECT nome, sobrenome, email, telefone FROM clientes '
                               'WHERE id = ?', self.cliente_selecionado['id'])
                cliente = cursor.fetchone()
                conexao.close()

                if cliente:
                    nome, sobrenome, email, telefone = cliente
                    self.texto_nome.setText(nome)
                    self.texto_sobrenome.setText(sobrenome)
                    self.texto_email.setText(email)
                    self.texto_telefone.setText(telefone)
                    self.botao_editar.setText('Cancelar')
                    self.botao_salvar.setText('Atualizar Contato')

        else:
            self.texto_nome.clear()
            self.texto_sobrenome.clear()
            self.texto_email.clear()
            self.texto_telefone.clear()
            self.botao_editar.setText('Editar Contato')
            self.botao_salvar.setText('Adicionar Contato')

    def validar_remocao(self):
        if self.cliente_selecionado is not None:
            mensagem = QMessageBox()
            mensagem.setWindowTitle('Confirmação')
            mensagem.setText('Tem certeza que você deseja remover o cliente')

            botao_sim = mensagem.addButton('Sim', QMessageBox.YesRole)
            botao_nao = mensagem.addButton('Não', QMessageBox.NoRole)
            #Define o icone como questionamento
            mensagem.setIcon(QMessageBox.Question)
            mensagem.exec()

            if mensagem.clickedButton() == botao_sim:
                self.remover_cliente()

    def remover_cliente(self):
        if self.cliente_selecionado is not None:
            conexao = sqlite3.connect('contatos.db')
            cursor = conexao.cursor()
            cursor.execute('DELETE FROM clientes WHERE ID = ?',
                           (self.cliente_selecionado['id']))
            conexao.commit()
            conexao.close()
            self.carregar_clientes()
            self.texto_nome.clear()
            self.texto_sobrenome.clear()
            self.texto_email.clear()
            self.texto_telefone.clear()
            self.cliente_selecionado = None

    def limpar_campos(self):
        self.texto_nome.clear()
        self.texto_sobrenome.clear()
        self.texto_email.clear()
        self.texto_telefone.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CadastroCliente()
    window.show()
    sys.exit(app.exec())
