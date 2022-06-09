from utils import Utils  # libreria per utilizzare funzioni JS
import js  # libreria per javascript
import pyodide  # libreria per pyscript
import random  # libreria per usare un valore casuale
PREMESSA:
L’esercizio serve ad allontanare le paure che ci possono affliggere all’idea di dover imparare da zero un nuovo linguaggio.
Se non ve ne siete accorti, negli ultimi mesi ne abbiamo imparati già due. Oggi però farete tutto da soli.

SCOPO DEL GIOCO:
Sicuramente avrete già giocato al gioco dell’impiccato sui banchi di scuola, nei momenti morti di alcune lezioni con il vostro vicino.
Uno dei giocatori pensa una parola e aggiunge su un foglio un numero di trattini pari al numero di lettere che la compongono.
L’altro giocatore dovrà indovinare la parola tentando di indovinare le lettere che la compongono.
Ogni tentativo sbagliato verrà contato come errore.

TECNOLOGIE:
Oggi si lavora con Python, per questo motivo dovete concentrarvi solo sul file YOUR_SOLUTION.py, non curatevi degli altri file.
Se volete poi dopo le 18.00 potrete sbirciare il resto del codice.
Ma l’escamotage che abbiamo usato per farvi lavorare tranquilli è solo un modo semplice e comodo per permettervi di lavorare senza distrazioni

CONSEGNA:
I giocatori sono l'utente e il computer.
Il computer sceglie casualmente una parola e l'utente la dovrà indovinare.
Ha a disposizione 5 tentativi.

L'utente potrà provare ad indovinare una sola lettera per volta.
Ad ogni inserimento(sia che avvenga tramite tasto INVIO oppure tramite CLICK su apposito pulsante) il computer deve controllare
se quella lettera è presente nella parola da indovinare.

Se la lettera è presente, deve apparire al posto giusto, sostituendo il trattino(o i trattini) corrispondente.
Se la lettera non è presente, l'utente deve essere avvisato dell'errore con un messaggio che mostra anche quanti tentativi sono rimasti.
Se la lettera è già stata usata, l'utente deve essere avvisato con un messaggio, ma i tentativi a disposizione non devono diminuire.

Nella parte sottostante il campo di input saranno mostrate tutte le lettere già utilizzate dall'utente(sia quelle corrette che quelle errate).

Il gioco termina quando l'utente esaurisce i tentativi a disposizione oppure se indovina la parola.
In entrambi i casi si deve mostrare un messaggio adatto alla situazione.

# CONSIGLI:
# - occhio alla indentazione

# ------------------------------------------LIBRERIE-------------------------------------------------------


# istanza della libreria - ripensate all'esercizio di PHP con Movie ;)
custom_utils = Utils(pyodide, js)

# ---------------------------------------ELEMENTI DAL DOM------------------------------------------------------

# questi elementi sono già stati catturati per te,
# ti serviranno per prendere il valore inserito e catturare l'evento di invio

user_letter = custom_utils.getHtmlElement("user-letter")
add_letter_btn = custom_utils.getHtmlElement("add-letter-btn")
# questo elemento conterrà il testo segnaposto per la parola da indovinare
word_html_container = custom_utils.getHtmlElement('word')
errors_html = custom_utils.getHtmlElement("errors")
used_letters_html = custom_utils.getHtmlElement("used-letters")

# ----------------------------------------------------------------------------------------------------


def main():

    # le variabili sono definite come esempi, non siete obbligati ad utilizzarle tutte o solo queste

    global words
    global count
    #global length
    global word
    global display
    global already_guessed
    #global limit
    global convertList
    global newList
    global tentativiMax
    global lettereInserite
    custom_utils.writeToConsole(user_letter.value)
    count = 5
    lettereInserite = []
    words = ['matto', 'gatto', 'pazzo']  # array con le parole da indovinare
    word = random.choice(words)
    # inserisco la stringa segnaposto dentro il contenitore HTML
    display = '_'*len(word)
    custom_utils.writeToHtmlElement(word_html_container, '%s' % (display))
    # verificare numero tentativi possibili
    convertList = list(word)
    newList = set(convertList)
    tentativiMax = len(newList)


def trovaLettera(event):

    custom_utils.writeToConsole(event)
    # iseriamo la lettere in una list
    lettereInserite.append(user_letter.value)
    custom_utils.writeToConsole(lettereInserite)
    # verificare se user_letter è contenuta
    if (word.find(user_letter.value) != -1):
        index = 0
        indici = []
        while index < len(word):
            index = word.find(user_letter.value, index)
            custom_utils.writeToConsole(index)
            indici.append(index)
            custom_utils.writeToConsole(indici)
            if index == -1:
                break
            index += 1
        # sostituiamo le lettere
        for i in indici:
            letteraSvelata = display[i] + user_letter.value + display[i+1:]

        # stampiamo
        display = letteraSvelata

        # inseriamo la lettera nelle lettere indovinate
        if (user_letter.value not in already_guessed):
            already_guessed.append(user_letter.value)
            custom_utils.writeToConsole(already_guessed)
    else:
        count -= 1
        custom_utils.writeToHtmlElement(
            errors_html, 'Ti sono rimasti ' + count + ' tentativi')
        custom_utils.writeToHtmlElement(
            used_letters_html, 'Lettere usate: ' + lettereInserite)
        errors_html


main()
custom_utils.addOnClickEventToHtmlElement(add_letter_btn, trovaLettera)
