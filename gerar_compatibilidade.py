import pandas as pd

def compute_factor(task_skills_str, consultant_skills_str, seniority):
    """
    Calcula o fator de produção para uma tarefa considerando:
    - task_skills_str: string com as skills requeridas (ex: "java,communication")
    - consultant_skills_str: string com as skills do consultor (ex: "java,linux,api")
    - seniority: string indicando a senioridade (junior, mid-level ou senior)
    
    Regras:
      - Se todas as skills requeridas estão presentes (match_ratio == 1):
          • junior    -> 1.80  (180%)
          • mid-level -> 1.00  (100%)
          • senior    -> 0.85  (85%)
      - Se houver compatibilidade parcial (match_ratio entre 0 e 1):
          O fator é interpolado entre um valor de “penalidade” e o valor para full match.
          Penalidades:
          • junior    -> 2.00
          • mid-level -> 1.20
          • senior    -> 1.00
      - Se nenhuma skill coincidir (match_ratio == 0), retorna a penalidade correspondente.
    """
    # Converte as strings em conjuntos (minúsculas, sem espaços em excesso)
    task_skills = {skill.strip().lower() for skill in task_skills_str.split(',') if skill.strip()}
    consultant_skills = {skill.strip().lower() for skill in consultant_skills_str.split(',') if skill.strip()}
    
    if not task_skills:
        return 1.0  # Se não há skills requeridas, fator neutro
    
    matched = task_skills.intersection(consultant_skills)
    match_ratio = len(matched) / len(task_skills)
    
    # Compatibilidade total
    if match_ratio == 1.0:
        if seniority.lower() == 'junior':
            return 1.80
        elif seniority.lower() == 'mid-level':
            return 1.00
        elif seniority.lower() == 'senior':
            return 0.85
        else:
            return 1.00
    # Compatibilidade parcial
    elif match_ratio > 0:
        if seniority.lower() == 'junior':
            penalty = 2.00
            full_match = 1.80
        elif seniority.lower() == 'mid-level':
            penalty = 1.20
            full_match = 1.00
        elif seniority.lower() == 'senior':
            penalty = 1.00
            full_match = 0.85
        else:
            penalty = 1.20
            full_match = 1.00
        # Interpolação linear: quanto maior o match, mais próximo do full_match
        return match_ratio * full_match + (1 - match_ratio) * penalty
    else:
        # Se nenhuma skill coincidir, retorna a penalidade padrão conforme a senioridade
        if seniority.lower() == 'junior':
            return 2.00
        elif seniority.lower() == 'mid-level':
            return 1.20
        elif seniority.lower() == 'senior':
            return 1.00
        else:
            return 1.20

def main():
    # Lê os arquivos CSV de tarefas e consultores
    tarefas_df = pd.read_csv('data/tasks.csv')
    consultores_df = pd.read_csv('data/consultants.csv')
    
    num_tasks = len(tarefas_df)
    num_consultants = len(consultores_df)
    
    # Cria uma lista para armazenar os resultados de compatibilidade
    compatibilidade_data = []
    
    # Para cada tarefa, calcula o fator para cada consultor
    for _, tarefa in tarefas_df.iterrows():
        row = {}
        row['task_id'] = tarefa['id']
        task_skills = tarefa['skills']
        for _, consultor in consultores_df.iterrows():
            consultant_id = consultor['id']
            consultant_skills = consultor['skills']
            seniority = consultor['senioridade']
            factor = compute_factor(task_skills, consultant_skills, seniority)
            # Chave no formato "consultant_X"
            col_name = f"consultant_{int(consultant_id)}"
            # Multiplica por 100 para expressar o fator em porcentagem (ex: 1.80 -> 180%)
            row[col_name] = factor * 100  
        compatibilidade_data.append(row)
    
    # Cria o DataFrame e organiza as colunas
    compatibilidade_df = pd.DataFrame(compatibilidade_data)
    col_order = ['task_id'] + [f'consultant_{i+1}' for i in range(num_consultants)]
    compatibilidade_df = compatibilidade_df[col_order]
    
    # Salva o DataFrame em um arquivo CSV
    compatibilidade_df.to_csv('data/compatibility.csv', index=False)
    print("Arquivo 'compatibility.csv' gerado com sucesso.")
    print(compatibilidade_df)

if __name__ == '__main__':
    main()
