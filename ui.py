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
    
    if len(a)==3:
        a += [255]
    if len(b)==3:
        b += [255]
    
    return [(x + (y-x)*amount) for x,y in zip(a,b)]



class BaseUIElement:
    def __init__(self):
        """
        Initialises the object.
        """
        pass
    
    def update(self, fps):
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
    
    def handle_event(self, event):
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
        """
        self.pos = list(pos)
        
        # by default unchecked
        self.checked = kwargs.get('checked',False)
        
        # 1,0 if checked else 0.0
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
        
        self.ink_duration = 0.15
        
        self.visible = kwargs.get('visible',True)
        
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
        
        self._check_mask = pygame.Surface([min(self.size)]*2,
                                          pygame.SRCALPHA, 32)
        self._check_mask = self._check_mask.convert_alpha()
        
        self._inktmp = pygame.Surface([min(size)*2]*2,
                                      pygame.SRCALPHA, 32)
        self._inktmp = self._inktmp.convert_alpha()
        
        self._radius = self._check_mask.get_width()*2.9 # Just cover the check
        
        pygame.transform.scale(self._icon,[min(self.size)]*2,
                               self._check_mask)
    
    @property
    def icon(self):
        return self.icon
    
    @icon.setter
    def icon(self, icon):
        self._icon = icon
        
        pygame.transform.scale(self,_icon,[min(self,size)]*2,
                               self._check_mask)
        
    def update(self):
        # Update animation progress
        
        # We divide by the number of
        # frames per second to get
        # a smooth animation going.
        self._animprogress += (float(self.checked)*2-1) / (get_fps() * 0.15)
        
        # Clip to range [0.0,1.0]
        self._animprogress = min(max(0.0,self._animprogress),1.0)
        
    def collide(self, pos):
        if not self.visible:
            return
            
        return 0 <= pos[0]-(self.pos[0]) < self.size[0] and \
               0 <= pos[1]-(self.pos[1]) < self.size[1]
        
    def handle_event(self, event, mousepos):
        if not self.visible:
            return
        
        # If the event was a click on the button
        if event.type == pygame.MOUSEBUTTONUP and \
           self.collide(mousepos):
            self.checked = False if self.checked else True
            # Add an ink ripple
            if self.ink:
                self._inks.append(get_time())

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
                                   int(self._radius*self._animprogress/5)
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
                self._inktmp.fill((255,255,255,0))
                pygame.draw.circle(self._inktmp, self.colour[:3]+
                                   [255-int(255*(curr_time-t)/(self.ink_duration*1000))],
                                   [min(self.size)]*2,
                                   int(min(self.size)/2+
                                       (min(self.size)/1.5)*
                                       math.sqrt( # So we have a deceleration curve
                                            (curr_time-t)/
                                            (self.ink_duration*1000)
                                            )
                                       )
                                   )
                surface.blit(self._inktmp,
                             [self.pos[0]-min(self.size)/2,self.pos[1]-min(self.size)/2])
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
