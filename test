#RequireAdmin
Dim $i
$i=1
While $i <=20
   Run("C:\Users\wuzhongshan\Desktop\测试\战旗加速器\暴击加速器测试\暴击加速器.exe");启动客户端进程
   sleep(1000);延时1秒
   WinWaitActive("暴击加速器");等待出现title “暴击加速器”
   MouseClick("left",1055,187,1);点击坐标为1055，187的像素位,登录按钮
   Sleep(1000)
   MouseClick("left",1078,653,1);点击 用户账号登陆按钮
   Sleep(1000)
   MouseClick("left",957,567,1);点击确定登陆按钮
   Sleep(1000)
   If WinWaitActive("暴击加速器") Then;判断，如果再次出现title-暴击加速器，则杀掉进程进入下一个循环
	  ;MsgBox(64,"测试结果","succ")
	  ;WinWaitActive("测试结果")
	  ;MouseClick("left",970,600,1)
	  ProcessClose("暴击加速器.exe")
	  ;MouseClick("left",970,600,1)
	  $i+=1
	  ContinueLoop
   Else
	  MsgBox(64,"测试结果","fail");如果没有出现期望的title，则闪退，向桌面抛出弹窗，提示fail，推出循环
	  ExitLoop
   EndIf
WEnd