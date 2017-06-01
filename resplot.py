# -*- coding: utf-8 -*-
#importing relevant packages (for plotting and analytics)
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import colors as cols
import six
import pandas as pd
import os




path = os.getcwd() #path definition
fdir  = ''

def read_res(file): #read data from xls files
    Size, R, xr,xl,xc,yu,yd,yc = [] ,[], [],[] ,[], [],[],[] #lists for areas, Fij's,  deps cordinates
    out = pd.read_excel(file, sheetname = "Out") #read model results
    Rout = pd.read_excel(file, sheetname = "R") #read Fij's
    Sizeout = pd.read_excel(file, sheetname = "Size") #read deps wanted sizes
    Wout = pd.read_excel(file, sheetname = "W") # w1 and w2
    w1 = float(Wout['w1'][0])
    w2 = 1.0-w1
    totx = float(out['totx'][0]) #total length in x axis
    toty = float(out['toty'][0]) #total length in y axis
    for d in range(len(Sizeout)): #insert data results into python lists
        R.append([])
        Size.append(float(Sizeout['Area'][d]))
        xr.append(float(out['Xr'][d]))
        xl.append(float(out['Xl'][d]))
        xc.append((float(out['Xl'][d])+float(out['Xr'][d]))/2)
        yu.append(float(out['Yu'][d]))
        yd.append(float(out['Yd'][d]))   
        yc.append((float(out['Yu'][d])+float(out['Yd'][d]))/2)
        for i in range(len(Rout)):
            R[d].append(float(Rout.iloc[d,i]))
    return Size, R, totx, toty, xr,xl,xc,yu,yd,yc, w1, w2
            
    

def result(Size,R,w1,xr,xl,yu,yd,xc,yc,totx,toty): #get results of specific instance and weight and compute objective function value
    l = len(Size)
    Dist = 0
    A = totx*toty #layout area
    for i in range(l): # dist is: Dij*Rij
        for j in range(l):
            Dist += (abs(xc[i]-xc[j])+abs(yc[i] - yc[j]))*R[i][j]*0.5     
    return w1*Dist+(1-w1)*A, Dist,A
    

def build_chart(Size,R,w1,xr,xl,yu,yd,xc,yc,totx,toty,name,prints,doc):
    # build layout sketch, name = filename to build, prints = binary variable - print all values in the file?,
    # doc - binary variable - create layout sketch file and text file with model results?
    Area = [ (xr[i]-xl[i])*(yu[i]-yd[i]) for i in range(len(Size))]
    if doc: fi = open('txt\\'+name+'.txt','w')  #open xls file as given
    colors = list(six.iteritems(cols.cnames))
    m = max(totx,toty)*1.1 #size of square
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')
    ax1.axes.xaxis.set_ticklabels([])
    ax1.axes.yaxis.set_ticklabels([])
    ax1.add_patch(
            patches.Rectangle( #create rectangle
                (0, 0),   # (x,y)
                totx/m,          # width
                toty/m,          # height
                facecolor = 'w'
            )
            )
    for i in range(len(xr)): #draw each dep acording to its cordintes
        ax1.add_patch(
            patches.Rectangle(
                (xl[i]/m, yd[i]/m),   # (x,y)
                xr[i]/m-xl[i]/m,          # width
                yu[i]/m-yd[i]/m,          # height
                facecolor =  colors[i%len(colors)][1]
            )
            )
        if i+1 in [1,19,29]:
            c='white'
        else: c='black'
        plt.text((xl[i]+xc[i])/(2*m), (yc[i]+yd[i])/(2*m), str(i+1), fontsize = 8, color = c) # print dep number
        if prints: # print all results
            print i+1,'(',round(xc[i],2),',',round(yc[i],2),') m2:',round(max((xr[i]-xl[i])/(yu[i]-yd[i]),(yu[i]-yd[i])/(xr[i]-xl[i])),2), 'Area:', round(Area[i],2), '(',round((xr[i]-xl[i]),2),'x',round((yu[i]-yd[i]),2),')',round(Area[i]*100/Size[i],2),'% of wanted'
        if doc: #write all data into txt file
            fi.write(str(i+1)+' ('+str(round(xc[i],2))+','+str(round(yc[i],2))+') m2:'+str(round(max((xr[i]-xl[i])/(yu[i]-yd[i]),(yu[i]-yd[i])/(xr[i]-xl[i])),2))+ ' Area:'+str(round(Area[i],2))+ ' ('+str(round((xr[i]-xl[i]),2))+'x'+str(round((yu[i]-yd[i]),2))+') '+str(round(Area[i]*100/Size[i],2))+'% of wanted \n')
        if Area[i]/Size[i]<0.9:
            print '************** Size Error ***************'
    plt.show() #show layout sketch
    if doc:  #write all data into txt file
        fig1.savefig('png\\'+name+'.png', dpi=200, bbox_inches='tight')
        res =  result(Size,R,w1,xr,xl,yu,yd,xc,yc,totx,toty)
        fi.write( 'Score:'+str(res[0])+ ' Dist:'+str(res[1])+' Area:'+str(res[2])+' ('+str(totx)+'x'+str(toty)+') w1:'+str(w1)+'\n')
        fi.close
        
    

'''Main'''
problem, w ,runnow = 0, -1.0, -1
doall = 0# change to 1 to run all the problems

if not doall: #run specific problem
    while not (problem<=10 and problem >=1):
        try:
            problem = int(input("Enter problem number (1-10)")) #choose problem numer
        except:
            print 'wrong number'
    while not (w==1.0 or w ==0.0  or w==0.5):
        try:
            w = float(input("Enter w1 value (0,0.5,1)")) #choose weight w1
        except:
            print 'wrong number'
    while  (runnow<0):
        try:
            runnow = int(input("Would you like to execute OPL run now or just show the results? Full run usually takes about 5-10 minutes.     Press 1 For runopl     Press 0 For presenting previously calculated results.    ")) #history results or calculation
        except:
            print 'wrong input (input 0 or 1)'
    
    ws = str(w)
    ws= ws[0]+ws[2]
    filename = 'input'+str(problem)+ws+'.xlsx' #choose relevant xls file to the chosen problen

    if runnow ==1:
        os.system("oplrun "+path+"\\Planning.mod "+path+"\\input"+str(problem)+ws+".dat")   #executing run  
    
    
    
    Size, R, totx, toty, xr,xl,xc,yu,yd,yc, w1, w2 = read_res(filename)   #read problem data results
    res =  result(Size,R,w1,xr,xl,yu,yd,xc,yc,totx,toty) # compute objective function value
    build_chart(Size,R,w1,xr,xl,yu,yd,xc,yc,totx,toty,'rec1.png',True,False) #create layout sketch
    print 'Score:',res[0], 'Dist:',res[1],'Area:',res[2],'(',totx,'x',toty,') w1:',w1

if doall: #run all problems
    while  (runnow<0):
        try:
            runnow = int(input("Would you like to execute OPL run now or just show the results? Full run usually takes about 5-10 minutes.     Press 1 For runopl     Press 0 For presenting previously calculated results.    ")) #history results or calculation
        except:
            print 'wrong input (input 0 or 1)'

    ww = ['00','05','10']
    for i in range(1,11):
        for w in ww:
            if runnow ==1:
                os.system("oplrun "+path+"\\Planning.mod "+path+"\\input\\input"+str(problem)+w+".dat") 
            filename = path+'\\input\\input'+str(i)+w+'.xlsx'   
            Size, R, totx, toty, xr,xl,xc,yu,yd,yc, w1, w2 = read_res(filename)   
            res =  result(Size,R,w1,xr,xl,yu,yd,xc,yc,totx,toty)
            build_chart(Size,R,w1,xr,xl,yu,yd,xc,yc,totx,toty,str(i)+w,False,True)
            print i, len(Size), w1, w2, res[0]
            
    
    
    
    
    
    
    
    
