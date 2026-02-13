/**
 * @file student.cpp
 * @brief Implementazione della classe Student e StudentManager
 */

#include "student.h"
#include <iostream>
#include <sstream>
#include <algorithm>
#include <iomanip>

// ==================== IMPLEMENTAZIONE CLASSE STUDENT ====================

// Costruttore di default
Student::Student() : id(0), name(""), surname(""), age(0), course(""), averageGrade(0.0) {}

// Costruttore con parametri
Student::Student(int id, const std::string& name, const std::string& surname,
                 int age, const std::string& course, double averageGrade)
    : id(id), name(name), surname(surname), age(age), course(course), averageGrade(averageGrade) {}

// Getter
int Student::getId() const { return id; }
std::string Student::getName() const { return name; }
std::string Student::getSurname() const { return surname; }
int Student::getAge() const { return age; }
std::string Student::getCourse() const { return course; }
double Student::getAverageGrade() const { return averageGrade; }

// Setter
void Student::setId(int id) { this->id = id; }
void Student::setName(const std::string& name) { this->name = name; }
void Student::setSurname(const std::string& surname) { this->surname = surname; }
void Student::setAge(int age) { this->age = age; }
void Student::setCourse(const std::string& course) { this->course = course; }
void Student::setAverageGrade(double averageGrade) { this->averageGrade = averageGrade; }

// Metodo per visualizzare le informazioni dello studente
void Student::display() const {
    std::cout << "ID: " << id << " | Nome: " << name << " " << surname
              << " | Età: " << age << " | Corso: " << course
              << " | Media: " << std::fixed << std::setprecision(2) << averageGrade << std::endl;
}

// Metodo per convertire lo studente in stringa (formato CSV)
std::string Student::toString() const {
    std::stringstream ss;
    ss << id << "," << name << "," << surname << ","
       << age << "," << course << "," << averageGrade;
    return ss.str();
}

// Metodo statico per creare uno studente da una stringa
Student Student::fromString(const std::string& str) {
    std::stringstream ss(str);
    std::string token;
    std::vector<std::string> tokens;

    // Suddividi la stringa usando la virgola come delimitatore
    while (std::getline(ss, token, ',')) {
        tokens.push_back(token);
    }

    // Crea e restituisci uno studente con i dati parsati
    if (tokens.size() >= 6) {
        return Student(
            std::stoi(tokens[0]),      // id
            tokens[1],                  // name
            tokens[2],                  // surname
            std::stoi(tokens[3]),      // age
            tokens[4],                  // course
            std::stod(tokens[5])       // averageGrade
        );
    }
    return Student(); // Restituisci studente vuoto se parsing fallito
}

// ==================== IMPLEMENTAZIONE CLASSE STUDENTMANAGER ====================

// Costruttore
StudentManager::StudentManager() : nextId(1) {}

// Genera un nuovo ID univoco
int StudentManager::generateId() {
    return nextId++;
}

// Aggiunge un nuovo studente
void StudentManager::addStudent(const std::string& name, const std::string& surname,
                                int age, const std::string& course, double averageGrade) {
    int newId = generateId();
    Student newStudent(newId, name, surname, age, course, averageGrade);
    students.push_back(newStudent);
    std::cout << "\n✓ Studente aggiunto con successo! ID assegnato: " << newId << std::endl;
}

// Elimina uno studente per ID
bool StudentManager::deleteStudent(int id) {
    for (auto it = students.begin(); it != students.end(); ++it) {
        if (it->getId() == id) {
            students.erase(it);
            std::cout << "\n✓ Studente con ID " << id << " eliminato con successo!" << std::endl;
            return true;
        }
    }
    std::cout << "\n✗ Errore: Studente con ID " << id << " non trovato!" << std::endl;
    return false;
}

// Aggiorna le informazioni di uno studente
bool StudentManager::updateStudent(int id, const std::string& name, const std::string& surname,
                                   int age, const std::string& course, double averageGrade) {
    for (auto& student : students) {
        if (student.getId() == id) {
            student.setName(name);
            student.setSurname(surname);
            student.setAge(age);
            student.setCourse(course);
            student.setAverageGrade(averageGrade);
            std::cout << "\n✓ Studente con ID " << id << " aggiornato con successo!" << std::endl;
            return true;
        }
    }
    std::cout << "\n✗ Errore: Studente con ID " << id << " non trovato!" << std::endl;
    return false;
}

// Cerca uno studente per ID
Student* StudentManager::searchById(int id) {
    for (auto& student : students) {
        if (student.getId() == id) {
            return &student;
        }
    }
    return nullptr;
}

// Cerca studenti per nome
std::vector<Student> StudentManager::searchByName(const std::string& name) {
    std::vector<Student> results;
    for (const auto& student : students) {
        if (student.getName() == name) {
            results.push_back(student);
        }
    }
    return results;
}

// Cerca studenti per cognome
std::vector<Student> StudentManager::searchBySurname(const std::string& surname) {
    std::vector<Student> results;
    for (const auto& student : students) {
        if (student.getSurname() == surname) {
            results.push_back(student);
        }
    }
    return results;
}

// Visualizza tutti gli studenti
void StudentManager::displayAll() const {
    if (students.empty()) {
        std::cout << "\nNessuno studente presente nel database." << std::endl;
        return;
    }

    std::cout << "\n============================================" << std::endl;
    std::cout << "         ELENCO STUDENTI (" << students.size() << ")" << std::endl;
    std::cout << "============================================" << std::endl;

    for (const auto& student : students) {
        student.display();
    }

    std::cout << "============================================" << std::endl;
}

// Restituisce il numero di studenti
int StudentManager::getCount() const {
    return students.size();
}

// Salva gli studenti su file
bool StudentManager::saveToFile(const std::string& filename) const {
    std::ofstream outFile(filename);

    if (!outFile.is_open()) {
        std::cout << "\n✗ Errore: Impossibile aprire il file " << filename << " per la scrittura!" << std::endl;
        return false;
    }

    // Salva ogni studente su una riga
    for (const auto& student : students) {
        outFile << student.toString() << std::endl;
    }

    outFile.close();
    std::cout << "\n✓ " << students.size() << " studenti salvati su " << filename << std::endl;
    return true;
}

// Carica gli studenti da file
bool StudentManager::loadFromFile(const std::string& filename) {
    std::ifstream inFile(filename);

    if (!inFile.is_open()) {
        std::cout << "\n✗ Errore: Impossibile aprire il file " << filename << " per la lettura!" << std::endl;
        return false;
    }

    students.clear(); // Pulisci il vettore corrente
    nextId = 1;      // Resetta il contatore ID

    std::string line;
    int count = 0;

    // Leggi ogni riga e crea gli studenti
    while (std::getline(inFile, line)) {
        if (!line.empty()) {
            Student student = Student::fromString(line);
            if (student.getId() != 0) {
                students.push_back(student);
                count++;
                // Aggiorna nextId se necessario
                if (student.getId() >= nextId) {
                    nextId = student.getId() + 1;
                }
            }
        }
    }

    inFile.close();
    std::cout << "\n✓ " << count << " studenti caricati da " << filename << std::endl;
    return true;
}
