import csv

class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo_base):
        self.codice = codice
        self.superficie = float(superficie)
        self.padiglione = int(padiglione)
        self.prezzo_base = float(prezzo_base)
        self.espositore = None

    def get_prezzo(self):
        return self.prezzo_base

    def __lt__(self, other):
        return self.get_prezzo() < other.get_prezzo()

    def __eq__(self, other):
        return isinstance(other, Stand) and self.codice == other.codice

    def __str__(self):
        stato = "Disponibile" if self.espositore is None else f"Assegnato a {self.espositore.codice}"
        return f"{self.codice}: Standard | {int(self.superficie)} mq - Padiglione {self.padiglione} - Prezzo {self.get_prezzo():.2f}€ - {stato}"

class StandPreseExtra(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, prese):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.prese = int(prese)

    def get_prezzo(self):
        return self.prezzo_base * (1 + 0.07 * self.prese)

    def __str__(self):
        stato = "Disponibile" if self.espositore is None else f"Assegnato a {self.espositore.codice}"
        return f"{self.codice}: Prese Extra | {int(self.superficie)} mq - Padiglione {self.padiglione} - Prezzo {self.get_prezzo():.2f}€ - Prese aggiuntive: {self.prese} - {stato}"

class StandPremium(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, posizione):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.posizione = posizione

    def get_prezzo(self):
        return self.prezzo_base * 1.30

    def __str__(self):
        stato = "Disponibile" if self.espositore is None else f"Assegnato a {self.espositore.codice}"
        return f"{self.codice}: Premium ({self.posizione}) | {int(self.superficie)} mq - Padiglione {self.padiglione} - Prezzo {self.get_prezzo():.2f}€ - {stato}"

class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self.stand = None

    def __eq__(self, other7):
        return isinstance(other, Espositore) and self.codice == other.codice

    def __str__(self):
        if self.stand:
            return f"{self.codice} - {self.nome} {self.cognome} (Stand: {self.stand.codice})"
        return f"{self.codice} - {self.nome} {self.cognome} (Nessuno stand)"
class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        # TODO
        self._nome = nome
        self.stands = {}
        self.espositori = {}

    """Aggiungere setter e getter se necessari"""
    # TODO
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nuovo_nome):
        self._nome = nuovo_nome

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        # TODO
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for riga in reader:
                if not riga:
                    continue
                tipo_codice = riga[0].strip()
                if tipo_codice.startswith("ST"):
                    codice = tipo_codice
                    sup = riga[1].strip()
                    pad = riga[2].strip()
                    prezzo = riga[3].strip()
                    if len(riga) == 4 or not riga[4].strip():
                        self.stands[codice] = Stand(codice, sup, pad, prezzo)
                    elif riga[4].strip().isdigit():
                        self.stands[codice] = StandPreseExtra(codice, sup, pad, prezzo, riga[4].strip())
                    else:
                        self.stands[codice] = StandPremium(codice, sup, pad, prezzo, riga[4].strip())
                elif tipo_codice.startswith("ES"):
                    self.espositori[tipo_codice] = Espositore(tipo_codice, riga[1].strip(), riga[2].strip())

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        # TODO
        if codice_stand not in self.stands:
            raise Exception("Stand non trovato.")
        if codice_espositore not in self.espositori:
            raise Exception("Espositore non trovato.")

        stand = self.stands[codice_stand]
        espositore = self.espositori[codice_espositore]

        if stand.espositore is not None:
            raise Exception("Stand non disponibile.")
        if espositore.stand is not None:
            raise Exception("Espositore ha già uno stand.")

        stand.espositore = espositore
        espositore.stand = stand

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        # TODO
        for esp in self.espositori.values():
            print(esp)

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        # TODO
        return sorted(self.stands.values())
