/**
 * @file main.cpp
 * @brief Programma principale per il sistema di gestione studenti
 * @details Menù interattivo per tutte le operazioni CRUD
 */

#include "student.h"
#include <iostream>
#include <limits>
#include <string>

// Funzione per pulire il buffer di input
void clearInputBuffer() {
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

// Funzione per visualizzare il menù principale
void displayMenu() {
    std::cout << "\n╔══════════════════════════════════════════════╗" << std::endl;
    std::cout << "║   SISTEMA DI GESTIONE STUDENTI                ║" << std::endl;
    std::cout << "╠══════════════════════════════════════════════╣" << std::endl;
    std::cout << "║  1. Aggiungi nuovo studente                   ║" << std::endl;
    std::cout << "║  2. Visualizza tutti gli studenti            ║" << std::endl;
    std::cout << "║  3. Cerca studente per ID                     ║" << std::endl;
    std::cout << "║  4. Cerca studente per nome                   ║" << std::endl;
    std::cout << "║  5. Cerca studente per cognome                ║" << std::endl;
    std::cout << "║  6. Aggiorna studente                         ║" << std::endl;
    std::cout << "║  7. Elimina studente                         ║" << std::endl;
    std::cout << "║  8. Salva dati su file                       ║" << std::endl;
    std::cout << "║  9. Carica dati da file                      ║" << std::endl;
    std::cout << "║  0. Esci                                     ║" << std::endl;
    std::cout << "╚══════════════════════════════════════════════╝" << std::endl;
    std::cout << "\nScelta: ";
}

// Funzione per aggiungere un nuovo studente
void addStudentMenu(StudentManager& manager) {
    std::string name, surname, course;
    int age;
    double grade;

    std::cout << "\n--- AGGIUNGI NUOVO STUDENTE ---" << std::endl;

    std::cout << "Nome: ";
    std::getline(std::cin, name);

    std::cout << "Cognome: ";
    std::getline(std::cin, surname);

    std::cout << "Età: ";
    std::cin >> age;
    clearInputBuffer();

    std::cout << "Corso di studi: ";
    std::getline(std::cin, course);

    std::cout << "Media voti: ";
    std::cin >> grade;
    clearInputBuffer();

    manager.addStudent(name, surname, age, course, grade);
}

// Funzione per cercare uno studente per ID
void searchByIdMenu(StudentManager& manager) {
    int id;
    std::cout << "\n--- CERCA STUDENTE PER ID ---" << std::endl;
    std::cout << "Inserisci ID: ";
    std::cin >> id;
    clearInputBuffer();

    Student* student = manager.searchById(id);
    if (student != nullptr) {
        std::cout << "\n✓ Studente trovato:" << std::endl;
        student->display();
    } else {
        std::cout << "\n✗ Nessuno studente trovato con ID: " << id << std::endl;
    }
}

// Funzione per cercare studenti per nome
void searchByNameMenu(StudentManager& manager) {
    std::string name;
    std::cout << "\n--- CERCA STUDENTI PER NOME ---" << std::endl;
    std::cout << "Inserisci nome: ";
    std::getline(std::cin, name);

    std::vector<Student> results = manager.searchByName(name);
    if (results.empty()) {
        std::cout << "\n✗ Nessuno studente trovato con nome: " << name << std::endl;
    } else {
        std::cout << "\n✓ Trovati " << results.size() << " studenti:" << std::endl;
        for (const auto& student : results) {
            student.display();
        }
    }
}

// Funzione per cercare studenti per cognome
void searchBySurnameMenu(StudentManager& manager) {
    std::string surname;
    std::cout << "\n--- CERCA STUDENTI PER COGNOME ---" << std::endl;
    std::cout << "Inserisci cognome: ";
    std::getline(std::cin, surname);

    std::vector<Student> results = manager.searchBySurname(surname);
    if (results.empty()) {
        std::cout << "\n✗ Nessuno studente trovato con cognome: " << surname << std::endl;
    } else {
        std::cout << "\n✓ Trovati " << results.size() << " studenti:" << std::endl;
        for (const auto& student : results) {
            student.display();
        }
    }
}

// Funzione per aggiornare uno studente
void updateStudentMenu(StudentManager& manager) {
    int id;
    std::cout << "\n--- AGGIORNA STUDENTE ---" << std::endl;
    std::cout << "Inserisci ID dello studente da aggiornare: ";
    std::cin >> id;
    clearInputBuffer();

    // Verifica se lo studente esiste
    Student* student = manager.searchById(id);
    if (student == nullptr) {
        std::cout << "\n✗ Nessuno studente trovato con ID: " << id << std::endl;
        return;
    }

    std::cout << "\nStudente attuale:" << std::endl;
    student->display();

    std::string name, surname, course;
    int age;
    double grade;

    std::cout << "\nInserisci i nuovi dati (lascia vuoto per mantenere il valore attuale):" << std::endl;

    std::cout << "Nome [" << student->getName() << "]: ";
    std::getline(std::cin, name);
    if (name.empty()) name = student->getName();

    std::cout << "Cognome [" << student->getSurname() << "]: ";
    std::getline(std::cin, surname);
    if (surname.empty()) surname = student->getSurname();

    std::cout << "Età [" << student->getAge() << "]: ";
    std::string ageStr;
    std::getline(std::cin, ageStr);
    if (ageStr.empty()) {
        age = student->getAge();
    } else {
        age = std::stoi(ageStr);
    }

    std::cout << "Corso [" << student->getCourse() << "]: ";
    std::getline(std::cin, course);
    if (course.empty()) course = student->getCourse();

    std::cout << "Media [" << student->getAverageGrade() << "]: ";
    std::string gradeStr;
    std::getline(std::cin, gradeStr);
    if (gradeStr.empty()) {
        grade = student->getAverageGrade();
    } else {
        grade = std::stod(gradeStr);
    }

    manager.updateStudent(id, name, surname, age, course, grade);
}

// Funzione per eliminare uno studente
void deleteStudentMenu(StudentManager& manager) {
    int id;
    std::cout << "\n--- ELIMINA STUDENTE ---" << std::endl;
    std::cout << "Inserisci ID dello studente da eliminare: ";
    std::cin >> id;
    clearInputBuffer();

    // Mostra lo studente prima di eliminarlo
    Student* student = manager.searchById(id);
    if (student != nullptr) {
        std::cout << "\nStudente da eliminare:" << std::endl;
        student->display();

        char conferma;
        std::cout << "\nConfermi l'eliminazione? (s/n): ";
        std::cin >> conferma;
        clearInputBuffer();

        if (conferma == 's' || conferma == 'S') {
            manager.deleteStudent(id);
        } else {
            std::cout << "\n✗ Eliminazione annullata." << std::endl;
        }
    } else {
        std::cout << "\n✗ Nessuno studente trovato con ID: " << id << std::endl;
    }
}

// Funzione per salvare su file
void saveToFileMenu(StudentManager& manager) {
    std::string filename;
    std::cout << "\n--- SALVA DATI SU FILE ---" << std::endl;
    std::cout << "Nome del file (premi INVIO per 'students.txt'): ";
    std::getline(std::cin, filename);

    if (filename.empty()) {
        filename = "students.txt";
    }

    manager.saveToFile(filename);
}

// Funzione per caricare da file
void loadFromFileMenu(StudentManager& manager) {
    std::string filename;
    std::cout << "\n--- CARICA DATI DA FILE ---" << std::endl;
    std::cout << "Nome del file (premi INVIO per 'students.txt'): ";
    std::getline(std::cin, filename);

    if (filename.empty()) {
        filename = "students.txt";
    }

    // Chiedi conferma se ci sono già dati in memoria
    if (manager.getCount() > 0) {
        char conferma;
        std::cout << "\nAttenzione: Ci sono già " << manager.getCount()
                  << " studenti in memoria." << std::endl;
        std::cout << "Vuoi sostituirli con i dati del file? (s/n): ";
        std::cin >> conferma;
        clearInputBuffer();

        if (conferma != 's' && conferma != 'S') {
            std::cout << "\n✗ Caricamento annullato." << std::endl;
            return;
        }
    }

    manager.loadFromFile(filename);
}

// Funzione principale
int main() {
    StudentManager manager;
    int choice;

    std::cout << "╔════════════════════════════════════════════════════════════╗" << std::endl;
    std::cout << "║        SISTEMA DI GESTIONE STUDENTI - C++ Project          ║" << std::endl;
    std::cout << "║                  Progetto OOP con C++                      ║" << std::endl;
    std::cout << "╚════════════════════════════════════════════════════════════╝" << std::endl;

    // Tentativo di caricare automaticamente i dati salvati
    if (manager.loadFromFile("students.txt")) {
        std::cout << "\nDati caricati automaticamente all'avvio." << std::endl;
    }

    do {
        displayMenu();
        std::cin >> choice;
        clearInputBuffer();

        switch (choice) {
            case 1:
                addStudentMenu(manager);
                break;
            case 2:
                manager.displayAll();
                break;
            case 3:
                searchByIdMenu(manager);
                break;
            case 4:
                searchByNameMenu(manager);
                break;
            case 5:
                searchBySurnameMenu(manager);
                break;
            case 6:
                updateStudentMenu(manager);
                break;
            case 7:
                deleteStudentMenu(manager);
                break;
            case 8:
                saveToFileMenu(manager);
                break;
            case 9:
                loadFromFileMenu(manager);
                break;
            case 0:
                // Salva automaticamente prima di uscire
                if (manager.getCount() > 0) {
                    char save;
                    std::cout << "\nVuoi salvare i dati prima di uscire? (s/n): ";
                    std::cin >> save;
                    if (save == 's' || save == 'S') {
                        manager.saveToFile("students.txt");
                    }
                }
                std::cout << "\nArrivederci! 📚" << std::endl;
                break;
            default:
                std::cout << "\n✗ Scelta non valida. Riprova." << std::endl;
        }
    } while (choice != 0);

    return 0;
}
