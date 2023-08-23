from PrettyColorPrinter import add_printer
from pdferli import get_pdfdf
import numpy as np
import pandas as pd

path = r"modelo_de_nota_de_envio_de_amostra.pdf"
add_printer(1)
df = get_pdfdf(path, normalize_content=False)
togi = []
for r in np.split(df, df.loc[df.aa_element_type == "LTAnno"].index):
    df2 = r.dropna(subset="aa_size")
    if not df2.empty:
        df3 = df2.sort_values(by="aa_x0")
        togi.append(df3.iloc[:1].copy())
df4 = pd.concat(togi).copy()
df4.loc[:, "x0round"] = df4.aa_x0.round(2)
resultado = []
for name, group in df4.groupby("x0round"):
    if len(group) > 1:
        group2 = group.reset_index(drop=True)
        group3 = np.split(
            group2, group2.loc[group2.aa_fontname == "Helvetica-Bold"].index
        )
        for group4 in group3:
            if len(group4) > 1:
                group5 = group4.sort_values(by="bb_hierachy_page")
                t1 = group5.aa_text_line.iloc[0]
                t2 = "\n".join(group5.aa_text_line.iloc[1:].to_list())
                resultado.append((t1, t2))

df5 = pd.DataFrame(resultado).set_index(0).T  # .to_excel('c:\\resultadospdf.xlsx')
