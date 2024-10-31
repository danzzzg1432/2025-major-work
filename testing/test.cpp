#include <iostream>
#include <vector>
#include <thread>
#include <chrono>
#include <atomic>
#include <cmath>

std::atomic<uint64_t> primeCount(0);

bool isPrime(uint64_t n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    
    for (uint64_t i = 3; i * i <= n; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

void countPrimesInRange(uint64_t start, uint64_t end) {
    uint64_t localCount = 0;
    
    // Make sure start is odd
    if (start % 2 == 0) start++;
    
    // Check only odd numbers
    for (uint64_t i = start; i <= end; i += 2) {
        if (isPrime(i)) {
            localCount++;
        }
    }
    
    primeCount += localCount;
}

int main() {
    const uint64_t LIMIT = 1000000000; // 1 billion
    const unsigned int threadCount = std::thread::hardware_concurrency();
    std::vector<std::thread> threads;
    
    // Start timing
    auto start = std::chrono::high_resolution_clock::now();
    
    // Account for 2 being prime
    primeCount = 1;
    
    // Calculate range for each thread
    uint64_t rangePerThread = (LIMIT - 1) / threadCount;
    
    // Create threads
    for (unsigned int i = 0; i < threadCount; i++) {
        uint64_t start = i * rangePerThread + 1;
        uint64_t end = (i == threadCount - 1) ? LIMIT : (i + 1) * rangePerThread;
        threads.emplace_back(countPrimesInRange, start, end);
    }
    
    // Wait for all threads to complete
    for (auto& thread : threads) {
        thread.join();
    }
    
    // End timing
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::seconds>(end - start);
    
    std::cout << "Number of primes found: " << primeCount << std::endl;
    std::cout << "Time taken: " << duration.count() << " seconds" << std::endl;
    std::cout << "Number of threads used: " << threadCount << std::endl;
    
    return 0;
}