import requests,re,sys,click,os
from bs4 import BeautifulSoup as Bs

info={}

def search(query):
	c=1
	req=requests.get(f'https://an1.com/tags/MOD/?story={query}&do=search&subaction=search')
	bs=Bs(req.text,'html.parser')
	tit=bs.find_all('div',{'class':'title'})
	info['title']=[]
	for x in tit:
		try:
			info['title'].append((f'{c}. {x.text}',x.find('a').get('href')))
			c+=1
		except: sys.exit('[!] Tidak dapat ditemukan')
#		print(x.find('a').get('href'))
#	print(info)
	grep()

def grep():
	cc=1
	info['dl']=[]
	for i in info['title']:
		print(i[0])
	pil=int(input('pilih_> '))
	get=info['title'][pil-1][1]
	print()
	req2=requests.get(get)
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
#	print(info)

def download(url,judul):
	print("#",re.findall(r'. (.*)',judul)[0])
	req3=requests.get('https://an1.com'+url)
#	print(req3.text)
	rg=re.findall(r'href=(.*)><input',req3.text)
	print(f'{rg}\n')
	if "https://files.an1.net" in rg[0]:
		link=rg[0]
	elif '.apk' in rg[0] or '.zip' in rg[0]:
		link=rg[0]
	elif "www.4sync.com" in rg[0]:
		req4=requests.get(rg[0])
		bs3=Bs(req4.text,'html.parser')
		link=bs3.find('input',{'class':'jsDLink'})['value']
	else:
		bps=requests.get(rg[0]).url
		nya=input(f"[Maaf] link download {re.findall(r'https://(.*)/',bps)} saat ini belum kami support\n[?] Apakah anda mau membuka link tersebut (y/n) ")
		if nya.lower() == 'y':
			click.launch(rg[0])
		return True

	#Downloading
	file=re.findall(r'Download (.*)  ',judul)[0]
	with open(f"result/{file}","wb") as save:
		response=requests.get(link,stream=True)
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
				ges=int(100*dlw/total_length)
				dlw+=len(data)
				save.write(data)
				done=int(30*dlw/total_length)
				print(end=f"\r\033[97m[\033[92m{'>'*done}\033[91m{'='*(30-done)}\033[97m] \033[96m{ges+1}% ",flush=True)
	print("[OK] file saved in result")

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
