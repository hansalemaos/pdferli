# Convert PDFs into pandas DataFrames, remove restrictions, put/crack PDF passwords

## pip install pdferli 

#### Tested against Windows 10 / Python 3.10 / Anaconda 

```python

crack_password(file, chars, processes=4, minlen=None, maxlen=None, verbose=True)
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


get_pdfdf(path, normalize_content=False, **kwargs)
	Extract structured data from a PDF document and return it as a pandas DataFrame.
	
	Args:
		path (str): Path to the PDF file.
		normalize_content (bool, optional): Whether to normalize content extraction. Defaults to False.
		**kwargs: Additional keyword arguments for pikepdf.open and extract_pages methods.
	
	Returns:
		pandas.DataFrame: DataFrame containing extracted structured data from the PDF.

put_password_encryption(inputfile, outputfile, password)
	Encrypt a PDF file using a specified password.
	
	Args:
		inputfile (str): Path to the input PDF file.
		outputfile (str): Path to the output encrypted PDF file.
		password (str): Password for encryption.


remove_restrictions(inputfile, outputfile, **kwargs)
	Remove encryption and restrictions from a PDF file.
	
	Args:
		inputfile (str): Path to the input encrypted PDF file.
		outputfile (str): Path to the output decrypted PDF file.
		**kwargs: Additional keyword arguments for pikepdf.save method.


Examples:

from time import perf_counter

from pdferli import (
    crack_password,
    put_password_encryption,
    remove_restrictions,
    get_pdfdf,
)


put_password_encryption(
    r"C:\sample.pdf",
    r"C:\sample4.pdf",
    password="1234",
)
path = r"C:\Arquivo.pdf"
remove_restrictions(path, "c:\\norestrictions.pdf")
df = get_pdfdf(path, normalize_content=False)




if __name__ == "__main__":  # necessary for crack_password since it uses multiprocessing
    start = perf_counter()
    x = crack_password(
        file=r"C:\sample4.pdf",
        chars=list("0123456789"),
        processes=4,
        minlen=0,
        maxlen=None,
        verbose=True,
    )
    print(perf_counter() - start)
    print(x)
    start = perf_counter()



# output df
   aa_adv  aa_bits aa_colorspace  aa_element_index aa_element_type  aa_evenodd  aa_fill aa_fontname  aa_height aa_imagemask  aa_linewidth aa_name    aa_size aa_srcsize aa_stream  aa_stroke aa_text      aa_text_element aa_text_line  aa_upright   aa_width       aa_x0       aa_x1       aa_y0       aa_y1 bb_hierachy_element bb_hierachy_page
0  31.968     <NA>          <NA>                 0          LTChar        <NA>     <NA>     ArialMT  56.546172         <NA>          <NA>    <NA>  56.546172       <NA>      <NA>       <NA>       A  APENAS VISUALIZAÇÃO            A        True  11.336388  126.431281  137.767669  242.012331  298.558504           (0, 0, 0)           (0, 0)
1    <NA>     <NA>          <NA>                 1          LTAnno        <NA>     <NA>        <NA>       <NA>         <NA>          <NA>    <NA>       <NA>       <NA>      <NA>       <NA>                           \n         <NA>       False       <NA>        <NA>        <NA>        <NA>        <NA>           (0, 0, 0)           (0, 0)
2  31.968     <NA>          <NA>                 2          LTChar        <NA>     <NA>     ArialMT  56.546172         <NA>          <NA>    <NA>  56.546172       <NA>      <NA>       <NA>       P  APENAS VISUALIZAÇÃO            P        True  11.336388  149.036174  160.372561  264.617224  321.163396           (0, 0, 0)           (0, 0)
3    <NA>     <NA>          <NA>                 3          LTAnno        <NA>     <NA>        <NA>       <NA>         <NA>          <NA>    <NA>       <NA>       <NA>      <NA>       <NA>                           \n         <NA>       False       <NA>        <NA>        <NA>        <NA>        <NA>           (0, 0, 0)           (0, 0)
4  31.968     <NA>          <NA>                 4          LTChar        <NA>     <NA>     ArialMT  56.546172         <NA>          <NA>    <NA>  56.546172       <NA>      <NA>       <NA>       E  APENAS VISUALIZAÇÃO            E        True  11.336388  171.641066  182.977454  287.222116  343.768289           (0, 0, 0)           (0, 0)
```