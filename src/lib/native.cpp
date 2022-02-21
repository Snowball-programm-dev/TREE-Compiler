#include <string>
#include <iostream>
#include <fstream>


std::string get(std::string path)
{
    std::string line;
    std::string file;
    std::ifstream myFile(path);
    if (myFile.is_open())
    {
        while (getline(myFile,line)) {
            file += line + "\n";
        }
    }
    return file;

}

