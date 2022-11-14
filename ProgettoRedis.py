import redis
from time import sleep


class RedisDB():
    def __init__(self):
        try:
            # la connessione funziona :) :)
            self.r = redis.Redis(host='127.0.0.1', port=6379, db=0, charset='utf-8', decode_responses=True)
        except Exception as e:
            print('Errore di connessione al server Redis ...')
            print(e)

    def _login(self):
        try:
            print('Per utilizzare il programma è necessario effettuare il Login!')
            while True:
                nome = input('Inserisci il tuo nome >>: ')
                if nome == '':
                    print('Errore, il nome inserito non è valido')
                else:
                    break
            while True:
                cognome = input('Inserisci il tuo cognome >>: ')
                if cognome == '':
                    print('Errore, il cognome inserito non è valido')
                else:
                    break
            self.user = nome.lower() + '_' + cognome.lower()
        except Exception as exc:
            print(exc)

    def _nuovaproposta(self):
        len_proposta = self.r.llen('PROPOSTE')
        key_proposta = 'p' + str(len_proposta)
        self.r.rpush('PROPOSTE', key_proposta)
        print('Inserisci x per uscire e tornare al Menu')
        while True:
            proposta = input('Inserisci la tua proposta >>: ')
            if proposta == '':
                print('Proposta inserita non valida')
            else:
                break
        if proposta.lower() != 'x':
            proponenti = input('Inserisci i proponenti >>: ')
            self.r.hset(key_proposta, 'Titolo', proposta.lower())
            self.r.hset(key_proposta, 'Proponenti', proponenti.lower())
            print('NUOVA PROPOSTA INSERITA')
        sleep(2)

    def _votoproposta(self):
        lista_Keyproposte = self.r.lrange('PROPOSTE', 0, -1)
        print('LISTA DELLE PROPOSTE')
        voto_utente = self.r.smembers('voti:'+self.user)
        keyproposte_valide = []
        if len(voto_utente) == 0:
            for e in lista_Keyproposte:
                titolo_proposta = self.r.hget(e, 'Titolo')
                keyproposte_valide.append(e)
                print(f'{e} --> {titolo_proposta}')
        else:
            for ep in lista_Keyproposte:
                if ep not in voto_utente:
                    titolo_proposta = self.r.hget(ep, 'Titolo')
                    keyproposte_valide.append(ep)
                    print(f'{ep} --> {titolo_proposta}')
        print('x  --> Esci senza votare e torna al Menu')
        while True:
            key_proposta = input('Inserisci il codice della proposta che vuoi votare >>: ')
            if key_proposta.lower() == 'x':
                break
            if key_proposta.lower() in keyproposte_valide:
                self.r.zincrby('CLASSIFICA', 1, key_proposta)
                setKey_utente = 'voti:' + self.user
                self.r.sadd(setKey_utente, key_proposta)
                print('PROPOSTA VOTATA CORRETTAMENTE ')
                break
            else:
                print('Errore,il codice inserito non è valido ... \n RIPROVA!')
        sleep(2)

    def _proposteconvoti(self):
        print('LISTA DELLE PROPOSTE IN ORDINE DI VOTO')
        propostewithscore = self.r.zrevrange('CLASSIFICA',0,-1,withscores=True)
        if len(propostewithscore) == 0:
            print('Nessuna proposta registrata...')
        else:
            for elem in propostewithscore:
                titolo = self.r.hget(elem[0], 'Titolo')
                print(f'{titolo} --> {int(elem[1])} Voti')
        sleep(3)

    def _listaproponenti(self):
        print('LISTA DELLE PROPOSTE CON I VARI PROPONENTI \n')
        proposte = self.r.lrange('PROPOSTE',0,-1)
        if len(proposte) == 0:
            print('Nessuna proposta registrata...')
        else:
            for elem in proposte:
                titolo = self.r.hget(elem,'Titolo')
                proponents = self.r.hget(elem,'Proponenti')
                print(f'{titolo} \n        proposto da : {proponents} \n ')
        sleep(3)

    def Menu(self):
        self._login()
        sleep(1)
        print(
            '------------------------------------------------------------------------------------------------')
        print()
        print(
            f'                                           BENVENUTO :) {self.user}                       ')
        print()
        print(
            '------------------------------------------------------------------------------------------------')
        sleep(2)
        while True:
            print()
            try:
                comando = int(input(
                    (f'''
                            ________________________________________________________________________________
                            |                                      MENU                                    |
                            |______________________________________________________________________________|  
                            |  0  |                    Terminare il programma                              |
                            |     |                                                                        |
                            |  1  |                    Fare una proposta                                   |
                            |     |                                                                        |
                            |  2  |                    Votare una proposta                                 |
                            |     |                                                                        |
                            |  3  |                    Lista delle proposte in ordine di voto              |
                            |     |                                                                        |
                            |  4  |                    Lista dei proponenti per ogni proposta              |
                            |_____|________________________________________________________________________|
                            
                            
                            Utente corrente   -->   {self.user}
                            
                            
                            Inserire il numero corrispondente all' operazione desiderata >>: ''')))
                print()
                print()
                print()
                if comando == 0:
                    print(
                        '------------------------------------------------------------------------------------------------')
                    print()
                    print(
                        f'                                           ARRIVEDERCI                       ')
                    print()
                    print(
                        '------------------------------------------------------------------------------------------------')
                    break
                elif comando == 1:
                    self._nuovaproposta()
                elif comando == 2:
                    self._votoproposta()
                elif comando == 3:
                    self._proposteconvoti()
                elif comando == 4:
                    self._listaproponenti()
                else:
                    print('ERRORE, il numero inserito non corrisponde a nessuna operazione ...')
                    print('RIPROVA!')
                    sleep(3)
            except Exception as eccezione:
                print(eccezione)

    def __str__(self):
        return 'Programma per gestire le votazioni degli studenti'


if __name__ == '__main__':
    redis = RedisDB()
    redis.Menu()
