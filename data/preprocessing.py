import pandas as pd
from datetime import timedelta
import ast

def safe_parse(x):
    if isinstance(x, str):
        try:
            return ast.literal_eval(x.replace(";", ","))
        except Exception:
            return []
    elif isinstance(x, list):
        return x
    else:
        return []

df = pd.read_csv("data/raw/20230120-data-collector-dailyRegister.csv", parse_dates=["Day"])

df.rename(columns={"Day": "date", "ID": "patient_id"}, inplace=True)

sleep_cols = ["LightSleep", "DeepSleep", "REMSleep", "AwakeSleep"]
for col in sleep_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce") / 3600

df["TotalSleep"] = df["LightSleep"] + df["DeepSleep"] + df["REMSleep"] + df["AwakeSleep"]

df["HeartRate"] = df["HeartRate"].apply(safe_parse)

df["Steps"] = pd.to_numeric(df["Steps"], errors="coerce")

df["Calories"] = pd.to_numeric(df["Steps"], errors="coerce")

def gerar_descricao(grupo):
    id = grupo["patient_id"].iloc[0]
    data_inicial = grupo["date"].min().date()
    data_final = grupo["date"].max().date()

    def stats(col):
        serie = grupo[col].dropna()
        valores_validos = serie[serie != 0]

        if valores_validos.empty:
            return {"disponivel": False}

        return {
            "disponivel": True,
            "média": valores_validos.mean(),
            "mínimo": valores_validos.min(),
            "máximo": valores_validos.max(),
            "valores": ", ".join(f"{v:.2f}" for v in valores_validos)
        }

    def heart_rate_stats(grupo):
        all_rates = [rate for sublist in grupo["HeartRate"] for rate in sublist if rate != 0]
        por_dia = [f"[{', '.join(str(r) for r in rates if r != 0)}]" for rates in grupo["HeartRate"]]

        if not all_rates:
            return {"disponivel": False}

        return {
            "disponivel": True,
            "média": sum(all_rates) / len(all_rates),
            "mínimo": min(all_rates),
            "máximo": max(all_rates),
            "valores": ", ".join(por_dia)
        }

    altura_média = grupo["Height"].mean()
    peso_médio = grupo["Weight"].mean()

    s = lambda col: stats(col)
    hr = heart_rate_stats(grupo)

    texto = f"""
    Paciente ID: {id}
    Período: de {data_inicial} até {data_final}

    Altura média: {altura_média:.2f} cm
    Peso médio: {peso_médio:.2f} kg

    Passos:
    {f'''
    - Média: {s("Steps")["média"]:.0f}
    - Mínimo: {s("Steps")["mínimo"]}
    - Máximo: {s("Steps")["máximo"]}
    - Valores diários: {s("Steps")["valores"]}
    ''' if s("Steps")["disponivel"] else 'Leitura não realizada no período.'}

    Calorias:
    {f'''
    - Média: {s("Calories")["média"]:.0f} cal
    - Mínimo: {s("Calories")["mínimo"]} cal
    - Máximo: {s("Calories")["máximo"]} cal
    - Valores diários: {s("Calories")["valores"]}
    ''' if s("Calories")["disponivel"] else 'Leitura não realizada no período.'}

    Batimentos Cardíacos:
    {f'''
    - Média: {hr["média"]:.0f} bpm
    - Mínimo: {hr["mínimo"]} bpm
    - Máximo: {hr["máximo"]} bpm
    - Valores diários: {hr["valores"]}
    ''' if hr["disponivel"] else 'Leitura não realizada no período.'}

    Sono (valores em horas):

    Sono Leve:
    {f'''
    - Média: {s("LightSleep")["média"]:.2f} h
    - Mínimo: {s("LightSleep")["mínimo"]:.2f} h
    - Máximo: {s("LightSleep")["máximo"]:.2f} h
    - Valores diários: {s("LightSleep")["valores"]}
    ''' if s("LightSleep")["disponivel"] else 'Leitura não realizada no período.'}

    Sono Profundo:
    {f'''
    - Média: {s("DeepSleep")["média"]:.2f} h
    - Mínimo: {s("DeepSleep")["mínimo"]:.2f} h
    - Máximo: {s("DeepSleep")["máximo"]:.2f} h
    - Valores diários: {s("DeepSleep")["valores"]}
    ''' if s("DeepSleep")["disponivel"] else 'Leitura não realizada no período.'}

    Sono REM:
    {f'''
    - Média: {s("REMSleep")["média"]:.2f} h
    - Mínimo: {s("REMSleep")["mínimo"]:.2f} h
    - Máximo: {s("REMSleep")["máximo"]:.2f} h
    - Valores diários: {s("REMSleep")["valores"]}
    ''' if s("REMSleep")["disponivel"] else 'Leitura não realizada no período.'}

    Tempo Acordado:
    {f'''
    - Média: {s("AwakeSleep")["média"]:.2f} h
    - Mínimo: {s("AwakeSleep")["mínimo"]:.2f} h
    - Máximo: {s("AwakeSleep")["máximo"]:.2f} h
    - Valores diários: {s("AwakeSleep")["valores"]}
    ''' if s("AwakeSleep")["disponivel"] else 'Leitura não realizada no período.'}

    Tempo Total de Sono:
    {f'''
    - Média: {s("TotalSleep")["média"]:.2f} h
    - Mínimo: {s("TotalSleep")["mínimo"]:.2f} h
    - Máximo: {s("TotalSleep")["máximo"]:.2f} h
    - Valores diários: {s("TotalSleep")["valores"]}
    ''' if s("TotalSleep")["disponivel"] else 'Leitura não realizada no período.'}

    Fim do relatório do paciente {id} para o período de {data_inicial} a {data_final}.
    """.strip()

    return {
        "patient_id": id,
        "start_date": data_inicial,
        "end_date": data_final,
        "text": texto
    }

resultados = []
for pid, grupo_paciente in df.groupby("patient_id"):
    grupo_paciente = grupo_paciente.sort_values("date")
    inicio = grupo_paciente["date"].min()
    fim = grupo_paciente["date"].max()

    while inicio <= fim:
        intervalo = grupo_paciente[
            (grupo_paciente["date"] >= inicio) &
            (grupo_paciente["date"] < inicio + timedelta(days=7))
        ]
        if not intervalo.empty:
            resultados.append(gerar_descricao(intervalo))
        inicio += timedelta(days=7)

df_resultado = pd.DataFrame(resultados)
df_resultado.to_csv("data/processed/patients_register_documents.csv", index=False)

print("Arquivo de pacientes processado e salvo!")