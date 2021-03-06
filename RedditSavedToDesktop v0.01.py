#! python3
#RedditSavedToDesktop.py    porta i thread salvati sul pc
#PRAW VECCHIO DA AGGIORNARE v3.0
import praw, pprint, os, shelve, docx, datetime
   
def main():	
    '''DIAMO IL VIA ALLE DANZE: Definizione dell'user Agent'''
#L'user agent va definito sempre prima di cominciare, e nel modo più descrittivo possibile
    user_agent = 'SavedReddit to TextFile 0.1 by u/jackn3'  
	
    r = praw.Reddit(user_agent=user_agent) 
    username = input('Utente: ')
	
    #Crea la Cartella per l'utente specificato e prende la Password
    #LA CARTELLA LA DEVE SCEGLIERE L'UTENTE CAZZO!
    if not os.path.exists(os.path.join(os.sys.path[0], 'RedditSaved', username)):
        configFile = shelve.open(os.path.join(configurazione(username), 'config'))
        configFile['utente'] = username
        configFile['password'] = input('Qual è la password di: %s\n' % username)
    else:
        configFile = shelve.open(os.path.join(configurazione(username), 'config'))

    #Login su Reddit.com
    user = r.login(login(0, configFile), login(1, configFile), disable_warning=True)
    configFile.close()

    print('L utente %s è un gold? ' %username + str(r.get_redditor(username).is_gold) )
    
    #if not os.path.exists(os.path.join('E:\\Clouding\\Dropbox\\Python\\WPrograms', 'RedditSaved', 'subreddit.py')):
#os.sys.path[0] restituisce il percorso in cui viene lanciato Questo script!
    if not os.path.exists(os.path.join(os.sys.path[0], 'RedditSaved', username, 'subreddit.py')):
    	dizsub = subSalvati(username, r)
    else:
        print('Abbiamo già la lista dei subreddit [vedere come poter fare per aggiornarla]')


#Ma perchè creare un modulo e non un normale file? Oppure creare una semplice lista? SEI SCEMO?

#bisogna spostare il file subreddit.py, almeno momentaneamente, nella stessa cartella da cui si lancia lo script per far funzionare 
#l'import statement!
    print(dizsub)
    

    if r.get_redditor(username).is_gold:
        import subreddit
        print(os.getcwd())
        print(len(subreddit.listone_sub))
        print(subreddit.listone_sub)
        u_gold(r, username)
    else:
        u_no(r, username, dizsub)

	
def configurazione(username):
    '''Crea la cartella per l'username che conterrà tutti i file config e i word'''
#la cartella andrebbe chiesta all'utente piuttosto che fatta così a capocchia'''
    cartella = os.path.join(os.sys.path[0], 'RedditSaved', username)
#CHECK: se la cartella già esiste: exist_ok=True impedisce che il programma crashi per un errore
    os.makedirs(cartella, exist_ok=True)
    os.makedirs(os.path.join(cartella, 'Commenti'), exist_ok=True)
    os.makedirs(os.path.join(cartella, 'Threads'), exist_ok=True)
    os.chdir(cartella)
    return cartella

def login(x, configFile):
    '''Usa i dati nei file shelve per effettuare il login'''
    dati = [configFile['utente'], configFile['password']]
    return dati[x]        
    

def subSalvati(username, r):
    '''crea il modulo subreddit.py che verrà importato successivamente'''
    fileLista = open(os.path.join(os.sys.path[0], 'RedditSaved', username, 'subreddit.py'), 'w')
#Ma perchè creare un modulo e non un normale file? Oppure creare una semplice lista? SEI SCEMO?
 
 

#trova tutti i thread salvati su reddit dall'utente che ha effettuato il login [vale solo per gli utenti GILDED]
    saves = r.user.get_saved(sort="new", time='all', limit=None) 
    #listasub = []
    dizsub = {}
    x = 1

#questo loop è stato un dito in culo: cicla tra gli elementi salvati e prende il loro subreddit e lo schiaffa nella lista:
#listasub creata poco fa, se il subreddit è già stato inserito, viene saltata.
    for elem in saves:
	    subr = str(elem.subreddit)
	    if subr in dizsub:
		    dizsub[subr].append([type(elem), elem]) #elem.title, elem.permalink,  ]
	    else:
		    dizsub[subr] = []        
		#listasub.append(str(elem.subreddit))
	    print('%s Aggiungo alla lista: r/' % x + str(elem.subreddit))
	    x += 1
    
#la lista creata viene copiata in un file con .pformat() che così crea un MODULO da poter importare ##MA PERCHE'??
    
    #fileLista.write('listone_sub =' + pprint.pformat(listasub) + '\n')
    #fileLista.close()
    
    print('Fatto')
    return dizsub

#Bisognerebbe creare un file unico per subreddit in cui mettere il thread, se ci sono anche commenti salvati nel thread
#metterli sotto!

def u_gold(r, username):	#Crea il tutto per gli utenti con Reddit Gold
	for x in range(len(subreddit.listone_sub)):
		s = r.user.get_saved(sort="new", time='all', limit=None, params={'sr': subreddit.listone_sub[x]})
		c = 1
		t = 1
		d = docx.Document()
		for link in s:
			if type(link) == praw.objects.Comment:
				print('%s. Commento in: ' %c, link.subreddit)
				d.add_paragraph(str(link.submission)).style = 'Title'
				d.add_paragraph(link.permalink).style = 'caption'
				d.add_paragraph('Pubblicato il: (aaaa/mm/dd)' + str(datetime.date.fromtimestamp(link.created)))
				body = d.add_paragraph(link.body).style = 'Body Text 3' #----> QUELLO CHE c'è scritto
				d.add_paragraph('Autore: ' + str(link.author))
				d.add_page_break()
				d.save(os.path.join(os.sys.path[0], 'RedditSaved', username, 'Commenti', 'CC%s.docx' %str(link.subreddit)))
				c += 1
			else:
				print('%s. Thread in: ' %t, link.subreddit)
				d.add_paragraph(link.title).style = 'Title'
				d.add_paragraph(link.short_link).style = 'caption' #---> link del post su reddit
				d.add_paragraph(link.url).style = 'caption' #----> link del post a cui reddit si riferisce (es. imgur.com)
				#d.add_paragraph(link.short_link).style = 'caption' #--->boh
				d.add_paragraph('Pubblicato il: (aaaa/mm/dd)' + str(datetime.date.fromtimestamp(link.created)))
				d.add_paragraph(link.selftext).style = 'Body Text 3'            
				d.add_paragraph('Autore: ' + str(link.author))
				d.add_page_break()
				d.save(os.path.join(os.sys.path[0], 'RedditSaved', username, 'Threads', 'TT%s.docx' %str(link.subreddit)))
				t+=1

	
#Va migliorato molto, crea tantissimi file inutili, perchè non divisi per subreddit! tutti uguali tra di loro!	
def u_no(r, username, dizsub):	#Crea il tutto per gli utenti senza Reddit Gold
	
	#dizsub = {subreddit : [[link, tipo], [link, tipo]], subreddit : [[link, tipo], [link, tipo]]}
	
	#cicla per ogni chiave del dizionario, che corrispondono alle singole subreddit.
	for sub in dizsub:	
		#s = r.user.get_saved(sort="new", time='all', limit=None)#, params={'sr': subreddit.listone_sub[x]})
		o = 0
		d = docx.Document()
		for num_lista in range(len(dizsub[sub])):
			o += 1 
			link = dizsub[sub][num_lista]
			#if dizsub[sub][num_lista][0] == praw.objects.Submission:
			if link[0] == praw.objects.Submission:	
				print('%s. Thread in: ' %o, sub)	
				d.add_paragraph(link[1].title).style = 'Title'
				d.add_paragraph('Pubblicato in: /r/' + str(sub)).style = 'caption'
				d.add_paragraph('Il giorno: (aaaa/mm/dd) ' + str(datetime.date.fromtimestamp(link[1].created))).style = 'caption'
				d.add_paragraph('Autore: ' + str(link[1].author))
				d.add_paragraph(link[1].short_link).style = 'caption' #---> link del post su reddit
				d.add_paragraph(link[1].url).style = 'caption' #----> link del post a cui reddit si riferisce (es. imgur.com)
				d.add_paragraph(link[1].selftext).style = 'Body Text 3'            
				d.add_page_break()
				d.save(os.path.join(os.sys.path[0], 'RedditSaved', username, 'Threads', 'TT%s.docx' %str(sub)))
				
				
			else:
				print('%s. Commento in: ' %o, sub)
				d.add_paragraph(str(link[1].submission)).style = 'Title'
				d.add_paragraph('Pubblicato in: ' + str(sub)).style = 'caption'
				d.add_paragraph(link[1].permalink).style = 'caption'
				d.add_paragraph('Pubblicato il: (aaaa/mm/dd)' + str(datetime.date.fromtimestamp(link[1].created)))
				body = d.add_paragraph(link[1].body).style = 'Body Text 3' #----> QUELLO CHE c'è scritto
				d.add_paragraph('Autore: ' + str(link[1].author))
				d.add_page_break()
				d.save(os.path.join(os.sys.path[0], 'RedditSaved', username, 'Commenti', 'CC%s.docx' %str(sub)))		
			
						

if __name__ == "__main__":
	main()
