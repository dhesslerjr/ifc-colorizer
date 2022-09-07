import sys
import json


class ColorMap:
    inval = ''
    outval = ''
     
    # parameterized constructor
    def __init__(self, inv, outv):
        self.inval = inv
        self.outval = outv    

instr='''[
    {"inval":"IFCCOLOURRGB($,1.0000000,1.0000000,0.1000000)","outval":"IFCCOLOURRGB($,0.8705882,0.8039216,0.4705882)"},
    {"inval":"IFCCOLOURRGB($,0.8039216,0.3764706,0.0000000)","outval":"IFCCOLOURRGB($,0.4784314,0.4078431,0.0509804)"},
    {"inval":"IFCCOLOURRGB($,1.0000000,0.8392157,0.0000000)","outval":"IFCCOLOURRGB($,0.5882353,0.5098039,0.1176471)"},
    {"inval":"IFCCOLOURRGB($,1.0000000,1.0000000,0.0000000)","outval":"IFCCOLOURRGB($,0.8117647,0.7450980,0.4117647)"},
    {"inval":"IFCCOLOURRGB($,0.0000000,1.0000000,1.0000000)","outval":"IFCCOLOURRGB($,0.4509804,0.1686275,0.1176471)"},
    {"inval":"IFCCOLOURRGB($,0.0000000,0.5098039,1.0000000)","outval":"IFCCOLOURRGB($,0.4196078,0.3803922,0.3803922)"},
    {"inval":"IFCCOLOURRGB($,0.7058824,0.1176471,0.1176471)","outval":"IFCCOLOURRGB($,0.8705882,0.8039216,0.4705882)"} 
    ]'''
#cmap=json.loads(instr)

c_IN=open('hz_ifc_colors.map')
cmap = json.loads(c_IN.read())
c_IN.close()

      
#cmap = []
#cmap.append(ColorMap('IFCCOLOURRGB($,1.0000000,1.0000000,0.1000000)','IFCCOLOURRGB($,0.8705882,0.8039216,0.4705882)'))
#cmap.append(ColorMap('IFCCOLOURRGB($,0.8039216,0.3764706,0.0000000)','IFCCOLOURRGB($,0.4784314,0.4078431,0.0509804)'))
#cmap.append(ColorMap('IFCCOLOURRGB($,1.0000000,0.8392157,0.0000000)','IFCCOLOURRGB($,0.5882353,0.5098039,0.1176471)'))
#cmap.append(ColorMap('IFCCOLOURRGB($,1.0000000,1.0000000,0.0000000)','IFCCOLOURRGB($,0.8117647,0.7450980,0.4117647)'))
#cmap.append(ColorMap('IFCCOLOURRGB($,0.0000000,1.0000000,1.0000000)','IFCCOLOURRGB($,0.4509804,0.1686275,0.1176471)'))
#cmap.append(ColorMap('IFCCOLOURRGB($,0.0000000,0.5098039,1.0000000)','IFCCOLOURRGB($,0.4196078,0.3803922,0.3803922)'))
#cmap.append(ColorMap('IFCCOLOURRGB($,0.7058824,0.1176471,0.1176471)','IFCCOLOURRGB($,0.8705882,0.8039216,0.4705882)'))


fallback_color='IFCCOLOURRGB($,1.0000000,1.0000000,1.0000000)'

f_name=''
if(len(sys.argv)>1):
    f_name=sys.argv[1]
#f_name='color_map_nugget1_full.ifc'
else:
    print('provide input IFC filepath')
    quit()
    
print('Processing input IFC: ' + f_name)

fp = open(f_name)
f_IN = fp.readlines()
fp.close()
outfile_name=f_name.replace('.ifc','_hzcolors.ifc')
f_OUT = open(outfile_name,"wt")

lines=0

for x in f_IN:
    lines=lines+1
    txt = '{progress:.1f}%'
    print(txt.format(progress=float(lines)/len(f_IN)*100.0),end="\r")
    if(x.find('IFCCOLOURRGB(')>-1):
        
        #print(x)
        replaced=False
        for c in cmap:
            if(x.find(c['inval'])>-1):
                x=x.replace(c['inval'],c['outval'])
                #print('found')
                replaced=True
                break
        if(not replaced):
            #print('default')
            x=x.split('=')[0] + '= ' + fallback_color + ';\n'
        
    f_OUT.write(x)

f_OUT.close()

print('\nfinished output IFC: ' + outfile_name +'\n')



    

