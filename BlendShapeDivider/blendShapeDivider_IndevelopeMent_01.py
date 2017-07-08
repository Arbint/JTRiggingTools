#BlendShape Divider
"""
Developed by Jingtian Li

Ver 1.0
"""
import maya.cmds as mc




########################################################################
####                              UI                                ####
########################################################################


BlendShapeDividerWindowID = "BlendshapeDividerWindowID"
if (mc.window(BlendShapeDividerWindowID, q = True, exists = True)):
    mc.deleteUI(BlendShapeDividerWindowID)
mc.window(BlendShapeDividerWindowID, title = "BlendShape Divider", rtf = True)
BlendShapeWindowMasterLayout = mc.frameLayout(lv = 0, bv = False)
mc.rowColumnLayout(nc = 2)
divisitonintField = mc.intSliderGrp(l = "Number of Divisions:   ", f = True, s = True, min = 2, max = 20, v= 2)
mc.setParent(BlendShapeWindowMasterLayout)
createControllerPortionlayout = mc.rowColumnLayout(nc = 5)
createCtrlCB = mc.checkBox(l = "Create Controller",v = True,onc = "createCtrlCBOnCmd()", ofc = "createCtrlCBOffCmd()")
controllerStyleRC = mc.radioCollection("ControllerSelectionID")
mc.radioButton("Slider",l = "Sliders", sl = True)
mc.radioButton("Circle",l = "Circles")
mc.text("ControllerTextID",l = "      Namebase: ")
mc.textField("ControllerTextFieldID")
mc.setParent(BlendShapeWindowMasterLayout)
SpecifyBaseShapeLayout = mc.rowColumnLayout(nc = 5)
SpecifyBaseShapeCB = mc.checkBox(l = "Specify BaseShape", v = True, onc = "SpecifyBaseShapeCBOnCmd()", ofc = "SpecifyBaseShapeCBOffCmd()")
BasicShapeTextField = mc.textField("BasicShapeTextFieldID", w = 250, ed = False, vis = True)
assingBaseShapeBtn = mc.button("assingBaseShapeBtnID", l = "<<<", vis = True, c = "assingBaseShapeBtnCmd()")
mc.setParent(BlendShapeWindowMasterLayout)
mc.button(l = "Create", c = "CreateBtnCmd()")
mc.button(l = "Cancel", c = "CancelBtnCmd()")
mc.showWindow(BlendShapeDividerWindowID)

########################################################################
####                            Methods                             ####
########################################################################
def printInfo():
    #Gather Info
    NumberOfDivision = mc.intSliderGrp(divisitonintField, q = True, v =True)
    createCtroller = mc.checkBox(createCtrlCB, q = True, v = True)
    controllerType = mc.radioCollection("ControllerSelectionID", q = True, sl = True)
    NameBase = mc.textField("ControllerTextFieldID", q = True, tx = True)
    specifyBaseShape = mc.checkBox(SpecifyBaseShapeCB, q = True, v = True)
    BaseShape = mc.textField("BasicShapeTextFieldID", q = True, tx = True)
    
    print "Number of Division is:", NumberOfDivision
    print "Should create controller:", createCtroller
    print "Controller type:",controllerType
    print "Name base:", NameBase
    print "Should Specify BaseShape:", specifyBaseShape
    print "BaseShape:", BaseShape

#UI Visibility section:    
def createCtrlCBOnCmd():
    mc.radioButton("Slider",e = True, vis = True)
    mc.radioButton("Circle",e = True, vis = True)
    mc.text("ControllerTextID", e = True, vis = True)
    mc.textField("ControllerTextFieldID", e = True, vis = True)
def createCtrlCBOffCmd():
    mc.radioButton("Slider",e = True, vis = False)
    mc.radioButton("Circle",e = True, vis = False)
    mc.text("ControllerTextID", e = True, vis = False)
    mc.textField("ControllerTextFieldID", e = True, vis = False)
    
def SpecifyBaseShapeCBOnCmd():
    mc.textField("BasicShapeTextFieldID", e = True, vis = True)
    mc.button("assingBaseShapeBtnID", e = True, vis = True)

def SpecifyBaseShapeCBOffCmd():
    mc.textField("BasicShapeTextFieldID", e = True, vis = False)
    mc.button("assingBaseShapeBtnID", e = True, vis = False)

def assingBaseShapeBtnCmd():
    selection = mc.ls(sl = True)[0]
    shapeOfSelection = mc.listRelatives(selection, s = True)[0]
    mc.textField("BasicShapeTextFieldID", e = True, tx = shapeOfSelection)


def CancelBtnCmd():
    if (mc.window(BlendShapeDividerWindowID, q = True, exists = True)):
        mc.deleteUI(BlendShapeDividerWindowID)
    

def CreateBtnCmd():
    #create paramaters
    #get base shape
    #get number of divisions
    
    #Gather Info
    NumberOfDivision = mc.intSliderGrp(divisitonintField, q = True, v =True)
    createCtroller = mc.checkBox(createCtrlCB, q = True, v = True)
    controllerType = mc.radioCollection("ControllerSelectionID", q = True, sl = True)
    NameBase = mc.textField("ControllerTextFieldID", q = True, tx = True)
    specifyBaseShape = mc.checkBox(SpecifyBaseShapeCB, q = True, v = True)
    BaseShapeFiledText = mc.textField("BasicShapeTextFieldID", q = True, tx = True)
    
    printInfo()
    
    #get selection:
    if(mc.ls(sl = True)):
        sel = mc.ls(sl = True)[0]
    else:
        mc.error("Nothing is selected")
        return
        
    #get Shapes:    
    ShapeNodeList = mc.listRelatives(sel, s = True)
    BaseShape = ""
    TargetShape = ""
    for item in ShapeNodeList:
        if mc.getAttr(item + ".intermediateObject"):
            BaseShape = item
        else:
            TargetShape = item
    
    #print "base shape is: " + BaseShape
    #print "Target Shape is: " + TargetShape
    if specifyBaseShape:
        BaseShape = BaseShapeFiledText
    if BaseShape == "":
        print mc.error("Cannot Find Baseshape, please specify BaseShape Mannually? if the model has intermidiate shape, uncheck specify BaseShape")
    
    #gether per vertex translation and object translation
    baseVertexLocations= GetVertexLocations(BaseShape)
    targetVertexLocations = GetVertexLocations(TargetShape)
    baseTranlation = getTranslateNodePostion(BaseShape)
    targetTranlation = getTranslateNodePostion(TargetShape)
    
#get the world space location of the translatation node of the given shape        
def getTranslateNodePostion(shape):
    translateNode = mc.listRelatives(shape,p = True)[0]
    location = mc.xform(translateNode, q = True, ws = True, t= True)
    return location
    
#return the world space locations of all the vertex on the shape as a list     
def GetVertexLocations(shape):
    #Basic Variables:
    vertexAmount = 0
    #get Translateion node for future use
    translateNode = mc.listRelatives(shape, p = True)[0]
    
    #determine if it is a Nurbs or Mesh
    if mc.objectType(shape,i = "nurbsSurface"):
        print "nurbs"
        vertexAmount = GetNurbsVertexCount(translateNode)
    elif mc.objectType(shape,i = "mesh"):
        print "Mesh"
        vertexAmount = mc.polyEvaluate(shape, v = True)
    else:
        mc.error("Unsupported Geo, use polygon or nurbs")
    
    bIsSurface = mc.objectType(shape,i = "nurbsSurface")
    #print "vertexAmount on " + shape + "is: ", vertexAmount
    #Loop through vertex and get their wordspace postion in to a list and return the list to the caller:
    vertexLocationList = []
    for i in range(0, vertexAmount):
        if not bIsSurface:
            vertexName = shape + ".vtx[" + str(i) + "]"
        else:
            vertexName = shape + ".cv[" + str(i) + "]"
        vertexLocation = mc.xform(vertexName, q = True, ws = True, t = True)
        vertexLocationList.append(vertexLocation) 
    return vertexLocationList
    

#TODO this only support plane surfaces like ribbon
#return how many CV a Nurbs surface has
def GetNurbsVertexCount(surfaceName):
    TempGeo = mc.nurbsToPoly(surfaceName, f = 3, ch = False)
    geoVertCont = mc.polyEvaluate(TempGeo, v = True)
    mc.delete(TempGeo)
    return geoVertCont

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    