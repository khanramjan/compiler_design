#include <bits/stdc++.h>
using namespace std;

int main() {
    vector<string> keywords = {"int", "return", "if", "else", "while", "for", "break", "continue", "include", "main"};

    ifstream file("program.cpp");
    if (!file.is_open()) {
        cerr << "Error opening file" << endl;
        return 1;
    }

    string line;
    int lineNumber = 0;
    unordered_map<string, int> keywordCount;
    unordered_map<string, vector<int>> keywordLines;

    while (getline(file, line)) {
        lineNumber++;
        for (const string& keyword : keywords) {
            size_t pos = line.find(keyword);
            if (pos != string::npos) {
                keywordCount[keyword]++;
                keywordLines[keyword].push_back(lineNumber);
            }
        }
    }

    for (const string& keyword : keywords) {
        if (keywordCount[keyword] > 0) {
            cout << "Keyword '" << keyword << "' found " << keywordCount[keyword] << " times on lines: ";
            for (int ln : keywordLines[keyword]) {
                cout << ln << " ";
            }
            cout << endl;
        }
    }

    return 0;
}