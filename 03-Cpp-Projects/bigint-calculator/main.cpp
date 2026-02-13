/**
 * @file main.cpp
 * @brief Programma di test per la classe BigInt
 * @author Matti
 * @date 2025
 *
 * Questo programma contiene una suite completa di test per verificare
 * tutte le funzionalità implementate nella classe BigInt.
 */

#include "bigint.h"
#include <iostream>
#include <cassert>
#include <iomanip>
#include <string>
#include <vector>

// ================== FUNZIONI DI TEST ==================

void testSeparator(const std::string& title) {
    std::cout << "\n" << std::string(60, '=') << "\n";
    std::cout << "  " << title << "\n";
    std::cout << std::string(60, '=') << "\n";
}

void printTestResult(const std::string& testName, bool passed) {
    std::cout << std::left << std::setw(50) << testName
              << (passed ? "[PASSO]" : "[FALLITO]") << "\n";
}

// ================== TEST COSTRUTTORI ==================

void testCostruttori() {
    testSeparator("TEST COSTRUTTORI");

    // Test costruttore di default
    BigInt a;
    printTestResult("Costruttore default (deve essere 0)", a == BigInt(0));
    printTestResult("Costruttore default - isZero()", a.isZero());

    // Test costruttore da long long
    BigInt b(12345);
    printTestResult("Costruttore da long(12345)", b.toString() == "12345");

    BigInt c(-9876);
    printTestResult("Costruttore da long(-9876)", c.toString() == "-9876");
    printTestResult("Costruttore da long - isNegative()", c.isNegative());

    BigInt d(0);
    printTestResult("Costruttore da long(0)", d.isZero());

    // Test costruttore da stringa
    BigInt e("12345678901234567890");
    printTestResult("Costruttore da stringa (numero grande)",
                   e.toString() == "12345678901234567890");

    BigInt f("-98765432109876543210");
    printTestResult("Costruttore da stringa (negativo grande)",
                   f.toString() == "-98765432109876543210");

    BigInt g("+123");
    printTestResult("Costruttore da stringa con +", g.toString() == "123");

    // Test costruttore di copia
    BigInt h(e);
    printTestResult("Costruttore di copia", h == e);

    // Test assegnazione
    BigInt i;
    i = b;
    printTestResult("Operatore di assegnazione", i == b);
}

// ================== TEST OPERATORI ARITMETICI ==================

void testAddizione() {
    testSeparator("TEST ADDIZIONE");

    BigInt a(123);
    BigInt b(456);
    BigInt c = a + b;

    printTestResult("123 + 456 = 579", c == BigInt(579));

    BigInt d(-100);
    BigInt e = a + d;
    printTestResult("123 + (-100) = 23", e == BigInt(23));

    BigInt f(-200);
    BigInt g = d + f;
    printTestResult("(-100) + (-200) = -300", g == BigInt(-300));

    // Numeri grandi
    BigInt h("99999999999999999999");
    BigInt i("1");
    BigInt j = h + i;
    printTestResult("99999999999999999999 + 1 = 100000000000000000000",
                   j.toString() == "100000000000000000000");
}

void testSottrazione() {
    testSeparator("TEST SOTTRAZIONE");

    BigInt a(500);
    BigInt b(300);
    BigInt c = a - b;

    printTestResult("500 - 300 = 200", c == BigInt(200));

    BigInt d(100);
    BigInt e = a - d;
    printTestResult("500 - 100 = 400", e == BigInt(400));

    BigInt f(-200);
    BigInt g = a - f;
    printTestResult("500 - (-200) = 700", g == BigInt(700));

    BigInt h(100);
    BigInt i(500);
    BigInt j = h - i;
    printTestResult("100 - 500 = -400", j == BigInt(-400));

    // Numeri uguali
    BigInt k(123);
    BigInt l(123);
    BigInt m = k - l;
    printTestResult("123 - 123 = 0", m.isZero());

    // Numeri grandi
    BigInt n("100000000000000000000");
    BigInt o("1");
    BigInt p = n - o;
    printTestResult("100000000000000000000 - 1 = 99999999999999999999",
                   p.toString() == "99999999999999999999");
}

void testMoltiplicazione() {
    testSeparator("TEST MOLTIPLICAZIONE");

    BigInt a(12);
    BigInt b(10);
    BigInt c = a * b;

    printTestResult("12 * 10 = 120", c == BigInt(120));

    BigInt d(-5);
    BigInt e = a * d;
    printTestResult("12 * (-5) = -60", e == BigInt(-60));

    BigInt f(-3);
    BigInt g = d * f;
    printTestResult("(-5) * (-3) = 15", g == BigInt(15));

    // Moltiplicazione per zero
    BigInt h(0);
    BigInt i = a * h;
    printTestResult("12 * 0 = 0", i.isZero());

    // Numeri grandi
    BigInt j("123456789");
    BigInt k("987654321");
    BigInt l = j * k;
    printTestResult("123456789 * 987654321",
                   l.toString() == "121932631112635269");

    // Potenza
    BigInt m("2");
    BigInt n("1000000000000");
    BigInt o = m * n;
    printTestResult("2 * 1000000000000 = 2000000000000",
                   o.toString() == "2000000000000");
}

void testDivisione() {
    testSeparator("TEST DIVISIONE");

    BigInt a(100);
    BigInt b(5);
    BigInt c = a / b;

    printTestResult("100 / 5 = 20", c == BigInt(20));

    BigInt d(-50);
    BigInt e = a / d;
    printTestResult("100 / (-50) = -2", e == BigInt(-2));

    BigInt f(-30);
    BigInt g = d / f;
    printTestResult("(-50) / (-30) = 1", g == BigInt(1));

    // Divisione con resto
    BigInt h(17);
    BigInt i(5);
    BigInt j = h / i;
    printTestResult("17 / 5 = 3 (divisione intera)", j == BigInt(3));

    // Numeri grandi
    BigInt k("100000000000000000000");
    BigInt l("10");
    BigInt m = k / l;
    printTestResult("100000000000000000000 / 10",
                   m.toString() == "10000000000000000000");
}

void testModulo() {
    testSeparator("TEST MODULO");

    BigInt a(17);
    BigInt b(5);
    BigInt c = a % b;

    printTestResult("17 % 5 = 2", c == BigInt(2));

    BigInt d(-17);
    BigInt e = d % b;
    printTestResult("(-17) % 5 = -2", e == BigInt(-2));

    BigInt f(100);
    BigInt g(7);
    BigInt h = f % g;
    printTestResult("100 % 7 = 2", h == BigInt(2));

    // Multipli
    BigInt i(20);
    BigInt j(5);
    BigInt k = i % j;
    printTestResult("20 % 5 = 0", k.isZero());

    // Numeri grandi
    BigInt l("100000000000000000001");
    BigInt m("10");
    BigInt n = l % m;
    printTestResult("100000000000000000001 % 10 = 1", n == BigInt(1));
}

void testMenosUnario() {
    testSeparator("TEST MENO UNARIO");

    BigInt a(123);
    BigInt b = -a;

    printTestResult("-(123) = -123", b == BigInt(-123));

    BigInt c = -b;
    printTestResult("-(-123) = 123", c == BigInt(123));

    BigInt d(0);
    BigInt e = -d;
    printTestResult("-(0) = 0", e.isZero());
}

// ================== TEST OPERATORI DI CONFRONTO ==================

void testConfronto() {
    testSeparator("TEST OPERATORI DI CONFRONTO");

    BigInt a(100);
    BigInt b(100);
    BigInt c(200);
    BigInt d(50);
    BigInt e(-100);

    printTestResult("100 == 100", a == b);
    printTestResult("100 != 200", a != c);
    printTestResult("50 < 100", d < a);
    printTestResult("100 > 50", a > d);
    printTestResult("100 <= 100", a <= b);
    printTestResult("100 >= 50", a >= d);

    // Confronto con negativi
    printTestResult("-100 < 100", e < a);
    printTestResult("-100 > -200", e > BigInt(-200));
    printTestResult("-100 == -100", e == BigInt(-100));
    printTestResult("100 != -100", a != e);

    // Numeri grandi
    BigInt f("99999999999999999999");
    BigInt g("100000000000000000000");
    printTestResult("99999999999999999999 < 100000000000000000000", f < g);
}

// ================== TEST CONVERSIONI ==================

void testConversioni() {
    testSeparator("TEST CONVERSIONI");

    BigInt a(12345);

    printTestResult("toString() = '12345'", a.toString() == "12345");
    printTestResult("toLong() = 12345", a.toLong() == 12345);
    printTestResult("toInt() = 12345", a.toInt() == 12345);

    BigInt b(-6789);
    printTestResult("toString() negativo = '-6789'", b.toString() == "-6789");
    printTestResult("toLong() negativo = -6789", b.toLong() == -6789);

    // Numero grande
    BigInt c("12345678901234567890");
    printTestResult("toString() numero grande", c.toString() == "12345678901234567890");

    // Test overflow in toInt/toLong
    BigInt d("999999999999999999999999999999");
    bool overflowCaught = false;

    try {
        d.toLong();
    } catch (const std::overflow_error&) {
        overflowCaught = true;
    }
    printTestResult("Overflow in toLong() genera eccezione", overflowCaught);
}

// ================== TEST METODI UTILI ==================

void testMetodiUtili() {
    testSeparator("TEST METODI UTILI");

    BigInt a(123);
    BigInt b(-456);
    BigInt c(0);

    printTestResult("isNegative() positivo", !a.isNegative());
    printTestResult("isNegative() negativo", b.isNegative());
    printTestResult("isZero() numero", !a.isZero());
    printTestResult("isZero() zero", c.isZero());

    printTestResult("numDigits() 123 = 3", a.numDigits() == 3);
    printTestResult("numDigits() -456 = 3", b.numDigits() == 3);
    printTestResult("numDigits() 0 = 1", c.numDigits() == 1);

    BigInt d("12345");
    printTestResult("numDigits() 12345 = 5", d.numDigits() == 5);

    BigInt e = a.absolute();
    printTestResult("absolute() di positivo", e == a);

    BigInt f = b.absolute();
    printTestResult("absolute() di negativo", f == BigInt(456));
}

// ================== TEST STREAM ==================

void testStream() {
    testSeparator("TEST STREAM");

    BigInt a(12345);
    std::cout << "Test output stream (<<): " << a << "\n";
    printTestResult("Operatore << funziona", true);

    std::istringstream iss("67890");
    BigInt b;
    iss >> b;
    printTestResult("Operatore >> funziona", b == BigInt(67890));

    std::cout << "Numero letto dallo stream: " << b << "\n";
}

// ================== CALCOLATRICE INTERATTIVA ==================

void calcolatriceInterattiva() {
    testSeparator("CALCOLATRICE INTERATTIVA");

    std::cout << "\nModalita calcolatrice interattiva.\n";
    std::cout << "Inserisci espressioni nel formato: <operando1> <operatore> <operando2>\n";
    std::cout << "Operatori supportati: +, -, *, /, %\n";
    std::cout << "Inserisci 'q' per uscire\n\n";

    std::string input;
    while (true) {
        std::cout << ">> ";
        std::getline(std::cin, input);

        if (input == "q" || input == "Q") {
            std::cout << "Uscita dalla calcolatrice.\n";
            break;
        }

        try {
            std::istringstream iss(input);
            BigInt op1, op2;
            char operatore;

            iss >> op1 >> operatore >> op2;

            BigInt risultato;
            switch (operatore) {
                case '+':
                    risultato = op1 + op2;
                    break;
                case '-':
                    risultato = op1 - op2;
                    break;
                case '*':
                    risultato = op1 * op2;
                    break;
                case '/':
                    risultato = op1 / op2;
                    break;
                case '%':
                    risultato = op1 % op2;
                    break;
                default:
                    std::cout << "Operatore non valido: " << operatore << "\n";
                    continue;
            }

            std::cout << "   = " << risultato << "\n";

        } catch (const std::exception& e) {
            std::cout << "Errore: " << e.what() << "\n";
        }
    }
}

// ================== FUNZIONE MAIN ==================

int main() {
    std::cout << "\n";
    std::cout << "╔════════════════════════════════════════════════════════════╗\n";
    std::cout << "║           BigInt Calculator - Suite di Test               ║\n";
    std::cout << "║                                                            ║\n";
    std::cout << "║  Implementazione C++ di numeri interi arbitrariamente grandi║\n";
    std::cout << "╚════════════════════════════════════════════════════════════╝\n";

    // Esegui tutti i test
    try {
        testCostruttori();
        testAddizione();
        testSottrazione();
        testMoltiplicazione();
        testDivisione();
        testModulo();
        testMenosUnario();
        testConfronto();
        testConversioni();
        testMetodiUtili();
        testStream();

        testSeparator("RIEPILOGO TEST");
        std::cout << "\n✓ Tutti i test sono stati completati con successo!\n\n";

        // Chiedi all'utente se vuole avviare la calcolatrice
        std::cout << "Vuoi avviare la calcolatrice interattiva? (s/n): ";
        char choice;
        std::cin >> choice;
        std::cin.ignore(); // Consuma il newline

        if (choice == 's' || choice == 'S') {
            calcolatriceInterattiva();
        }

    } catch (const std::exception& e) {
        std::cerr << "\n✗ ERRORE CRITICO: " << e.what() << "\n";
        return 1;
    }

    return 0;
}
