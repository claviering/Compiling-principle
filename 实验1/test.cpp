#include <iostream>
#include <cstdio>
#include <string>
#include <map>
using namespace std;

class Precompiled
{
public:
	Precompiled(FILE *p_in, FILE *p_out);
	~Precompiled();
	void run();
private:
	FILE *p_in_file;
	FILE *p_out_file;
	char c;
	map<string, string> change_map;

	void init_map();
	void process();
};

Precompiled::Precompiled(FILE *p_in, FILE *p_out)
{
	if (p_in == NULL)
		perror("Error opening file");
	if (p_out == NULL)
		perror("Error opening file");
	p_in_file = p_in;
	p_out_file = p_out;

	init_map();
}

Precompiled::~Precompiled()
{
	fclose(p_in_file);
}

void Precompiled::init_map()
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

void Precompiled::run()
{
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
	FILE *p_in = fopen("Test_in.cpp", "r");
	FILE *p_out = fopen("Test_out.cpp", "w");
	Precompiled obj(p_in, p_out);
	obj.run();
	cout << "ok" << endl;
	return 0;
}