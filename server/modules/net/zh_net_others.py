import globals as g
import os
import time
import pickle
import json
import datetime
import urllib.parse
import requests
from threading import Thread
from timer import timer

def handle_channel_others(e):
	global languages
	if e.channel==5:
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if g.players[index].hidden: return
			mess=e.message
			send_to=[]
			if 1:
				for i in g.players:
					if g.players[index].name in i.blocks or i.name in send_to or i.voicemessage==0: continue
					if i.name==g.players[index].name and g.players[index].listen==1: g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,5); send_to.append(i.name); continue
					if i.name==g.players[index].name and g.players[index].listen==0: continue
					if i.map!=g.players[index].map or (i.map==g.players[index].map and i.distancecheck(g.players[index].x,g.players[index].y,g.players[index].z)>30): continue
					#if i.name not in send_to: g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,5); send_to.append(i.name)

			if g.players[index].voicechatmap==1:
				for i in g.players:
					if i.voicechatmap==0 or g.players[index].name in i.blocks or i.name in send_to or i.voicemessage==0: continue
					if i.name==g.players[index].name and g.players[index].listen==1: g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,5); send_to.append(i.name); continue
					if i.name==g.players[index].name and g.players[index].listen==0: continue
					if i.map!=g.players[index].map or (i.map==g.players[index].map and i.distancecheck(g.players[index].x,g.players[index].y,g.players[index].z)>30): continue
					g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,5); send_to.append(i.name)
			if g.players[index].voicechatgroup==1:
				for i in g.players:
					if i.voicechatgroup==0 or g.players[index].name in i.blocks or i.name in send_to or i.voicemessage==0: continue
					if i.name==g.players[index].name and g.players[index].listen==1: g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,5); send_to.append(i.name); continue
					if i.name==g.players[index].name and g.players[index].listen==0: continue
					if i.group!=g.players[index].group: continue
					if i.group=="": continue
					g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,5); send_to.append(i.name)

			if g.players[index].voicechatteam==1:
				for i in g.players:
					if i.voicechatteam==0 or g.players[index].name in i.blocks or i.name in send_to or i.voicemessage==0: continue
					if i.name==g.players[index].name and g.players[index].listen==1: g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,5); send_to.append(i.name); continue
					if i.name==g.players[index].name and g.players[index].listen==0: continue
					if i.matchteam!=g.players[index].matchteam and i.matchteam!="" and g.players[index].matchteam!="": continue
					if i.matchteam=="": continue
					g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,5); send_to.append(i.name)
			if g.players[index].voicechatfriend==1:
				for i in g.players:
					if i.voicechatfriend==0 or g.players[index].name in i.blocks or i.name in send_to or i.voicemessage==0: continue
					if i.name==g.players[index].name and g.players[index].listen==1: g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,5); send_to.append(i.name); continue
					if i.name==g.players[index].name and g.players[index].listen==0: continue
					if i.name not in g.players[index].friendlist: continue
					g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,5); send_to.append(i.name)
	if e.channel==6:
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if g.players[index].hidden: return
			mess=e.message
			send_to=[]
			if 1:
				for i in g.players:
					if g.players[index].name in i.blocks or i.name in send_to or i.voicemessage2==0: continue
					try:
						if i.name==g.players[index].name and g.players[index].listen==1: g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,6); send_to.append(i.name); continue
					except: pass
					if i.name==g.players[index].name and g.players[index].listen==0: continue
					if i.map!=g.players[index].map: continue
					#if i.name not in send_to: g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,6); send_to.append(i.name)

			if 1:
				for i in g.players:
					if g.players[index].name in i.blocks or i.name in send_to or i.voicemessage2==0: continue
					if i.name==g.players[index].name and g.players[index].listen==1:
						try: g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,6); send_to.append(i.name); continue
						except: pass
					if i.name==g.players[index].name and g.players[index].listen==0: continue
					if i.community!=g.players[index].community: continue
					if i.community=="": continue
					try: g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,6); send_to.append(i.name)
					except: pass


	if (e.channel==2):
	
		parsed=string_split(e.message, "{}[]", True)
		if parsed[0]=="answerticket":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				ticket=find_ticket_by_title(parsed[1])
				if ticket is None:
					g.n.send_reliable(e.peer_id,"Error, ticket not found!",0); return
				if ticket["closed"]:
					g.n.send_reliable(e.peer_id,"This ticket is closed, you can't answer!",0); return
				ticket["pending"]=False
				if g.players[index].dev:
					prank = "Support Team"
				elif g.players[index].is_admin():
					prank = "Support Team"
				elif g.players[index].moderator==True:
					prank = "Support Team"
				elif g.players[index].builder:
					prank = "Support Team"
				else:
					prank = ""
				if prank!="":
					ticket["messages"]+="\nSupport Team, "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"\n"+parsed[2]

				elif prank=="":
					ticket["messages"]+="\n"+g.players[index].name+", "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"\n"+parsed[2]

				ticket["lastupdate"]=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				g.n.send_reliable(e.peer_id,"Done, answer sent successfully.",0)
				adminsend(g.players[index].name+" answered to the "+ticket["title"]+" ticket, "+parsed[2])
				notify_admins("zero_hour_assault, "+g.players[index].name+" answered to the "+ticket["title"]+" ticket, "+parsed[2])

				getmail=file_get_contents("chars/"+ticket["owner"]+"/mail.usr")
				ticket["closetimer"].restart()
				#if is_enabled_ticket_mail(ticket["owner"]): send_mail(getmail,"Your ticket "+ticket["title"]+" has been updated","Hello<br>You'r ticket "+ticket["title"]+" is updated and answered by staff.<br>"+g.players[index].name+" answered you: "+parsed[2]+"<br>We will wait your answer back.<br>If you do not answer back within 24 hours, the ticket will automaticaly be closed.<br>Regards,<br>Nbm studios team")

				if g.players[index].name!=ticket["owner"]:
					ind=get_player_index_from(ticket["owner"])
					if ind>-1:
						g.n.send_reliable(g.players[ind].peer_id,"Your ticket with id "+ticket["id"]+" is updated, please check!",2)
						g.n.send_reliable(g.players[ind].peer_id,"play_s misc304.ogg",0)
					else:
						file_put_contents("chars/"+ticket["owner"]+"/ticketinform.usr","Your ticket with "+ticket["id"]+" is updated, please check!")
		if parsed[0]=="pointticket":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				file_delete("chars/"+g.players[index].name+"/rateneeded.usr")
				ticket=find_ticket_by_title(parsed[1])
				if ticket is None:
					g.n.send_reliable(e.peer_id,"Error, ticket not found!",0); return
				ticket["messages"]+="\n"+g.players[index].name+" rated this ticket "+parsed[2]+" points at "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"\n"
				ticket["lastupdate"]=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				g.n.send_reliable(e.peer_id,"Done, rating sent successfully.",0)
				adminsend(g.players[index].name+" rated "+parsed[2]+" points to the "+ticket["title"]+" ticket")
				notify_admins("zero hour assault, "+g.players[index].name+" rated "+parsed[2]+" points to the "+ticket["title"]+" ticket")


		if parsed[0]=="closeticket":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				ticket=find_ticket_by_title(parsed[1])
				if ticket is None:
					g.n.send_reliable(e.peer_id,"Error, ticket not found!",0); return
				if ticket["closed"]:
					g.n.send_reliable(e.peer_id,"This ticket is already closed!",0); return
				ticket["closed"]=True
				ticket["messages"]+="\nThis ticket was closed by Support Team in "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				ticket["lastupdate"]=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				adminsend(g.players[index].name+" closed the "+ticket["title"]+" ticket.")
				notify_admins("zero hour assault, "+g.players[index].name+" closed the "+ticket["title"]+" ticket.")
				getmail=file_get_contents("chars/"+ticket["owner"]+"/mail.usr")
				if is_enabled_ticket_mail(ticket["owner"]): send_mail(getmail,"your ticket "+ticket["title"]+" has been resolved and closed","Hello "+ticket["owner"]+"<br>your ticket "+ticket["title"]+" has been closed by Support Team.<br>Below is all the ticket messages:<br>"+ticket["messages"].replace("\n","<br>")+"<br>If you have more questions or need help, please create a support ticket again from the game or contact us at contact@nbmstudios.com<br>regards,<br>Nbm studios team")

				file_put_contents("chars/"+ticket["owner"]+"/rateneeded.usr","")
				g.n.send_reliable(g.players[index].peer_id,"Done, ticket closed successfully.",0)
				if g.players[index].name!=ticket["owner"]:
					ind=get_player_index_from(ticket["owner"])
					if ind>-1:
						g.n.send_reliable(g.players[ind].peer_id,"Your ticket with id "+ticket["id"]+" is closed",2)
					else:
						file_put_contents("chars/"+ticket["owner"]+"/ticketinform.usr","Your ticket with "+ticket["id"]+" is closed")

		if parsed[0]=="openticket":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				ticket=find_ticket_by_title(parsed[1])
				if ticket is None:
					g.n.send_reliable(e.peer_id,"Error, ticket not found!",0); return
				if not ticket["closed"]:
					g.n.send_reliable(e.peer_id,"This ticket is not closed!",0); return
				ticket["closed"]=False
				ticket["closetimer"].restart()
				ticket["messages"]+="\nThis ticket was reopened by Support Team at "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				ticket["lastupdate"]=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				adminsend(g.players[index].name+" reopened the "+ticket["title"]+" ticket.")
				notify_admins("zero hour assault, "+g.players[index].name+" reopened the "+ticket["title"]+" ticket.")
				g.n.send_reliable(e.peer_id,"Done, ticket reopened successfully.",0)
				getmail=file_get_contents("chars/"+ticket["owner"]+"/mail.usr")
				if is_enabled_ticket_mail(ticket["owner"]): send_mail(getmail,"your ticket "+ticket["title"]+" has been reopened","Hello "+ticket["owner"]+"<br>your ticket "+ticket["title"]+" has been reopened by Support Team.<br>We will answer you as soon as possible. We will resolve your issue soon.<br>regards,<br>Nbm studios team")

				if g.players[index].name!=ticket["owner"]:
					ind=get_player_index_from(ticket["owner"])
					if ind>-1:
						g.n.send_reliable(g.players[ind].peer_id,"Your ticket with id "+ticket["id"]+" is reopened",0)
					else:
						file_put_contents("chars/"+ticket["owner"]+"/ticketinform.usr","Your ticket with "+ticket["id"]+" is reopened")

		if parsed[0]=="maketicketpending":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				ticket=find_ticket_by_title(parsed[1])
				if ticket is None:
					g.n.send_reliable(e.peer_id,"Error, ticket not found!",0); return
				if ticket["pending"]:
					g.n.send_reliable(e.peer_id,"This ticket is already pending!",0); return
				ticket["pending"]=True
				ticket["messages"]+="\nThis ticket was marked as pending by Support Team at "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				ticket["lastupdate"]=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				adminsend(g.players[index].name+" made pending the "+ticket["title"]+" ticket.")
				notify_admins("zero hour assault, "+g.players[index].name+" made pending the "+ticket["title"]+" ticket.")
				g.n.send_reliable(e.peer_id,"Done, ticket made pending successfully.",0)
				#getmail=file_get_contents("chars/"+ticket["owner"]+"/mail.usr")
				#if is_enabled_ticket_mail(ticket["owner"]): send_mail(getmail,"your ticket "+ticket["title"]+" has been marked as pending","Hello "+ticket["owner"]+"<br>your ticket "+ticket["title"]+" has been marked as pending by "+g.players[index].name+"<br>We will answer you as soon as possible. We will resolve your issue soon.<br>Staff will make your ticket not pending and answer you once a solution is found to your problem.<br>regards,<br>Nbm studios team")

				if g.players[index].name!=ticket["owner"]:
					ind=get_player_index_from(ticket["owner"])
					if ind>-1:
						g.n.send_reliable(g.players[ind].peer_id,"Your ticket with id "+ticket["id"]+" is marked as pending",0)
					else:
						file_put_contents("chars/"+ticket["owner"]+"/ticketinform.usr","Your ticket with "+ticket["id"]+" is marked as pending")


		if parsed[0]=="maketicketnotpending":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				ticket=find_ticket_by_title(parsed[1])
				if ticket is None:
					g.n.send_reliable(e.peer_id,"Error, ticket not found!",0); return
				if not ticket["pending"]:
					g.n.send_reliable(e.peer_id,"This ticket is not pending!",0); return
				ticket["pending"]=False
				ticket["messages"]+="\nThis ticket was marked as not pending by Support Team at "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				ticket["lastupdate"]=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				ticket["closetimer"].restart()
				ticket["closetimer"].pause()
				adminsend(g.players[index].name+" made not pending the "+ticket["title"]+" ticket.")
				notify_admins("zero hour assault, "+g.players[index].name+" made not pending the "+ticket["title"]+" ticket.")
				g.n.send_reliable(e.peer_id,"Done, ticket made not pending successfully.",0)
				getmail=file_get_contents("chars/"+ticket["owner"]+"/mail.usr")
				if is_enabled_ticket_mail(ticket["owner"]): send_mail(getmail,"your ticket "+ticket["title"]+" has been marked as not pending","Hello "+ticket["owner"]+"<br>your ticket "+ticket["title"]+" has been marked as not pending by Support Team.<br>We will answer you as soon as possible. We will resolve your issue soon.<br>regards,<br>Nbm studios team")

				if g.players[index].name!=ticket["owner"]:
					ind=get_player_index_from(ticket["owner"])
					if ind>-1:
						g.n.send_reliable(g.players[ind].peer_id,"Your ticket with id "+ticket["id"]+" is marked as not pending",0)
					else:
						file_put_contents("chars/"+ticket["owner"]+"/ticketinform.usr","Your ticket with "+ticket["id"]+" is marked as not pending")


		if parsed[0]=="newticket":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				if file_exists("chars/"+g.players[index].name+"/rateneeded.usr"): g.n.send_reliable(e.peer_id,"you cannot create a new ticket without raing your last closed ticket",0); return
				found_tickets=0
				for ticket in g.tickets:
					if not ticket["closed"] and ticket["owner"]==g.players[index].name:
						found_tickets+=1
				if found_tickets>=5: g.n.send_reliable(e.peer_id,"You can't have more than 5 open tickets",0); return
				title=parsed[1]
				title="#"+str(len(g.tickets)+1)+" "+title
				g.tickets.append({"title":title,"closetimer":timer(),"messages":title+"\ndepartment\n"+parsed[3]+"\n"+g.players[index].name+", "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\n"+parsed[2]),"department":parsed[3],"closed":False,"pending":False,"owner":g.players[index].name,"id":"#"+str(len(g.tickets)+1),"lastupdate":str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),"createdate":str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))})
				g.n.send_reliable(g.players[index].peer_id,"play_s misc216.ogg",0)
				g.n.send_reliable(e.peer_id,"Done, ticket has been created with id: #"+str(len(g.tickets)),0)
				adminsend("The "+title+" ticket was created by "+g.players[index].name)
				notify_admins("zero hour assault, The "+title+" ticket was created by "+g.players[index].name + "\n\nMessages:\n" + g.tickets[-1]["messages"])
				save_tickets()

