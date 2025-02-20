#!/usr/bin/env python3
"""
Script de Validação por Força Bruta para o Problema de Escalonamento

Este script utiliza os mesmos dados dos CSVs (tasks.csv, consultants.csv e compatibility.csv)
para validar a solução ótima encontrada pelo solver de otimização.

A validação é realizada por meio de uma busca exaustiva (força bruta) em que:
  - Cada tarefa pode ser atribuída a qualquer consultor.
  - Para cada combinação de atribuição, calcula-se a carga de cada consultor (soma dos tempos de processamento)
    e, consequentemente, o makespan (o maior valor dentre as cargas).
  - A melhor atribuição é aquela que minimiza o makespan.

OBSERVAÇÕES:
  - A abordagem por força bruta é viável somente para instâncias pequenas do problema, pois
    o número total de combinações cresce exponencialmente com o número de tarefas.
  - Para acompanhar o progresso, utilizamos a biblioteca 'tqdm'.
  
Requisitos:
  pip install tqdm
"""

import pandas as pd
from itertools import product
from tqdm import tqdm

def read_data(tasks_file, consultants_file, compatibility_file):
    """
    Lê os dados dos arquivos CSV e retorna os DataFrames ordenados.
    
    Args:
      tasks_file (str): Caminho do arquivo de tarefas.
      consultants_file (str): Caminho do arquivo de consultores.
      compatibility_file (str): Caminho do arquivo de compatibilidade.
      
    Returns:
      tasks_df, consultants_df, compatibility_df (DataFrame, DataFrame, DataFrame)
    """
    tasks_df = pd.read_csv(tasks_file)
    consultants_df = pd.read_csv(consultants_file)
    compatibility_df = pd.read_csv(compatibility_file)
    
    # Ordena os DataFrames pelos identificadores para garantir consistência
    tasks_df.sort_values('id', inplace=True)
    consultants_df.sort_values('id', inplace=True)
    compatibility_df.sort_values('task_id', inplace=True)
    
    return tasks_df, consultants_df, compatibility_df

def process_compatibility(compatibility_df, num_consultants):
    """
    Converte os fatores de compatibilidade de porcentagem para multiplicadores.
    
    Args:
      compatibility_df (DataFrame): DataFrame com a compatibilidade.
      num_consultants (int): Número de consultores.
      
    Returns:
      processed_factors (list of lists): Cada linha corresponde à tarefa e cada elemento é o multiplicador.
    """
    # Assume que as colunas de compatibilidade são: consultant_1, consultant_2, ..., consultant_m
    factor_cols = [f'consultant_{i+1}' for i in range(num_consultants)]
    factors = compatibility_df[factor_cols].values.tolist()
    
    processed_factors = []
    for row in factors:
        # Converte cada valor para float e divide por 100
        processed_row = [float(val) / 100.0 for val in row]
        processed_factors.append(processed_row)
    return processed_factors

def calculate_processing_times(tasks_df, processed_factors, num_tasks, num_consultants):
    """
    Calcula a matriz de tempos de processamento (P).
    
    Para cada tarefa j e consultor i:
        P[j][i] = (horas base da tarefa j) * (multiplicador de compatibilidade)
    
    Args:
      tasks_df (DataFrame): DataFrame com as tarefas.
      processed_factors (list of lists): Fatores de compatibilidade processados.
      num_tasks (int): Número de tarefas.
      num_consultants (int): Número de consultores.
      
    Returns:
      P (list of lists): Matriz de tempos de processamento.
    """
    t = tasks_df['horas'].tolist()  # Lista com o tempo base de cada tarefa
    P = []
    for j in range(num_tasks):
        row = []
        for i in range(num_consultants):
            row.append(processed_factors[j][i] * t[j])
        P.append(row)
    return P

def brute_force_validation(tasks_df, processed_factors, num_tasks, num_consultants):
    """
    Realiza a validação por força bruta:
      - Gera todas as combinações possíveis de atribuição de tarefas aos consultores.
      - Calcula o makespan (máxima carga entre os consultores) para cada atribuição.
      - Retorna o melhor makespan e a atribuição correspondente.
      
    Durante a iteração, utiliza 'tqdm' para exibir uma barra de progresso.
    
    Args:
      tasks_df (DataFrame): DataFrame com as tarefas.
      processed_factors (list of lists): Fatores de compatibilidade processados.
      num_tasks (int): Número de tarefas.
      num_consultants (int): Número de consultores.
      
    Returns:
      best_makespan (float): O menor makespan encontrado.
      best_assignment (tuple): Atribuição (tupla) que gera o menor makespan.
      P (list of lists): Matriz de tempos de processamento.
    """
    P = calculate_processing_times(tasks_df, processed_factors, num_tasks, num_consultants)
    
    best_makespan = float('inf')
    best_assignment = None
    
    # Número total de combinações possíveis
    total_iterations = num_consultants ** num_tasks
    
    # Utiliza tqdm para mostrar o progresso
    progress_bar = tqdm(product(range(num_consultants), repeat=num_tasks), total=total_iterations, desc="Processando combinações")
    
    for assignment in progress_bar:
        # Calcula a carga de cada consultor para essa atribuição
        loads = [0] * num_consultants
        for j, consultant in enumerate(assignment):
            loads[consultant] += P[j][consultant]
        current_makespan = max(loads)
        if current_makespan < best_makespan:
            best_makespan = current_makespan
            best_assignment = assignment
            
    return best_makespan, best_assignment, P

def main():
    # Caminhos dos arquivos CSV
    tasks_file = 'data/tasks.csv'
    consultants_file = 'data/consultants.csv'
    compatibility_file = 'data/compatibility.csv'
    
    # Passo 1: Leitura dos dados
    tasks_df, consultants_df, compatibility_df = read_data(tasks_file, consultants_file, compatibility_file)
    
    num_tasks = tasks_df.shape[0]
    num_consultants = consultants_df.shape[0]
    
    # Passo 2: Processamento dos fatores de compatibilidade
    processed_factors = process_compatibility(compatibility_df, num_consultants)
    
    # Passo 3: Validação por força bruta
    best_makespan, best_assignment, P = brute_force_validation(tasks_df, processed_factors, num_tasks, num_consultants)
    
    # Exibe o resultado da validação
    print("\nValidação por Força Bruta:")
    print("Melhor makespan encontrado: {:.2f} horas".format(best_makespan))
    print("Melhor atribuição (índices dos consultores para cada tarefa):")
    for j, consultant_index in enumerate(best_assignment):
        task_id = tasks_df.iloc[j]['id']
        # Considera que a ordem dos consultores em consultants_df corresponde aos índices usados na atribuição
        consultant_id = consultants_df.iloc[consultant_index]['id']
        print(f"  Tarefa {task_id} -> Consultor {consultant_id}")

if __name__ == '__main__':
    main()
