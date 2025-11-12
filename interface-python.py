import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import PyPDF2
import re

def ler_datas_pdf(caminho_pdf):
    leitor = PyPDF2.PdfReader(caminho_pdf)
    texto = ""
    for pagina in leitor.pages:
        texto += pagina.extract_text()

    padrao_data = r"\b\d{2}[/-]\d{2}[/-]\d{4}\b"
    datas_encontradas = re.findall(padrao_data, texto)
    return list(set(datas_encontradas))

def obter_feriados(ano):
    url = f"https://date.nager.at/api/v3/PublicHolidays/{ano}/BR"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        return [f["date"] for f in resposta.json()]
    else:
        messagebox.showerror("Erro", "Falha ao obter feriados da API.")
        return []

def verificar_feriados():
    caminho_pdf = filedialog.askopenfilename(
        title="Escolha um arquivo PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    if not caminho_pdf:
        return

    datas_pdf = ler_datas_pdf(caminho_pdf)
    if not datas_pdf:
        messagebox.showinfo("Resultado", "Nenhuma data encontrada no PDF.")
        return

    ano = 2025
    feriados_api = obter_feriados(ano)

    feriados_encontrados = []
    for data in datas_pdf:
        formato_api = "-".join(data.replace("/", "-").split("-")[::-1]) 
        if formato_api in feriados_api:
            feriados_encontrados.append(data)

    if feriados_encontrados:
        messagebox.showinfo("Feriados Encontrados", "\n".join(feriados_encontrados))
    else:
        messagebox.showinfo("Resultado", "Nenhum feriado encontrado.")

def main():
    root = tk.Tk()
    root.title("Verificador de Feriados")
    root.geometry("400x200")

    label = tk.Label(root, text="Escolha um arquivo PDF com datas:", font=("Arial", 12))
    label.pack(pady=20)

    botao = tk.Button(root, text="Selecionar PDF e Verificar", command=verificar_feriados)
    botao.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
