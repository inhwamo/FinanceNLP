#include <iostream>

int main() {
    int val = 0x1337 & 0x28 | 0xa;
    std::cout << val << std::endl;
    return 0;
}