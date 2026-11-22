import os
import random

# Definir semente fixa 
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

OUTPUT_DIR = "dataset"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Tamanhos dos subconjuntos/ Vercoes
SIZES = [5000, 10000, 20000, 30000, 40000]
INTERSECTION_RATIO = 0.10  # 10% de intersecao entre as duas entidades

def format_size_label(size):
    return f"{size // 1000}k" if size % 1000 == 0 else str(size)

def generate_utente_id(prefix, number):
    """Formata um identificador de utente com 9 dígitos."""
    return f"{prefix}{number:09d}"

for size in SIZES:
    label = format_size_label(size)
    num_intersection = int(size * INTERSECTION_RATIO)
    num_exclusive = size - num_intersection

    # 1. Gerar elementos comuns
    common_elements = [
        generate_utente_id("SNS", i) for i in range(1, num_intersection + 1)
    ]

    # 2. Gerar elementos exclusivos do Hospital
    hospital_exclusive = [
        generate_utente_id("HOSP", i) for i in range(1, num_exclusive + 1)
    ]

    # 3. Gerar elementos exclusivos da Seguradora
    seguradora_exclusive = [
        generate_utente_id("SEG", i) for i in range(1, num_exclusive + 1)
    ]

    # 4. Juntando
    hospital_list = common_elements + hospital_exclusive
    seguradora_list = common_elements + seguradora_exclusive

    # 5. Gerando aleatoriedade
    random.shuffle(hospital_list)
    random.shuffle(seguradora_list)

    # 6. Gravar ficheiros
    hospital_filename = os.path.join(OUTPUT_DIR, f"hospital_{label}.txt")
    seguradora_filename = os.path.join(OUTPUT_DIR, f"seguradora_{label}.txt")
    # Se necessario salvar as interseções de cada base.
    #intersection_filename = os.path.join(OUTPUT_DIR, f"ground_truth_intersection_{label}.txt")

    with open(hospital_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(hospital_list) + "\n")

    with open(seguradora_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(seguradora_list) + "\n")

    # Guardar a lista da interseção esperada para validação dos resultados do demo.exe
    # with open(intersection_filename, "w", encoding="utf-8") as f:
    #     f.write("\n".join(sorted(common_elements)) + "\n")

    print(f" -> Gerado base com {label.upper()}: {size} | {num_intersection} intersecao (10%)")
