import itertools
import os

import pikepdf
import touchtouch
from a_pandas_ex_less_memory_more_speed import pd_add_less_memory_more_speed

pd_add_less_memory_more_speed()
import pandas as pd
from pdfminer.high_level import extract_pages
import io
import multiprocessing
from flatten_any_dict_iterable_or_whatsoever import fla_tu

text = b""

def put_password_encryption(inputfile, outputfile, password):
    r"""
    Encrypt a PDF file using a specified password.

    Args:
        inputfile (str): Path to the input PDF file.
        outputfile (str): Path to the output encrypted PDF file.
        password (str): Password for encryption.
    """

    touchtouch.touch(outputfile)
    try:
        os.remove(outputfile)
    except Exception:
        pass
    with pikepdf.open(inputfile) as pdf:
        pdf.save(
            outputfile, encryption=pikepdf.Encryption(user=password, owner=password)
        )


def remove_restrictions(inputfile, outputfile, **kwargs):
    r"""
    Remove encryption and restrictions from a PDF file.

    Args:
        inputfile (str): Path to the input encrypted PDF file.
        outputfile (str): Path to the output decrypted PDF file.
        **kwargs: Additional keyword arguments for pikepdf.save method.
    """
    touchtouch.touch(outputfile)
    try:
        os.remove(outputfile)
    except Exception:
        pass
    with pikepdf.open(inputfile) as pdf:
        pdf.save(outputfile, encryption=False, **kwargs)


def get_password_pdf(pwd):

    isright = False
    pwdl=''.join(list(pwd))
    try:
        next(extract_pages(text, password=pwdl))
        isright = True
    except Exception:
        pass
    return pwdl, isright



def password_gen(chars,minlen=None,maxlen=None):
    chars=list(map(str,chars))
    if not minlen:
        minlen=1
    if not maxlen:
        maxlen = len(chars)+1
    for no in range(minlen, maxlen, 1):
        for charlst in (itertools.product(chars, repeat=no)):
            yield charlst

def initpool(arr):
    global text
    text = arr

def read_zipfile(file):
    with open(file, mode="rb") as f:
        data = f.read()
    return data

def crack_password(file, chars, processes=4, minlen=None, maxlen=None, verbose=True):
    """
    Attempt to crack a PDF password using a brute-force approach.

    Args:
        file (str): Path to the encrypted PDF file.
        chars (iterable): List of characters to generate passwords from.
        processes (int, optional): Number of parallel processes for password cracking. Defaults to 4.
        minlen (int, optional): Minimum length of generated passwords. Defaults to 1.
        maxlen (int, optional): Maximum length of generated passwords. Defaults to length of chars + 1.
        verbose (bool, optional): Whether to display progress information. Defaults to True.

    Returns:
        str: Cracked password if successful, None if not successful
    """
    data = read_zipfile(file)
    text = io.BytesIO(data)
    gener = password_gen(chars=chars, minlen=minlen, maxlen=maxlen)
    gotpass = False
    with multiprocessing.Pool(processes=processes, initializer=initpool, initargs=(text,)) as pool:
        processed_results = pool.imap_unordered(get_password_pdf, gener)
        for ini, pr in enumerate(processed_results):
            if verbose:
                print(str(ini).zfill(10), pr[0], end="\r")
            if pr[1]:
                gotpass = True
                break
    if gotpass:
        return pr[0]


def get_pdfdf(path, normalize_content=False, **kwargs):
    r"""
    Extract structured data from a PDF document and return it as a pandas DataFrame.

    Args:
        path (str): Path to the PDF file.
        normalize_content (bool, optional): Whether to normalize content extraction. Defaults to False.
        **kwargs: Additional keyword arguments for pikepdf.open and extract_pages methods.

    Returns:
        pandas.DataFrame: DataFrame containing extracted structured data from the PDF.
    """
    inp1 = io.BytesIO()
    with pikepdf.open(path, **kwargs) as pdf:
        pdf.save(inp1, encryption=False, normalize_content=normalize_content)

    lis = list(fla_tu(extract_pages(inp1)))
    tempup = [
        [x[0].__dict__, x[-1], str(type(x[0])).split(" ", maxsplit=1)[-1].strip("'>\"")]
        for x in lis
    ]
    [
        x[0].update({"bb_hierachy_element": x[1][0], "element_type": x[2]})
        for x in tempup
    ]
    tempup = [x[0] for x in tempup]
    df = pd.DataFrame(tempup)
    df["element_index"] = df.bb_hierachy_element.str[-1]
    df.bb_hierachy_element = df.bb_hierachy_element.str[:-1]
    df["bb_hierachy_page"] = df.bb_hierachy_element.str[:-1]
    df = df.drop(
        columns=[
            x
            for x in df.columns
            if x in ["ncs", "graphicstate", "bbox", "graphicstate", "pts"]
        ]
    )
    df.columns = [
        f'aa_{x.replace("-","_").strip("_")}' if not str(x).startswith("bb_") else x
        for x in df.columns
    ]
    df = df.fillna(pd.NA)
    df["aa_text_line"] = pd.NA
    for name, group in df.groupby(
        ["aa_y0", "aa_y1", "bb_hierachy_element", "aa_element_type"]
    ):
        df.loc[group.index, "aa_text_line"] = "".join(
            group.aa_text.fillna(" ").astype("string").to_list()
        )
    df["aa_text_element"] = pd.NA
    for name, group in df.groupby(["bb_hierachy_page", "aa_element_type"]):
        df.loc[group.index, "aa_text_element"] = "".join(
            group.aa_text.fillna(" ").astype("string").to_list()
        )
    dfcolor, dfcolor2, dfm = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    try:
        df["aa_non_stroking_color"] = df.aa_non_stroking_color.ds_apply_ignore(
            (pd.NA, pd.NA, pd.NA),
            lambda y: tuple(
                (round(x * 255) for x in y)
                if isinstance(y, tuple)
                else (0, 0, 0)
                if isinstance(y, int)
                else (pd.NA, pd.NA, pd.NA)
            ),
        )
        dfcolor = df.aa_non_stroking_color.ds_horizontal_explode(concat=False).rename(
            columns={
                "0_0": "aa_non_stroke_r",
                "0_1": "aa_non_stroke_g",
                "0_2": "aa_non_stroke_b",
            }
        )
    except Exception:
        pass
    try:
        dfcolor2 = df.aa_stroking_color.ds_horizontal_explode(concat=False).rename(
            columns={"0_0": "aa_stroke_r", "0_1": "aa_stroke_g", "0_2": "aa_stroke_b"}
        )
    except Exception:
        pass
    try:
        dfm = df.aa_matrix.ds_horizontal_explode("aa_matrix", concat=False)
    except Exception:
        pass
    df = pd.concat([q for q in [df, dfcolor, dfcolor2, dfm] if not q.empty], axis=1)
    df = df.drop(
        columns=[
            r
            for r in df.columns
            if r in ["aa_non_stroking_color", "aa_matrix", "aa_stroking_color"]
        ]
    )
    try:
        df.aa_upright = df.aa_upright.fillna(False)
    except Exception:
        pass
    try:
        df.aa_element_type = df.aa_element_type.str.split(".").str[-1]
    except Exception:
        pass
    return df.ds_reduce_memory_size_carefully(verbose=False).filter(sorted(df.columns))
