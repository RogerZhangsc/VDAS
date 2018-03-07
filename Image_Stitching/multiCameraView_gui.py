# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 23:40:19 2018

@author: Sunny
"""

import numpy as np
import cv2

print(cv2.__version__)

class Window(QMainWindow):
    
    def __init__(self):
        super(Window, self).__init__()
        #Initialize members
        self.HEIGHT = 240
        self.WIDTH = 320
        self.RECORD_WIDTH = 960
        self.RECORD_HEIGHT = 240
        self.FPS = 90
        self.cam = []
        self.frame = []
        self.ret = []
        self.rgb = []
        self.record_flag = True
        self.i = 0
        self.rgb_current=0
        
        #Create Window
        self.setGeometry(50, 50, 500, 500)
        self.setWindowTitle("PyQt5 Tutorial")
        self.setWindowIcon(QIcon("testImg.jpg"))
       
        #creating Record item
        extractAction = QAction("&Record", self)
        extractAction.setShortcut("Ctrl+R")
        extractAction.setStatusTip("Start Recording")
        extractAction.triggered.connect(self.close_application)
        
        #creating Record item
        extractAction = QAction("&Quit", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip("Closing the App")
        extractAction.triggered.connect(self.close_application)
        
        self.statusBar()
        
        #creating menu bar menus
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")
        fileMenu.addAction(extractAction)
       
        #Enable Cameras
        try:
            while(cv2.VideoCapture(i).isOpened()):
                self.cam.append(cv2.VideoCapture(i))
                self.i=self.i+1
                print(self.i)
        except Exception as e:
            print(e)
            print("All cameras detected.")
        

         self.home()
       
        
    def home(self):
        
        #creating frame for gui
        #cv2.imshow("App",cv2.imread("testImg.jpg"))
        quit_btn = QPushButton("Quit", self)
        quit_btn.clicked.connect(self.close_application)
        quit_btn.resize(quit_btn.sizeHint())
        quit_btn.move(100,100)
        
        #CheckBox
        checkbox = QCheckBox("Full Screen",self)
        checkbox.move(200,100)
        checkbox.resize(300,300)
        checkbox.stateChanged.connect(self.enlarge_window)
        checkbox.toggle()

        
        #Create Tool Bar
        extractAction = QAction(QIcon("testImg.jpg"),"ICON HOVER",self)
        extractAction.triggered.connect(self.close_application)
        self.toolbar = self.addToolBar("Extraction")
        self.toolbar.addAction(extractAction)
        
        #Progress bar
        self.progress = QProgressBar(self)
        self.progress.setGeometry(200,80,250,20)
        
        dwn_btn = QPushButton("Download", self)
        dwn_btn.clicked.connect(self.download)
        dwn_btn.resize(dwn_btn.sizeHint())
        dwn_btn.move(300,200)
        
        
        self.show()
    
    def download(self):
        self.completed = 0
        
        while(self.completed <100):
            self.completed+= 0.0001
            self.progress.setValue(self.completed)
        
    def enlarge_window(self, state):
        if state == Qt.Checked:
            self.setGeometry(50,50,1000,600)
        else:
            self.setGeometry(50,50,500,300)
        
        
        
    def close_application(self):
        #Pop UP Box
        choice = QMessageBox.question(self, 'Extract!', 
                                      "Are you sure you want to exit?",
                                      QMessageBox.Yes | QMessageBox.No)
        if(choice == QMessageBox.Yes):
            print("Exiting")
            self.close()
        else:
            pass
        #print("Closing")
        #QCoreApplication.instance().quit
        #sys.exit()

    #def random_function(self):
    
def run():
    app = QApplication(sys.argv)
    GUI = Window()
    app.exec_()


run()




fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('C:\\Users\\Sunny\\Desktop\\saveOutput.avi',fourcc, 30, (RECORD_WIDTH,RECORD_HEIGHT))
    
try:
    while(cv2.VideoCapture(i).isOpened()):
        cam.append(cv2.VideoCapture(i))
        i=i+1
        print(i)
except Exception as e:
    print(e)
    print("All cameras detected.")
     
 #flags = [i for i in dir(cv2) if i.startswith('COLOR_')]
 #print(flags)q



try:
     
     temp = cam[2] 
     cam[2] = cam[1]
     cam[1] = temp
     while (True):
         # Capture frame-by-frame
         print("check 1")
         final_frame=0
         j = 0
         rgb = []
         while(j<i):
             ret_current, frame_current = cam[j].read()
             ret.append(ret_current)
             frame.append(frame_current)
              # Our operations on the frame come here
            
              #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
              
             rgb_current = cv2.cvtColor(frame_current, cv2.COLOR_RGBA2RGB)        
             rgb_current = cv2.resize(rgb_current,(WIDTH, HEIGHT),interpolation=cv2.INTER_CUBIC);
             rgb.append(rgb_current)
             j=j+1 
             print("J=",j)
              #cv2.resize(frame[j], frame[j], Size(640, 360), 0, 0, INTER_CUBIC);
              #cv2.imshow('final_frame',frame_current)

              # Display the resulting frame
         count = 2
         final_frame = np.hstack((rgb[0],rgb[1]))
         while(count<i):
             final_frame = np.hstack((final_frame,rgb[count]))
             count=count+1
             print("count=",count)
            
         # stitch the images together to create a panorama


         #DISPLAY INTERFACE 
         k=0
         textX=10
         while(k<i):
             overlayText = 'CAM_' + str(k)
             cv2.putText(final_frame,overlayText, 
                     (textX,30), 
                     cv2.FONT_HERSHEY_SIMPLEX, 
                     0.75,
                     (255,255,255),
                     2)
             textX = WIDTH+textX
             print(overlayText)
             k=k+1
             
             cv2.putText(final_frame,"Q to QUIT", 
                     (10,230), 
                     cv2.FONT_HERSHEY_SIMPLEX, 
                     0.5,
                     (0,0,255),
                     2)
             
             if(record_flag==False):
                 cv2.putText(final_frame,"Not Recording", 
                     (290,230), 
                     cv2.FONT_HERSHEY_SIMPLEX, 
                     0.5,
                     (0,0,255),
                     2)
             elif(record_flag==True):
                 cv2.putText(final_frame,"Recording", 
                     (290,230), 
                     cv2.FONT_HERSHEY_SIMPLEX, 
                     0.5,
                     (0,0,255),
                     2)
                 
         
         cv2.imshow('final_frame',final_frame)
         if(record_flag==True):
             out.write(final_frame)
         print("frame displayed")
         
         if cv2.waitKey(1) & 0xFF == ord('q'):
             break
         elif cv2.waitKey(1) & 0xFF == ord('r'):
             if(record_flag==False):
                 record_flag=True
                 print("Starting Video Save")
             elif(record_flag==True):
                 record_flag=False
                 print("Relesing Video Save")
                 out.release()
                 
                 
except Exception as e:
     print("Check 2")
     print(e)
     
finally:
 # When everything done, release the capture
   
   print("Check 3")
   k =  0
   while(k<i):
         cam[k].release()
         print("releasing camera - "+str(k))
         k=k+1   
   if(record_flag==True):
       print("Relesing Video Save")
       out.release()
   print("Destroying All Windows")
   cv2.destroyAllWindows()
