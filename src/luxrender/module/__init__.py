from ef.ef import ef
import bpy
import pylux as lux
import threading

def LuxLog(msg):
    ef.log('[LuxRender] %s' % msg)

class LuxOutput(object):
    '''
    Base class for any Lux output
    '''
    pass



class LuxFile(LuxOutput):
    '''
    Write to LXS file
    '''
    
    pass
    
class LuxTimerThread(threading.Thread):
    '''
    Periodically call self.kick()
    '''
    KICK_PERIOD = 8
    
    active = True
    timer = None
    
    def stop(self):
        self.active = False
        if self.timer is not None:
            self.timer.cancel()
            
    def run(self):
        '''
        Timed Thread loop
        '''
        
        while self.active:
            self.timer = threading.Timer(self.KICK_PERIOD, self.kick)
            self.timer.start()
            if self.timer.isAlive(): self.timer.join()
            
    def kick(self):
        '''
        sub-classes do their work here
        '''
        pass
    
class LuxAPIStats(LuxTimerThread):
    '''
    Periodically get lux stats
    '''
    
    KICK_PERIOD = 1
    
    stats_dict = {
        'secElapsed':       0.0,
        'samplesSec':       0.0,
        'samplesTotSec':    0.0,
        'samplesPx':        0.0,
        'efficiency':       0.0,
        #'filmXres':         0.0,
        #'filmYres':         0.0,
        #'displayInterval':  0.0,
        'filmEV':           0.0,
        #'sceneIsReady':     0.0,
        #'filmIsReady':      0.0,
        #'terminated':       0.0,
    }
    
    stats_string = ''
    
    def stop(self):
        self.active = False
        if self.timer is not None:
            self.timer.cancel()
            
    def kick(self):
        for k in self.stats_dict.keys():
            self.stats_dict[k] = lux.statistics(k)
        
        self.stats_string = ' | '.join(['%s: %0.2f'%(k,v) for k,v in self.stats_dict.items()])
              
class LuxFilmDisplay(LuxTimerThread):
    '''
    Periodically update render result with Lux's framebuffer
    '''
    RE = None
            
    def start(self, RE):
        self.RE = RE
        LuxTimerThread.start(self)
            
    def kick(self, render_end=False):
        if self.RE is not None:
            px = [] #lux.framebuffer()
            xres = int(lux.statistics('filmXres'))
            yres = int(lux.statistics('filmYres'))
            time = lux.statistics('secElapsed')
            if render_end:
                LuxLog('Final render result %ix%i' % (xres,yres))
            else:
                LuxLog('Updating render result %ix%i' % (xres,yres))
            self.RE.update_framebuffer(xres,yres,px)
        
def luxlog(a,b,c):
    print(a,b,c)

class LuxManager(LuxOutput):
    '''
    Use the pylux API
    '''
    
    lux_module = lux
    
    stats_thread    = None
    fb_thread       = None
    started         = True
    
    def __init__(self):
        lux.init()
        self.reset()
        
#    @staticmethod
#    def luxlog(a, b, c):
#        LuxLog('%s %s %s' % (a,b,c))

    def start(self, RE):
        if self.started:
            LuxLog('Already rendering!')
            return
        lux.worldEnd()
        self.stats_thread.start()
        self.fb_thread.start(RE)
        self.started = True
    
    def reset(self):
        #causes segfault
        #lux.errorHandler(LuxManager.luxlog)
        
        if self.stats_thread is not None and self.stats_thread.isAlive():
            self.stats_thread.stop()
            self.stats_thread.join()
        
        self.stats_thread  = LuxAPIStats()
        
        if not self.started: return
        self.started = False
        
        lux.exit()
        lux.wait()
        
        # Get the last image
        if self.fb_thread is not None and self.fb_thread.isAlive():
            self.fb_thread.stop()
            self.fb_thread.join()
            # Get last FB
            self.fb_thread.kick(render_end=True)
        
        self.fb_thread  = LuxFilmDisplay()
        
        lux.cleanup()
        
    def __del__(self):
        self.reset()
        

def test():
    LM = LuxManager()
    lux.lookAt(0,0,0,0,1,0,1,0,0)
    lux.worldBegin()
    lux.lightSource('sunsky', [])
    
    return LM
