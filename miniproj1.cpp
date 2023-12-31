#include <iostream>

struct Node {
    Node* next;
    Node* prev;
    int value;
};

Node* makenode(int value) {
    Node* newnode = new Node;
    newnode->next = nullptr;
    newnode->prev = nullptr;
    newnode->value = value;
    return newnode;
}

Node* addnode(int value, Node* head) {
    Node* new_node = makenode(value);
    Node* temp = head;
    while (temp->next != nullptr) {
        temp = temp->next;
    }
    temp->next = new_node;
    new_node->prev = temp;
    new_node->next = nullptr;
    return head;
}

void deleteNode(int value, Node* head) {
    Node* temp = head;
    while (temp->next != nullptr) {
        if (temp->value == value) {
            break;
        }
        temp = temp->next;
    }
    Node* temp1 = temp->prev;
    Node* temp2 = temp->next;
    temp1->next = temp2;
    if (temp2 != nullptr) {
        temp2->prev = temp1;
    }
    delete temp;
}

Node* forrk(int value, Node* head, int new_value) {
    Node* temp = head;
    while (temp->next != nullptr) {
        if (temp->value == value) {
            break;
        }
        temp = temp->next;
    }
    Node* temp2 = temp->next;
    Node* new_node = makenode(new_value);

    temp->next = new_node;
    new_node->prev = temp;
    new_node->next = temp2;
    if (temp2 != nullptr) {
        temp2->prev = new_node;
    }

    return head;
}

void print(Node* head) {
    Node* temp = head->next;
    while (temp != nullptr) {
        std::cout << temp->value << " ";
        temp = temp->next;
    }
    std::cout << std::endl;
}

int main() {
    Node* head = makenode(-1);
    head->next = nullptr;
    head->prev = nullptr;

    int t;
    std::cin >> t;

    for (int i = 1; i <= t; i++) {
        int oper;
        std::cin >> oper;
        if (oper == 0) {
            int value;
            std::cin >> value;
            head = addnode(value, head);
        }
        else if (oper == 1) {
            int value;
            std::cin >> value;
            deleteNode(value, head);
        }
        else if (oper == 2) {
            int value;
            int new_value;
            std::cin >> value;
            std::cin >> new_value;
            head = forrk(value, head, new_value);
        }
        else if (oper == 3) {
            print(head);
        }
    }

    Node* temp = head;
    while (temp != nullptr) {
        Node* next = temp->next;
        delete temp;
        temp = next;
    }

    return 0;
}
