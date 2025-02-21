import pandas as pd
import os

 
def read_data(tasks_file, consultants_file, compatibility_file):
    """
    Lê os dados dos arquivos CSV da pasta sample_data no Google Colab e retorna os DataFrames ordenados.
    """
    base_path = "data/"
 
    tasks_path = os.path.join(base_path, tasks_file)
    consultants_path = os.path.join(base_path, consultants_file)
    compatibility_path = os.path.join(base_path, compatibility_file)
 
    tasks_df = pd.read_csv(tasks_path)
    consultants_df = pd.read_csv(consultants_path)
    compatibility_df = pd.read_csv(compatibility_path)
 
    tasks_df.sort_values('horas', ascending=False, inplace=True)  # Ordena por tempo de duração (decrescente)
    consultants_df.sort_values('id', inplace=True)  # Mantém a ordem dos consultores
    compatibility_df.sort_values('task_id', inplace=True)  # Mantém a compatibilidade organizada
 
    return tasks_df, consultants_df, compatibility_df
 
def greedy_scheduling(tasks_df, consultants_df, compatibility_df):
    """
    Algoritmo guloso para escalonamento de tarefas em consultoria minimizando o makespan.
    """
    # Dicionário para armazenar quando cada consultor estará disponível
    consultant_availability = {row['id']: 0 for _, row in consultants_df.iterrows()}
   
    # Dicionário para armazenar tarefas atribuídas por consultor
    consultant_tasks = {row['id']: [] for _, row in consultants_df.iterrows()}
   
    # Lista para armazenar as atribuições de tarefas
    task_assignments = []
 
    for _, task in tasks_df.iterrows():
        task_id = task['id']
        duration = task['horas']
 
        # Obtém a compatibilidade dos consultores com essa tarefa
        compatible_consultants = compatibility_df[compatibility_df['task_id'] == task_id].iloc[:, 1:].T
        compatible_consultants.columns = ['compatibility']
        compatible_consultants['consultant_id'] = compatible_consultants.index.str.replace('consultant_', '').astype(int)
        compatible_consultants = compatible_consultants.sort_values(by='compatibility', ascending=False)
 
        # Escolhe o consultor disponível mais cedo dentre os compatíveis
        best_consultant = min(compatible_consultants['consultant_id'], key=lambda c: consultant_availability[c])
 
        # Atualiza o tempo de disponibilidade do consultor
        start_time = consultant_availability[best_consultant]
        end_time = start_time + duration
        consultant_availability[best_consultant] = end_time
 
        # Registra a atribuição
        task_assignments.append((task_id, best_consultant, start_time, end_time))
        consultant_tasks[best_consultant].append(task_id)
 
    return task_assignments, consultant_availability, consultant_tasks, max(consultant_availability.values())
 
# Lê os dados da pasta sample_data
tasks_df, consultants_df, compatibility_df = read_data("tasks.csv", "consultants.csv", "compatibility.csv")
 
# Executa o algoritmo guloso
assignments, consultant_availability, consultant_tasks, makespan = greedy_scheduling(tasks_df, consultants_df, compatibility_df)
 
# Converte para DataFrame
assignments_df = pd.DataFrame(assignments, columns=["Task ID", "Consultant ID", "Start Time", "End Time"])
 
# Calcula o total de horas contratadas (soma de todas as tarefas)
total_hours_contracted = tasks_df["horas"].sum()
 
# Cálculo de custos e exibição dos resultados
total_project_cost = 0
 
print("\n🔹 Solução ótima encontrada:")
print(f"Makespan (Tempo total do projeto): {makespan:.2f} horas")
print(f"Total de horas contratadas (soma dos tempos das tarefas): {total_hours_contracted:.2f} horas\n")
 
print("🔹 Detalhamento por consultor:")
for _, consultant in consultants_df.iterrows():
    consultant_id = consultant["id"]
    cost_per_hour = consultant["custo"]
   
    # Tarefas atribuídas
    tasks_assigned = consultant_tasks[consultant_id]
    hours_worked = sum(tasks_df[tasks_df["id"].isin(tasks_assigned)]["horas"]) if tasks_assigned else 0
   
    # Horas ociosas até o makespan
    idle_hours = makespan - hours_worked
   
    # Cálculo do custo total do consultor
    consultant_cost = hours_worked * cost_per_hour
    total_project_cost += consultant_cost
   
    print(f"Consultor {consultant_id} (Custo R$ {cost_per_hour:.2f}/h):")
    print(f"  Tarefas atribuídas: {tasks_assigned}")
    print(f"  Horas de trabalho efetivas: {hours_worked:.2f} h")
    print(f"  Horas ociosas: {idle_hours:.2f} h")
    print(f"  Custo: R$ {consultant_cost:.2f}\n")
 
print(f"🔹 Custo total do projeto: R$ {total_project_cost:.2f}")
 
 