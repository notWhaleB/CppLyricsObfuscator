# CppLyricsObfuscator
Turn your code into the lyrics

Script allows you to choose some of your c++ code and turn it into lyrics and code will continue to work.

## Usage
You can specify parameters in program arguments or input it after script running. 
First parameter is path to the .cpp code file and second is path to the file with lyrics.
In source .cpp code file you need to markup region of code which will changed with the `//LOBEGIN//` and `//LOEND//` tags.
Example:
```c++
#include <iostream>

//LOBEGIN//

int main() {
  std::cout << "Obfuscate me!";
  
  return 0;
}

//LOEND//
```
Important. For the region between the tags, there are some limitations:
  1. There should be no comments
  2. There should be no structures beginning with # (such as #include or #define and other)
  
After program message "Done." next to your source file will be created changed file with same name and .lo extension.

Have fun!
