import requests
import tldextract
from jellyfish import levenshtein_distance


def requisicao_da_url(url):
	try:
		response = requests.get(url)
		url_final = str(response.url)
	except:
		print("Erro ao realizar request!")
		url_final = None

	return url_final


def extract_data(url):
    dominio = tldextract.extract(url).domain
    subdominio = tldextract.extract(url).subdomain
    tld = tldextract.extract(url).suffix

    return subdominio, dominio, tld


def check_url_domain(url):
	sub, dom, tld = extract_data(url)
	if not sub:
		sub = ''

	domain = f'https://{dom}.{tld}'
	return domain, sub


def url_strings_equal(url1, url2):
	value = 1 - levenshtein_distance(url2, url1) / max(len(url1), len(url2))
	return value


def analise_redirect(url_inicial, url_final):
	if url_inicial == url_final:
		print("Não houve redirecionamento de URL.")
	else:
		# Buscando dominios e subdominios
		inicial_domain, inicial_subdomain = check_url_domain(url_inicial)
		final_domain, final_subdomain = check_url_domain(url_final)
		# Buscando igualdade entre strings
		url_inicial_url_final = url_strings_equal(url_inicial, url_final)
		dom_inicial_url_final = url_strings_equal(inicial_domain, url_final)
		dom_inicial_dom_final = url_strings_equal(inicial_domain, final_domain)

		print(f"Diferença entre URL inicial e URL final: {url_inicial_url_final}")
		print(f"Diferença entre dominio inicial e URL final: {dom_inicial_url_final}")
		print(f"Diferença entre dominio inicial e dominio final: {dom_inicial_dom_final}")

		if url_inicial_url_final < 0.7:
			if dom_inicial_url_final > 0.7:
				print("URL redirecionou para Homepage.")
			elif dom_inicial_dom_final < 0.7:
				print("URL redirecionou para outro site.")
			elif dom_inicial_dom_final > 0.7:
				print("URL redirecionou para o mesmo site mas houve uma mudança não identificada.")
		elif final_domain != inicial_domain:
			print("URL redirecionou para outro site.")
		elif inicial_subdomain != final_subdomain:
			print("Subdominio da URL mudou")
		else:
			if url_final.startswith('https:') and str(url_inicial).startswith('http:'):
				print("Houve mudança de http ou https na URL")
			elif url_final.startswith('http:') and str(url_inicial).startswith('https:'):
				print("Houve mudança de http ou https na URL")
			else:
				print("URL mudou mas de uma maneira que o script não conseguiu identificar, analisar!")


def main(url_inicial):
	url_final = requisicao_da_url(url_inicial)

	if url_final:
		print(f"Url inicial: {url_inicial}\nURL final: {url_final}")
		analise_redirect(url_inicial, url_final)
