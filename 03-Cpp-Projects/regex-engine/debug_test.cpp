#include <iostream>
#include <string>

int main() {
    // Test if CONCAT character works
    const char CONCAT = '\1';
    std::string test = "a";
    test += CONCAT;
    test += "b";
    
    std::cout << "String length: " << test.length() << std::endl;
    std::cout << "Characters: ";
    for (char c : test) {
        std::cout << (int)c << " ";
    }
    std::cout << std::endl;
    
    return 0;
}
