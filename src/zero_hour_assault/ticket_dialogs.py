import wx
import pygame
import globals as g
import ctypes
import datetime
import sound
from translation import translate as _
from speech import speak
from network import event_receive
from Miscellaneous import is_game_window_active
from events import process_events
class ticket_dlg(wx.Dialog):
	def __init__(self,title,messages,isclosed,ispending):
		wx.Dialog.__init__(self,None,title=title)
		self.title=title
		wx.StaticText(self,label=_("Ticket messages"));self.txt2=wx.TextCtrl(self,style=wx.TE_READONLY|wx.TE_MULTILINE,size=(640,480));self.txt2.SetValue(messages)
		self.messages=messages
		self.isclosed=isclosed
		if not isclosed:
			wx.StaticText(self,label=_("Send new message"));self.txt=wx.TextCtrl(self,style=wx.TE_MULTILINE,size=(640,480))
			wx.Button(self,label=_("Send message")).Bind(wx.EVT_BUTTON,self.on_send_message)
		if self.isclosed and "points at " not in self.messages:
			wx.StaticText(self,label=_("rate the ticket"))
			self.lst=wx.ListBox(self)
			for i in range(1,11):
				self.lst.Append(str(i))
			wx.Button(self,label=_("rate")).Bind(wx.EVT_BUTTON,self.on_point)
		wx.Button(self,label=_("Return to previous menu")).Bind(wx.EVT_BUTTON,self.on_back)
		self.t=wx.Timer()
		self.t.Bind(wx.EVT_TIMER,self.loop)
		self.t.Start(1)
	def on_back(self,event):
		g.screen.fill((0,0,0)); pygame.display.flip(); self.t.Destroy(); self.Destroy(); g.app.ExitMainLoop(); pygame.event.clear()
	def loop(self,event):
		g.netloop()
		g.fallloop()
		g.fallcheck()
		g.fallingloop()
		self.SetFocus()
	def on_send_message(self,event):
		usermess=self.txt.GetValue()
		if usermess!="":
			g.n.send_reliable(0,"answerticket{}[]"+self.title+"{}[]"+usermess,2)
			self.txt2.SetValue(self.txt2.GetValue()+"\n"+g.name+", "+send_wait("getdate")+"\n"+usermess+"\n")
			self.txt.Clear()
	def on_point(self,event):
		usermess=self.lst.GetStringSelection()
		if usermess!="" and usermess is not None:
			g.n.send_reliable(0,"pointticket{}[]"+self.title+"{}[]"+usermess,2)
			self.on_back(None)
def ticket_dialog(title,messages,isclosed,ispending):
	dlg=ticket_dlg(title,messages,isclosed,ispending)
	pygame.display.set_caption(chr(65533))
	ctypes.windll.user32.SetParent(dlg.GetHandle(),pygame.display.get_wm_info()["window"])
	def on_key_down(event):
		if g.shouldsetcaption2: pygame.display.set_caption("Zero hour assault "+g.ver); g.shouldsetcaption2=False
		event.Skip()
	dlg.Bind(wx.EVT_CHAR_HOOK,on_key_down); g.shouldsetcaption2=True
	dlg.Show(); g.app.MainLoop()
	if len(g.p1)!=0:
		p1=g.p1.pop()
		p2=g.p2.pop()
		p3=g.p3.pop()
		p4=g.p4.pop()
		g.n.send_reliable(0,"mpacket "+p1,0)
		g.n.send_reliable(0,"mitems "+p3,0)
		g.serverside_menu(p1,p2,p3,p4)
class ticket_dlg2(wx.Dialog):
	def __init__(self,title,messages,isclosed,ispending):
		wx.Dialog.__init__(self,None,title=title)
		self.title=title
		self.messages=messages
		self.isclosed=isclosed
		self.ispending=ispending

		wx.StaticText(self,label=_("Ticket messages"));self.txt2=wx.TextCtrl(self,style=wx.TE_READONLY|wx.TE_MULTILINE,size=(640,480));self.txt2.SetValue(messages)
		if not isclosed:
			wx.StaticText(self,label=_("Send new message"));self.txt=wx.TextCtrl(self,style=wx.TE_MULTILINE,size=(640,480))
			self.send=wx.Button(self,label=_("Send message"));self.send.Bind(wx.EVT_BUTTON,self.on_send_message)
		if isclosed:
			self.open=wx.Button(self,label=_("Open ticket"));self.open.Bind(wx.EVT_BUTTON,self.on_open_ticket)
		if not isclosed and not ispending:
			self.close=wx.Button(self,label=_("Close ticket"));self.close.Bind(wx.EVT_BUTTON,self.on_close_ticket)
		if not ispending and not isclosed:
			self.p1=wx.Button(self,label=_("Add pending status"));self.p1.Bind(wx.EVT_BUTTON,self.on_add_pending_status)
		if ispending:
			self.p2=wx.Button(self,label=_("Remove pending status"));self.p2.Bind(wx.EVT_BUTTON,self.on_remove_pending_status)
		self.back=wx.Button(self,label=_("Return to previous menu"));self.back.Bind(wx.EVT_BUTTON,self.on_back)
		self.t=wx.Timer()
		self.t.Bind(wx.EVT_TIMER,self.loop)
		self.t.Start(1)
	def on_back(self,event):
		g.screen.fill((0,0,0)); pygame.display.flip(); self.t.Destroy(); self.Destroy(); g.app.ExitMainLoop(); pygame.event.clear()

	def loop(self,event):
		g.netloop()
		g.fallloop()
		self.SetFocus()
	def on_send_message(self,event):
		usermess=self.txt.GetValue()
		if usermess!="":
			g.n.send_reliable(0,"answerticket{}[]"+self.title+"{}[]"+usermess,2)
			self.messages+="\n"+g.name+": "+usermess+send_wait("getdate")
			self.txt2.SetValue(self.txt2.GetValue()+"\n"+g.name+": "+usermess+send_wait("getdate"))
			self.txt.Clear()
		if self.ispending:
			self.ispending=False
			self.txt2.Destroy()
			self.txt.Destroy()
			self.back.Destroy()
			self.send.Destroy()
			try: self.p1.Destroy()
			except: pass
			try: self.p2.Destroy()
			except: pass
			try: self.open.Destroy()
			except: pass
			try: self.close.Destroy()
			except: pass
			if self.isclosed:
				self.open=wx.Button(self,label=_("Open ticket"));self.open.Bind(wx.EVT_BUTTON,self.on_open_ticket)
			if not self.isclosed and not self.ispending:
				self.close=wx.Button(self,label=_("Close ticket"));self.close.Bind(wx.EVT_BUTTON,self.on_close_ticket)
			if not self.ispending and not self.isclosed:
				self.p1=wx.Button(self,label=_("Add pending status"));self.p1.Bind(wx.EVT_BUTTON,self.on_add_pending_status)
			if self.ispending:
				self.p2=wx.Button(self,label=_("Remove pending status"));self.p2.Bind(wx.EVT_BUTTON,self.on_remove_pending_status)
			self.back=wx.Button(self,label=_("Return to previous menu"));self.back.Bind(wx.EVT_BUTTON,self.on_back)
			wx.StaticText(self,label=_("Ticket messages"));self.txt2=wx.TextCtrl(self,style=wx.TE_READONLY|wx.TE_MULTILINE,size=(640,480));self.txt2.SetValue(self.messages)
			if not self.isclosed: wx.StaticText(self,label=_("Send new message"));self.txt=wx.TextCtrl(self,style=wx.TE_MULTILINE,size=(640,480))
			self.send=wx.Button(self,label=_("Send message"));self.send.Bind(wx.EVT_BUTTON,self.on_send_message)
			self.p1.SetFocus()

	def on_close_ticket(self,event):
		g.n.send_reliable(0,"closeticket{}[]"+self.title,2)
		self.txt2.SetValue(self.txt2.GetValue()+"\nthis ticket was closed by "+g.name+" in "+send_wait("getdate"))
		self.isclosed=True
		self.messages+="\nthis ticket was closed by "+g.name+" in "+send_wait("getdate")
		self.back.Destroy()
		self.txt2.Destroy()
		self.txt.Destroy()
		self.send.Destroy()
		try: self.p1.Destroy()
		except: pass
		try: self.p2.Destroy()
		except: pass
		try: self.open.Destroy()
		except: pass
		try: self.close.Destroy()
		except: pass
		if self.isclosed:
			self.open=wx.Button(self,label=_("Open ticket"));self.open.Bind(wx.EVT_BUTTON,self.on_open_ticket)
		if not self.isclosed and not self.ispending:
			self.close=wx.Button(self,label=_("Close ticket"));self.close.Bind(wx.EVT_BUTTON,self.on_close_ticket)
		if not self.ispending and not self.isclosed:
			self.p1=wx.Button(self,label=_("Add pending status"));self.p1.Bind(wx.EVT_BUTTON,self.on_add_pending_status)
		if self.ispending:
			self.p2=wx.Button(self,label=_("Remove pending status"));self.p2.Bind(wx.EVT_BUTTON,self.on_remove_pending_status)
		self.back=wx.Button(self,label=_("Return to previous menu"));self.back.Bind(wx.EVT_BUTTON,self.on_back)
		wx.StaticText(self,label=_("Ticket messages"));self.txt2=wx.TextCtrl(self,style=wx.TE_READONLY|wx.TE_MULTILINE,size=(640,480));self.txt2.SetValue(self.messages)
	def on_open_ticket(self,event):
		g.n.send_reliable(0,"openticket{}[]"+self.title,2)
		self.messages+="\nthis ticket was reopened by "+g.name+" in "+send_wait("getdate")
		self.isclosed=False
		self.back.Destroy()
		self.txt2.Destroy()
		try: self.p1.Destroy()
		except: pass
		try: self.p2.Destroy()
		except: pass
		try: self.open.Destroy()
		except: pass
		try: self.close.Destroy()
		except: pass
		if self.isclosed:
			self.open=wx.Button(self,label=_("Open ticket"));self.open.Bind(wx.EVT_BUTTON,self.on_open_ticket)
		if not self.isclosed and not self.ispending:
			self.close=wx.Button(self,label=_("Close ticket"));self.close.Bind(wx.EVT_BUTTON,self.on_close_ticket)
		if not self.ispending and not self.isclosed:
			self.p1=wx.Button(self,label=_("Add pending status"));self.p1.Bind(wx.EVT_BUTTON,self.on_add_pending_status)
		if self.ispending:
			self.p2=wx.Button(self,label=_("Remove pending status"));self.p2.Bind(wx.EVT_BUTTON,self.on_remove_pending_status)
		self.back=wx.Button(self,label=_("Return to previous menu"));self.back.Bind(wx.EVT_BUTTON,self.on_back)
		wx.StaticText(self,label=_("Ticket messages"));self.txt2=wx.TextCtrl(self,style=wx.TE_READONLY|wx.TE_MULTILINE,size=(640,480));self.txt2.SetValue(self.messages)
		wx.StaticText(self,label=_("Send new message"));self.txt=wx.TextCtrl(self,style=wx.TE_MULTILINE,size=(640,480))
		self.send=wx.Button(self,label=_("Send message"));self.send.Bind(wx.EVT_BUTTON,self.on_send_message)
	def on_add_pending_status(self,event):
		g.n.send_reliable(0,"maketicketpending{}[]"+self.title,2)
		self.txt2.SetValue(self.txt2.GetValue()+"\nthis ticket was marked as pending by "+g.name+" in "+send_wait("getdate"))
		self.messages+="\nthis ticket was marked as pending by "+g.name+" in "+send_wait("getdate")
		self.ispending=True
		self.txt2.Destroy()
		self.txt.Destroy()
		self.back.Destroy()
		self.send.Destroy()
		try: self.p1.Destroy()
		except: pass
		try: self.p2.Destroy()
		except: pass
		try: self.open.Destroy()
		except: pass
		try: self.close.Destroy()
		except: pass
		if self.isclosed:
			self.open=wx.Button(self,label=_("Open ticket"));self.open.Bind(wx.EVT_BUTTON,self.on_open_ticket)
		if not self.isclosed and not self.ispending:
			self.close=wx.Button(self,label=_("Close ticket"));self.close.Bind(wx.EVT_BUTTON,self.on_close_ticket)
		if not self.ispending and not self.isclosed:
			self.p1=wx.Button(self,label=_("Add pending status"));self.p1.Bind(wx.EVT_BUTTON,self.on_add_pending_status)
		if self.ispending:
			self.p2=wx.Button(self,label=_("Remove pending status"));self.p2.Bind(wx.EVT_BUTTON,self.on_remove_pending_status)
		self.back=wx.Button(self,label=_("Return to previous menu"));self.back.Bind(wx.EVT_BUTTON,self.on_back)
		wx.StaticText(self,label=_("Ticket messages"));self.txt2=wx.TextCtrl(self,style=wx.TE_READONLY|wx.TE_MULTILINE,size=(640,480));self.txt2.SetValue(self.messages)
		if not self.isclosed: wx.StaticText(self,label=_("Send new message"));self.txt=wx.TextCtrl(self,style=wx.TE_MULTILINE,size=(640,480))
		self.send=wx.Button(self,label=_("Send message"));self.send.Bind(wx.EVT_BUTTON,self.on_send_message)
	def on_remove_pending_status(self,event):
		g.n.send_reliable(0,"maketicketnotpending{}[]"+self.title,2)
		self.txt2.SetValue(self.txt2.GetValue()+"\nthis ticket was marked as not pending by "+g.name+" in "+send_wait("getdate"))
		self.messages+="\nthis ticket was marked as not pending by "+g.name+" in "+send_wait("getdate")
		self.ispending=False
		self.txt2.Destroy()
		self.txt.Destroy()
		self.back.Destroy()
		self.send.Destroy()
		try: self.p1.Destroy()
		except: pass
		try: self.p2.Destroy()
		except: pass
		try: self.open.Destroy()
		except: pass
		try: self.close.Destroy()
		except: pass
		if self.isclosed:
			self.open=wx.Button(self,label=_("Open ticket"));self.open.Bind(wx.EVT_BUTTON,self.on_open_ticket)
		if not self.isclosed and not self.ispending:
			self.close=wx.Button(self,label=_("Close ticket"));self.close.Bind(wx.EVT_BUTTON,self.on_close_ticket)
		if not self.ispending and not self.isclosed:
			self.p1=wx.Button(self,label=_("Add pending status"));self.p1.Bind(wx.EVT_BUTTON,self.on_add_pending_status)
		if self.ispending:
			self.p2=wx.Button(self,label=_("Remove pending status"));self.p2.Bind(wx.EVT_BUTTON,self.on_remove_pending_status)
		self.back=wx.Button(self,label=_("Return to previous menu"));self.back.Bind(wx.EVT_BUTTON,self.on_back)
		wx.StaticText(self,label=_("Ticket messages"));self.txt2=wx.TextCtrl(self,style=wx.TE_READONLY|wx.TE_MULTILINE,size=(640,480));self.txt2.SetValue(self.messages)
		if not self.isclosed: wx.StaticText(self,label=_("Send new message"));self.txt=wx.TextCtrl(self,style=wx.TE_MULTILINE,size=(640,480))
		self.send=wx.Button(self,label=_("Send message"));self.send.Bind(wx.EVT_BUTTON,self.on_send_message)
		self.p1.SetFocus()
def ticket_dialog2(title,messages,isclosed,ispending):

	dlg=ticket_dlg2(title,messages,isclosed,ispending)
	pygame.display.set_caption(chr(65533))
	ctypes.windll.user32.SetParent(dlg.GetHandle(),pygame.display.get_wm_info()["window"])
	def on_key_down(event):
		if g.shouldsetcaption2: pygame.display.set_caption("Zero hour assault "+g.ver); g.shouldsetcaption2=False
		event.Skip()
	dlg.Bind(wx.EVT_CHAR_HOOK,on_key_down); g.shouldsetcaption2=True
	dlg.Show(); g.app.MainLoop()
	if len(g.p1)!=0:
		p1=g.p1.pop()
		p2=g.p2.pop()
		p3=g.p3.pop()
		p4=g.p4.pop()
		g.n.send_reliable(0,"mpacket "+p1,0)
		g.n.send_reliable(0,"mitems "+p3,0)
		g.serverside_menu(p1,p2,p3,p4)

class create_ticket_dlg(wx.Dialog):
	def __init__(self):
		wx.Dialog.__init__(self,None,title=_("Create ticket"))

		wx.StaticText(self,label="Title")
		self.title=wx.TextCtrl(self,size=(640,480))
		wx.StaticText(self,label="Message")
		self.message=wx.TextCtrl(self,size=(640,480),style=wx.TE_MULTILINE)
		wx.StaticText(self,label=_("Department"))
		self.department=wx.Choice(self,choices=[_("support"),_("report a bug"),_("game suggestion"),_("report a player"),_("other")])
		self.department.SetSelection(0)
		self.agree=wx.CheckBox(self,label=_("By checking this box, I understand that this ticket I am making is for serious inquiries only, doesn't violate the games rules and that misuse of the ticket system in any way including but not limited to spam or misinformation of any kind could result in severe punishments to my account"))
		wx.Button(self,label=_("submit ticket")).Bind(wx.EVT_BUTTON,self.on_submit)
		wx.Button(self,label=_("Return to previous menu")).Bind(wx.EVT_BUTTON,self.on_back)
		self.t=wx.Timer()
		self.t.Bind(wx.EVT_TIMER,self.loop)
		self.t.Start(1)
		self.departments=["support","report a bug","game suggestion","report a player","other"]
	def on_back(self,event):
		g.screen.fill((0,0,0)); pygame.display.flip(); self.t.Destroy(); self.Destroy(); g.app.ExitMainLoop(); pygame.event.clear()

	def loop(self,event):
		g.netloop()
		g.fallloop()
		self.SetFocus()
	def on_submit(self,event):
		title=self.title.GetValue()
		message=self.message.GetValue()
		department=self.departments[self.department.GetSelection()]
		if not self.agree.GetValue(): speak("Please check the above checkbox to continue"); return
		if title!="" and message!="" and department!="":
			g.n.send_reliable(0,"newticket{}[]"+title+"{}[]"+message+"{}[]"+department,2)
			g.screen.fill((0,0,0)); pygame.display.flip(); self.t.Destroy(); self.Destroy(); g.app.ExitMainLoop(); pygame.event.clear()
def create_ticket_dialog():

	dlg=create_ticket_dlg()
	pygame.display.set_caption(chr(65533))
	ctypes.windll.user32.SetParent(dlg.GetHandle(),pygame.display.get_wm_info()["window"])
	def on_key_down(event):
		if g.shouldsetcaption2: pygame.display.set_caption("Zero hour assault "+g.ver); g.shouldsetcaption2=False
		event.Skip()
	dlg.Bind(wx.EVT_CHAR_HOOK,on_key_down); g.shouldsetcaption2=True
	dlg.Show(); g.app.MainLoop()
	if len(g.p1)!=0:
		p1=g.p1.pop()
		p2=g.p2.pop()
		p3=g.p3.pop()
		p4=g.p4.pop()
		g.n.send_reliable(0,"mpacket "+p1,0)
		g.n.send_reliable(0,"mitems "+p3,0)
		g.serverside_menu(p1,p2,p3,p4)

def send_wait(message):
	g.n.send_reliable(0,message,0)
	while 1:
		g.e=g.n.request()
		try:
			if g.e.type==event_receive and g.e.message.startswith("dateis "):
				return g.e.message.replace("dateis ","",1)
			if g.e.type==event_receive and not g.e.message.startswith("dateis "): g.netloop(False,False)
		except: pass