import urllib.request
import bs4
import ssl

# Context For urllib, needed for verification
context = ssl._create_unverified_context()




def requestcountry(country, datapoint):

	#make 'country' readable
	country = country.lower().replace(' ','-')

	#get webpage
	try:
		url = 'https://www.worldatlas.com/maps/'+country
		uopen = urllib.request.urlopen(url,context=context)
	except:
		print(country+" is not a viable input")
		return([' ', ' ',' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
	else:
		url = 'https://www.worldatlas.com/maps/'+country
		uopen = urllib.request.urlopen(url,context=context)	


	page = uopen
	html = page.read().decode("utf-8")
	soup = bs4.BeautifulSoup(html, "html.parser")

	out = str(soup)


	#removing unwanted characters
	out_safe = out.replace('\u200b','_')
	out_safe = out_safe.replace('\u0141','_')
	out_safe = out_safe.replace('\u017a','_')
	out_safe = out_safe.replace('\u0142','_')
	out_safe = out_safe.replace('\u0144','_')
	out_safe = out_safe.replace('\x9f','_')
	out_safe = out_safe.replace('\x83','_')

	out_split = out_safe.split("""</tr>
</table>
<p>This page was last updated on""",1)
	out_split=out_split[0]
	out_split=out_split.split("""<h2 class="anchor_point" id="keyFactsSection">Key Facts</h2>
<table class="data_merged_rows" id="ncore_info_table">
<tr>""",1)
	Table=out_split[1]
	print("""
	***************
	***************
	"""+Table+"""
	***************
	***************
	""")

	#Legal name of country
	Legalname = Table.split("""<th scope="row">Legal Name</th>
<td>""",1)[1].split("<",1)[0]
	#print(Legalname)

	#Capital city of country
	Capitalcity = Table.split("""scope="rowgroup">Capital City</th>
<td class="data_paragraph">""",1)[1].split("<",1)[0]
	#print (Capitalcity)

	#Totalarea of country
	Totalarea = float(Table.split("Total Area",1)[1].split("<td>",1)[1].split(" ",1)[0].replace(',',''))
	#print(Totalarea)

	#Land area of county
	Landarea = float(Table.split("""<th scope="row">Land Area</th>
<td>""",1)[1].split(" ",1)[0].replace(',',''))
	#print(Totalarea)

	#Water area of country, not taken from website to avoid N/A
	Waterarea = Totalarea-Landarea
	print(Waterarea)

	#Population of country
	Population = int(Table.split("""<th scope="row">Population</th>
<td>""",1)[1].split("<",1)[0].replace(',',''))
	#print(Population)

	#Currency of country
	Currency = Table.split("""<td><a href="/flags/""",1)[1].split("""#currency">""",1)[1].split("<",1)[0]
	#print(Currency)

	#GDP and GDPpercapita of country
	try: 
		GDP = Table.split("<td>$",1)[1].split('<',1)[0]
	except :
		GDP = (0-1.0)
		#print('no GDP value')
	else:
		if 'Trillion'in Table.split("<td>$",1)[1].split('<',1)[0]:
			GDP = 1000000000000*(float(Table.split("<td>$",1)[1].split('<',1)[0].split(" ",1)[0]))
		elif 'Billion'in Table.split("<td>$",1)[1].split('<',1)[0]:
			GDP = 1000000000*(float(Table.split("<td>$",1)[1].split('<',1)[0].split(" ",1)[0]))
		elif 'Million'in Table.split("<td>$",1)[1].split('<',1)[0]:
			GDP = 1000000*(float(Table.split("<td>$",1)[1].split('<',1)[0].split(" ",1)[0]))
		else:
			GDP = (0-1.0)
			#print('no GDP value')

	try: 
		GDPpercapita = Table.split("<td>$",1)[1].split('<',1)[0]
	except:
		GDPpercapita = (0-1.0)
		#print('no GDPpercapita value')
	else:
		GDPpercapita = float(Table.split("""GDP Per Capita</th>
<td>$""",1)[1].split('<',1)[0].replace(',',''))
	#print(GDP)
	#print(GDPpercapita)

	# configuring datapoint index
	data = [Legalname,Capitalcity,Totalarea,Landarea,Waterarea,Population,Currency,GDP,GDPpercapita]
	if datapoint >= len(data) or datapoint < 0:
		return data
	else:
		return data[datapoint]

