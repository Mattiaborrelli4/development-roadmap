/**
 * @file student.h
 * @brief Header file per la classe Student
 * @details Definisce la struttura e i metodi per la gestione degli studenti
 */

#ifndef STUDENT_H
#define STUDENT_H

#include <string>
#include <vector>
#include <fstream>

/**
 * @class Student
 * @brief Classe che rappresenta uno studente con tutti i suoi attributi
 */
class Student {
private:
    int id;                    // Identificativo unico dello studente
    std::string name;          // Nome dello studente
    std::string surname;       // Cognome dello studente
    int age;                   // Età dello studente
    std::string course;        // Corso di studi
    double averageGrade;      // Media dei voti

public:
    // Costruttore di default
    Student();

    // Costruttore con parametri
    Student(int id, const std::string& name, const std::string& surname,
            int age, const std::string& course, double averageGrade);

    // Getter
    int getId() const;
    std::string getName() const;
    std::string getSurname() const;
    int getAge() const;
    std::string getCourse() const;
    double getAverageGrade() const;

    // Setter
    void setId(int id);
    void setName(const std::string& name);
    void setSurname(const std::string& surname);
    void setAge(int age);
    void setCourse(const std::string& course);
    void setAverageGrade(double averageGrade);

    // Metodo per visualizzare le informazioni dello studente
    void display() const;

    // Metodo per convertire lo studente in stringa (per il salvataggio su file)
    std::string toString() const;

    // Metodo per creare uno studente da una stringa (per il caricamento da file)
    static Student fromString(const std::string& str);
};

/**
 * @class StudentManager
 * @brief Classe per la gestione della lista degli studenti (CRUD operations)
 */
class StudentManager {
private:
    std::vector<Student> students;  // Vettore che contiene tutti gli studenti
    int nextId;                    // Prossimo ID disponibile

public:
    // Costruttore
    StudentManager();

    // Operazioni CRUD
    void addStudent(const std::string& name, const std::string& surname,
                    int age, const std::string& course, double averageGrade);
    bool deleteStudent(int id);
    bool updateStudent(int id, const std::string& name, const std::string& surname,
                       int age, const std::string& course, double averageGrade);

    // Operazioni di ricerca
    Student* searchById(int id);
    std::vector<Student> searchByName(const std::string& name);
    std::vector<Student> searchBySurname(const std::string& surname);

    // Operazioni di visualizzazione
    void displayAll() const;
    int getCount() const;

    // Operazioni su file
    bool saveToFile(const std::string& filename) const;
    bool loadFromFile(const std::string& filename);

    // Metodo per generare un nuovo ID univoco
    int generateId();
};

#endif // STUDENT_H
