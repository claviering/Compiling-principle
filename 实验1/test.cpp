#include <iostream>
#include <cstdio>
#include <string>
#include <map>
using namespace std;

class Precompiled
{
public:
public:
	Precompiled();
	~Precompiled();
	void run();
private:
	FILE *p_in_file;
	FILE *p_out_file;
	char c;
	map<string, string> change_map;

	void open_file();
	void process();
};

Precompiled::Precompiled()
{
	change_map["begin"] = "{";
	change_map["end"] = "}";
	change_map["(*"] = "/*";
	change_map["*)"] = "*/";
	change_map["integer"] = "int";
	change_map["read"] = "cin";
	change_map[":="] = "=";
	change_map["<>"] = "!=";
	change_map["write"] = "cout";
}


Precompiled::~Precompiled()
{
	fclose(p_in_file);
}

void Precompiled::run()
{
	open_file();
}

void Precompiled::open_file()
{
	FILE *stream;
	p_in_file = fopen("Test_in.cpp", "r");
	if (p_in_file == NULL) 
		perror("Error opening file");

	p_out_file = fopen("Test_out.cpp", "w");
	if (p_out_file == NULL)
		perror("Error opening file");


	process();
}

void Precompiled::process()
{
	c = fgetc(p_in_file);
	while (c != EOF)
	{
		if (c == '$')
		{
			string str = "";
			c = fgetc(p_in_file);
			while (c != '$')
			{
				str.insert(str.end(), c);
				c = fgetc(p_in_file);
			}
			string new_str = change_map[str];
			for (int i = 0; new_str[i] != '\0'; i++)
				putc(new_str[i], p_out_file);
			c = fgetc(p_in_file);
		}
		else
		{
			putc(c, p_out_file);
			c = fgetc(p_in_file);
		}
	}

}


int main()
{
	Precompiled obj;
	obj.run();
	cout << "ok" << endl;
	return 0;
}