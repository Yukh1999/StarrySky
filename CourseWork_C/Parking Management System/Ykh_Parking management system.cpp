/*
*C���Կγ����:��������ϵͳ
*����ʱ��:2017/6/8	15:36
*����:�����
*Ժϵ:��ѧԺ
*�༶:Ӧ������1601
*���һ���޸�����:2017/6/14
*/

#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<conio.h>
void use_explain()
{
	printf("\n\n*��������ϵͳʹ��˵��\n\n");
	printf("*�������û��޸�ʱ����Ϊ��λ\n\n*���������а�������ɾ�����ո���ȶ�����Ϊ��Ч�ַ�\n\n");
	system("pause");
	system("cls");
	printf("\n\n*ע�����ʹ��ʱ����ʾ���������������ó�λ����\n\n");
	system("pause");
	system("cls");
	printf("\n\n*ʹ�ô�ϵͳʱ��ע����ʾ�ַ������뻹�ǰ���\n");
	printf("\n*��������������������ݺ󰴻س����������\n");
	printf("\n*����������ֱ�Ӱ�������������ʱ������ΪӢ�����뷨������������Ϣ����)\n\n");
	system("pause");
	system("cls");
	return;
}
void Judge()                                    //�����ļ�
{
	void password();
	FILE*fp;
	int n;
	fp = fopen("./ALL_Carport.txt", "r");
	if (fp == NULL)                            //��ʧ�ܣ��������ļ�
	{
		fp = fopen("./ALL_Carport.txt", "w");
		fprintf(fp, "%d", 0);
		fclose(fp);
		printf("\n\n���ν���ϵͳ�������Ķ�ʹ��˵��\n\n");
		system("pause");
		system("cls");
		use_explain();
		printf("��������ϵͳ...\n\n");
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
	if (fp == NULL)							//��ʧ�ܣ��������ļ�
	{
		fp = fopen("./user.txt", "w");
		fclose(fp);
		printf("����ʹ��������������\n");
		password();
	}
	else
		fclose(fp);
	fp = fopen("./Car.txt", "r");
	if (fp == NULL)							//��ʧ�ܣ��������ļ�
	{
		fp = fopen("./Car.txt", "w");
		fclose(fp);
	}
	else
		fclose(fp);
	fp = fopen("./num.txt", "r");
	if (fp == NULL)							//��ʧ�ܣ��������ļ�
	{
		fp = fopen("./num.txt", "w");
		fprintf(fp, "%d", 0);
		fclose(fp);
	}
	else
	{
		int a;
		a = fscanf(fp, "%d", &n);
		if (n < 0 || a <= 0)								//��Ϣ¼�벻�ɹ�����Ϣ���󽫻��ʼ��
		{
			fclose(fp);
			fp = fopen("./num.txt", "w");
			fprintf(fp, "%d", 0);
			fclose(fp);
			fp = fopen("./Car.txt", "w");
			fclose(fp);
			printf("\n!!!������Ϣ���ݴ��ڴ����ѳ�ʼ����������¼����Ϣ\n");
		}
		else
			fclose(fp);
	}
	return;
}
struct Information_Car    //����ṹ��(������Ϣ��
{
	char car_name[15];    //��������
	char owner[15];       //��������
	int num;              //�������
	char LPN[15];         //���ƺ�
	Information_Car *next;//����
};
int menu()                //�˵���
{
	int a;
	printf("\n********************************\n\n");
	printf("*          ��������ϵͳ        *\n\n");
	printf("         ¼����Ϣ:������1\n\n");
	printf("         ɾ����Ϣ:������2\n\n");
	printf("         ��ѯ��Ϣ:������3\n\n");
	printf("         �޸�����:������4\n\n");
	printf("         �޸���Ϣ:������5\n\n");
	printf("         ʹ��˵��:������6\n\n");
	printf("         �˳�ϵͳ:������0\n\n");
	printf("********************************\n\n");
	printf("         ��ѡ����Ҫʹ�õĹ���:");
	a = getch() - 48;
	printf("\n");
	if (a < 0 || a > 6)                     //�����ѡ���ں���ʱ��������ʾ
	{
		system("cls"); printf("         ��������ȷ����...");
		return a;
	}
	else
	{
		system("cls");
		return a;                         //�������ֵ���ظ�������
	}
}
void All_carport_modification()            //�޸ĳ�λ����
{
	FILE *fp;
	int num, ALL_Carport;
	fp = fopen("./num.txt", "r");
	fscanf(fp, "%d", &num);
	fclose(fp);
	while (1)                           //ѭ��ֱ������ɹ�
	{
		printf("\n\n#�������µĳ�λ����:");
		scanf("%d", &ALL_Carport);
		getchar();                      //��ջ�����
		if (ALL_Carport < num)          //�ж������ó�λ�����Ƿ�С���Ѵ��ڳ�����Ŀ
		{
			char n = 0;
			printf("\n���ò�����ͣ�����ڳ�����Ŀ�Ѵ����³�λ��\n\n");
			printf("��1������������������˳�����\n");
			n = getch();
			system("cls");
			if (n != '1')
			{
				printf("\n!�˳���λ����\n\n");
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
	printf("\n��λ�������³ɹ���Ϊ:%d\n\n", ALL_Carport);
	fclose(fp);
	system("pause");
	system("cls");
	return;
}
void find_1()				//��ѯȫ����Ϣ
{
	Information_Car*car, *Car;
	Information_Car head = { 0 };
	FILE*fp;
	int n, a = 0;
	int x=0;
	int t=0;
	fp = fopen("./Car.txt", "r");				//���ļ�
	printf("\n�����˳��鿴�밴1\n\n");
	printf("������˳��鿴�밴2\n\n");
	printf("������˳��鿴�밴3\n\n");
	printf("�������Ӧ���:");
	while (1)
	{	
		n = getch() - 48;
		printf("%d", n);
		// scanf("%d", &n);	//����ѡ��
		// getchar();				//��ջ�����
		if (n > 3 || n < 1)
			printf("\n��������ȷ�ĺ���:");
		else
			break;
	}
	system("cls");
	if (n == 1)
	{
		Information_Car *pre;			//������һλָ��
		car = (Information_Car*)malloc(sizeof(Information_Car));		//��ȡ�ڴ�ռ�
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
			if (feof(fp))    //���ļ�ĩβ����ֹ¼��
			{
				break;
			}
			while (Car != NULL)					//��������
			{
				if ((Car->num) > (car->num))    //�ҵ�Ŀ�꽫���ڴ�ӵ�Ŀ����һλ����
				{
					car->next = pre->next;
					pre->next = car;
					n = 0;
					break;
				}
				pre = Car;					//�洢��һλָ��
				Car = Car->next;
			}
			if (n)					//δ�ҵ�Ŀ�꣬�����ڴ��������ĩβ
			{
				car->next = pre->next;
				pre->next = car;
			}
		}
		free(car);					//�ͷŶ����ڴ�
		Car = head.next;			//ָ��ָ������ͷ��һλ���������洢��Ϣ�ĵ�һλ
		printf("---------------------------------------------------\n");
		printf("���\t��������  \t�����ͺ�  \t���ƺ�\n");
		printf("---------------------------------------------------\n");
		if (x)
		{
			printf("�����ݣ�����¼��...\n");
			printf("---------------------------------------------------\n");
			system("pause");
			system("cls");
			return;
		}
		else
		while (Car != NULL)			//��������
		{
			a++;
			printf("%-4d\t%-10s\t%-10s\t%-10s\n",
				Car->num, Car->owner, Car->car_name, Car->LPN);   //����Ϣ�������Ļ
			Car = Car->next;		//��ת����һλ
			printf("---------------------------------------------------\n");
		}
		while (true)
		{
			t++;
			char s;
			printf("����鿴�밴1,������������˳�\n");
			s = getch();
			system("cls");
			if (s == '1')
			{
				int i, j;
				printf("---------------------------------------------------\n");
				printf("���\t��������  \t�����ͺ�  \t���ƺ�\n");
				printf("---------------------------------------------------\n");
				if (t % 2 == 0)
				{
					Car = head.next;
					while (Car != NULL)			//��������
					{
						printf("%-4d\t%-10s\t%-10s\t%-10s\n",
							Car->num, Car->owner, Car->car_name, Car->LPN);   //����Ϣ�������Ļ
						Car = Car->next;		//��ת����һλ
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
						Car->num, Car->owner, Car->car_name, Car->LPN);   //����Ϣ�������Ļ
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
	if (n == 2)      //����ͬ��
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
		printf("�����ͺ�  \t��������  \t���\t���ƺ�\n");
		printf("---------------------------------------------------\n");
		if (x)
		{
			printf("�����ݣ�����¼��...\n");
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
			printf("����鿴�밴1,������������˳�\n");
			s = getch();
			system("cls");
			if (s == '1')
			{
				int i, j;
				printf("---------------------------------------------------\n");
				printf("�����ͺ�  \t��������  \t���\t���ƺ�\n");
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
						Car->car_name, Car->owner, Car->num, Car->LPN);   //����Ϣ�������Ļ
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
	if (n == 3)    //����ͬ��
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
		printf("���ƺ�    \t��������\t���\t�����ͺ�\n");
		printf("---------------------------------------------------\n");
		if (x)
		{
			printf("�����ݣ�����¼��...\n");
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
			printf("����鿴�밴1,������������˳�\n");
			s = getch();
			system("cls");
			if (s == '1')
			{
				int i, j;
				printf("---------------------------------------------------\n");
				printf("���ƺ�    \t��������\t���\t�����ͺ�\n");
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
						Car->LPN, Car->owner, Car->num, Car->car_name);  //����Ϣ�������Ļ
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
	fclose(fp);    //�Ͽ�ָ�����ļ��Ĺ���
	return;
}
void find_2(Information_Car*C)        //���ؼ���Ϣ��ѯ
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
	printf("��������Ҫ��ѯ�������Ϣ...\n");
	while (true)
	{
		rewind(fp);
		t = 0;
		while (1)     //ѭ��ֱ���ɹ����յ���ȷ��Ϣ
		{
			Jump = 0;
			a = b = c = d = 0;
			printf("\n���(�����밴0,��������������������)\n");
			Jump = getch();
			if (Jump != '0')
			{
				printf("������(���):");
				a = 1;
				scanf("%d", &num);
				getchar();     //��ջ�����
			}
			Jump = 0;
			printf("\n�����ͺ�(�����밴����0,��������������������)\n");
			Jump = getch();
			if (Jump != '0')
			{
				printf("������(�����ͺ�):");
				b = 1;
				scanf("%s", Car_name);
				getchar();     //��ջ�����
			}
			Jump = 0;
			printf("\n��������(�����밴����0,��������������������)\n");
			Jump = getch();
			if (Jump != '0')
			{
				printf("������(��������):");
				c = 1;
				scanf("%s", owner);
				getchar();     //��ջ�����
			}
			Jump = 0;
			printf("\n���ƺ�(�����밴����0,��������������������)\n");
			Jump = getch();
			if (Jump != '0')
			{
				printf("������(���ƺ�):");
				d = 1;
				scanf("%s", LPN);
				getchar();     //��ջ�����
			}
			if (a == 0 && b == 0 && c == 0 && d == 0)
			{
				system("cls");
				printf("\nδ��ȡ��Ϣ������������ؼ���...\n");
			}
			else
				break;
		}
		system("cls");
		printf("\n��ѯ��Ϣ����\n");
		printf("**************************************************\n");
		if (a == 1)      //��������ţ�ֱ�Ӽ��������Ϣ
		{
			printf("���\t��������  \t�����ͺ�  \t���ƺ�\n");
			printf("---------------------------------------------------\n");
			while (1)
			{
				if (feof(fp))    //�������ļ�ĩβ���޽��������ѭ��
				{
					t = 1;
					printf("��ѯ�޹�...\n");
					break;
				}
				fscanf(fp, "%s%s%d%s", head.car_name, head.owner, &head.num, head.LPN);   //��ȡ�ļ��������Ϣ
				if (head.num == num)    //�ж��Ƿ���������Ϣ��ͬ
				{
					printf("%-4d\t%-10s\t%-10s\t%-10s\n",
						head.num, head.owner, head.car_name, head.LPN);   //�������������Ļ
					printf("---------------------------------------------------\n");
					break;
				}
			}
			printf("**************************************************\n\n");
		}
		else
		{
			if (d == 1)    //δ��ȡ��ţ���ȡ�����ƺź�Ҳֱ�Ӽ���  ����ͬ��
			{
				printf("���ƺ�    \t��������\t���\t�����ͺ�\n");
				printf("---------------------------------------------------\n");
				while (1)
				{
					if (feof(fp))
					{
						t = 1;
						printf("��ѯ�޹�...\n");
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
			else     //δ��ȡ����복�ƺţ��������ݱȶԼ���
			{
				int n = 1;
				if (c == 1 && b != 1)     //ֻ��ȡ����������
				{
					printf("��������  \t�����ͺ�  \t���\t���ƺ�\n");
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
						printf("��ѯ�޹�...\n");
					}
					printf("**************************************************\n\n");
				}
				if (c == 1 && b == 1)     //��ȡ��������Ϣ�복���ͺ�
				{
					printf("��������  \t�����ͺ�  \t���\t���ƺ�\n");
					printf("---------------------------------------------------\n");
					while (1)
					{

						fscanf(fp, "%s%s%d%s",
							head.car_name, head.owner, &head.num, head.LPN);
						if (feof(fp))
						{
							break;
						}
						if (strcmp(head.owner, owner) == 0 && strcmp(head.car_name, Car_name) == 0)  //��ͬʱ������������
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
						printf("��ѯ�޹�...\n");
					}
					printf("**************************************************\n\n");
				}
				if (b == 1 && c != 1)     //ֻ��ȡ�������ͺ�
				{
					printf("�����ͺ�  \t��������  \t���\t���ƺ�\n");
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
						printf("��ѯ�޹�...\n");
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
				printf("��ѯ�޹����������ٴβ�ѯ��������Ч��Ϣ\n");
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
	printf("\n\n*��ͣ���������г���:%d", num);
	printf("\n\n-----------------------");
	printf("\n\n*��ͣ�����ڳ�λ����:%d", A_C);
	printf("\n\n-----------------------\n\n");
	fclose(fp);
	fclose(FP);
	system("pause");
	system("cls");
	return;
}
void Car_modification()							//�޸���Ϣ
{
	FILE *fp;
	Information_Car C_M, *Car, *car;
	Information_Car head = { 0 };
	int a;
	int x, y, z;
	printf("\n�޸�ǰ���Ȳ�ѯ���޸�����\n");
	while (1)
	{
		find_2(&C_M);
		printf("\n\n����1ȷ�Ͻ����޸�,����2�����޸Ĳ��˳����������������ٴν��в�ѯ:");
		scanf("%d", &a);
		system("cls");
		if (a == 1)
			break;
		if (a == 2)
		{
			system("cls");
			printf("\n�ѷ����޸�\n");
			system("pause");
			system("cls");
			return;
		}
	}
	getchar();				//��ջ�����
	char Jump;
	printf("\n�������޸�����\n");
	while (true)
	{
		x = y = z = 0;
		printf("---------------------------------------------\n");
		printf("��������(�����밴0,�������������������)\n");
		Jump = getch();
		if (Jump != '0')
		{
			x = 1;
			printf("������(��������):");
			scanf("%s", C_M.owner); getchar();
		}
		printf("��������(�����밴0,�������������������)\n");
		Jump = getch();
		if (Jump != '0')
		{
			y = 1;
			printf("������(��������):");
			scanf("%s", C_M.car_name); getchar();
		}
		printf("���ƺ�(�����밴0,�������������������)\n");
		Jump = getch();
		if (Jump != '0')
		{
			z = 1;
			printf("������(���ƺ�):");
			scanf("%s", C_M.LPN); getchar();
		}
		if (x == 0 && y == 0 && z == 0)
		{
			system("cls");
			printf("\n�������м�ֵ���޸���Ϣ\n");
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
				, car->car_name, ' ', car->owner, ' ', car->num, car->LPN, ' ');			//����Ϣ������ļ������ַ���Ϊ������Ա�֮���ȡ
		car = car->next;
		printf("*");																	//�ɹ�¼�����һ��*��Ϊ��ʾ
	}
	fclose(fp);
	system("cls");
	printf("\n\n�޸ĳɹ�...\n\n");
	system("pause");
	system("cls");
}
void modification()
{
	printf("\n\n-------------------------\n");
	printf("\n��ӭ������Ϣ�޸�ϵͳ\n\n");
	printf("�����µĳ�λ�����밴1\n\n");
	printf("�޸ĳ�����Ϣ�밴2\n\n");
	printf("-------------------------\n\n");
	printf("�밴��ѡ��\n\n");
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
			printf("\n\n\t��������\n\n");
			printf("�����µĳ�λ�����밴1\n\n");
			printf("�޸ĳ�����Ϣ�밴2\n\n");
			printf("-------------------------\n\n");
			printf("�밴��ѡ��\n");
		}
	}
	return;
}
void find_menu()         //��ѯ���ܲ˵�
{
	int n;
	bool leap = false;
	while (1)
	{
		printf("\n********************************\n\n");    //�˵�
		printf("            ��ѯϵͳ              \n\n");
		printf("#��ѯͣ������ȫ��������Ϣ������1\n\n");
		printf("#��ѯָ��������Ϣ������2\n\n");
		printf("#������Ϣͳ��������3\n\n");
		printf("#�������˵�������0\n\n");
		printf("********************************\n\n");
		printf("�������Ӧ����:");
		while (1)
		{	
			n = getch() - 48;
			printf("%d", n);
			// scanf("%d", &n);
			// getchar();				//��ջ�����
			if (n < 0 || n>3)
			{
				printf("\n������룬���ٴ�����:");
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
void delte()					//ɾ������
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
	printf("\n����������Ҫɾ����Ϣ�Ĺؼ�����\n\n");
	while (1)       //��ȡ�û���ɾ������Ϣ
	{
		printf("���(�����밴����0,��������������������)\n");
		Jump = getch();
		if (Jump != '0')
		{
			printf("������(���):");
			a = 1;
			scanf("%d", &Car.num);
			getchar();     //��ջ�����
		}
		Jump = 0;
		printf("\n���ƺ�(�����밴����0,��������������������)\n");
		Jump = getch();
		if (Jump != '0')
		{
			printf("������(���ƺ�):");
			b = 1;
			scanf("%s", Car.LPN);
			getchar();     //��ջ�����
		}
		if (a == b&&a == 0)
		{
			system("cls");
			printf("\n��������Ч��Ϣ\n");
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
			if (Car.num == car->num)      //����Ϣ������û����ṩ�ж�
			{
				p = 0;
				printf("\n����Ҫɾ������Ϣ����,��ȷ��(����1ȷ��������2����ɾ�����˳�)\n\n");
				printf("���\t��������  \t�����ͺ�  \t���ƺ�\n");
				printf("---------------------------------------------------\n");
				printf("%-4d\t%-10s\t%-10s\t%-10s\n",
					car->num, car->owner, car->car_name, car->LPN);
				printf("---------------------------------------------------\n");
				int a;
				printf("\n��ȷ������ѡ��(1��2):");
				while (1)
				{
					scanf("%d", &a);
					system("cls");
					if (a != 2 && a != 1)
						printf("\n\n\n#��������ȷ�ĺ���(1ȷ��/2�������˳�):");
					if (a == 1)
						break;
					if (a == 2)
					{
						printf("\n\n�˳�ɾ��ϵͳ...\n\n");
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
				printf("\n����Ҫɾ������Ϣ����,��ȷ��(����1ȷ��������2�˳�)\n");
				printf("���\t��������  \t�����ͺ�  \t���ƺ�\n");
				printf("%-4d\t%-10s\t%-10s\t%-10s\n",
					car->num, car->owner, car->car_name, car->LPN);
				int a;
				Car.num = car->num;
				printf("\n��ȷ������ѡ��:");
				while (1)
				{
					scanf("%d", &a);
					system("cls");
					if (a != 2 && a != 1)
						printf("��������ȷ�ĺ���:");
					if (a == 1)
						break;
					if (a == 2)
					{
						printf("�˳�ɾ��ϵͳ������");
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
				printf("\n*δ�ܼ����������Ϣ\n\n");
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
	while (car != NULL)      //�������е���Ϣ��������������ļ�
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
	printf("\n\nɾ���ɹ��������Ѹ���...\n\n");
	FP = fopen("./num.txt", "w");                             //���ó�����Ŀ
	fprintf(FP, "%d", num);										//���������������Ӧ�ļ���
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
	Information_Car head = { 0 };			//��������ͷ
	fseek(fp, 0L, 2);
	fclose(FP);
	while (true)
	{
		Car = (Information_Car*)malloc(sizeof(Information_Car));      //��̬��ȡ�ڴ�ռ�
		Car->num = ++num;
		if ((num - 1) >= Carport)									//�жϳ�λ�Ƿ񱥺�
		{
			num--;
			printf("\n#warning!!!��λ����\n\n");
			system("pause");
			system("cls");
			break;
		}
		printf("\n\n�����복������:");
		scanf("%s", Car->car_name);
		if (strcmp(Car->car_name, "exit") == 0)
		{
			system("cls");
			printf("\n\n����¼��...�������˵�\n\n");
			system("pause");
			system("cls");
			num--;
			break;
		}
		printf("\n\n�����복������:");
		scanf("%s", Car->owner);
		printf("\n\n�����복�ƺ�:");
		scanf("%s", Car->LPN);
		Car->next = head.next;
		head.next = Car;
		printf("\n\n¼��ɹ�����������룬���복������Ϊ exit ʱ����\n\n");
	}
	Car = head.next;
	FP = fopen("./num.txt", "w");
	fprintf(FP, "%d", num);
	while (Car != NULL)						//��������
	{
		fprintf(fp, "%s%c%s%c%d %s%c"
			, Car->car_name, ' ', Car->owner, ' ', Car->num, Car->LPN, ' ');			//����Ϣ������ļ������ַ���Ϊ������Ա�֮���ȡ
		Car = Car->next;
		printf(" *");																	//�ɹ�¼�����һ��*��Ϊ��ʾ
	}
	fclose(fp);
	fclose(FP);
	fclose(Car_port);
	return;
}

void password()       //�������ģ��
{
	FILE *fp;
	char a[9] = { 0 }, b[9] = { 0 };
	int i;
	int psw;
	while (true)
	{	
		system("cls");
		printf("\n\n������������(8λ����):");
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
					printf("\n\n������������(8λ����):");
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
		printf("\n\n�ٴ�ȷ������:");
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
					printf("\n\n�ٴ�ȷ������:");
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
		if (strcmp(a, b) == 0)     //��������һ�½����ģ��
		{
			fp = fopen("./user.txt", "w");
			for (i = 0; i < 8; i++)		 //�洢������,����������м��ܣ����ַ�ASCII��ֵ�洢���ļ��У�
			{
				if (i == 7)
					fprintf(fp, "%d", a[i]);
				else
				fprintf(fp,"%d\n", a[i]);
			}
			break;                   //�˳���ѭ��
		}
		else
		{
			system("cls"); printf("\n\n����:�������벻һ��\n\n");
		}
	}
	fclose(fp);
	printf("\n\n�޸�����ɹ������μ������룡\n\n");
	system("pause");
	system("cls");
}
int main()
{
	Judge();				//���ú����ж��ļ��Ƿ���ڡ������Ƿ���ȷ��������ش���
	system("cls");			//����
	char a[9] = { 0 };
	int b[9] = { 0 };
	char t;
	int i, select, All_Carport, p = 3;
	int n = 1;
	FILE *fp1, *fp2;
	fp1 = fopen("./user.txt", "r");				//�������ļ���������
	fp2 = fopen("./ALL_Carport.txt", "r+");		//�복λ�����ļ���������
	fscanf(fp2, "%d", &All_Carport);
	printf("\n********************************\n\n");        //������������ʾ�ַ� 
	printf("      ��ӭ������������ϵͳ      \n\n");
	while (true)
	{
		i = 0;
		n = 1;
		int psw;
		printf("#����������:");
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
					printf("\n********************************\n\n");        //������������ʾ�ַ� 
					printf("      ��ӭ������������ϵͳ      \n\n");
					printf("#����������:");
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
		if (n)				//����������ȷ�����ģ��
		{
			if (All_Carport == 0)			//�жϳ�λ�����Ƿ��Ѿ�����
			{
				printf("\n*********�����ó�λ����*********\n");
				printf("\n#�����복λ����:");
				scanf("%d", &All_Carport);
				system("cls");
				fprintf(fp2, "%d", All_Carport);
			}
			break;
		}
		else
		{
			p--;
			if (p == 0)				//������������������
			{
				printf("\n!  !  !  !  !\n�����������������Ѵ�3�Σ������˳�...\n");
				return 0;
			}
			printf("\n\n������� ���ٴ����� ��1���� ������������˳�\n\n");
			t = getch();
			system("cls");
			if (t == '1')
			{
				if (p == 2)
					printf("\n##�㻹��%d�λ���\n\n", p);
				else
					printf("\n###���ʣ%d�λ���\n\n", p);
			}
			else
			{
				printf("\n\n�����˳�...\t\n\n");
				return 0;
			}
		}
	}
	fclose(fp1);
	fclose(fp2);
	while (true)                       //�ظ����˵�
	{
		bool leap = false;
		select = menu();
		switch (select)                 //������Ӧѡ��
		{
		case 1:
		{	printf("\n\n¼����Ϣ...���� exit ������\n"); record(); } break;
		case 2:
			delte(); break;
		case 3:
		{	printf("\n��ѯϵͳ..."); find_menu(); }break;
		case 4:
			password(); break;
		case 5:
			modification(); break;
		case 6:
			use_explain(); break;
		case 0:
		{	printf("\n\n\n�����˳�...\n\n"); leap = true; } break;
		}
		if (leap)
			return 0;						//�˳�������
	}
	return 0;
}