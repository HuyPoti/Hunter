import pygame

#button class
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color = base_color
		self.hovering_color = hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if text_input == "HUNTER":
			self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
		else:
			self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos - 15))
		if text_input == "HUNTER":
			self.image = pygame.transform.scale(self.image, (self.text_rect.width*4, self.text_rect.height*2.5))
		else:
			self.image = pygame.transform.scale(self.image, (self.text_rect.width + 100, self.text_rect.height * 1.8))
		# width = image.get_width()
		# height = image.get_height()
		# self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.clicked = False
	def update(self, screen):
		# draw button on screen
		screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)
	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False
	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)
	def turnon(self):
		self.text_input = "MUSIC ON"
		self.text = self.font.render(self.text_input, True, self.base_color)
		self.image = pygame.transform.scale(self.image, (self.text_rect.width + 100, self.text_rect.height * 1.8))
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
	def turnoff(self):
		self.text_input = "MUSIC OFF"
		self.text = self.font.render(self.text_input, True, self.base_color)
		self.image = pygame.transform.scale(self.image, (self.text_rect.width + 100, self.text_rect.height * 1.8))
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))


	# def draw(self, surface):
	# 	action = False
	# 	#get mouse position
	# 	pos = pygame.mouse.get_pos()

	# 	#check mouseover and clicked conditions
	# 	if self.rect.collidepoint(pos):
	# 		if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
	# 			self.clicked = True
	# 			action = True

	# 	if pygame.mouse.get_pressed()[0] == 0:
	# 		self.clicked = False

	# 	#draw button on screen
	# 	surface.blit(self.image, self.rect)

	# 	return action