import os

# ==============================
# CONFIGURAÇÃO
# ==============================

# caminho da pasta onde estão os labels .txt
LABELS_DIR = "./test/labels"   # <-- coloque o caminho certo

# mapeamento antigo → novo (exemplo)
# {classe_antiga: classe_nova}
index_map = {
    80: 1,   # 0 vira 80
    81: 2,   # 1 vira 81
    82: 3    # 2 vira 82
}

# ==============================
# EXECUÇÃO
# ==============================

def process_labels():
    for filename in os.listdir(LABELS_DIR):
        if filename.endswith(".txt"):
            file_path = os.path.join(LABELS_DIR, filename)

            # lê file
            with open(file_path, "r") as f:
                lines = f.readlines()

            new_lines = []
            for line in lines:
                parts = line.strip().split()

                if len(parts) < 5:
                    continue  # linha inválida

                old_index = int(parts[0])

                if old_index not in index_map:
                    print(f"Aviso: Classe {old_index} não está no index_map.")
                    continue

                new_index = index_map[old_index]

                # substitui o índice
                parts[0] = str(new_index)

                new_lines.append(" ".join(parts) + "\n")

            # reescreve o arquivo
            with open(file_path, "w") as f:
                f.writelines(new_lines)

            print(f"Atualizado: {filename}")

    print("\n✔️ Finalizado! Todos os labels foram convertidos.")


if __name__ == "__main__":
    process_labels()
