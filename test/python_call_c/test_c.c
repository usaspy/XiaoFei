#include <stdio.h>
#include <string.h>
#include <stdlib.h>
 
typedef struct StructPointerTest
{
	char name[20];
	int age;
}StructPointerTest, *StructPointer;
 
StructPointer test()	// 返回结构体指针
{ 
	StructPointer p = (StructPointer)malloc(sizeof(StructPointerTest)); 
	strcpy(p->name, "Joe");
	p->age = 20;
	
	return p; 
}
