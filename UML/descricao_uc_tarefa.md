ID do Caso de Uso: uc_task

Caso de Uso: Gerenciar Tarefas

Ator Principla: Usuário Autenticado

Interessados e Interesses:
- Usuário Autenticado: Deseja criar, visualizar, editar e excluir tarefas associadas a uma disciplina.

Pré-Condições: Deve haver pelo menos uma disciplina cadastrada no sistema.

Pós-Condições: A tarefa é persistida no banco de dados ou removida, a depender da ação em questão.

Cenário de Sucesso Principal: 
1. O usuário solicita adicionar uma nova tarefa em uma disciplina específica.

2. O sistema solicita os dados: Título, Tipo (Atividade, Prova, Trabalho), Data de Entrega/Realização e Descrição.


3. O usuário fornece os dados solicitados.

4. O sistema valida os dados (ex: data válida, campos obrigatórios preenchidos).

5. O sistema salva a nova tarefa com o status inicial "Pendente".


6. O sistema exibe a lista de tarefas atualizada.


Fluxo Alternativo 1:
1. O usuário acessa a lista de tarefas.

2. O sistema exibe as tarefas com seus dados (data, status).

3. O usuário pode selecionar uma tarefa específica para ver detalhes, editar ou excluir.


Fluxo Alternativo 2:
1. O usuário seleciona uma tarefa da lista

2. O usuário solicita a exclusão da tarefa

3. O sistema pede confirmação.

4. O usuário confirma.

5. O sistema remove a tarefa e atualiza a lista.

---

ID do Caso de Uso: uc_done

Caso de Uso: Concluir Tarefa

Ator Principal: Usuário Autenticado

Interessados e Interesses:
- Usuário Autenticado: Deseja alterar indicar que uma tarefa foi finalizada para organizar suas pendências.

Pré-Condições: O caso de uso "Gerenciar Tarefas" deve ter sido realizado antes. Assim, a tarefa deve existir e estar com status "Pendente".

Pós-Condições: O status da tarefa é atualizado para "Concluída".

Cenário de Sucesso Principal:
1. O usuário seleciona uma tarefa da lista.

2. O usuário seleciona a opção "Marcar como Concluída".

3. O sistema atualiza o status da tarefa para "Concluída".

4. O sistema risca a tarefa na lista para indicar visualmente o sucesso da operação.

---

ID do Caso de Uso: uc_grade

Caso de Uso: Registrar/Editar Nota

Ator Principal: Usuário Autenticado

Interessados e Interesses:
- Usuário Autenticado: Deseja registrar e editar notas referentes a uma tarefa, para acompanhar seu desempenho na disciplina.

Pré-Condições: O caso de uso "Gerenciar Tarefas" deve ter sido realizado antes. Assim, a tarefa deve existir.

Pós-Condições: A tarefa possui uma nota registrada que será usada para cálculos de média.

Cenário de Sucesso Principal:
1. O usuário seleciona uma tarefa da lista.

2. O usuário seleciona a opção "Registrar Nota".

3. O sistema exibe o campo de nota atual (se houver).

4. O usuário insere a nota.

5. O sistema valida se a nota é um valor númerico não negativo.

6. O sistema salva a nota associada à tarefa.

---

ID do Caso de Uso: uc_reminder

Caso de Uso: Registrar/Editar Lembrete

Ator Principal: Usuário Autenticado

Interessados e Interesses:
- Usuário Autenticado: Deseja registrar e editar lembretes das datas limites de realização das tarefas para não perder o prazo.

Pré-Condições: O caso de uso "Gerenciar Tarefas" deve ter sido realizado antes. Assim, a tarefa deve existir e estar com o status pendente.

Pós-Condições: Um gatilho de envio de email é criado associado aquela tarefa.

Cenário de Sucesso Principal:
1. O usuário seleciona uma tarefa.

2. O usuário seleciona a opção "Criar Lembrete".

3. O sistema solicita informações de data do prazo de entrega e quantas horas antes o lembrete deve ser disparado.

4. O usuário fornece as informações.

5. O sistema agenda o envio de email.

6. O sistema confirma o agendamento ao usuário.