import pygame.font, pygame.event, pygame.draw, string
from pygame import *
from pygame.locals import *

def display_box(screen, message,RECT):
	# "Print a message in a box in the middle of the screen"
	fontobject = pygame.font.Font(None,18)
	pygame.draw.rect(screen, (0,0,0),RECT, 0)
	pygame.draw.rect(screen, (255,255,255),RECT, 1)
	if len(message) != 0:
		screen.blit(fontobject.render(message, 1, (255,255,255)),(RECT[0]+2,RECT[1]+RECT[3]/3))
	pygame.display.flip()

def which_btn(mousex,mousey,btn_list):
    for btn in btn_list:
        if pygame.Rect(btn).collidepoint(mousex,mousey):
            # print(btn_list.index(btn))
            return btn_list.index(btn)
    return -1

def main():
	screen = pygame.display.set_mode((320,240))
	name_rect = (30,30,100,30)
	ip_rect = (30,70,100,30)
	connect_rect = (70,150,80,30)
	confirm_rect = (170,150,80,30)
	pygame.font.init()
	name_string = []
	ip_string = []
	flag = True
	btn_list = [name_rect,ip_rect,connect_rect,confirm_rect]
	idx=0
	connect_string = pygame.font.Font(None,18).render("connect", 1, (255,255,255))
	c_rect = connect_string.get_rect()
	c_rect.center = pygame.draw.rect(screen,(150,150,150),connect_rect).center
	screen.blit(connect_string,c_rect)
	confirm_string = pygame.font.Font(None,18).render("confirm", 1, (255,255,255))
	c_rect = confirm_string.get_rect()
	c_rect.center = pygame.draw.rect(screen,(150,150,150),confirm_rect).center
	screen.blit(confirm_string,c_rect)
	display_box(screen, "name" + ": " + "".join(name_string),name_rect)
	display_box(screen, "ip" + ": " + "".join(ip_string),ip_rect)
	while flag:
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				mousex, mousey = event.pos
				idx = which_btn(mousex,mousey,btn_list)
				if idx==3:
					flag=False
					break
			elif event.type == KEYDOWN and idx==0:
				inkey = event.key
				if inkey == K_BACKSPACE:
					name_string = name_string[0:-1]
				elif inkey == K_RETURN:
					flag = False
					break
				elif inkey == K_MINUS:
					name_string.append("_")
				elif inkey <= 127:
					name_string.append(chr(inkey))
				display_box(screen, "name" + ": " + "".join(name_string),name_rect)
			elif event.type == KEYDOWN and idx==1:
				inkey = event.key
				if inkey == K_BACKSPACE:
					ip_string = ip_string[0:-1]
				elif inkey == K_RETURN:
					flag = False
					break
				elif inkey == K_MINUS:
					ip_string.append("_")
				elif inkey <= 127:
					ip_string.append(chr(inkey))
				display_box(screen, "ip" + ": " + "".join(ip_string),ip_rect)
			name = "".join(name_string)
			ip = "".join(ip_string)
	print("name: "+name)
	print("ip: "+ip)

if __name__ == '__main__': 
	main()