import numpy as np
import math
import matplotlib.pyplot as plt

def calculate_entropy(file_path, max_n=5):
    # Odpre datoteko in prebere njene bajte
    with open(file_path, 'rb') as file:
        b = np.frombuffer(file.read(), dtype=np.uint8)
    
    entropies = {}
    # Za vsako dolžino n od 1 do max_n izračuna entropijo
    for n in range(1, max_n + 1):
        n_counts = {}
        # Šteje pojavljanja vsakega n-zaporedja bajtov
        for i in range(len(b) - n + 1):
            n_value = bytes(b[i:i+n])
            if n_value in n_counts:
                n_counts[n_value] += 1
            else:
                n_counts[n_value] = 1
        
        # Izračuna skupno število n-zaporedij
        total_n_values = sum(n_counts.values())
        # Izračuna verjetnosti za vsako n-zaporedje
        probabilities = {n_value: count / total_n_values for n_value, count in n_counts.items()}
        # Izračuna entropijo kot povprečje entropije n-zaporedij
        entropy = -sum(prob * math.log2(prob) for prob in probabilities.values()) / n
        entropies[n] = entropy
    return entropies

def plot_entropies(files):
    n_groups = len(files)
    max_n = 5
    # Izračuna entropije za podane datoteke
    entropy_values = [calculate_entropy(file) for file in files]
    
    # Izpiše vrednosti entropije za vsako datoteko
    for i, file in enumerate(files):
        print(f'Vrednosti entropije za {file}:')
        for n in range(1, max_n + 1):
            print(f'  n={n}: {entropy_values[i][n]:.4f}')
        print()

    # Nastavitve za prikaz grafa
    fig, ax = plt.subplots(figsize=(12, 8))
    
    index = np.arange(n_groups)
    bar_width = 0.15
    opacity = 0.8
    
    # Doda stolpce za vsako vrednost n na graf
    for n in range(1, max_n + 1):
        means = [entropies[n] for entropies in entropy_values]
        plt.bar(index + bar_width * (n-1), means, bar_width, alpha=opacity, label=f'n={n}')
    
    plt.xlabel('Datoteke')
    plt.ylabel('Entropija / n')
    plt.title('Entropija v različnih datotekah')
    plt.xticks(index + bar_width * 1.5, [f.split('/')[-1] for f in files], rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.show()

files = ['besedilo.txt', 'besedilo.zip', 'sifrirano_besedilo.zip', 'slika.bmp', 'slika.png', 'slika.jpg', 'posnetek.wav', 'posnetek.flac', 'posnetek.mp3']
plot_entropies(files)
