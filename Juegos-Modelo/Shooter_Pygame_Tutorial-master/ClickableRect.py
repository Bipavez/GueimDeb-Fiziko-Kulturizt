import pygame, utils

interact = None

#Clickable Rect
class ClickableRect():
    def __init__(self, pos, size):

        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = pos

        self.hasClicked = False

    def isMouseOver(self):
        cur = pygame.mouse.get_pos()

        if self.rect.left < cur[0] < self.rect.right and self.rect.top < cur[1] < self.rect.bottom:
            return True
        else:
            return False

    def doMouseOver(self):
        pass

    def isLeftMouseDown(self):
        return self.hasClicked

    def doLeftMouseDown(self):
        pass

    def isClicked(self):
        global interact
        mouse = pygame.mouse.get_pressed()

        if self.isMouseOver():
            if mouse[0] and self.hasClicked == False and not interact:
                self.hasClicked = True
                interact = self
                return True
        if mouse[0] == False and self.hasClicked == True:
            self.hasClicked = False
            interact = None

        return False

    def doClick(self):
        print "You Clicked a Rect"

    def update(self, gw):

        if self.isMouseOver():
            self.doMouseOver()

        if self.isLeftMouseDown():
            self.doLeftMouseDown()

        if self.isClicked():
            self.doClick()

#Button
class Button(ClickableRect):
    def __init__(self, pos, size, color, action):
        ClickableRect.__init__(self, pos, size)

        self.color = color
        self.image = pygame.Surface(size)
        self.image.fill(self.color)
        self.action = action

    def doMouseOver(self):
        overlay = pygame.Surface(self.rect.size)
        overlay.set_alpha(120)
        overlay.fill(utils.black)
        self.image.blit(overlay, (0, 0))

    def doLeftMouseDown(self):
        self.image.fill(utils.green)

    def doClick(self):
        self.action()

    def draw(self, gw):
        gw.blit(self.image, self.rect)

    def update(self, gw):
        self.image.fill(self.color)

        ClickableRect.update(self, gw)

        self.draw(gw)


#Text Button
class TextButton(Button):
    def __init__(self, pos, size, color, text, action):
        Button.__init__(self, pos, size, color, action)

        self.fontSize = self.rect.h
        self.text = utils.getFont(size=self.fontSize, style='bold').render(text, True, utils.black)
        self.textRect = self.text.get_rect()

        while self.textRect.w > self.rect.w:
            self.fontSize -= 2
            self.text = utils.getFont(size=self.fontSize, style='bold').render(text, True, utils.black)
            self.textRect = self.text.get_rect()


    def draw(self, gw):
        self.image.blit(self.text, ((self.rect.w - self.textRect.w)/2, (self.rect.h - self.textRect.h)/2))
        Button.draw(self, gw)