import pandas as pd
from ortools.linear_solver import pywraplp

def main():
    # Caminhos dos arquivos CSV
    tasks_file = 'data/tasks.csv'
    consultants_file = 'data/consultants.csv'
    compatibility_file = 'data/compatibility.csv'

    # Leitura dos dados
    tasks_df = pd.read_csv(tasks_file)          # Colunas: id, horas, descricao, skills, etc.
    consultants_df = pd.read_csv(consultants_file)  # Colunas: id, custo, senioridade, especializacao, skills, etc.
    compatibility_df = pd.read_csv(compatibility_file)  # Colunas: task_id, consultant_1, consultant_2, ...

    # Ordena os dataframes pelos ids
    tasks_df.sort_values('id', inplace=True)
    consultants_df.sort_values('id', inplace=True)
    compatibility_df.sort_values('task_id', inplace=True)

    # Dados das tarefas: tempo de referência (em horas)
    t = tasks_df['horas'].tolist()
    num_tasks = len(t)
    
    # Total de horas contratadas (soma dos tempos das tarefas)
    total_contracted_hours = sum(t)
    
    # Dados dos consultores: custo por hora
    costs = consultants_df['custo'].tolist()
    num_consultants = len(costs)

    # Extraindo os fatores de produção da tabela de compatibilidade
    # Supõe-se que a tabela possua colunas: task_id, consultant_1, consultant_2, ...
    factor_cols = [f'consultant_{i+1}' for i in range(num_consultants)]
    factors = compatibility_df[factor_cols].values.tolist()

    # Processa os fatores: converte de percentual para multiplicador
    processed_factors = []
    for row in factors:
        processed_row = []
        for factor in row:
            f_val = float(factor)
            processed_row.append(f_val / 100.0)
        processed_factors.append(processed_row)

    # Calcula os tempos de processamento para cada tarefa e consultor:
    # P[j][i] = processed_factors[j][i] * t[j]
    P = []
    for j in range(num_tasks):
        row = []
        for i in range(num_consultants):
            row.append(processed_factors[j][i] * t[j])
        P.append(row)

    # Criação do solver CBC do OR‑Tools
    solver = pywraplp.Solver('scheduling', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    if not solver:
        print("Solver CBC não encontrado.")
        return

    # Variáveis de decisão: x[i,j] = 1 se o consultor i for designado para a tarefa j; 0 caso contrário
    x = {}
    for j in range(num_tasks):
        for i in range(num_consultants):
            x[i, j] = solver.BoolVar(f'x[{i},{j}]')

    # Variável makespan K (tempo total para conclusão do projeto)
    K = solver.NumVar(0, solver.infinity(), 'K')

    # Restrição 1: Cada tarefa deve ser atribuída a exatamente um consultor
    for j in range(num_tasks):
        solver.Add(sum(x[i, j] for i in range(num_consultants)) == 1)

    # Restrição 2: O tempo total de processamento de cada consultor não pode ultrapassar o makespan K
    for i in range(num_consultants):
        solver.Add(sum(P[j][i] * x[i, j] for j in range(num_tasks)) <= K)

    # Função objetivo: minimizar o makespan K
    solver.Minimize(K)

    # Resolve o modelo
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        makespan = K.solution_value()
        print("Solução ótima encontrada:")
        print("Makespan (Tempo total do projeto): {:.2f} horas".format(makespan))
        print("Total de horas contratadas (soma dos tempos das tarefas): {:.2f} horas".format(total_contracted_hours))
        print("\nDetalhamento por consultor:")
        
        total_project_cost = 0.0
        for i in range(num_consultants):
            # Lista de tarefas atribuídas ao consultor i
            assigned_tasks = [int(tasks_df.iloc[j]['id']) for j in range(num_tasks) if x[i, j].solution_value() > 0.5]
            # Carga de trabalho efetiva para o consultor i (soma dos tempos de processamento)
            working_hours = sum(P[j][i] * x[i, j].solution_value() for j in range(num_tasks))
            # Tempo ocioso = makespan - carga de trabalho (pois o consultor é remunerado por makespan)
            idle_time = makespan - working_hours
            # Custo do consultor: ele é remunerado por makespan horas, independentemente da carga
            consultant_cost = makespan * costs[i]
            total_project_cost += consultant_cost
            print(f"Consultor {consultants_df.iloc[i]['id']} (Custo R$ {costs[i]:.2f}/h):")
            print(f"  Tarefas atribuídas: {assigned_tasks}")
            print(f"  Horas de trabalho efetivas: {working_hours:.2f} h")
            print(f"  Horas ociosas: {idle_time:.2f} h")
            print(f"  Custo: R$ {consultant_cost:.2f}")
        
        print("\nCusto total do projeto: R$ {:.2f}".format(total_project_cost))
    else:
        print("Solução não encontrada ou o problema não é viável.")

if __name__ == '__main__':
    main()
