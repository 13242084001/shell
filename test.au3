#RequireAdmin
Dim $i
$i=1
While $i <=20
   Run("C:\Users\wuzhongshan\Desktop\����\ս�������\��������������\����������.exe");�����ͻ��˽���
   sleep(1000);��ʱ1��
   WinWaitActive("����������");�ȴ�����title ��������������
   MouseClick("left",1055,187,1);�������Ϊ1055��187������λ,��¼��ť
   Sleep(1000)
   MouseClick("left",1078,653,1);��� �û��˺ŵ�½��ť
   Sleep(1000)
   MouseClick("left",957,567,1);���ȷ����½��ť
   Sleep(1000)
   If WinWaitActive("����������") Then;�жϣ�����ٴγ���title-��������������ɱ�����̽�����һ��ѭ��
	  ;MsgBox(64,"���Խ��","succ")
	  ;WinWaitActive("���Խ��")
	  ;MouseClick("left",970,600,1)
	  ProcessClose("����������.exe")
	  ;MouseClick("left",970,600,1)
	  $i+=1
	  ContinueLoop
   Else
	  MsgBox(64,"���Խ��","fail");���û�г���������title�������ˣ��������׳���������ʾfail���Ƴ�ѭ��
	  ExitLoop
   EndIf
WEnd