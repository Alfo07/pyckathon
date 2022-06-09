'''
REPO: pyckathon

PREMESSA:
l’esercizio serve ad allontanare le paure che ci possono affliggere all’idea di dover imparare da zero un nuovo linguaggio.
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
Ad ogni inserimento (sia che avvenga tramite tasto INVIO oppure tramite CLICK su apposito pulsante) il computer deve controllare
se quella lettera è presente nella parola da indovinare.

Se la lettera è presente, deve apparire al posto giusto, sostituendo il trattino (o i trattini) corrispondente.
Se la lettera non è presente, l'utente deve essere avvisato dell'errore con un messaggio che mostra anche quanti tentativi sono rimasti.
Se la lettera è già stata usata, l'utente deve essere avvisato con un messaggio, ma i tentativi a disposizione non devono diminuire.

Nella parte sottostante il campo di input saranno mostrate tutte le lettere già utilizzate dall'utente (sia quelle corrette che quelle errate).

Il gioco termina quando l'utente esaurisce i tentativi a disposizione oppure se indovina la parola.
In entrambi i casi si deve mostrare un messaggio adatto alla situazione.

BONUS:
Se l'utente invia testo vuoto, avvisarlo con un messaggio di errore, ma i tentativi a disposizione non devono diminuire.
Una volta terminato il gioco (sia in caso di vittoria che di sconfitta) impedire all'utente di fare ulteriori tentativi.


Lettura consigliata:
https://blog.devgenius.io/pyscript-a-new-way-of-building-html-websites-tutorial-for-beginners-67a75935e039
'''

import random
# Non per forza necessario visto l'approccio base utilizzato nella funzione updateDisplayString
import re
import pyodide
import js
from utils import Utils

custom_utils = Utils(pyodide, js)

user_letter = custom_utils.getHtmlElement("user-letter")
add_letter_btn = custom_utils.getHtmlElement("add-letter-btn")

word_html_container = custom_utils.getHtmlElement('word')
errors_html_container = custom_utils.getHtmlElement('errors')
result_html_container = custom_utils.getHtmlElement('result')
used_letters_html_container = custom_utils.getHtmlElement('used-letters')
solution_html_container = custom_utils.getHtmlElement('solution')

def main():

    global words
    global count
    global length
    global word
    global display
    global already_guessed
    global limit

    words = ['boolean', 'php', 'javascript']
    count = 0
    already_guessed = []
    limit = 5

    # https://www.w3schools.com/python/module_random.asp
    # https://www.w3schools.com/python/ref_random_choice.asp
    word = random.choice(words)
    length = len(word)
    # https://stackoverflow.com/questions/29321723/how-to-repeat-characters-in-python-without-string-concatenation
    display = '_' * length
    custom_utils.writeToHtmlElement(word_html_container, '%s' % (display))

def game(event):

    global count
    global display

    letter = user_letter.value
    letter = letter.strip()

    # pulisco i messaggi di errore
    custom_utils.writeToHtmlElement(errors_html_container, '')

    # ignoro i tentativi non validi (es. input vuoto oppure troppo lungo)
    if not letter or len(letter) > 1:

        custom_utils.writeToHtmlElement(errors_html_container, 'Input non valido!')

    elif letter in already_guessed:

        custom_utils.writeToHtmlElement(errors_html_container, 'Lettera già usata!')

    elif letter in word:

        display = updateDisplayString(letter, display)
        custom_utils.writeToHtmlElement(word_html_container, '%s' % (display))

    else:

        count += 1

        if count == 4:

            custom_utils.writeToHtmlElement(result_html_container, "Lettera sbagliata! Ti rimane un solo tentativo!")

        elif count < 5:

            tentativi = limit - count
            custom_utils.writeToHtmlElement(result_html_container, "Lettera sbagliata! Hai altri %d tentativi!" % (tentativi))


    # pulisco l'input
    custom_utils.emptyInputElement(user_letter)

    # aggiungo la lettera alla lista delle lettere usate
    if letter not in already_guessed:
        # https://www.journaldev.com/33182/python-add-to-list
        already_guessed.extend([letter])

    # controllo se il gioco deve finire
    checkEndGame()

    # concatenazione delle singole lettere presenti nell'array already_guessed, separandole con uno spazio
    # https://stackoverflow.com/questions/12453580/how-do-i-concatenate-items-in-a-list-to-a-single-string
    lettere_usate = " ".join(already_guessed)
    custom_utils.writeToHtmlElement(used_letters_html_container, 'Lettere usate: <span>%s</span>' % (lettere_usate))

def updateDisplayString(letter, display):
    
    # Metodo con la libreria esterna re (regex)
    # indexes = [m.start() for m in re.finditer(letter, word)]

    # for i in indexes:

    #     temp = list(display)
    #     temp[i] = letter
    #     display = "".join(temp)

    # Metodo con for ed enumerate per ciclare la stringa
    # https://realpython.com/python-enumerate/
    for index, currentLetter in enumerate(word):

        if currentLetter == letter:
            temp = list(display)
            temp[index] = letter
            display = "".join(temp)

    return display

def checkEndGame():

    if count == 5:

        custom_utils.writeToHtmlElement(result_html_container, "Hai perso!!!")
        custom_utils.writeToHtmlElement(solution_html_container, "La parola da indovinare era: <span>%s</span>" % (word))
        
        custom_utils.disableInputElement(user_letter)
        custom_utils.removeOnClickEventFromHtmlElement(add_letter_btn)

    elif display.lower() == word.lower():

        custom_utils.writeToHtmlElement(result_html_container, "Hai VINTO!!!")
        custom_utils.writeToHtmlElement(solution_html_container, "<span>GIOCA DI NUOVO</span>")

        custom_utils.disableInputElement(user_letter)
        custom_utils.removeOnClickEventFromHtmlElement(add_letter_btn)

def send_letter_event(event):

    custom_utils.writeToConsole(event)

    if custom_utils.checkIfEventIsEnterKey(event):

        game(event)


custom_utils.addKeyupEventToHtmlElement(user_letter, send_letter_event)
custom_utils.addOnClickEventToHtmlElement(add_letter_btn, game)

main()