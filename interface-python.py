import tkinter as tk
from tkinter import filedialog, messagebox
import os
import webbrowser

def abrir_pdf():
    caminho_pdf = filedialog.askopenfilename(
        title="Selecione um arquivo PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    if caminho_pdf:
        try:
            webbrowser.open_new(r'file://' + os.path.abspath(caminho_pdf))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o PDF:\n{e}")

janela = tk.Tk()
janela.title("Projeto Python")
janela.geometry("300x150")
janela.resizable(False, False)

botao = tk.Button(
    janela,
    text="Abrir PDF",
    command=abrir_pdf,
    font=("Arial", 12),
    bg="#4CAF50",
    fg="white",
    padx=10,
    pady=5
)
botao.pack(expand=True)

janela.mainloop()
