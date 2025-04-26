from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import re
 

def apri_file():
    filetypes = (
        ("Tutti i file .tex", "*.tex"),
        ("Tutti i file di testo", "*.txt"),
        ("Tutti i ifile .html", "*.html"),
        ("Tutti i file", "*.*"),
        )
    percorso = os.getcwd()
#    filename = filedialog.askopenfilename(title="Apri un file", initialdir=percorso, filetype=filetypes)
    filename = filedialog.askopenfilename(title="Apri un file", initialdir=percorso)
        
        
    if filename=='':
        return
    else:
        file = open(filename, "rt",encoding="utf-8")
    testo = file.read() # copia il contenuto del file tex
    file.close()


    label = Label(root, text='Sto convertendo il file')
    label.pack(ipadx=10, ipady=10)

    testo = accenti(testo) # sistema tutti gli accenti (italiani) scritti con la sintassi del TeX
    
    articolo=corpo(testo)  # corpo del testo

    articolo_finale="[latexpage]<br>\n" # L'ARTICOLO FINALE INIZIA SEMPRE CON IL tag [latexpage] PER RICHIAMARE IL PLUGIN QuickLaTeX

    titolo_completo = titolo(testo)
    tit = html_titolo(titolo_completo)
    aut = html_autore(autore(testo))

    articolo = fnsize_tex_to_html(articolo)
    articolo = italico_tex_to_html(articolo)
    articolo = italico2_tex_to_html(articolo)
    articolo = bold_tex_to_html(articolo)
    articolo = bold2_tex_to_html(articolo)
    articolo = underline_tex_to_html(articolo)
    articolo = section_tex_to_html(articolo)
    articolo = subsection_tex_to_html(articolo)
    articolo = subsection_ast_tex_to_html(articolo)
    articolo = breakline_tex_to_html(articolo)
    articolo = smallskip_tex_to_html(articolo)
    articolo = medskip_tex_to_html(articolo)
    articolo = bigskip_tex_to_html(articolo)
    articolo = fright_tex_to_html(articolo)
    articolo = itemize_tex_to_html(articolo)
    articolo = enumerate_tex_to_html(articolo)
    articolo = description_tex_to_html(articolo)
    articolo = figure_tex_to_html(articolo)
    articolo = wrapfigure_tex_to_html(articolo)
    articolo = url_tex_to_html(articolo)
    articolo = img_std(articolo)
    #articolo = accenti_full(articolo) # sistema tutti gli accenti (italiani) scritti con la sintassi del TeX

    count = 0
    while "\\begin{table}" in articolo:
        articolo = table_tex_to_html(articolo)
        count +=1
        print(count)
    
    while "\\begin{wraptable}" in articolo:
        articolo = wraptable_tex_to_html(articolo)
        count +=1
        print(count,'w')
        
    articolo = table_tex_to_html(articolo)
    articolo = wraptable_tex_to_html(articolo)
    

    


    articolo = trova_commenti(articolo)

    articolo_finale += tit+aut+articolo

    file_html = open(filename[:-4]+".txt", "w",encoding="utf-8")
    file_html.write(articolo_finale)
    file_html.close()

    label = Label(root, text='Il file è stato convertito con successo')
    label.pack(ipadx=10, ipady=10)



##def salva_file():
##    percorso = os.getcwd()
##    filename = filedialog.asksaveasfile(mode = "w", title="Salva file", initialdir=percorso, defaultextension=".txt")
##    print(filename, " salvato")






def corpo(testo): # restituisce il corpo dell'articolo: tutto il testo contenuto tra \begin{document} e \end{document}
    inizio = testo.find("\\maketitle") + len("\\maketitle\n")
    fine = testo.find("\\end{document}")
    corpo = testo[inizio+1:fine]
    return corpo

def titolo(testo): #restituisce il titolo dell'articolo
    tit_in = testo.find("\\title{")
    tit_fin = testo[tit_in:].find("}")
    titolo = testo[tit_in + len("\\title{"):tit_in + tit_fin]
    return titolo

def html_titolo(string): # restituisce il codice html per il titolo
    ## impostazioni: h1 (tipo di header); style=\"text-align: center (allineamento in centro); style=\"font-size: 24px (dimensione del font)
    return "<h1 style=\"text-align: center;\"><span style=\"font-size: 30px;\">"+string+"</span></h1><br>\n"


def autore(testo): #restituisce l'autore e la data dell'articolo
    aut_in = testo.find("\\author{")
    aut_fin = testo[aut_in:].find("}")
    autore = testo[aut_in + len("\\author{"):aut_in + aut_fin]
    return autore

def html_autore(string): # restituisce il codice html per l'autore
    ## impostazioni: h3 (tipo di header); style=\"text-align: center (allineamento in centro)
    return "<h3 style=\"text-align: center;\">"+string+"</h3><br>\n"


def section(testo): # individua il titolo di una sezione
    sec_in = testo.find("\\section{")
    sec_fin = testo[sec_in:].find("}")
    section_name = testo[sec_in + len("\\section{"):sec_in + sec_fin]
    return section_name

def html_section(string,num=0): # restituisce il codice html per il titolo della sottosezione
    ## impostazioni: h4 (tipo di header)
    return "<h4>"+str(num)+". "+string+"</h4><br>\n"

def section_ast(testo): # individua il titolo di una sezione
    sec_in = testo.find("\\section*{")
    sec_fin = testo[sec_in:].find("}")
    section_name = testo[sec_in + len("\\section*{"):sec_in + sec_fin]
    return section_name

def html_section_ast(string): # restituisce il codice html per il titolo della sottosezione
    ## impostazioni: h4 (tipo di header)
    return "<h4>"+string+"</h4><br>"

def section_tex_to_html(testo): # converte i titoli delle sezioni in formato html
    loc_testo=testo
    count=0
    while "\\section{" in loc_testo:
        sect=section(loc_testo)
        count+=1
        loc_testo=loc_testo.replace("\\section{"+sect+"}",html_section(sect,count))
    while "\\section*{" in loc_testo:
        sect=section_ast(loc_testo)
        loc_testo=loc_testo.replace("\\section*{"+sect+"}",html_section_ast(sect))
    return loc_testo

def subsection(testo): # individua il titolo di una sottosezione
    subsec_in = testo.find("\\subsection{")
    subsec_fin = testo[subsec_in:].find("}")
    subsection_name = testo[subsec_in + len("\\subsection{"):subsec_in + subsec_fin]
    return subsection_name

def html_subsection(string,num_sec,num_subsec): # restituisce il codice html per il titolo della sottosezione
    ## impostazioni: h6 (tipo di header)
    return "<h6>"+str(num_sec)+"."+str(num_subsec)+" "+string+"</h6><br>\n"

def cerca_sec(testo):
    find_sec = testo.rfind("<h4>")
    if find_sec == -1:
        current_sec = 0
    else:
        current_sec = testo[find_sec+len("<h4>")]
    return current_sec

def subsection_tex_to_html(testo): # converte i titoli delle sottosezioni in formato html
    # bisognerebbe inserire una ricerca sulla parte precedente per leggeere la sezione in cui ci si trova e mettere quel valore davanti all'output
    loc_testo=testo
    subsec_count=0
    while "\\subsection{" in loc_testo:
        posizione = loc_testo.find("\\subsection{")
        subsect=subsection(loc_testo)
        subsec_count+=1
        sec_numb=cerca_sec(loc_testo[:posizione]) 
        loc_testo=loc_testo.replace("\\subsection{"+subsect+"}",html_subsection(subsect,sec_numb,subsec_count))
    return loc_testo

def subsection_ast(testo): # individua il titolo di una sottosezione
    subsec_in = testo.find("\\subsection*{")
    subsec_fin = testo[subsec_in:].find("}")
    subsection_name = testo[subsec_in + len("\\subsection*{"):subsec_in + subsec_fin]
    return subsection_name

def html_subsection_ast(string): # restituisce il codice html per il titolo della sottosezione
    ## impostazioni: h6 (tipo di header)
    return "<h6>"+string+"</h6><br>\n"

def cerca_sec_ast(testo):
    find_sec = testo.rfind("<h4>")
    if find_sec == -1:
        current_sec = 0
    else:
        current_sec = testo[find_sec+len("<h4>")]
    return current_sec

def subsection_ast_tex_to_html(testo): # converte i titoli delle sottosezioni in formato html
    # bisognerebbe inserire una ricerca sulla parte precedente per leggeere la sezione in cui ci si trova e mettere quel valore davanti all'output
    loc_testo=testo
    subsec_count=0
    while "\\subsection*{" in loc_testo:
        posizione = loc_testo.find("\\subsection*{")
        subsect=subsection_ast(loc_testo)
        subsec_count+=1
        sec_numb=cerca_sec_ast(loc_testo[:posizione]) 
        loc_testo=loc_testo.replace("\\subsection*{"+subsect+"}",html_subsection_ast(subsect))
    return loc_testo

#######################################################
#### Trova la fine di un testo chiuso tra graffe
#######################################################
def trova_testo(testo):
    loc_testo = testo
    parti = testo.split("}")                                     # suddivide il testo usando } come separatore
    graffe = [p.count("{") for p in parti]                       # conta le { presenti in ogni parte del testo 
    cum = [sum(graffe[:idx])-1 for idx in range(1,len(graffe)+1)]  # vettore delle somme cumulate del numero di graffe { in una parte di testo
    buoni = [cum[i]==i for i in range(len(graffe))]              # trova la posizione delle parti in cui il numero di graffe } bilancia il numero di { 
    index = buoni.index(True)                                    # trova la parte in cui si chiude il testo tra graffe
    testo_utile = "}".join(parti[:index+1])
    return testo_utile[testo_utile.find("{")+1:]
    
############ table, wraptable e tabular ##############

def table(testo): # individua un blocco table
    caption = ''
    table_in = testo.find("\\begin{table}")
    table_fin = testo[table_in:].find("\end{table}")
    table = testo[table_in + len("\\begin{table}"):table_in + table_fin]
    if "caption" in table:
        cap_in = testo.find("\\caption{")
        cap_fin = testo[cap_in:].find("}")
        caption = testo[cap_in + len("\\caption{"):cap_in + cap_fin]
    return table, caption

def wraptable(testo): # individua un blocco wraptable
    caption = ''
    wraptable_in = testo.find("\\begin{wraptable}")
    wraptable_fin = testo[wraptable_in:].find("\end{wraptable}")
    wraptable = testo[wraptable_in + len("\\begin{wraptable}"):wraptable_in + wraptable_fin]
    if "caption" in wraptable:
        cap_in = testo.find("\\caption{")
        cap_fin = testo[cap_in:].find("}")
        caption = testo[cap_in + len("\\caption{"):cap_in + cap_fin]
    return wraptable, caption


def convert_latex_table_to_html(latex_table):
    # Rimuovi il testo iniziale fino alla tabella
    table_content = re.search(r'\\begin{tabular}{.*?}(.+?)\\end{tabular}', latex_table, re.DOTALL)
    if table_content:
        table_content = table_content.group(1)
    else:
        return None
    rows = table_content.strip().split('\n')

    html_table = '<table border="1">\n'
    for row in rows:
        # Rimuovi '\hline' e '\cr'
        row = row.replace('\hline', '').replace('\\cr', '')
        # Split in colonne
        columns = row.split('&')
        html_table += '<tr>\n'
        for column in columns:
            # Rimuovi spazi e simboli '$'
            cell_content = column.strip().replace('$', '')
            html_table += '<td>{cell_content}</td>\n'
        html_table += '</tr>\n'
    html_table += '</table>'
    return html_table

def tex_table(testo):
    tabular_in = testo.find("\\begin{tabular}")
    tabular_fin = testo[tabular_in:].find("\end{tabular}")
    table = testo[tabular_in :tabular_in + tabular_fin+ len("\\end{tabular}")]
    return latex_table
    
def tabular(testo): # individua un blocco tabular e le caratteristiche del tabular
    tabular_in = testo.find("\\begin{tabular}")
    tabular_fin = testo[tabular_in:].find("\end{tabular}")
    tabular = testo[tabular_in + len("\\begin{tabular}"):tabular_in + tabular_fin]
    struttura = tabular[tabular.find("{")+1:tabular.find("}")]
    tabular=tabular[tabular.find("}")+2:]  # escludo dal testo della tabular le proprietà e il carattere per andare a capo \n
    struttura = struttura.replace(" ","")
    sep = [i for i, ltr in enumerate(struttura) if ltr == "|"]   # individua le posizioni dei separatori verticali
    n_colonne = len(struttura.replace("|",""))
    n_righe = tabular.count("\\cr")
    return tabular, struttura

    
def html_tabular(tabular, struttura,caption=''): # restituisce il codice html per il blocco tabular
    loc_testo = tabular
    l = ""
##    <table border="1" width="100%">
##    <caption>This is the caption</caption>
##  <tr>
##    <th>Nome</th>
##    <th>Cognome</th>
##    <th>Indirizzo Email</th>
##  </tr>
##  <tr>
##   <td>Hillary</td>
##   <td>Nyakundi</td>
##   <td>tables@mail.com</td>
##  </tr>
##  <tr>
##    <td>Lary</td>
##    <td>Mak</td>
##    <td>developer@mail.com</td>
##  </tr>
##</table>

    #loc_testo = loc_testo.replace("&","</td><td>")  # conversione dei separatori
    #loc_testo = loc_testo.replace("\n","")
    #lines = loc_testo.split("\\cr")   # individuo ogni riga
    #for line in lines:
    #    l=l+"\n<tr><td>"+line+"</td></tr>"
    #start = '<table>'
    #if caption!='':
    #    start +='<caption>'+caption+'</caption>'
    #return start+l+"\n</table>"

    rows = loc_testo.strip().split('\n')

    html_table = '<table border="1">\n'
    for row in rows:
        # Rimuovi '\hline' e '\cr'
        row = row.replace('\hline', '').replace('\\cr', '')
        # Split in colonne
        columns = row.split('&')
        html_table += '  <tr>\n'
        for column in columns:
            # Rimuovi spazi e simboli '$'
            cell_content = column.strip().replace('$', '')
            html_table += f'    <td>{cell_content}</td>\n'
        html_table += '  </tr>\n'
    html_table += '</table>'
    return html_table

    

def table_tex_to_html(testo): # converte i tabular in formato html
    loc_testo=testo
#    while "\\begin{tabular}" in loc_testo:
    if "\\begin{table}" in loc_testo:
        table_cont, caption = table(loc_testo)
        whole_in = table_cont.find("\\begin{table}")
        whole_fin = table_cont[whole_in:].find("\end{table}")
        whole = table_cont
        tab,struct=tabular(table_cont)
        loc_testo=loc_testo.replace("\\begin{table}"+whole+"\end{table}",html_tabular(tab,struct,caption))
    return loc_testo

def wraptable_tex_to_html(testo):
    loc_testo=testo
    if "\\begin{wraptable}" in loc_testo:
        table_cont, caption = wraptable(loc_testo)
        whole_in = table_cont.find("\\begin{wraptable}")
        whole_fin = table_cont[whole_in:].find("\end{wraptable}")
        whole = table_cont
        tab,struct=tabular(table_cont)
        loc_testo=loc_testo.replace("\\begin{wraptable}"+whole+"\end{wraptable}",html_tabular(tab,struct,caption))
    return loc_testo


########################################################

def itemize(testo): # individua un blocco itemize
    itemize_in = testo.find("\\begin{itemize}")
    itemize_fin = testo[itemize_in:].find("\end{itemize}")
    item_list = testo[itemize_in + len("\\begin{itemize}"):itemize_in + itemize_fin]
    return item_list

def item_list(testo): #individua un item di itemize
    item_list = []
    while "\\item" in testo:
        item_in = testo.find("\\item")
        if "\\item" in testo[item_in+len("\\item"):]:
            item_fin = testo[item_in+len("\\item"):].find("\\item")
        else:
            item_fin = len(testo)
        item = testo[item_in + len("\\item"):item_in + item_fin+ len("\\item")]
        item_list+=[item[1:]]
        testo = testo[item_fin:]
    return item_list
    
def html_itemize(items): # restituisce il codice html per il blocco itemize
    l = ""
    for item in items:
        l+="<li>"+item+"</li>\n"
    return "<ul type=\"disc\">\n"+l+"</ul>\n"

def itemize_tex_to_html(testo): # converte i blocchi itemize in formato html
    loc_testo=testo
    while "\\begin{itemize}" in loc_testo:
        item_blk=itemize(loc_testo)
        items=item_list(item_blk)
        loc_testo=loc_testo.replace("\\begin{itemize}"+item_blk+"\end{itemize}",html_itemize(items))
    return loc_testo



def enumerate_bl(testo): # individua un blocco enumerate
    enumerate_in = testo.find("\\begin{enumerate}")
    enumerate_fin = testo[enumerate_in:].find("\end{enumerate}")
    item_list = testo[enumerate_in + len("\\begin{enumerate}"):enumerate_in + enumerate_fin]
    return item_list

def enum_list(testo): #individua un item di enumerate
    enum_list = []
    while "\\item" in testo:
        enum_in = testo.find("\\item")
        if "\\item" in testo[enum_in+len("\\item"):]:
            enum_fin = testo[enum_in+len("\\item"):].find("\\item")
        else:
            enum_fin = len(testo)
        enum = testo[enum_in + len("\\item"):enum_in + enum_fin+ len("\\item")]
        enum_list+=[enum[1:]]
        testo = testo[enum_fin:]
    return enum_list
    
def html_enumerate(items): # restituisce il codice html per il blocco enumerate
    l = ""
    for item in items:
        l+="<li>"+item+"</li>\n"
    return "<ol type=\"1\" start = \"1\">\n"+l+"</ol>\n"

def enumerate_tex_to_html(testo): # converte i blocchi enumerate in formato html
    loc_testo=testo
    while "\\begin{enumerate}" in loc_testo:
        enum_blk=enumerate_bl(loc_testo)
        enums=enum_list(enum_blk)
        loc_testo=loc_testo.replace("\\begin{enumerate}"+enum_blk+"\end{enumerate}",html_enumerate(enums))
    return loc_testo

def description(testo): # individua un blocco description
    description_in = testo.find("\\begin{description}")
    description_fin = testo[description_in:].find("\end{description}")
    desc_list = testo[description_in + len("\\begin{description}"):description_in + description_fin]
    return desc_list

def desc_list(testo): #individua un item di itemize
    desc_list = []
    while "\\item" in testo:
        desc_in = testo.find("\\item") 
        if testo[desc_in+ len("\\item"):].startswith("["):
            par1 = testo.find("[")
            par2 = testo.find("]")
            testo = testo[desc_in:par1]+testo[par1+1:par2]+testo[par2+1:]
            if "\\item" in testo[desc_in+len("\\item"):]:
                desc_fin = testo[desc_in+len("\\item"):].find("\\item")
            else:
                desc_fin = len(testo)
            desc = testo[len("\\item"): desc_in + desc_fin + len("\\item")]
        else:
            if "\\item" in testo[desc_in+len("\\item"):]:
                desc_fin = testo[desc_in+len("\\item"):].find("\\item")
            else:
                desc_fin = len(testo)
            desc = testo[desc_in + len("\\item"):desc_in + desc_fin+ len("\\item")]
        desc_list+=[desc]
        testo = testo[desc_fin:]
    return desc_list
    
def html_description(items): # restituisce il codice html per il blocco itemize
    l = ""
    for item in items:
        l+="<li>"+item+"</li>\n"
    return "<ul type= none>\n"+l+"</ul>\n"

def description_tex_to_html(testo): # converte i blocchi itemize in formato html
    loc_testo=testo
    while "\\begin{description}" in loc_testo:
        item_blk=description(loc_testo)
        items=desc_list(item_blk)
        loc_testo=loc_testo.replace("\\begin{description}"+item_blk+"\end{description}",html_description(items))
    return loc_testo


def italico(testo): # individua un testo scritto in italico
    it_in = testo.find("\\textit{")
    it_text = trova_testo(testo[it_in:])
    return it_text

def html_italico(string): # restituisce il codice html per un testo scritto in italico
    ## impostazioni: em (per \textit o \emph)
    return "<em>"+string+"</em>"

def italico_tex_to_html(testo):
    loc_testo=testo
    while "\\textit{" in loc_testo:
        it=italico(loc_testo)
        loc_testo=loc_testo.replace("\\textit{"+it+"}",html_italico(it))
    return loc_testo

def italico2(testo): # individua un testo scritto in italico
    it_in = testo.find("\\it{")
    it_text = trova_testo(testo[it_in:])
    return it_text

def italico2_tex_to_html(testo):
    loc_testo=testo
    while "\\it{" in loc_testo:
        it=italico2(loc_testo)
        loc_testo=loc_testo.replace("\\it{"+it+"}",html_italico(it))
    return loc_testo

def bold(testo): # individua un testo scritto in boldface
    bf_in = testo.find("\\textbf{")
    bf_text = trova_testo(testo[bf_in:])
    return bf_text

def html_bold(string): # restituisce il codice html per un testo scritto in boldface
    return "<b>"+string+"</b>"

def bold_tex_to_html(testo):
    loc_testo=testo
    while "\\textbf{" in loc_testo:
        bf=bold(loc_testo)
        loc_testo=loc_testo.replace("\\textbf{"+bf+"}",html_bold(bf))
    return loc_testo

def bold2(testo): # individua un testo scritto in boldface
    bf_in = testo.find("{\\bf")
    bf_text = trova_testo(testo[bf_in:])
    bf_fin = testo[bf_in:].find("}")
    bf_text = testo[bf_in + len("{\\bf"):bf_in + bf_fin]
    return bf_text


def bold2_tex_to_html(testo):
    loc_testo=testo
    while "{\\bf" in loc_testo:
        bf=bold2(loc_testo)
        loc_testo=loc_testo.replace("{\\bf"+bf+"}",html_bold(bf))
    return loc_testo

def underline(testo): # individua un testo scritto in italico
    ul_in = testo.find("\\underline{")
    ul_text = trova_testo(testo[ul_in:])
    return ul_text

def html_underline(string): # restituisce il codice html per un testo sottolineato
    ## impostazioni:  (per \underline)
    return "<u>"+string+"</u>"

def underline_tex_to_html(testo):
    loc_testo=testo
    while "\\underline{" in loc_testo:
        ul=underline(loc_testo)
        loc_testo=loc_testo.replace("\\underline{"+ul+"}",html_underline(ul))
    return loc_testo


def trova_figure(testo):
    fig_in = testo.find("\\begin{figure}")
    fig_fin = testo[fig_in:].find("\\end{figure}")
    fig_text = testo[fig_in:fig_in + fig_fin+len("\\end{figure}")]
    include=fig_text.find("\\includegraphics")
    fig_name_in = fig_text[include:].find("{")
    fig_name_fin = fig_text[include:].find("}")
    fig_name = fig_text[include+fig_name_in+1:include+fig_name_fin]
    return [fig_text,fig_name]

def html_figure(string): 
    return "Inserire la figura "+string

def figure_tex_to_html(testo):
    loc_testo=testo
    while "\\begin{figure}" in loc_testo:
        fig=trova_figure(loc_testo)
        loc_testo=loc_testo.replace(fig[0],html_figure(fig[1]))
    return loc_testo


def trova_wrapfigure(testo):
    fig_in = testo.find("\\begin{wrapfigure}")
    fig_fin = testo[fig_in:].find("\\end{wrapfigure}")
    fig_text = testo[fig_in:fig_in + fig_fin+len("\\end{wrapfigure}")]
    include=fig_text.find("\\includegraphics")
    fig_name_in = fig_text[include:].find("{")
    fig_name_fin = fig_text[include:].find("}")
    fig_name = fig_text[include+fig_name_in+1:include+fig_name_fin]
    return [fig_text,fig_name]

def html_wrapfigure(string): 
    return "Inserire la wrapfigura "+string

def wrapfigure_tex_to_html(testo):
    loc_testo=testo
    while "\\begin{wrapfigure}" in loc_testo:
        fig=trova_wrapfigure(loc_testo)
        loc_testo=loc_testo.replace(fig[0],html_wrapfigure(fig[1]))
    return loc_testo


def fright(testo): # individua un testo scritto in flushright
    fr_in = testo.find("\\begin{flushright}")
    fr_fin = testo[fr_in:].find("\\end{flushright}")
    fr_text = testo[fr_in + len("\\begin{flushright}"):fr_in + fr_fin]
    return fr_text

def html_fright(string): # restituisce il codice html per un testo scritto in flushright
    return "<p style=\"text-align: right;\">"+string+"</p>"

def fright_tex_to_html(testo): # converte i blocchi flushright in html
    loc_testo=testo
    while "\\begin{flushright}" in loc_testo:
        fr=fright(loc_testo)
        loc_testo=loc_testo.replace("\\begin{flushright}"+fr+"\\end{flushright}",html_fright(fr))
    return loc_testo

def fnsize(testo): # individua un testo scritto in footnotesize
    fn_in = testo.find("\\footnotesize{")
    fn_fin = testo[fn_in:].find("}")
    fn_text = testo[fn_in + len("\\footnotesize{"):fn_in + fn_fin]
    return fn_text

def html_fnsize(string): # restituisce il codice html per un testo scritto in footnotesize
    return "<span class=\"wpex-text-sm\">"+string+"</span>" 

def fnsize_tex_to_html(testo): # converte i footnotesize in html
    loc_testo=testo
    while "\\footnotesize{" in loc_testo:
        fn=fnsize(loc_testo)
        loc_testo=loc_testo.replace("\\footnotesize{"+fn+"}",html_fnsize(fn))
    return loc_testo

def breakline_tex_to_html(testo): #converte i \\ in comandi html per andare a capo
    loc_testo=testo
    while "\\\\" in loc_testo:
        loc_testo=loc_testo.replace("\\\\","<br>")
    return loc_testo

def smallskip_tex_to_html(testo): # converte i \smallskip in html
    loc_testo=testo
    while "\\smallskip" in loc_testo:
        loc_testo=loc_testo.replace("\\smallskip","<br>")
    return loc_testo

def medskip_tex_to_html(testo): # converte i \medskip in html
    loc_testo=testo
    while "\\medskip" in loc_testo:
        loc_testo=loc_testo.replace("\\medskip","<br><br>")
    return loc_testo

def bigskip_tex_to_html(testo): # converte i \bigskip in html
    loc_testo=testo
    while "\\bigskip" in loc_testo:
        loc_testo=loc_testo.replace("\\bigskip","<br><br><br>")
    return loc_testo

def trova_commenti(testo): # trova e rimuove i commenti
    start = 0
    ind = 0
    vspace = 0
    while ind != -1:
        commento_in = testo.find("%",start)
        if testo[commento_in-1] != "\\":
            commento_fin = testo[commento_in:].find("\n")
            commento_text = testo[commento_in:commento_in + commento_fin]
            testo=testo.replace(testo[commento_in:commento_in + commento_fin],"")
        ind = commento_in
        start = commento_in + 1
    while "\\newpage" in testo:
        testo=testo.replace("\\newpage","")
    while "thispagestyle{fancy}" in testo:
        testo=testo.replace("thispagestyle{fancy}","")
    start = 0
    while vspace != -1:
        vs_in = testo.find("\\vspace",start)
        vs_fin = testo[vs_in:].find("\n")
        vs_text = testo[vs_in:vs_in + vs_fin]
        testo=testo.replace(testo[vs_in:vs_in + vs_fin],"")
        vspace = vs_in
        start = vs_in + 1
    return testo

def accenti(testo): # converte le lettere accentate "\'x" o "E'"
    loc_testo=testo
    while "\\'a" in loc_testo:
        loc_testo=loc_testo.replace("\\'a","à")
    while "\\'e" in loc_testo:
        loc_testo=loc_testo.replace("\\'e","è")
    while "\\'i" in loc_testo:
        loc_testo=loc_testo.replace("\\'i","ì")
    while "\\'o" in loc_testo:
        loc_testo=loc_testo.replace("\\'o","ò")
    while "\\'u" in loc_testo:
        loc_testo=loc_testo.replace("\\'u","ù")
    while "E'" in loc_testo:
        loc_testo=loc_testo.replace("E'","È")
    while "\\'E" in loc_testo:
        loc_testo=loc_testo.replace("\\'E","È")
    while "\\`e" in loc_testo:
        loc_testo=loc_testo.replace("\\`e","é")
    while "\\`o" in loc_testo:
        loc_testo=loc_testo.replace("\\`o","ó")
    return loc_testo


def accenti_full(testo):
    loc_testo = testo
    accenti_dict = {"\\'":"grave", "\\`":"acute","\\\"":"uml","\\^":"circ","\\~":"tilde","\\c":"cedil","\\r":"ring","\\v":"caron"}
    for accento in accenti_dict:
        while accento in loc_testo:
            acc_in = loc_testo.find(accento)
            char_acc = acc_in + len(accento)
            if loc_testo[char_acc] == ' ':
                char_acc = char_acc + 1
            acc_html = '&'+loc_testo[char_acc]+accenti_dict[accento]+';'
            loc_testo=loc_testo.replace(loc_testo[acc_in:char_acc+1],acc_html)
    return loc_testo
    

def url(testo): # individua un link esterno
    url_in = testo.find("\\url{")
    url_fin = testo[url_in:].find("}")
    url_text = testo[url_in + len("\\url{"):url_in + url_fin]
    return url_text

def html_url(string): # restituisce il codice html per un link
    return "<a href=\""+string+"\">"+string+"</a>"

def url_tex_to_html(testo):
    loc_testo=testo
    while "\\url{" in loc_testo:
        url_text=url(loc_testo)
        loc_testo=loc_testo.replace("\\url{"+url_text+"}",html_url(url_text))
    return loc_testo

# funzione che forza l'aspetto dei link standard ai siti di immagini (nella sezione Immagini)
# non elegante, ma funziona
def img_std(testo):
    loc_testo=testo
    links = "<a href=\"https://unsplash.com/\">https://unsplash.com/</a>","<a href=\"https://pixabay.com/\">https://pixabay.com/</a>","<a href=\"https://www.pexels.com/\">https://www.pexels.com/</a>"
    for link in links:
        if link in loc_testo:
            loc_testo=loc_testo.replace(link,"<li>"+link+"</li>")
    return loc_testo
	
	



root = Tk()
root.title('Polymath - Conversione da .tex a .html')
root.geometry('300x100')
root.iconbitmap('favicon.ico')


bottone_O = ttk.Button(root, text="Scegli un file .tex da convertire", command=apri_file)
bottone_O.pack(expand=True)

##bottone_S = ttk.Button(root, text="Salva file .html", command=salva_file)
##bottone_S.pack(expand=True)




root.mainloop()
