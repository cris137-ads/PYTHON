'''Nesta atividade, uma lista encadeada deverá ser criada e alguns elementos são adicionados usando
o método append. Em seguida, a lista é impressa e a função count_nodes é chamada passando a
lista encadeada como argumento. O resultado é então impresso na tela, exibindo o número de nós
presentes na lista.
Abaixo segue um espelho da atividade (algoritmo) a ser realizada (código fonte)'''

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def print_list(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")

    # Implementar uma função para contar o número de nós em uma lista encadeada.
def count_nodes(linked_list):
    current = linked_list.head
    count = 0
    while current:
        count += 1
        current = current.next
    return count