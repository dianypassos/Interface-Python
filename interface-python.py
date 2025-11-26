import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import PyPDF2
import re
from datetime import datetime

cache_feriados = {}

def ler_datas_pdf(caminho_pdf):
    leitor = PyPDF2.PdfReader(caminho_pdf)
    texto = ""
    for pagina in leitor.pages:
        texto += pagina.extract_text() or ""
    texto = re.sub(r"\s+", " ", texto)

    padrao_data = r"\b(?:\d{2}|\d{4})[./-](?:\d{2})[./-](?:\d{4}|\d{2})\b"
    datas_encontradas = re.findall(padrao_data, texto)
    return list(set(datas_encontradas))

def padronizar_data(data_str):
    formatos_possiveis = ["%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%Y/%m/%d", "%Y-%m-%d"]
    for fmt in formatos_possiveis:
        try:
            data_obj = datetime.strptime(data_str, fmt)
            return data_obj.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None

def obter_feriados(ano):
    if ano in cache_feriados:
        return cache_feriados[ano]

    url = f"https://date.nager.at/api/v3/PublicHolidays/{ano}/BR"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        dados = resposta.json()
        feriados = {f["date"]: f["localName"] for f in dados}
        cache_feriados[ano] = feriados
        return feriados
    else:
        messagebox.showerror("Erro", f"Falha ao obter feriados para {ano}.")
        return {}

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

    feriados_encontrados = []

    for data in datas_pdf:
        formato_api = padronizar_data(data)
        if not formato_api:
            continue

        ano = int(formato_api.split("-")[0])
        feriados_api = obter_feriados(ano)

        if formato_api in feriados_api:
            nome_feriado = feriados_api[formato_api]
            feriados_encontrados.append(f"{data} → {nome_feriado}")

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

