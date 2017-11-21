import pygame, math

def get_fps():
    return 60.0 # Temporary; changed by main
    
def get_time():
    """
    Returns the time in milliseconds
    since pygame was initialised.
    """
    return pygame.time.get_ticks()
    
def colour_mix(a, b, amount):
    """
    Interpolates between
    colour a and colour b
    by amount.
    """
    
    # We could use LCH.
    # ... but that's expensive
    # so we'll just use normal
    # RGB interpolation
    
    if len(a) < 2 or len(a) > 4 or \
       len(b) < 2 or len(b) > 4:
        raise ValueError("Incorrect number of channels in colour")
    
    if len(a) == 3:
        a += [255]
    if len(b) == 3:
        b += [255]
    
    return [(x + (y-x)*amount) for x,y in zip(a,b)]



class BaseUIElement:
    def __init__(self):
        """
        Initialises the object.
        """
        pass
    
    def update(self):
        """
        An update function.
        Called every frame,
        regardless of visibility.
        """
        pass
        
    def collide(self, pos):
        """
        Check if the object collides
        with a certain position.
        """
        pass
    
    def handle_event(self, event, mousepos):
        """
        Handle a pygame event.
        """
        pass
    
    def draw(self, surface):
        """
        Render the element onto
        the surface given.
        """
        pass


class Checkbox(BaseUIElement):
    """
    A checkbox.
    """
    check_mask = pygame.image.load('icons/check_mask.png').convert_alpha()
    
    def __init__(self, pos, **kwargs):
        """
        Initialises the checkbox object.
        Allows the following keyword arguments:
          checked: Whether the checkbox is initially
                   checked.
          size: The size of the checkbox.
                Of format (width, height).
          colour: The checkbox's colour.
                  Of format (red, green, blue).
                  Default is black.
          bg_colour: The checkbox's background colour.
                     Of format (red, green, blue).
                     Default is white.
          outline_colour: The colour of the outline.
                          Of format (red, green, blue).
                          Default is black.
          outline_width: The outline width. Default 2px.
          fill_type: The type of fill when the checkbox
                     is checked.
                     Can be either "background"
                     or "icon".
                     If fill type is "background", the
                     background will be filled with the
                     colour and a checbox shape will be
                     visible in the background colour
                     on top.
                     If fill type is "icon", the
                     background colour remains the same
                     and a checkbox icon is filled.
                     Default is "background".
          ink: whether or not to display circles
               rippling out in response to a checkbox
               click.
               Default is True.
          icon: The checkbox's icon.
                Should be passed in as a pygame surface consisting
                of entirely white pixels with varying transparency.
                White pixels are the 'foreground'.
          visible: Whether the checkbox should be drawn or not.
          onchange: A function taking two arguments,
                    the checkbox object and the mouse click
                    position relative to the checkbox object,
                    which is called every time the checkbox is
                    pressed. If the checkbox is changed
                    programmatically, the mouse click position
                    is 'None'.
          anim_duration: The duration of the animation.
                         Default 0.15 (seconds)
          ink_duration: The duration of the ink ripples.
                        Default 0.15 (seconds)
        """
        self.pos = list(pos)
        
        # by default unchecked
        self._checked = kwargs.get('checked',False)
        
        # 1.0 if checked else 0.0
        # bool is a subclass of int
        self._animprogress = float(self.checked)
        
        self._icon = kwargs.get('icon',Checkbox.check_mask)
        
        self.size = kwargs.get('size',(50,50))
        
        self.colour = list(kwargs.get('colour',(0,0,0)))
        self.bg_colour = list(kwargs.get('bg_colour',(255,255,255)))
        self.outline_colour = list(kwargs.get('outline_colour',(0,0,0)))
        self.outline_width = kwargs.get('outline_width',2)
        self.fill_type = kwargs.get('fill_type','background')
        self.ink = kwargs.get('ink',True)
        
        self.ink_duration = kwargs.get('ink_duration', 0.15)
        self.anim_duration = kwargs.get('anim_duration', 0.15)
        
        self.visible = kwargs.get('visible',True)
        self.onchange = kwargs.get('onchange', lambda x,y: 0)
        
        # Store ink ripples
        self._inks = []
        
    @property
    def size(self):
        return self._tmp.get_size()
    
    @size.setter
    def size(self, size):
        self._tmp = pygame.Surface(size, pygame.SRCALPHA, 32)
        self._tmp = self._tmp.convert_alpha()
        
        self._innertmp = pygame.Surface(size, pygame.SRCALPHA, 32)
        self._innertmp = self._innertmp.convert_alpha()
        
        self._check_mask = pygame.Surface([min(size)]*2,
                                          pygame.SRCALPHA, 32)
        self._check_mask = self._check_mask.convert_alpha()
        
        self._radius = min(size)
        
        self._inktmp = pygame.Surface([int(self._radius*2)]*2,
                                      pygame.SRCALPHA, 32)
        self._inktmp = self._inktmp.convert_alpha()
        
        pygame.transform.scale(self._icon,[min(size)]*2,
                               self._check_mask)
    
    @property
    def icon(self):
        return self._icon
    
    @icon.setter
    def icon(self, icon):
        self._icon = icon
        
        pygame.transform.scale(self,_icon,[min(self,size)]*2,
                               self._check_mask)
                               
    @property
    def checked(self):
        return self._checked
    
    @checked.setter
    def checked(self, checked):
        if checked != self._checked:
            # Programmatic change.
            self.onchange(self, None)
        
    def update(self):
        # Update animation progress
        
        # We divide by the number of
        # frames per second to get
        # a smooth animation going.
        self._animprogress += (float(self.checked)*2-1) / (get_fps() * self.anim_duration)
        
        # Clip to range [0.0,1.0]
        self._animprogress = min(max(0.0,self._animprogress),1.0)
        
    def collide(self, pos):
        if not self.visible:
            return
            
        return 0 <= pos[0]-(self.pos[0]) < self.size[0] and \
               0 <= pos[1]-(self.pos[1]) < self.size[1]
    
    def create_ink(self):
        """
        Generate an ink ripple on command.
        Useful if programmatically setting a
        checkbox state.
        """
        if self.ink:
            self._inks.append(get_time())
            
    def toggle(self, ink = True):
        """
        Toggle the checkbox.
        Has one argument, ink,
        which represents whether
        to create an ink ripple or
        not. (Obviously if self.ink
        is false no ink ripple will
        be created.)
        """
        self._checked ^= True
        if ink: self.create_ink()
        
        # call the onchange function
        self.onchange(self, None)
        
    def handle_event(self, event, mousepos):
        if not self.visible:
            return
        
        # If the event was a click on the button
        if event.type == pygame.MOUSEBUTTONUP and \
           self.collide(mousepos):
            self._checked ^= True
            self.create_ink()
            
            self.onchange(
                self,
                (mousepos[0] - self.pos[0],
                 mousepos[1] - self.pos[1])
            )

    def draw(self, surface):
        if not self.visible:
            return
        
        # We use the animation progress to fill the Checkbox
        # with a certain opacity.
        
        # Draw checkbox outline
        self._tmp.fill(self.outline_colour)
        
        BLIT_ICON = True
        
        if self.fill_type == "background":
            # Draw background colour, mixed with
            # foreground colour
            self._tmp.fill(colour_mix(self.bg_colour,self.colour,self._animprogress),
                      (self.outline_width,self.outline_width,
                       self.size[0] - 2*self.outline_width,
                       self.size[1] - 2*self.outline_width))
                       
            self._innertmp.fill(self.bg_colour)
            self._innertmp.blit(self._check_mask, (0,0),
                                None, pygame.BLEND_RGBA_MULT)
        elif self.fill_type == "icon":
            # Draw background colour
            self._tmp.fill(self.bg_colour,
                      (self.outline_width,self.outline_width,
                       self.size[0] - 2*self.outline_width,
                       self.size[1] - 2*self.outline_width))
                       
            # Draw a circle that is masked by the check mask icon
            # If we're at the start or end of the animation,
            # we optimise.
            
            if self._animprogress == 1.0:
                # We're at the end
                # Just draw the checkmark icon
                self._innertmp.fill(self.colour)
                self._innertmp.blit(self._check_mask, (0,0),
                                    None, pygame.BLEND_RGBA_MULT)
            elif self._animprogress == 0.0:
                # Well, nothing to do here
                BLIT_ICON=False
            else:
                self._innertmp.fill((255,255,255,0))
                pygame.draw.circle(self._innertmp, self.colour,
                                   (self.size[0]//2,self.size[1]//2),
                                   int(self._radius*self._animprogress)
                                   )
                self._innertmp.blit(self._check_mask, (0,0),
                                    None, pygame.BLEND_RGBA_MULT)
        
        # Draw ink ripples
        if self.ink:
            curr_time = get_time()
            newinks = []
            for t in self._inks:
                if curr_time - t > self.ink_duration*1000:
                    continue
                newinks.append(t)
                if curr_time < t:
                    # this is caused by a discrepancy
                    # in time calculations.
                    # just pretend nothing happened...
                    continue
                self._inktmp.fill((255,255,255,0))
                pygame.draw.circle(self._inktmp, self.colour[:3]+
                                   [255 - int(255 * 
                                              (curr_time-t) / 
                                              (self.ink_duration*1000)
                                              )],
                                   [int(self._radius)]*2,
                                   int(self._radius/2+
                                       (self._radius/2)*
                                       # Deceleration curve
                                       math.sqrt(
                                            (curr_time-t)/
                                            (self.ink_duration*1000)
                                            )
                                       )
                                   )
                surface.blit(self._inktmp,
                             [self.pos[0] - self._radius + self.size[0]//2,
                              self.pos[1] - self._radius + self.size[1]//2])
            self._inks = newinks
            
        # Draw main checkbox
        surface.blit(self._tmp,self.pos)
        # Draw checkbox icon
        if BLIT_ICON:
            surface.blit(self._innertmp,
                         (self.pos[0]+self.outline_width,self.pos[1]+self.outline_width),
                         (self.outline_width,self.outline_width,
                          self.size[0]-2*self.outline_width,self.size[1]-2*self.outline_width))
                          

class Container(BaseUIElement):
    """
    A container for other elements.
    """
    def __init__(self, pos, **kwargs):
        """
        Initialises the Container object.
        Allows the following keyword arguments:
          size: The size of the container.
          children: The container's children.
          visible: Whether the container is
                   visible or not.
        """
        self.pos = list(pos)
        
        self.size = kwargs.get('size',(300,300))
        self.children = kwargs.get('children',[])
        self.visible = kwargs.get('visible',True)
    
    @property
    def size(self):
        return self.surface.get_size()
    
    @size.setter
    def size(self, size):
        self.surface = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()
        
    def autosize(self, margin=5, recurse=False):
        """
        Automatically set the size of the
        Container object based on the
        size of the children.
        Does this by calculating the furthest
        point to the right and the furthest
        point down.
        
        Takes an optional argument margin,
        the amount to be padded on the bottom
        and the right. Defaults to 5 pixels.
        
        Takes an optional argument recurse.
        If set to True, all of the Containers
        that are children of this Container
        will be autoresized, and so on.
        (Specifically, any child with an
         autosize property will have that
         autosize property called.)
        Defaults to False.
        """
        
        maxx = 0
        maxy = 0
        
        for c in self.children:
            if recurse and hasattr(c, "autosize"):
                c.autosize(margin, recurse)
            maxx = max(maxx, c.pos[0]+c.size[0])
            maxy = max(maxy, c.pos[1]+c.size[1])
        
        self.size = [maxx+margin, maxy+margin]
    
        
    def update(self):
        for c in self.children:
            c.update()
    
    def handle_event(self, event, mousepos):
        if not self.visible:
            return
        
        # First, ensure that this
        # container has a defined size.
        # This isn't true for UnboundedContainer,
        # for instance.
        if self.size != None:
            # If the mouse position
            # is outside this container,
            # we don't want to handle the click.
            if not (0 <= mousepos[0] < self.size[0] and
                    0 <= mousepos[1] < self.size[1]):
                return
        
        for c in self.children:
            # We subtract our current pos because
            # our children are relatively positioned.
            c.handle_event(event, 
                           [mousepos[0]-self.pos[0], mousepos[1]-self.pos[1]])
    
    def __getitem__(self, key):
        return self.children[key]

    def draw(self, surface):
        if not self.visible:
            return
            
        self.surface.fill((255,255,255))
        
        for c in self.children:
            c.draw(self.surface)
        
        surface.blit(self.surface,self.pos)
        

class UnboundedContainer(Container):
    """
    Similar to a Container, but without
    any size. (So it draws straight onto
    the screen.) It will not draw anything
    on the screen underneath its children
    i.e. has no background colour.
    
    This is basically just an 'invisible' container
    that allows you to logically group elements
    without it having any effect on how they
    are drawn.
    
    It still has a visibility attribute so
    it can be made invisible.
    """
    def __init__(self, **kwargs):
        """
        Initialises the UnboundedContainer object.
        Allows the following keyword arguments:
          children: The container's children.
          visible: Whether the container is
                   visible or not.
        """
        
        self.pos = (0, 0)
        
        self.children = kwargs.get('children',[])
        self.visible = kwargs.get('visible',True)
        
    
    # Override these to make 'size' do nothing.
    @property
    def size(self):
        return None

    @size.setter
    def size(self, size):
        return
        
            
    def draw(self, surface):
        if not self.visible:
            return
        
        for c in self.children:
            c.draw(surface)


class Button(BaseUIElement):
    """
    A button.
    """

    def __init__(self, pos, **kwargs):
        """
        Initialises the button object.
        Allows the following keyword arguments:
          size: The size of the button.
                Of format (width, height).
          text: The text on the button.
          font: A pygame Font object representing
                the text's font.
          colour: The button's text colour.
                  Of format (red, green, blue).
                  Default is black.
          bg_colour: The button's background colour.
                     Of format (red, green, blue).
                     Default is white.
          outline_colour: The colour of the outline.
                          Of format (red, green, blue).
                          Default is black.
          outline_width: The outline width. Default 2px.
          onclick: A function taking two arguments,
                   the button object and the mouse position
                   relative to the button object, which is 
                   executed every time the button is clicked.
                   If the button is clicked programmatically,
                   the mouse position is 'None'.
          ink: Whether or not to display ink ripples.
               Default True.
          ink_colour: Colour of the ink.
                      Of format (red, green, blue).
                      Default is grey.
          visible: Whether the button should be drawn or not.
          ink_duration: The duration of ink ripples.
                        Default 0.3 seconds.
        """
        self.pos = list(pos)
        
        self._font = kwargs.get('font', pygame.font.Font(None, 36))
        
        self._colour = list(kwargs.get('colour',(0,0,0)))
        self._bg_colour = list(kwargs.get('bg_colour',(255,255,255)))
        self._outline_colour = list(kwargs.get('outline_colour',(0,0,0)))
        self._outline_width = kwargs.get('outline_width',2)
        
        self.onclick = kwargs.get('onclick', lambda x,y: 0)
        
        self.ink = kwargs.get('ink',True)
        self.ink_colour = list(kwargs.get('ink_colour',(192,192,192)))
        self.visible = kwargs.get('visible',True)
        self.ink_duration = kwargs.get('ink_duration',0.3)
        
        self._inks = []
        
        # trigger redraw
        self.size = kwargs.get('size',(50,50))
        self.text = kwargs.get('text', '')

    @property
    def size(self):
        return self._tmp.get_size()

    @size.setter
    def size(self, size):
        self._tmp = pygame.Surface(size, pygame.SRCALPHA, 32)
        self._tmp = self._tmp.convert_alpha()
        
        self._innertmp = pygame.Surface(size, pygame.SRCALPHA, 32)
        self._innertmp = self._innertmp.convert_alpha()
        
        self._tmp.fill(self.outline_colour)
        self._innertmp.fill(self.bg_colour)
        
        self._radius = max(size) * 0.25
        
        self._inktmp = pygame.Surface([int(self._radius*2)]*2, pygame.SRCALPHA, 32)
        self._inktmp = self._inktmp.convert_alpha()
        
        self._inksurf = pygame.Surface(size, pygame.SRCALPHA, 32)
        self._inksurf = self._inksurf.convert_alpha()
        
        self._textsurf = pygame.Surface(size, pygame.SRCALPHA, 32)
        self._textsurf = self._textsurf.convert_alpha()
        
        self._tmp.blit(self._innertmp,
                       (self.outline_width,) * 2,
                       (self.outline_width,) * 2 +
                       (size[0] - 2*self.outline_width,
                        size[1] - 2*self.outline_width))

    @property
    def text(self):
        return self._text

    @property
    def font(self):
        return self._font

    @property
    def colour(self):
        return self._colour

    @property
    def bg_colour(self):
        return self._bg_colour
    
    @property
    def outline_colour(self):
        return self._outline_colour

    @property
    def outline_width(self):
        return self._outline_width

    @text.setter
    def text(self, text):
        self._text = text
        
        # render text
        text = self.font.render(self.text, True, self.colour)
        self._textsurf.fill(0)
        self._textsurf.blit(text,
                           ((self.size[0] - text.get_width()) // 2,
                            (self.size[1] - text.get_height()) // 2))

    @font.setter
    def font(self, font):
        self._font = font
        
        # trigger text rerender
        self.text = self.text

    @colour.setter
    def colour(self, colour):
        self._colour = colour
        
        # trigger text rerender
        self.text = self.text

    @bg_colour.setter
    def bg_colour(self, bg_colour):
        self._bg_colour = bg_colour
        
        # trigger redraw
        self.size = self.size

    @outline_colour.setter
    def outline_colour(self, outline_colour):
        self._outline_colour = outline_colour
        
        # trigger redraw
        self.size = self.size

    @outline_width.setter
    def outline_width(self, outline_width):
        self._outline_width = outline_width
        
        # trigger redraw
        self.size = self.size

    def collide(self, pos):
        if not self.visible:
            return
            
        return 0 <= pos[0]-(self.pos[0]) < self.size[0] and \
               0 <= pos[1]-(self.pos[1]) < self.size[1]
               
    def create_ink(self, pos = None):
        """
        Create ink originating
        from a position on the button,
        given by pos.
        If pos is None (the default value),
        the ink will originate from the center.
        """
        if not self.ink:
            return
        
        if pos is None:
            pos = (self.size[0] // 2, self.size[1] // 2)
        
        self._inks.append((pos, get_time()))
               
    def click(self, ink = True):
        """
        Simulate a button press.
        Takes one argument, ink,
        representing whether or not
        to produce an ink ripple
        originating from the center
        of the button. If the button's
        ink attribute is false, this
        will not generate ink.
        The argument is by default True.
        """
        
        # Execute hook
        self.onclick(self, None)
        
        # Add ink
        if ink:
            self.create_ink()

    def handle_event(self, event, mousepos):
        if not self.visible:
            return
        
        # If the event was a click on the button
        if event.type == pygame.MOUSEBUTTONUP and \
           self.collide(mousepos):
            relpos = (mousepos[0] - self.pos[0],
                      mousepos[1] - self.pos[1])

            # Execute hook
            self.onclick(self, relpos)
            
            # Add ink
            self.create_ink(relpos)

    def draw(self, surface):
        if not self.visible:
            return
        
        # Draw ink ripples
        if self.ink:
            # clear temporary ink surface
            self._inksurf.fill(0)
            
            curr_time = get_time()
            newinks = []
            for p, t in self._inks:
                if curr_time - t > self.ink_duration*1000:
                    continue
                newinks.append((p, t))
                if curr_time < t:
                    # this is caused by a discrepancy
                    # in time calculations.
                    # just pretend nothing happened...
                    continue
                self._inktmp.fill((255,255,255,0))
                pygame.draw.circle(self._inktmp, self.ink_colour[:3]+
                                   [255 - int(255 * 
                                              (curr_time-t) / 
                                              (self.ink_duration*1000)
                                              )],
                                   [int(self._radius)]*2,
                                   int(self._radius/2+
                                       (self._radius/2)*
                                       # Deceleration curve
                                       math.sqrt(
                                            (curr_time-t)/
                                            (self.ink_duration*1000)
                                            )
                                       )
                                   )
                self._inksurf.blit(self._inktmp,
                                   [p[0]-self._radius,p[1]-self._radius])
            self._inks = newinks
            
        # Draw to screen
        surface.blit(self._tmp, self.pos)
        surface.blit(self._inksurf, self.pos)
        surface.blit(self._textsurf, self.pos)
