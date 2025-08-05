import pandas as pd
from datetime import timedelta
import ast

df = pd.read_csv("raw/20230120-data-collector-dailyRegister.csv", parse_dates=["Day"])

df.rename(columns={"Day": "date", "ID": "patient_id"}, inplace=True)

sleep_cols = ["LightSleep", "DeepSleep", "REMSleep", "AwakeSleep"]
for col in sleep_cols:
    df[col] = df[col] / 3600

df["TotalSleep"] = df["LightSleep"] + df["DeepSleep"] + df["REMSleep"] + df["AwakeSleep"]

df["HeartRate"] = df["HeartRate"].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])

def gerar_descricao(grupo):
    id = grupo["patient_id"].iloc[0]
    data_inicial = grupo["date"].min().date()
    data_final = grupo["date"].max().date()

    def stats(col):
        return {
            "média": grupo[col].mean(),
            "mínimo": grupo[col].min(),
            "máximo": grupo[col].max(),
            "valores": ", ".join(f"{v:.2f}" for v in grupo[col])
        }

    def heart_rate_stats(grupo):
        all_rates = [rate for sublist in grupo["HeartRate"] for rate in sublist]
        por_dia = [f"[{', '.join(str(r) for r in rates)}]" for rates in grupo["HeartRate"]]
        return {
            "média": sum(all_rates) / len(all_rates) if all_rates else 0,
            "mínimo": min(all_rates) if all_rates else 0,
            "máximo": max(all_rates) if all_rates else 0,
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
    - Média: {s("Steps")["média"]:.0f}
    - Mínimo: {s("Steps")["mínimo"]}
    - Máximo: {s("Steps")["máximo"]}
    - Valores diários: {s("Steps")["valores"]}

    Calorias:
    - Média: {s("Calories")["média"]:.0f} cal
    - Mínimo: {s("Calories")["mínimo"]} cal
    - Máximo: {s("Calories")["máximo"]} cal
    - Valores diários: {s("Calories")["valores"]}

    Batimentos Cardíacos:
    - Média: {hr["média"]:.0f} bpm
    - Mínimo: {hr["mínimo"]} bpm
    - Máximo: {hr["máximo"]} bpm
    - Valores diários: {hr["valores"]}

    Sono (valores em horas):

    Sono Leve:
    - Média: {s("LightSleep")["média"]:.2f} h
    - Mínimo: {s("LightSleep")["mínimo"]:.2f} h
    - Máximo: {s("LightSleep")["máximo"]:.2f} h
    - Valores diários: {s("LightSleep")["valores"]}

    Sono Profundo:
    - Média: {s("DeepSleep")["média"]:.2f} h
    - Mínimo: {s("DeepSleep")["mínimo"]:.2f} h
    - Máximo: {s("DeepSleep")["máximo"]:.2f} h
    - Valores diários: {s("DeepSleep")["valores"]}

    Sono REM:
    - Média: {s("REMSleep")["média"]:.2f} h
    - Mínimo: {s("REMSleep")["mínimo"]:.2f} h
    - Máximo: {s("REMSleep")["máximo"]:.2f} h
    - Valores diários: {s("REMSleep")["valores"]}

    Tempo Acordado:
    - Média: {s("AwakeSleep")["média"]:.2f} h
    - Mínimo: {s("AwakeSleep")["mínimo"]:.2f} h
    - Máximo: {s("AwakeSleep")["máximo"]:.2f} h
    - Valores diários: {s("AwakeSleep")["valores"]}

    Tempo Total de Sono:
    - Média: {s("TotalSleep")["média"]:.2f} h
    - Mínimo: {s("TotalSleep")["mínimo"]:.2f} h
    - Máximo: {s("TotalSleep")["máximo"]:.2f} h
    - Valores diários: {s("TotalSleep")["valores"]}

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
df_resultado.to_csv("processed/patients_register_documents.csv", index=False)
