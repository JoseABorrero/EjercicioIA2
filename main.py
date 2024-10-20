
import ollama
import requests

MODELO_IA="gemma2"

def obtener_info_pokemon(nombre):
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}"
    respuesta = requests.get(url)
    
    if respuesta.status_code == 200:
        return respuesta.json()
    else:
        print(f"No se encontró información para {nombre}.")
        return None

def generar_comparacion(pokemon1_info, pokemon2_info):
    prompt = f'Compara los siguientes Pokémon: ' \
             f'1. {pokemon1_info['name']}: ' \
             f' Altura: {pokemon1_info['height']} decímetros ' \
             f' Peso: {pokemon1_info['weight']} hectogramos ' \
             f' Tipos: {[tipo['type']['name'] for tipo in pokemon1_info['types']]}  ' \
             f'2. {pokemon2_info['name']}: ' \
             f' Altura: {pokemon2_info['height']} decímetros ' \
             f' Peso: {pokemon2_info['weight']} hectogramos ' \
             f' Tipos: {[tipo['type']['name'] for tipo in pokemon2_info['types']]}  '          
    
    return prompt

def usar_ollama_para_comparar(prompt):
     
    response = ollama.chat(model=MODELO_IA, messages=[
  {
    'role': 'user',
    'content': prompt,
  },
])
    return response['message']['content']

def usar_ollama_para_buscar_contrario(prompt):
     
    response = ollama.chat(model=MODELO_IA, messages=[
  {
    'role': 'system',
    'content': "Eres un entrenador pokemon,  busca el pokemon que sea fuerte contra hypno",
  },
  {
    'role': 'user',
    'content': prompt,
  },
])
    return response['message']['content']
    
def comparar_pokemons(pokemon1, pokemon2):
    info1 = obtener_info_pokemon(pokemon1)
    info2 = obtener_info_pokemon(pokemon2)

    if info1 and info2:
        prompt = generar_comparacion(info1, info2)
        print ("Prompt enviado a ollama para comparar sin contexto:")
        print (prompt)
        comparacion = usar_ollama_para_comparar(prompt)
        print(comparacion)
        print("Contexto: Eres un entrenador pokemon,  busca el pokemon que sea fuerte contra hypno")
        mejorcontrincante = usar_ollama_para_buscar_contrario(prompt)
        print(mejorcontrincante)



def main():
    print("La aplicación pide 2 pokemons, primero los compara físicamente y luego te dice cual sería mejor en una lucha contra hypno")
    pokemon1 = input("Introduce el nombre del primer Pokémon: (Si no se escribe se tomará pikachu) ")
    if pokemon1 == "":
        pokemon1 = "pikachu"

    pokemon2 = input("Introduce el nombre del segundo Pokémon: (Si no se escribe se tomará balbasaur) ")
    if pokemon2 == "":
        pokemon2 = "bulbasaur"
    comparar_pokemons(pokemon1, pokemon2)

if __name__ == "__main__":
    main()
