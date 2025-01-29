import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import ply.lex as lex

# Definição dos tokens
tokens = [
    'PROGRAM', 'BEGIN', 'END', 'PROCEDURE', 'FUNCTION', 'IF', 'THEN', 'ELSE',
    'WHILE', 'DO', 'REPEAT', 'UNTIL', 'VAR', 'INT', 'CHAR', 'FLOAT',
    'IDENTIFIER', 'NUMBER', 'ATTRIBUTION', 'WRITEC', 'WRITED', 'READC', 'READD',
    'DOT', 'SEMICOLON', 'COMMA', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
    'AND', 'OR', 'NOT', 'GT', 'LT', 'EQ', 'NE', 'GE', 'LE',
    'PLUS', 'MINUS', 'TIMES', 'DIV', 'CHAR_LITERAL'
]

# Palavras reservadas
reserved = {
    'program': 'PROGRAM',
    'begin': 'BEGIN',
    'end': 'END',
    'procedure': 'PROCEDURE',
    'function': 'FUNCTION',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'repeat': 'REPEAT',
    'until': 'UNTIL',
    'var': 'VAR',
    'int': 'INT',
    'char': 'CHAR',
    'float': 'FLOAT',
    'writec': 'WRITEC',
    'writed': 'WRITED',
    'readc': 'READC',
    'readd': 'READD',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'div': 'DIV'
}

# Regras para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_COMMA = r','
t_DOT = r'\.'
t_GT = r'>'
t_LT = r'<'
t_EQ = r'='
t_ATTRIBUTION = r':='
t_GE = r'>='
t_LE = r'<='
t_NE = r'<>'

# Ignorar espaços e tabs
t_ignore = ' \t'

# Contador de linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regra para números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regra para caracteres literais
def t_CHAR_LITERAL(t):
    r'\'.\''
    t.value = t.value[1:-1]  # Remove as aspas
    return t

# Regra para identificadores e palavras reservadas
def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'IDENTIFIER')
    return t

# Regra para comentários
def t_COMMENT(t):
    r'\{[^}]*\}'
    pass

# Regra para erro
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

### Análise Sintática


# Classe principal da interface
class LexicalAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analisador Léxico LPD")
        
        # Configurar o layout
        self.setup_ui()
        
        # Criar o lexer
        self.lexer = lex.lex()

    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Área de texto para entrada do código
        self.code_text = scrolledtext.ScrolledText(main_frame, width=60, height=15)
        self.code_text.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # Botão para análise
        analyze_button = ttk.Button(main_frame, text="Analisar", command=self.analyze_code)
        analyze_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Tabela para tokens
        self.token_tree = ttk.Treeview(main_frame, columns=('Token', 'Lexema', 'Linha'), show='headings')
        self.token_tree.heading('Token', text='Token')
        self.token_tree.heading('Lexema', text='Lexema')
        self.token_tree.heading('Linha', text='Linha')
        self.token_tree.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # Scrollbar para a tabela
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.token_tree.yview)
        scrollbar.grid(row=2, column=2, sticky=(tk.N, tk.S))
        self.token_tree.configure(yscrollcommand=scrollbar.set)

    def analyze_code(self):
        # Limpar a tabela anterior
        for item in self.token_tree.get_children():
            self.token_tree.delete(item)

        # Pegar o código da área de texto
        code = self.code_text.get("1.0", tk.END)
        
        # Dar input no lexer
        self.lexer.input(code)
        
        # Processar todos os tokens
        for token in self.lexer:
            self.token_tree.insert('', tk.END, values=(token.type, token.value, token.lineno))

# Função principal
def main():
    root = tk.Tk()
    app = LexicalAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()