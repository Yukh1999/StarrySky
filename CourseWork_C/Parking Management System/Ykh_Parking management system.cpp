/*
*C语言课程设计:泊车管理系统
*创建时间:2017/6/8	15:36
*作者:余轲辉
*院系:理学院
*班级:应用物理1601
*最后一次修改日期:2017/6/14
*/

#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<conio.h>
void use_explain()
{
	printf("\n\n*泊车管理系统使用说明\n\n");
	printf("*密码设置或修改时必须为八位\n\n*键盘上所有按键例如删除键空格键等都被视为有效字符\n\n");
	system("pause");
	system("cls");
	printf("\n\n*注意初次使用时按提示操作，必须先设置车位总数\n\n");
	system("pause");
	system("cls");
	printf("\n\n*使用此系统时请注意提示字符是输入还是按键\n");
	printf("\n*输入请待输入完所有内容后按回车键完成输入\n");
	printf("\n*按键操作，直接按键操作（操作时先设置为英文输入法，否则会出现信息错误)\n\n");
	system("pause");
	system("cls");
	return;
}
void Judge()                                    //创建文件
{
	void password();
	FILE*fp;
	int n;
	fp = fopen("./ALL_Carport.txt", "r");
	if (fp == NULL)                            //打开失败，创建新文件
	{
		fp = fopen("./ALL_Carport.txt", "w");
		fprintf(fp, "%d", 0);
		fclose(fp);
		printf("\n\n初次进入系统，请先阅读使用说明\n\n");
		system("pause");
		system("cls");
		use_explain();
		printf("即将进入系统...\n\n");
		system("pause");
		system("cls");
	}
	else
	{
		fscanf(fp, "%d", &n);
		if (n < 0)
		{
			fclose(fp);
			fp = fopen("./ALL_Carport.txt", "w");
			fprintf(fp, "%d", 0);
			fclose(fp);
		}
		else
			fclose(fp);
	}
	fp = fopen("./user.txt", "r");
	if (fp == NULL)							//打开失败，创建新文件
	{
		fp = fopen("./user.txt", "w");
		fclose(fp);
		printf("初次使用请先设置密码\n");
		password();
	}
	else
		fclose(fp);
	fp = fopen("./Car.txt", "r");
	if (fp == NULL)							//打开失败，创建新文件
	{
		fp = fopen("./Car.txt", "w");
		fclose(fp);
	}
	else
		fclose(fp);
	fp = fopen("./num.txt", "r");
	if (fp == NULL)							//打开失败，创建新文件
	{
		fp = fopen("./num.txt", "w");
		fprintf(fp, "%d", 0);
		fclose(fp);
	}
	else
	{
		int a;
		a = fscanf(fp, "%d", &n);
		if (n < 0 || a <= 0)								//信息录入不成功或信息错误将会初始化
		{
			fclose(fp);
			fp = fopen("./num.txt", "w");
			fprintf(fp, "%d", 0);
			fclose(fp);
			fp = fopen("./Car.txt", "w");
			fclose(fp);
			printf("\n!!!车辆信息数据存在错误，已初始化，请重新录入信息\n");
		}
		else
			fclose(fp);
	}
	return;
}
struct Information_Car    //定义结构体(车辆信息）
{
	char car_name[15];    //车辆名称
	char owner[15];       //车主姓名
	int num;              //车辆编号
	char LPN[15];         //车牌号
	Information_Car *next;//链表
};
int menu()                //菜单栏
{
	int a;
	printf("\n********************************\n\n");
	printf("*          泊车管理系统        *\n\n");
	printf("         录入信息:请输入1\n\n");
	printf("         删除信息:请输入2\n\n");
	printf("         查询信息:请输入3\n\n");
	printf("         修改密码:请输入4\n\n");
	printf("         修改信息:请输入5\n\n");
	printf("         使用说明:请输入6\n\n");
	printf("         退出系统:请输入0\n\n");
	printf("********************************\n\n");
	printf("         请选择您要使用的功能:");
	a = getch() - 48;
	printf("\n");
	if (a < 0 || a > 6)                     //输入非选项内号码时，给出提示
	{
		system("cls"); printf("         请输入正确号码...");
		return a;
	}
	else
	{
		system("cls");
		return a;                         //将输入的值返回给主函数
	}
}
void All_carport_modification()            //修改车位总数
{
	FILE *fp;
	int num, ALL_Carport;
	fp = fopen("./num.txt", "r");
	fscanf(fp, "%d", &num);
	fclose(fp);
	while (1)                           //循环直到输入成功
	{
		printf("\n\n#请输入新的车位总数:");
		scanf("%d", &ALL_Carport);
		getchar();                      //清空缓冲区
		if (ALL_Carport < num)          //判断新设置车位总数是否小于已存在车辆数目
		{
			char n = 0;
			printf("\n设置不合理，停车场内车辆数目已大于新车位数\n\n");
			printf("按1继续，按其他任意键退出设置\n");
			n = getch();
			system("cls");
			if (n != '1')
			{
				printf("\n!退出车位设置\n\n");
				system("pause");
				system("cls");
				return;
			}
		}
		else
			break;
	}
	fp = fopen("./ALL_Carport.txt", "w");
	fprintf(fp, "%d", ALL_Carport);
	printf("\n车位总数更新成功，为:%d\n\n", ALL_Carport);
	fclose(fp);
	system("pause");
	system("cls");
	return;
}
void find_1()				//查询全部信息
{
	Information_Car*car, *Car;
	Information_Car head = { 0 };
	FILE*fp;
	int n, a = 0;
	int x=0;
	int t=0;
	fp = fopen("./Car.txt", "r");				//打开文件
	printf("\n按编号顺序查看请按1\n\n");
	printf("按车名顺序查看请按2\n\n");
	printf("按车牌顺序查看请按3\n\n");
	printf("请输入对应编号:");
	while (1)
	{	
		n = getch() - 48;
		printf("%d", n);
		// scanf("%d", &n);	//输入选项
		// getchar();				//清空缓冲区
		if (n > 3 || n < 1)
			printf("\n请输入正确的号码:");
		else
			break;
	}
	system("cls");
	if (n == 1)
	{
		Information_Car *pre;			//储存上一位指针
		car = (Information_Car*)malloc(sizeof(Information_Car));		//获取内存空间
		if (fscanf(fp, "%s%s%d%s", car->car_name, car->owner, &car->num, car->LPN) <= 0)
		x = 1;
		car->next = head.next;
		head.next = car;
		while (true)
		{
			Car = head.next;
			pre = &head;
			int n = 1;
			car = (Information_Car*)malloc(sizeof(Information_Car));
			fscanf(fp, "%s%s%d%s", car->car_name, car->owner, &car->num, car->LPN);
			if (feof(fp))    //到文件末尾，终止录入
			{
				break;
			}
			while (Car != NULL)					//遍历链表
			{
				if ((Car->num) > (car->num))    //找到目标将该内存接到目标上一位后面
				{
					car->next = pre->next;
					pre->next = car;
					n = 0;
					break;
				}
				pre = Car;					//存储上一位指针
				Car = Car->next;
			}
			if (n)					//未找到目标，将该内存接在链表末尾
			{
				car->next = pre->next;
				pre->next = car;
			}
		}
		free(car);					//释放多余内存
		Car = head.next;			//指针指向链表头下一位，即真正存储信息的第一位
		printf("---------------------------------------------------\n");
		printf("编号\t车主姓名  \t车辆型号  \t车牌号\n");
		printf("---------------------------------------------------\n");
		if (x)
		{
			printf("无内容，请先录入...\n");
			printf("---------------------------------------------------\n");
			system("pause");
			system("cls");
			return;
		}
		else
		while (Car != NULL)			//遍历链表
		{
			a++;
			printf("%-4d\t%-10s\t%-10s\t%-10s\n",
				Car->num, Car->owner, Car->car_name, Car->LPN);   //将信息输出到屏幕
			Car = Car->next;		//跳转到下一位
			printf("---------------------------------------------------\n");
		}
		while (true)
		{
			t++;
			char s;
			printf("倒序查看请按1,按其他任意键退出\n");
			s = getch();
			system("cls");
			if (s == '1')
			{
				int i, j;
				printf("---------------------------------------------------\n");
				printf("编号\t车主姓名  \t车辆型号  \t车牌号\n");
				printf("---------------------------------------------------\n");
				if (t % 2 == 0)
				{
					Car = head.next;
					while (Car != NULL)			//遍历链表
					{
						printf("%-4d\t%-10s\t%-10s\t%-10s\n",
							Car->num, Car->owner, Car->car_name, Car->LPN);   //将信息输出到屏幕
						Car = Car->next;		//跳转到下一位
						printf("---------------------------------------------------\n");
					}
				}
				else
				for (i = a; i > 0; i--)
				{
					Car = head.next;
					for (j = 1; j < i; j++)
					{
						Car = Car->next;
					}
					printf("%-4d\t%-10s\t%-10s\t%-10s\n",
						Car->num, Car->owner, Car->car_name, Car->LPN);   //将信息输出到屏幕
					printf("---------------------------------------------------\n");
				}
			}
			else
			{
				fclose(fp);
				return;
			}
		}
	}
	if (n == 2)      //功能同上
	{
		Information_Car *pre;
		car = (Information_Car*)malloc(sizeof(Information_Car));
		if(fscanf(fp, "%s%s%d%s", car->car_name, car->owner, &car->num, car->LPN)<=0)
			x=1;
		car->next = head.next;
		head.next = car;
		while (true)
		{
			Car = head.next;
			pre = &head;
			int n = 1;
			car = (Information_Car*)malloc(sizeof(Information_Car));
			fscanf(fp, "%s%s%d%s", car->car_name, car->owner, &car->num, car->LPN);
			if (feof(fp))
			{
				break;
			}
			while (Car != NULL)
			{
				if (strcmp(Car->car_name, car->car_name) > 0)
				{
					car->next = pre->next;
					pre->next = car;
					n = 0;
					break;
				}
				pre = Car;
				Car = Car->next;
			}
			if (n)
			{
				car->next = pre->next;
				pre->next = car;
			}
		}
		free(car);
		Car = head.next;
		printf("---------------------------------------------------\n");
		printf("车辆型号  \t车主姓名  \t编号\t车牌号\n");
		printf("---------------------------------------------------\n");
		if (x)
		{
			printf("无内容，请先录入...\n");
			printf("---------------------------------------------------\n");
			system("pause");
			system("cls");
			return;
		}
		else
		while (Car != NULL)
		{
			a++;
			printf("%-10s\t%-10s\t%-4d\t%-10s\n", Car->car_name, Car->owner, Car->num, Car->LPN);
			printf("---------------------------------------------------\n");
			Car = Car->next;
		}
		while (true)
		{
			t++;
			char s;
			printf("倒序查看请按1,按其他任意键退出\n");
			s = getch();
			system("cls");
			if (s == '1')
			{
				int i, j;
				printf("---------------------------------------------------\n");
				printf("车辆型号  \t车主姓名  \t编号\t车牌号\n");
				printf("---------------------------------------------------\n");
				if (t % 2 == 0)
				{
					Car = head.next;
					while (Car != NULL)
					{
						printf("%-10s\t%-10s\t%-4d\t%-10s\n", Car->car_name, Car->owner, Car->num, Car->LPN);
						printf("---------------------------------------------------\n");
						Car = Car->next;
					}
				}
				else
				for (i = a; i > 0; i--)
				{
					Car = head.next;
					for (j = 1; j < i; j++)
					{
						Car = Car->next;
					}
					printf("%-10s\t%-10s\t%-4d\t%-10s\n",
						Car->car_name, Car->owner, Car->num, Car->LPN);   //将信息输出到屏幕
					printf("---------------------------------------------------\n");
				}
			}
			else
			{
				fclose(fp);
				return;
			}
		}
	}
	if (n == 3)    //功能同上
	{
		Information_Car *pre;
		car = (Information_Car*)malloc(sizeof(Information_Car));
		if(fscanf(fp, "%s%s%d%s", car->car_name, car->owner, &car->num, car->LPN)<=0)
			x=1;
		car->next = head.next;
		head.next = car;
		while (true)
		{
			Car = head.next;
			pre = &head;
			int n = 1;
			car = (Information_Car*)malloc(sizeof(Information_Car));
			fscanf(fp, "%s%s%d%s", car->car_name, car->owner, &car->num, car->LPN);
			if (feof(fp))
			{
				break;
			}
			while (Car != NULL)
			{
				if (strcmp(Car->LPN, car->LPN) > 0)
				{
					car->next = pre->next;
					pre->next = car;
					n = 0;
					break;
				}
				pre = Car;
				Car = Car->next;
			}
			if (n)
			{
				car->next = pre->next;
				pre->next = car;
			}
		}
		free(car);
		Car = head.next;
		printf("---------------------------------------------------\n");
		printf("车牌号    \t车主姓名\t编号\t车辆型号\n");
		printf("---------------------------------------------------\n");
		if (x)
		{
			printf("无内容，请先录入...\n");
			printf("---------------------------------------------------\n");
			system("pause");
			system("cls");
			return;
		}
		else
		while (Car != NULL)
		{
			a++;
			printf("%-10s\t%-10s\t%-4d\t%-10s\n", Car->LPN, Car->owner, Car->num, Car->car_name);
			printf("---------------------------------------------------\n");
			Car = Car->next;
		}
		while (true)
		{
			t++;
			char s;
			printf("倒序查看请按1,按其他任意键退出\n");
			s = getch();
			system("cls");
			if (s == '1')
			{
				int i, j;
				printf("---------------------------------------------------\n");
				printf("车牌号    \t车主姓名\t编号\t车辆型号\n");
				printf("---------------------------------------------------\n");
				if (t % 2 == 0)
				{
					Car = head.next;
					while (Car != NULL)
					{
						printf("%-10s\t%-10s\t%-4d\t%-10s\n", Car->LPN, Car->owner, Car->num, Car->car_name);
						printf("---------------------------------------------------\n");
						Car = Car->next;
					}
				}
				else
				for (i = a; i > 0; i--)
				{
					Car = head.next;
					for (j = 1; j < i; j++)
					{
						Car = Car->next;
					}
					printf("%-10s\t%-10s\t%-4d\t%-10s\n",
						Car->LPN, Car->owner, Car->num, Car->car_name);  //将信息输出到屏幕
					printf("---------------------------------------------------\n");
				}
			}
			else
			{
				fclose(fp);
				return;
			}
		}
	}
	fclose(fp);    //断开指针与文件的关联
	return;
}
void find_2(Information_Car*C)        //按关键信息查询
{
	Information_Car *Car;
	Information_Car head = { 0 };
	FILE*fp;
	fp = fopen("./Car.txt", "r");
	int num;
	int t;
	char Car_name[15];
	char owner[15];
	char LPN[15];
	char Jump;
	int a, b, c, d;
	printf("\n********************************\n");
	printf("请输入你要查询对象的信息...\n");
	while (true)
	{
		rewind(fp);
		t = 0;
		while (1)     //循环直到成功接收到正确信息
		{
			Jump = 0;
			a = b = c = d = 0;
			printf("\n编号(跳过请按0,按其他任意键后继续输入)\n");
			Jump = getch();
			if (Jump != '0')
			{
				printf("请输入(编号):");
				a = 1;
				scanf("%d", &num);
				getchar();     //清空缓冲区
			}
			Jump = 0;
			printf("\n车辆型号(跳过请按输入0,按其他任意键后继续输入)\n");
			Jump = getch();
			if (Jump != '0')
			{
				printf("请输入(车辆型号):");
				b = 1;
				scanf("%s", Car_name);
				getchar();     //清空缓冲区
			}
			Jump = 0;
			printf("\n车主姓名(跳过请按输入0,按其他任意键后继续输入)\n");
			Jump = getch();
			if (Jump != '0')
			{
				printf("请输入(车主姓名):");
				c = 1;
				scanf("%s", owner);
				getchar();     //清空缓冲区
			}
			Jump = 0;
			printf("\n车牌号(跳过请按输入0,按其他任意键后继续输入)\n");
			Jump = getch();
			if (Jump != '0')
			{
				printf("请输入(车牌号):");
				d = 1;
				scanf("%s", LPN);
				getchar();     //清空缓冲区
			}
			if (a == 0 && b == 0 && c == 0 && d == 0)
			{
				system("cls");
				printf("\n未获取信息，请重新输入关键字...\n");
			}
			else
				break;
		}
		system("cls");
		printf("\n查询信息如下\n");
		printf("**************************************************\n");
		if (a == 1)      //如果输入编号，直接检索相关信息
		{
			printf("编号\t车主姓名  \t车辆型号  \t车牌号\n");
			printf("---------------------------------------------------\n");
			while (1)
			{
				if (feof(fp))    //检索到文件末尾仍无结果，跳出循环
				{
					t = 1;
					printf("查询无果...\n");
					break;
				}
				fscanf(fp, "%s%s%d%s", head.car_name, head.owner, &head.num, head.LPN);   //存取文件内相关信息
				if (head.num == num)    //判断是否与输入信息相同
				{
					printf("%-4d\t%-10s\t%-10s\t%-10s\n",
						head.num, head.owner, head.car_name, head.LPN);   //将内容输出到屏幕
					printf("---------------------------------------------------\n");
					break;
				}
			}
			printf("**************************************************\n\n");
		}
		else
		{
			if (d == 1)    //未获取编号，获取到车牌号后也直接检索  功能同上
			{
				printf("车牌号    \t车主姓名\t编号\t车辆型号\n");
				printf("---------------------------------------------------\n");
				while (1)
				{
					if (feof(fp))
					{
						t = 1;
						printf("查询无果...\n");
						break;
					}
					fscanf(fp, "%s%s%d%s", head.car_name, head.owner, &head.num, head.LPN);
					if (strcmp(head.LPN, LPN) == 0)
					{
						printf("%-10s\t%-10s\t%-4d\t%-10s\n",
							head.LPN, head.owner, head.num, head.car_name);
						printf("---------------------------------------------------\n");
						break;
					}
				}
				printf("**************************************************\n\n");
			}
			else     //未获取编号与车牌号，按照内容比对检索
			{
				int n = 1;
				if (c == 1 && b != 1)     //只获取到车主姓名
				{
					printf("车主姓名  \t车辆型号  \t编号\t车牌号\n");
					printf("---------------------------------------------------\n");
					while (1)
					{
						fscanf(fp, "%s%s%d%s", head.car_name, head.owner, &head.num, head.LPN);
						if (feof(fp))
						{
							break;
						}
						if (strcmp(head.owner, owner) == 0)
						{
							n = 0;
							printf("%-10s\t%-10s\t%-4d\t%-10s\n",
								head.owner, head.car_name, head.num, head.LPN);
							printf("---------------------------------------------------\n");
						}
					}
					if (n)
					{
						t = 1;
						printf("查询无果...\n");
					}
					printf("**************************************************\n\n");
				}
				if (c == 1 && b == 1)     //获取到车主信息与车辆型号
				{
					printf("车主姓名  \t车辆型号  \t编号\t车牌号\n");
					printf("---------------------------------------------------\n");
					while (1)
					{

						fscanf(fp, "%s%s%d%s",
							head.car_name, head.owner, &head.num, head.LPN);
						if (feof(fp))
						{
							break;
						}
						if (strcmp(head.owner, owner) == 0 && strcmp(head.car_name, Car_name) == 0)  //需同时满足输入条件
						{
							n = 0;
							printf("%-10s\t%-10s\t%-4d\t%-10s\n",
								head.owner, head.car_name, head.num, head.LPN);
							printf("---------------------------------------------------\n");
						}
					}
					if (n)
					{
						t = 1;
						printf("查询无果...\n");
					}
					printf("**************************************************\n\n");
				}
				if (b == 1 && c != 1)     //只获取到车辆型号
				{
					printf("车辆型号  \t车主姓名  \t编号\t车牌号\n");
					printf("---------------------------------------------------\n");
					while (1)
					{

						fscanf(fp, "%s%s%d%s",
							head.car_name, head.owner, &head.num, head.LPN);
						if (feof(fp))
						{
							break;
						}
						if (strcmp(head.car_name, Car_name) == 0)
						{
							n = 0;
							printf("%-10s\t%-10s\t%-4d\t%-10s\n",
								head.car_name, head.owner, head.num, head.LPN);
							printf("---------------------------------------------------\n");
						}
					}
					if (n)
					{
						t = 1;
						printf("查询无果...\n");
					}
					printf("**************************************************\n\n");
				}
			}
		}
		if (C != NULL)
		{
			if (t)
			{
				system("cls");
				printf("查询无果。。。请再次查询并输入有效信息\n");
			}
			else
			{
				C->num = head.num;
				strcpy(C->car_name, head.car_name);
				strcpy(C->LPN, head.LPN);
				strcpy(C->owner, head.owner);
				break;
			}
		}
		else
			break;
	}
	fclose(fp);
	system("pause");
	system("cls");
}
void find_3()
{
	FILE *fp, *FP;
	fp = fopen("./num.txt", "r");
	FP = fopen("./ALL_Carport.txt", "r");
	int num, A_C;
	fscanf(fp, "%d", &num);
	fscanf(FP, "%d", &A_C);
	printf("\n\n*该停车场内已有车辆:%d", num);
	printf("\n\n-----------------------");
	printf("\n\n*该停车场内车位总数:%d", A_C);
	printf("\n\n-----------------------\n\n");
	fclose(fp);
	fclose(FP);
	system("pause");
	system("cls");
	return;
}
void Car_modification()							//修改信息
{
	FILE *fp;
	Information_Car C_M, *Car, *car;
	Information_Car head = { 0 };
	int a;
	int x, y, z;
	printf("\n修改前请先查询想修改内容\n");
	while (1)
	{
		find_2(&C_M);
		printf("\n\n输入1确认进入修改,输入2放弃修改并退出，输入其他内容再次进行查询:");
		scanf("%d", &a);
		system("cls");
		if (a == 1)
			break;
		if (a == 2)
		{
			system("cls");
			printf("\n已放弃修改\n");
			system("pause");
			system("cls");
			return;
		}
	}
	getchar();				//清空缓冲区
	char Jump;
	printf("\n请输入修改内容\n");
	while (true)
	{
		x = y = z = 0;
		printf("---------------------------------------------\n");
		printf("车主姓名(跳过请按0,按其他任意键继续输入)\n");
		Jump = getch();
		if (Jump != '0')
		{
			x = 1;
			printf("请输入(车主姓名):");
			scanf("%s", C_M.owner); getchar();
		}
		printf("车辆名称(跳过请按0,按其他任意键继续输入)\n");
		Jump = getch();
		if (Jump != '0')
		{
			y = 1;
			printf("请输入(车辆名称):");
			scanf("%s", C_M.car_name); getchar();
		}
		printf("车牌号(跳过请按0,按其他任意键继续输入)\n");
		Jump = getch();
		if (Jump != '0')
		{
			z = 1;
			printf("请输入(车牌号):");
			scanf("%s", C_M.LPN); getchar();
		}
		if (x == 0 && y == 0 && z == 0)
		{
			system("cls");
			printf("\n请输入有价值的修改信息\n");
		}
		else
			break;
	}
	fp = fopen("./Car.txt", "r");
	while (1)
	{
		car = (Information_Car*)malloc(sizeof(Information_Car));
		fscanf(fp, "%s%s%d%s", car->car_name, car->owner, &car->num, car->LPN);
		if (feof(fp))
			break;
		car->next = head.next;
		head.next = car;
	}
	fclose(fp);
	fp = fopen("./Car.txt", "w");
	car = head.next;
	while (car != NULL)
	{
		if (car->num == C_M.num)
			fprintf(fp, "%s%c%s%c%d %s%c"
				, C_M.car_name, ' ', C_M.owner, ' ', C_M.num, C_M.LPN, ' ');
		else
			fprintf(fp, "%s%c%s%c%d %s%c"
				, car->car_name, ' ', car->owner, ' ', car->num, car->LPN, ' ');			//将信息输出到文件，空字符作为间隔，以便之后读取
		car = car->next;
		printf("*");																	//成功录入输出一个*作为提示
	}
	fclose(fp);
	system("cls");
	printf("\n\n修改成功...\n\n");
	system("pause");
	system("cls");
}
void modification()
{
	printf("\n\n-------------------------\n");
	printf("\n欢迎进入信息修改系统\n\n");
	printf("设置新的车位总数请按1\n\n");
	printf("修改车辆信息请按2\n\n");
	printf("-------------------------\n\n");
	printf("请按键选择\n\n");
	char t;
	while (true)
	{
		t = getch();
		system("cls");
		if (t == '2')
		{
			Car_modification(); break;
		}
		else if (t == '1')
		{
			All_carport_modification(); break;
		}
		else
		{
			printf("\n\n-------------------------");
			printf("\n\n\t按键错误\n\n");
			printf("设置新的车位总数请按1\n\n");
			printf("修改车辆信息请按2\n\n");
			printf("-------------------------\n\n");
			printf("请按键选择\n");
		}
	}
	return;
}
void find_menu()         //查询功能菜单
{
	int n;
	bool leap = false;
	while (1)
	{
		printf("\n********************************\n\n");    //菜单
		printf("            查询系统              \n\n");
		printf("#查询停车场内全部车辆信息请输入1\n\n");
		printf("#查询指定车辆信息请输入2\n\n");
		printf("#车辆信息统计请输入3\n\n");
		printf("#返回主菜单请输入0\n\n");
		printf("********************************\n\n");
		printf("请输入对应号码:");
		while (1)
		{	
			n = getch() - 48;
			printf("%d", n);
			// scanf("%d", &n);
			// getchar();				//清空缓冲区
			if (n < 0 || n>3)
			{
				printf("\n错误号码，请再次输入:");
			}
			else
				break;
		}
		system("cls");
		switch (n)
		{
		case 1:
			find_1(); break;
		case 2:
			find_2(NULL); break;
		case 3:
			find_3(); break;
		case 0:
			leap = true; break;
		default:
			break;
		}
		if (leap)
			break;
	}
	return;
}
void delte()					//删除功能
{
	Information_Car head = { 0 };
	Information_Car *car;
	Information_Car Car;
	FILE *fp, *FP;
	int num = 0;
	char Jump = 0;
	int a, b;
	a = b = 0;
	fp = fopen("./Car.txt", "r");
	printf("\n请输入您想要删除信息的关键内容\n\n");
	while (1)       //获取用户想删除的信息
	{
		printf("编号(跳过请按输入0,按其他任意键后继续输入)\n");
		Jump = getch();
		if (Jump != '0')
		{
			printf("请输入(编号):");
			a = 1;
			scanf("%d", &Car.num);
			getchar();     //清空缓冲区
		}
		Jump = 0;
		printf("\n车牌号(跳过请按输入0,按其他任意键后继续输入)\n");
		Jump = getch();
		if (Jump != '0')
		{
			printf("请输入(车牌号):");
			b = 1;
			scanf("%s", Car.LPN);
			getchar();     //清空缓冲区
		}
		if (a == b&&a == 0)
		{
			system("cls");
			printf("\n请输入有效信息\n");
		}
		else
		{
			system("cls"); break;
		}
	}
	int p = 1;
	while (true)
	{
		car = (Information_Car*)malloc(sizeof(Information_Car));
		fscanf(fp, "%s%s%d%s", car->car_name, car->owner, &car->num, car->LPN);
		if (a = 1)
		{
			if (Car.num == car->num)      //将信息输出给用户，提供判断
			{
				p = 0;
				printf("\n你所要删除的信息如下,请确认(输入1确定，输入2放弃删除并退出)\n\n");
				printf("编号\t车主姓名  \t车辆型号  \t车牌号\n");
				printf("---------------------------------------------------\n");
				printf("%-4d\t%-10s\t%-10s\t%-10s\n",
					car->num, car->owner, car->car_name, car->LPN);
				printf("---------------------------------------------------\n");
				int a;
				printf("\n请确认您的选择(1或2):");
				while (1)
				{
					scanf("%d", &a);
					system("cls");
					if (a != 2 && a != 1)
						printf("\n\n\n#请输入正确的号码(1确定/2放弃并退出):");
					if (a == 1)
						break;
					if (a == 2)
					{
						printf("\n\n退出删除系统...\n\n");
						system("pause");
						system("cls");
						fclose(fp);
						return;
					}

				}
			}
		}
		else
		{
			if (strcmp(Car.LPN, car->LPN) == 0)
			{
				p = 0;
				printf("\n你所要删除的信息如下,请确认(输入1确定，输入2退出)\n");
				printf("编号\t车主姓名  \t车辆型号  \t车牌号\n");
				printf("%-4d\t%-10s\t%-10s\t%-10s\n",
					car->num, car->owner, car->car_name, car->LPN);
				int a;
				Car.num = car->num;
				printf("\n请确认您的选择:");
				while (1)
				{
					scanf("%d", &a);
					system("cls");
					if (a != 2 && a != 1)
						printf("请输入正确的号码:");
					if (a == 1)
						break;
					if (a == 2)
					{
						printf("退出删除系统。。。");
						fclose(fp);
						return;
					}
				}
			}
		}
		if (feof(fp))
		{
			if (p)
			{
				printf("\n*未能检索到相关信息\n\n");
				fclose(fp);
				return;
			}
			break;
		}
		car->next = head.next;
		head.next = car;
	}
	free(car);
	fclose(fp);
	fp = fopen("./Car.txt", "w");
	car = head.next;
	while (car != NULL)      //将链表中的信息按照条件输出到文件
	{
		if (car->num != Car.num && strcmp(car->LPN, Car.LPN) != 0)
		{
			if (car->num > Car.num)
				car->num -= 1;
			num++;
			fprintf(fp, "%s%c%s%c%d %s%c"
				, car->car_name, ' ', car->owner, ' ', car->num, car->LPN, ' ');
			printf("*");
		}
		car = car->next;
	}
	printf("\n\n删除成功，数据已更新...\n\n");
	FP = fopen("./num.txt", "w");                             //重置车辆数目
	fprintf(FP, "%d", num);										//将新数据输出到对应文件中
	fclose(fp);
	fclose(FP);
	system("pause");
	system("cls");
}
void record()
{
	int num, Carport;
	FILE *fp, *FP, *Car_port;
	fp = fopen("./Car.txt", "r+");
	FP = fopen("./num.txt", "r");
	Car_port = fopen("./ALL_Carport.txt", "r");
	fscanf(Car_port, "%d", &Carport);
	fscanf(FP, "%d", &num);
	Information_Car *Car;
	Information_Car head = { 0 };			//建立链表头
	fseek(fp, 0L, 2);
	fclose(FP);
	while (true)
	{
		Car = (Information_Car*)malloc(sizeof(Information_Car));      //动态获取内存空间
		Car->num = ++num;
		if ((num - 1) >= Carport)									//判断车位是否饱和
		{
			num--;
			printf("\n#warning!!!车位已满\n\n");
			system("pause");
			system("cls");
			break;
		}
		printf("\n\n请输入车辆名称:");
		scanf("%s", Car->car_name);
		if (strcmp(Car->car_name, "exit") == 0)
		{
			system("cls");
			printf("\n\n结束录入...返回主菜单\n\n");
			system("pause");
			system("cls");
			num--;
			break;
		}
		printf("\n\n请输入车主名称:");
		scanf("%s", Car->owner);
		printf("\n\n请输入车牌号:");
		scanf("%s", Car->LPN);
		Car->next = head.next;
		head.next = Car;
		printf("\n\n录入成功，请继续输入，输入车辆名称为 exit 时结束\n\n");
	}
	Car = head.next;
	FP = fopen("./num.txt", "w");
	fprintf(FP, "%d", num);
	while (Car != NULL)						//遍历链表
	{
		fprintf(fp, "%s%c%s%c%d %s%c"
			, Car->car_name, ' ', Car->owner, ' ', Car->num, Car->LPN, ' ');			//将信息输出到文件，空字符作为间隔，以便之后读取
		Car = Car->next;
		printf(" *");																	//成功录入输出一个*作为提示
	}
	fclose(fp);
	fclose(FP);
	fclose(Car_port);
	return;
}

void password()       //密码管理模块
{
	FILE *fp;
	char a[9] = { 0 }, b[9] = { 0 };
	int i;
	int psw;
	while (true)
	{	
		system("cls");
		printf("\n\n请输入新密码(8位密码):");
		i = 0;
		while (i < 8)
		{
			psw = getch();
			if (psw == 8)
			{	
				if (i == 0)
				{
					continue;
				}
				else
				{
					i--;
					system("cls");
					printf("\n\n请输入新密码(8位密码):");
					for (int j=0; j<i; j++)
					{
						printf("*");
					}
				}	
			}
			else
			{
				printf("*");
				a[i] = psw;
				i++;
			}
		}
		system("cls");
		printf("\n\n再次确认密码:");
		i = 0;
		while (i < 8)
		{	
			psw = getch();
			if (psw == 8)
			{	
				if (i == 0)
				{
					continue;
				}
				else
				{
					i--;
					system("cls");
					printf("\n\n再次确认密码:");
					for (int j=0; j<i; j++)
					{
						printf("*");
					}	
				}
			}
			else
			{
				b[i] = psw;
				printf("*");
				i++;
			}
		}
		if (strcmp(a, b) == 0)     //两次输入一致进入该模块
		{
			fp = fopen("./user.txt", "w");
			for (i = 0; i < 8; i++)		 //存储新密码,并对密码进行加密（以字符ASCII码值存储到文件中）
			{
				if (i == 7)
					fprintf(fp, "%d", a[i]);
				else
				fprintf(fp,"%d\n", a[i]);
			}
			break;                   //退出大循环
		}
		else
		{
			system("cls"); printf("\n\n错误:两次输入不一致\n\n");
		}
	}
	fclose(fp);
	printf("\n\n修改密码成功，请牢记新密码！\n\n");
	system("pause");
	system("cls");
}
int main()
{
	Judge();				//调用函数判断文件是否存在、数据是否正确，并做相关处理
	system("cls");			//清屏
	char a[9] = { 0 };
	int b[9] = { 0 };
	char t;
	int i, select, All_Carport, p = 3;
	int n = 1;
	FILE *fp1, *fp2;
	fp1 = fopen("./user.txt", "r");				//与密码文件建立关联
	fp2 = fopen("./ALL_Carport.txt", "r+");		//与车位总数文件建立关联
	fscanf(fp2, "%d", &All_Carport);
	printf("\n********************************\n\n");        //美化界面与提示字符 
	printf("      欢迎来到泊车管理系统      \n\n");
	while (true)
	{
		i = 0;
		n = 1;
		int psw;
		printf("#请输入密码:");
		while (i < 8)
		{	
			psw = getch();
			if (psw == 8)
			{	
				if (i == 0)
				{
					continue;
				}
				else
				{
					i--;
					system("cls");
					printf("\n********************************\n\n");        //美化界面与提示字符 
					printf("      欢迎来到泊车管理系统      \n\n");
					printf("#请输入密码:");
					for (int j=0; j<i; j++)
					{
						printf("*");
					}
				}
			}
			else
			{
				a[i] = psw;
				printf("*");
				i++;
			}
		}
		system("cls");
		for (i = 0; i < 8; i++)
		{
			fscanf(fp1, "%d", &b[i]);
		}
		for (i = 0; i < 8; i++)
		{
			if (a[i] != b[i])
				n = 0;
		}
		if (n)				//密码输入正确进入该模块
		{
			if (All_Carport == 0)			//判断车位总数是否已经设置
			{
				printf("\n*********请设置车位总数*********\n");
				printf("\n#请输入车位总数:");
				scanf("%d", &All_Carport);
				system("cls");
				fprintf(fp2, "%d", All_Carport);
			}
			break;
		}
		else
		{
			p--;
			if (p == 0)				//控制密码输入错误次数
			{
				printf("\n!  !  !  !  !\n你输入密码错误次数已达3次，即将退出...\n");
				return 0;
			}
			printf("\n\n密码错误 请再次输入 按1继续 按其他任意键退出\n\n");
			t = getch();
			system("cls");
			if (t == '1')
			{
				if (p == 2)
					printf("\n##你还有%d次机会\n\n", p);
				else
					printf("\n###你仅剩%d次机会\n\n", p);
			}
			else
			{
				printf("\n\n即将退出...\t\n\n");
				return 0;
			}
		}
	}
	fclose(fp1);
	fclose(fp2);
	while (true)                       //重复主菜单
	{
		bool leap = false;
		select = menu();
		switch (select)                 //检索对应选项
		{
		case 1:
		{	printf("\n\n录入信息...（以 exit 结束）\n"); record(); } break;
		case 2:
			delte(); break;
		case 3:
		{	printf("\n查询系统..."); find_menu(); }break;
		case 4:
			password(); break;
		case 5:
			modification(); break;
		case 6:
			use_explain(); break;
		case 0:
		{	printf("\n\n\n即将退出...\n\n"); leap = true; } break;
		}
		if (leap)
			return 0;						//退出主函数
	}
	return 0;
}