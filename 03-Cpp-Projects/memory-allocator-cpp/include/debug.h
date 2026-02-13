#ifndef DEBUG_H
#define DEBUG_H

#include <cstddef>
#include <cstdint>
#include <iostream>
#include <sstream>
#include <chrono>
#include <mutex>
#include <unordered_map>

namespace MemoryAllocator {

// Classe per logging e debug
class Debug {
public:
    static void set_enabled(bool enabled) {
        enabled_ = enabled;
    }

    // Log generico
    template<typename... Args>
    static void log(const char* format, Args... args) {
        if (!enabled_) return;

        std::cout << "[ALLOC] ";
        print_format(format, args...);
        std::cout << std::endl;
    }

    // Log allocazione
    template<typename... Args>
    static void log_alloc(size_t id, size_t size, const char* file, int line) {
        if (!enabled_) return;

        std::cout << "[ALLOC+] ID=" << id << " Size=" << size << " bytes";
        if (file) {
            std::cout << " at " << file << ":" << line;
        }
        std::cout << std::endl;
    }

    // Log deallocazione
    static void log_free(size_t id, const char* file, int line) {
        if (!enabled_) return;

        std::cout << "[ALLOC-] ID=" << id;
        if (file) {
            std::cout << " at " << file << ":" << line;
        }
        std::cout << std::endl;
    }

    // Log errore
    static void log_error(const char* message, const char* file = nullptr, int line = 0) {
        std::cerr << "[ERROR] " << message;
        if (file) {
            std::cerr << " at " << file << ":" << line;
        }
        std::cerr << std::endl;
    }

    // Log double-free
    static void log_error_double_free(size_t id, const char* file, int line) {
        std::cerr << "[ERROR] Double-free detectato! ID=" << id;
        if (file) {
            std::cerr << " at " << file << ":" << line;
        }
        std::cerr << std::endl;
    }

    // Log statistiche
    static void log_stats(size_t total_alloc, size_t total_free, size_t free_blocks, size_t total_blocks) {
        std::cout << "[STATS] Allocati: " << total_alloc << " bytes, "
                  << "Liberi: " << total_free << " bytes, "
                  << "Blocchi liberi: " << free_blocks << "/"
                  << total_blocks << std::endl;
    }

private:
    static inline bool enabled_ = false;

    // Helper per print format
    template<typename... Args>
    static void print_format(const char* format, Args... args) {
        std::cout << format_string(format, args...);
    }

    // Semplice format string
    template<typename... Args>
    static std::string format_string(const char* format, Args... args) {
        // Implementazione base - per production usare std::format (C++20)
        std::ostringstream oss;
        oss << format;
        return oss.str();
    }
};

// Timer per performance measurement
class Timer {
public:
    Timer() : start_(std::chrono::high_resolution_clock::now()) {}

    // Reset timer
    void reset() {
        start_ = std::chrono::high_resolution_clock::now();
    }

    // Ottieni elapsed time in millisecondi
    double elapsed_ms() const {
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start_);
        return duration.count() / 1000.0;
    }

    // Ottieni elapsed time in microsecondi
    double elapsed_us() const {
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start_);
        return duration.count();
    }

private:
    std::chrono::high_resolution_clock::time_point start_;
};

// Classe per tracking allocations
class AllocationTracker {
public:
    struct AllocationInfo {
        void* address;
        size_t size;
        const char* file;
        int line;
        std::chrono::time_point<std::chrono::high_resolution_clock> timestamp;
    };

    static AllocationTracker& getInstance() {
        static AllocationTracker instance;
        return instance;
    }

    void add_allocation(void* ptr, size_t size, const char* file, int line) {
        std::lock_guard<std::mutex> lock(mutex_);
        allocations_[ptr] = {ptr, size, file, line, std::chrono::high_resolution_clock::now()};
    }

    void remove_allocation(void* ptr) {
        std::lock_guard<std::mutex> lock(mutex_);
        allocations_.erase(ptr);
    }

    bool has_allocation(void* ptr) const {
        return allocations_.find(ptr) != allocations_.end();
    }

    void print_leaks() const {
        std::lock_guard<std::mutex> lock(mutex_);
        if (allocations_.empty()) {
            std::cout << "[TRACKER] Nessun memory leak detectato\n";
            return;
        }

        std::cout << "[TRACKER] Memory Leaks detectati:\n";
        for (const auto& [ptr, info] : allocations_) {
            std::cout << "  Leak: " << ptr << " (" << info.size << " bytes) at "
                      << info.file << ":" << info.line << "\n";
        }
    }

    size_t get_allocation_count() const {
        return allocations_.size();
    }

private:
    AllocationTracker() = default;

    mutable std::mutex mutex_;
    std::unordered_map<void*, AllocationInfo> allocations_;
};

} // namespace MemoryAllocator

// Macro helper per debug
#define DEBUG_LOG(msg) MemoryAllocator::Debug::log(msg)
#define DEBUG_LOG_ALLOC(id, size) MemoryAllocator::Debug::log_alloc(id, size, __FILE__, __LINE__)
#define DEBUG_LOG_FREE(id) MemoryAllocator::Debug::log_free(id, __FILE__, __LINE__)
#define DEBUG_ERROR(msg) MemoryAllocator::Debug::log_error(msg, __FILE__, __LINE__)

#endif // DEBUG_H
