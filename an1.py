import requests,re,sys,click,os,time
from bs4 import BeautifulSoup as Bs

ses=requests.Session()
info={
	'title':[],
	'dl':[],
}

def search(query):
	c=1
	req=ses.get(f'https://an1.com/tags/MOD/?story={query}&do=search&subaction=search')
	bs=Bs(req.text,'html.parser')
	tit=bs.find_all('div',{'class':'title'})
	for x in tit:
		try:
			info['title'].append((f'{c}. {x.text}',x.find('a').get('href')))
			c+=1
		except: sys.exit('[!] Tidak dapat ditemukan')
	grep()

def grep():
	cc=1
	for i in info['title']:
		print(i[0])
	pil=int(input('pilih_> '))
	if pil <= 0:
		print('index out of range')
		return True
	get=info['title'][pil-1][1]
	print()
	req2=ses.get(get)
	bs2=Bs(req2.text,'html.parser')
	prd=bs2.find_all('div',{'class':'get-product-holder'})
	for y in prd:
		info['dl'].append((f'{cc}. {y.text.strip()}',y.find('a')['href']))
		cc+=1
	print()
	if len(info['dl']) > 1:
		for j in info['dl']:
			print(j[0])
		print('\nA: Download semua')
		lih=input('pilih_> ')
		print()
		try:
			if int(lih):
				download(info['dl'][int(lih)-1][1], info['dl'][int(lih)-1][0])
		except:
			if lih.upper() == 'A':
				for l in info['dl']:
					download(l[1],l[0])
	else:
		download(info['dl'][0][1],info['dl'][0][0])

def download(url,judul):
	print("#",re.findall(r'. (.*)',judul)[0])
	req3=ses.get('https://an1.com'+url)
	rg=re.findall(r'href=(.*)><input',req3.text)
	
	if "bit.ly" in rg[0]:
		rq=ses.get(rg[0]).url
		rg=rq.split()
	
	if "files.an1.net" in rg[0]:
		link=rg[0]
	elif '.apk' in rg[0] or '.zip' in rg[0]:
		link=rg[0]
	elif "www.4sync.com" in rg[0]:
		req4=ses.get(rg[0])
		bs3=Bs(req4.text,'html.parser')
		link=bs3.find('input',{'class':'jsDLink'})['value']
	elif "racaty.com" in rg[0]:
		reqs=ses.get(rg[0])
		bss=Bs(reqs.text,'html.parser')
		op=bss.find('input',{'name':'op'})['value']
		id=bss.find('input',{'name':'id'})['value']
		
		rep=ses.post(rg[0],data={'op':op,'id':id})
		bss2=Bs(rep.text,'html.parser')
		link=bss2.find('div',{'id':'DIV_1'}).find('a')['href']
	else:
		bps=ses.get(rg[0]).url
		nya=input(f"[Maaf] link download {re.findall(r'https://(.*)/',bps)} saat ini belum kami support\n[?] Apakah anda ingin membuka link tersebut (y/n) ")
		if nya.lower() == 'y':
			click.launch(rg[0])
		return True
#	print(info)
	print(f"{rg}\n")

	#Downloading
	file=re.findall(r'Download (.*)  ',judul)[0]
	with open(f'result/{file.replace("/",",")}','wb') as save:
		count=1
		response=requests.get(link,stream=True)
		start=time.time()
		total_length=response.headers.get('content-length')
		if total_length is None:
			print("\n[Warn] Download GAGAL")
			tan=input("[?] anda ingin melanjutkannya ke website android-1.com (y/n) ")
			if tan.lower() == 'y':
				click.launch('https://an1.com'+url)
			else:
				sys.exit("okay bye bye:*")
		else:
			dlw=0
			total_length=int(total_length)
			for data in response.iter_content(chunk_size=4096):
				durasi=time.time() - start
				if durasi == 0:
					durasi=0.1
				
				ges=int(100*dlw/total_length)
				dsiz=int(count*4096)
				sped=int((dsiz/1024) / durasi)
				dlw+=len(data)
				save.write(data)
				done=int(15*dlw/total_length)
				print(end=f"\r\033[97m[\033[92m{'>'*done}\033[91m{'='*(15-done)}\033[97m] {ges+1}%, {round(dsiz/(1024*1024), 2)} MB, {sped} KB/s  ",flush=True)
				count+=1
	print("\n[OK] file saved in result")

if __name__ == "__main__":
	os.system('clear')
	print("""
	[ Android-1.com MOD Downloader ]
		| by: Noobie |
""")
	try:
		os.mkdir('result')
	except: pass

	try:
		que=input("query search: ")
		print()
		search(que)
	except Exception as Err:
		print(Err)
