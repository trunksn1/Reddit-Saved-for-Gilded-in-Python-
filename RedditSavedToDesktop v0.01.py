#! python3
#RedditSavedToDesktop.py    porta i thread salvati sul pc

import praw, pprint, os, shelve, docx, datetime

    
def configurazione(username):
    '''Crea la cartella per l'username che conterrà tutti i file config e i word'''
    cartella = os.path.join('E:\\Clouding\\Dropbox\\Python\\WPrograms', 'RedditSaved', username)
    os.makedirs(cartella, exist_ok=True)	#se la cartella già esiste exist_ok=True impedisce che il programma crashi per un errore
    os.makedirs(os.path.join(cartella, 'Commenti'), exist_ok=True)
    os.makedirs(os.path.join(cartella, 'Threads'), exist_ok=True)
    os.chdir(cartella)
    return cartella

def login(x):
    '''Usa i dati nei file shelve per effettuare il login'''
    dati = [configFile['utente'], configFile['password']]
    return dati[x]        
    
def subSalvati(username):
    '''crea il modulo subreddit.py che verrà importato successivamente'''
    #fileLista = open(os.path.join('E:\\Clouding\\Dropbox\\Python\\WPrograms', 'RedditSaved', 'subreddit.py'), 'a')  #questo file viene sovrascritto da ogni utente, va cancellato sennò fa casino
    fileLista = open(os.path.join('E:\\Clouding\\Dropbox\\Python\\WPrograms', 'RedditSaved', username, 'subreddit.py'), 'w')  #questo file viene sovrascritto da ogni utente, va cancellato sennò fa casino
    subr = r.user.get_saved(sort="new", time='all', limit=None) #trova tutti i thread salvati su reddit dall'utente che ha effettuato il login [vale solo per gli utenti GILDED
    listasub = []
    x = 1
#questo loop è stato un dito in culo: cicla tra gli elementi salvati e prende la loro subreddit di origine e la schiaffa nella lista: listasub creata poco fa, se la subreddit già è stata inserita viene saltata.
    for elem in subr:    
        while str(elem.subreddit) not in listasub:
            listasub.append(str(elem.subreddit)) 
            print('%s Aggiungo alla lista: r/' % x + str(elem.subreddit))
            x += 1
    fileLista.write('listone_sub =' + pprint.pformat(listasub) + '\n')    #la lista creata viene copiata in un file con .pformat() che così crea un MODULO da poter importare
    fileLista.close()
    print('Fatto')
    return fileLista

def u_gold():	#Crea il tutto per gli utenti con Reddit Gold
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
				d.save(os.path.join('E:\\Clouding\\Dropbox\\Python\\WPrograms', 'RedditSaved', username, 'Commenti', 'CC%s.docx' %str(link.subreddit)))
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
				d.save(os.path.join('E:\\Clouding\\Dropbox\\Python\\WPrograms', 'RedditSaved', username, 'Threads', 'TT%s.docx' %str(link.subreddit)))
				t+=1

	
	
def u_no():	#Crea il tutto per gli utenti senza Reddit Gold
	s = r.user.get_saved(sort="new", time='all', limit=None)#, params={'sr': subreddit.listone_sub[x]})
	o = 0
	d = docx.Document()
	for link in s:
		o += 1 
		if type(link) == praw.objects.Comment:
			print('%s. Commento in: ' %o, link.subreddit)
			d.add_paragraph(str(link.submission)).style = 'Title'
			d.add_paragraph('Pubblicato in: ' + str(link.subreddit)).style = 'caption'
			d.add_paragraph(link.permalink).style = 'caption'
			d.add_paragraph('Pubblicato il: (aaaa/mm/dd)' + str(datetime.date.fromtimestamp(link.created)))
			body = d.add_paragraph(link.body).style = 'Body Text 3' #----> QUELLO CHE c'è scritto
			d.add_paragraph('Autore: ' + str(link.author))
			d.add_page_break()
			d.save(os.path.join('E:\\Clouding\\Dropbox\\Python\\WPrograms', 'RedditSaved', username, 'Commenti', 'CC%s.docx' %str(link.subreddit)))		
		else:
			print('%s. Thread in: ' %o, link.subreddit)	
			d.add_paragraph(link.title).style = 'Title'
			d.add_paragraph('Pubblicato in: ' + str(link.subreddit)).style = 'caption'
			d.add_paragraph(link.short_link).style = 'caption' #---> link del post su reddit
			d.add_paragraph(link.url).style = 'caption' #----> link del post a cui reddit si riferisce (es. imgur.com)
			#d.add_paragraph(link.short_link).style = 'caption' #--->boh
			d.add_paragraph('Pubblicato il: (aaaa/mm/dd)' + str(datetime.date.fromtimestamp(link.created)))
			d.add_paragraph(link.selftext).style = 'Body Text 3'            
			d.add_paragraph('Autore: ' + str(link.author))
			d.add_page_break()
			d.save(os.path.join('E:\\Clouding\\Dropbox\\Python\\WPrograms', 'RedditSaved', username, 'Threads', 'TT%s.docx' %str(link.subreddit)))
						
	
	
	
#DIAMO IL VIA ALLE DANZE: Definizione dell'user Agent
user_agent = 'SavedReddit to TextFile 0.1 by u/jackn3'  #L'user agent va definito sempre prima di cominciare, e nel modo più descrittivo possibile
r = praw.Reddit(user_agent=user_agent) 
   
username = input('Utente: ')

#Crea la Cartella per l'utente specificato e prende la Password
if not os.path.exists(os.path.join('E:\\Clouding\\Dropbox\\Python\\WPrograms', 'RedditSaved', username)):
    configFile = shelve.open(os.path.join(configurazione(username), 'config'))
    configFile['utente'] = username
    configFile['password'] = input('Qual è la password di: %s\n' % username)
else:
    configFile = shelve.open(os.path.join(configurazione(username), 'config'))
    
    
#Login su Reddit.com
user = r.login(login(0), login(1), disable_warning=True)
configFile.close()

print('L utente %s è un gold? ' %username + str(r.get_redditor(username).is_gold) )

	
#if not os.path.exists(os.path.join('E:\\Clouding\\Dropbox\\Python\\WPrograms', 'RedditSaved', 'subreddit.py')):
if not os.path.exists(os.path.join('E:\\Clouding\\Dropbox\\Python\\WPrograms', 'RedditSaved', username, 'subreddit.py')):
    subSalvati(username)
else:
    print('Abbiamo già la lista dei subreddit [vedere come poter fare per aggiornarla]')



import subreddit


print(os.getcwd())
print(len(subreddit.listone_sub))
print(subreddit.listone_sub)

if r.get_redditor(username).is_gold:
	u_gold()
else:
	u_no()


#pprint.pprint(links)
