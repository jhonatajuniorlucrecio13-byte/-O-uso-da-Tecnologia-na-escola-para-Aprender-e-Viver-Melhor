import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random

DATA_FILE = "alimentacao_app_data.json"

# Dados estáticos do app (dicas, receitas e perguntas do quiz)
DICAS = [
    "Coma frutas todos os dias — são ricas em vitaminas e fibras.",
    "Prefira água em vez de refrigerantes.",
    "Inclua verduras no prato: elas ajudam no crescimento e na saúde.",
    "Evite alimentos ultraprocessados com excesso de açúcar e sal.",
    "Faça pequenas refeições ao longo do dia para manter energia."
]

RECEITAS = [
    {"titulo": "Salada colorida", "ingredientes": ["Alface", "Tomate", "Cenoura ralada"], "modo": "Misture os ingredientes e tempere com limão e azeite."},
    {"titulo": "Smoothie de banana e aveia", "ingredientes": ["1 banana", "2 colheres de aveia", "200ml de leite ou água"], "modo": "Bata tudo no liquidificador até ficar cremoso."},
    {"titulo": "Sanduíche natural", "ingredientes": ["Pão integral", "Peito de peru", "Folhas verdes"], "modo": "Monte o sanduíche com pouco sal e sem maionese industrial."}
]

QUIZ = [
    {"pergunta": "Qual é a bebida mais saudável para o dia a dia?", "opcoes": ["Refrigerante", "Suco industrial", "Água", "Energético"], "resposta": 2},
    {"pergunta": "Qual alimento é fonte de proteína?", "opcoes": ["Maçã", "Feijão", "Alface", "Biscoito"], "resposta": 1},
    {"pergunta": "O que é uma boa opção de lanche escolar?", "opcoes": ["Batata frita", "Fruta e iogurte", "Doces embalados", "Bebida energética"], "resposta": 1},
]

# Funções de persistência simples
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class AlimentacaoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aprender e Viver Melhor - Alimentação")
        self.geometry("720x480")
        self.resizable(False, False)

        self.data = load_data()
        self.username = self.data.get("username", "")

        # Container para frames
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        # Cabeçalho
        header = ttk.Frame(container)
        header.pack(fill="x", padx=10, pady=8)
        title_label = ttk.Label(header, text="Aprender e Viver Melhor", font=("Helvetica", 16, "bold"))
        title_label.pack(side="left")
        self.user_label = ttk.Label(header, text=f"Aluno: {self.username or 'Não informado'}")
        self.user_label.pack(side="right")

        # Menu lateral
        nav = ttk.Frame(container)
        nav.pack(side="left", fill="y", padx=10, pady=8)

        btn_home = ttk.Button(nav, text="Início", command=lambda: self.show_frame("Home"))
        btn_dicas = ttk.Button(nav, text="Dicas", command=lambda: self.show_frame("Dicas"))
        btn_receitas = ttk.Button(nav, text="Receitas", command=lambda: self.show_frame("Receitas"))
        btn_quiz = ttk.Button(nav, text="Quiz", command=lambda: self.show_frame("Quiz"))
        btn_atividade = ttk.Button(nav, text="Atividade: Horta", command=lambda: self.show_frame("Horta"))
        btn_settings = ttk.Button(nav, text="Configurar Nome", command=self.ask_username)

        for b in (btn_home, btn_dicas, btn_receitas, btn_quiz, btn_atividade, btn_settings):
            b.pack(fill="x", pady=4)

        # Área principal
        main_area = ttk.Frame(container)
        main_area.pack(side="left", fill="both", expand=True, padx=10, pady=8)

        self.frames = {}
        for F in (HomeFrame, DicasFrame, ReceitasFrame, QuizFrame, HortaFrame):
            name = F.__name__.replace("Frame", "")
            frame = F(parent=main_area, controller=self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[name] = frame

        self.show_frame("Home")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def ask_username(self):
        def save():
            name = entry.get().strip()
            if name:
                self.username = name
                self.user_label.config(text=f"Aluno: {self.username}")
                self.data["username"] = self.username
                save_data(self.data)
                top.destroy()
            else:
                messagebox.showwarning("Nome", "Por favor, insira um nome válido.")
        top = tk.Toplevel(self)
        top.title("Configurar Nome do Aluno")
        top.geometry("320x120")
        ttk.Label(top, text="Digite o nome do aluno:").pack(pady=8)
        entry = ttk.Entry(top)
        entry.pack(pady=4, padx=8, fill="x")
        ttk.Button(top, text="Salvar", command=save).pack(pady=8)

class HomeFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Bem-vindo!", font=("Helvetica", 14)).pack(pady=10)
        texto = ("Este protótipo apresenta dicas e atividades sobre alimentação saudável.\n"
                 "Use o menu à esquerda para navegar entre as seções.\n\n"
                 "Objetivos:\n- Ensinar hábitos alimentares saudáveis\n- Propor atividades lúdicas\n- Fixar conteúdo com quizzes")
        ttk.Label(self, text=texto, wraplength=520, justify="left").pack(padx=10, pady=8)

class DicasFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Dicas de Alimentação", font=("Helvetica", 14)).pack(pady=10)
        self.listbox = tk.Listbox(self, height=8, width=70)
        self.listbox.pack(padx=10)
        for dica in DICAS:
            self.listbox.insert(tk.END, "• " + dica)

        ttk.Button(self, text="Mostrar aleatória", command=self.mostrar_aleatoria).pack(pady=8)
        self.label_aleatoria = ttk.Label(self, text="", wraplength=520)
        self.label_aleatoria.pack(padx=10)

    def mostrar_aleatoria(self):
        dica = random.choice(DICAS)
        self.label_aleatoria.config(text=dica)

class ReceitasFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Receitas Simples", font=("Helvetica", 14)).pack(pady=10)
        self.tree = ttk.Treeview(self, columns=("ingredientes",), show="headings", height=6)
        self.tree.heading("ingredientes", text="Título")
        self.tree.column("ingredientes", width=400)
        self.tree.pack(padx=10, pady=4)
        for r in RECEITAS:
            self.tree.insert("", tk.END, values=(r["titulo"],))

        btn_ver = ttk.Button(self, text="Ver Receita", command=self.ver_receita)
        btn_ver.pack(pady=6)
        self.text = tk.Text(self, height=6, width=60, wrap="word")
        self.text.pack(padx=10, pady=4)

    def ver_receita(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Receita", "Selecione uma receita da lista.")
            return
        title = self.tree.item(sel[0])["values"][0]
        for r in RECEITAS:
            if r["titulo"] == title:
                self.text.delete("1.0", tk.END)
                content = f"Título: {r['titulo']}\n\nIngredientes:\n- " + "\n- ".join(r["ingredientes"]) + f"\n\nModo de preparo:\n{r['modo']}"
                self.text.insert(tk.END, content)
                break

class QuizFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Quiz: Alimentação Saudável", font=("Helvetica", 14)).pack(pady=10)
        self.q_index = 0
        self.score = 0
        self.var = tk.IntVar(value=-1)

        self.question_label = ttk.Label(self, text="", wraplength=520, justify="left")
        self.question_label.pack(padx=10, pady=6)

        self.radio_buttons = []
        for i in range(4):
            rb = ttk.Radiobutton(self, text="", variable=self.var, value=i)
            rb.pack(anchor="w", padx=20)
            self.radio_buttons.append(rb)

        nav = ttk.Frame(self)
        nav.pack(pady=8)
        ttk.Button(nav, text="Resposta", command=self.check_answer).pack(side="left", padx=6)
        ttk.Button(nav, text="Próxima", command=self.next_question).pack(side="left", padx=6)
        self.feedback = ttk.Label(self, text="")
        self.feedback.pack()

        self.load_question()

    def load_question(self):
        if self.q_index >= len(QUIZ):
            self.finish_quiz()
            return
        q = QUIZ[self.q_index]
        self.question_label.config(text=f"{self.q_index+1}. {q['pergunta']}")
        for i, opt in enumerate(q["opcoes"]):
            self.radio_buttons[i].config(text=opt)
        self.var.set(-1)
        self.feedback.config(text="")

    def check_answer(self):
        if self.var.get() == -1:
            messagebox.showinfo("Quiz", "Selecione uma opção antes de verificar.")
            return
        q = QUIZ[self.q_index]
        if self.var.get() == q["resposta"]:
            self.score += 1
            self.feedback.config(text="Correto!")
        else:
            correct = q["opcoes"][q["resposta"]]
            self.feedback.config(text=f"Errado. A resposta certa é: {correct}")

    def next_question(self):
        self.q_index += 1
        if self.q_index < len(QUIZ):
            self.load_question()
        else:
            self.finish_quiz()

    def finish_quiz(self):
        total = len(QUIZ)
        messagebox.showinfo("Quiz Finalizado", f"Você acertou {self.score} de {total} perguntas.")
        data = self.controller.data
        scores = data.get("scores", [])
        scores.append({"user": self.controller.username or "Anon", "score": self.score, "total": total})
        data["scores"] = scores
        save_data(data)
        self.q_index = 0
        self.score = 0
        self.load_question()

class HortaFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Atividade: Mini Horta", font=("Helvetica", 14)).pack(pady=10)
        descricao = ("Proposta: plantar uma pequena semente em copo reciclável e acompanhar seu crescimento.\n"
                     "Objetivos: aprender sobre alimentação saudável e agricultura sustentável.")
        ttk.Label(self, text=descricao, wraplength=520, justify="left").pack(padx=10, pady=6)
        ttk.Label(self, text="Passos:").pack(anchor="w", padx=12)
        passos = [
            "1. Escolher uma semente (feijão, ervilha).",
            "2. Preparar o copo com terra.",
            "3. Plantar a semente e regar.",
            "4. Anotar observações a cada semana."
        ]
        for p in passos:
            ttk.Label(self, text=p).pack(anchor="w", padx=20)

        ttk.Label(self, text="Diário de Observações (anote o que viu):").pack(pady=8)
        self.text = tk.Text(self, height=6, width=60)
        self.text.pack(padx=10)
        btn_save = ttk.Button(self, text="Salvar Observação", command=self.salvar_obs)
        btn_save.pack(pady=6)

    def salvar_obs(self):
        content = self.text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Diário", "Escreva uma observação antes de salvar.")
            return
        data = load_data()
        diary = data.get("horta", [])
        diary.append({"user": data.get("username", "Anon"), "text": content})
        data["horta"] = diary
        save_data(data)
        messagebox.showinfo("Diário", "Observação salva com sucesso!")
        self.text.delete("1.0", tk.END)

if __name__ == "__main__":
    app = AlimentacaoApp()
    app.mainloop()
