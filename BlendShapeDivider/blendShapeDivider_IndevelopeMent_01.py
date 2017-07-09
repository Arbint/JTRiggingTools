#BlendShape Divider
"""
Original reference: BlendTapper 5.0
Developed by Jingtian Li

Ver 1.0
"""

#Libraries
import maya.cmds as mc
import maya.OpenMaya as om
import maya.mel as mel


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
ApplyButtonSectionLayout = mc.rowColumnLayout(nc = 3)
mc.button(l = "Create Plane", w = 135, c = "CreatePlaneBtnCmd()")
mc.button(l = "Make blendshapes",w = 135, c = "MakeBlspBtnCmd()")
mc.button(l = "Cancel", w = 135,c = "CancelBtnCmd()")
mc.showWindow(BlendShapeDividerWindowID)

########################################################################
####                            Methods                             ####
########################################################################

#simple clamp fucntion:
def clamp(min, max, value):
    if value < min:
        value = min
    elif value > max:
        value = max
    return value

#smooth step using maya.mel.eval
def smoothStep(min, max, value):
    minString = str(min)
    maxString = str(max)
    valueString = str(value)    
    percentage = mel.eval("smoothstep(" + minString + "," + maxString + "," + valueString + ")" )
    return percentage

#print the x, y, z value of the om.MVector passed in
def printMVector(VectorToPrint):
    print VectorToPrint.x, VectorToPrint.y, VectorToPrint.z

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
    
def MakeBlspBtnCmd():

    #Gather Info from UI
    createCtroller = mc.checkBox(createCtrlCB, q = True, v = True)
    controllerType = mc.radioCollection("ControllerSelectionID", q = True, sl = True)
    NameBase = mc.textField("ControllerTextFieldID", q = True, tx = True)
    specifyBaseShape = mc.checkBox(SpecifyBaseShapeCB, q = True, v = True)
    BaseShapeFiledText = mc.textField("BasicShapeTextFieldID", q = True, tx = True)
    
    #find targetShape: 
    sel = mc.ls(sl = True)[0]
    ShapeNodeList = mc.listRelatives(sel, s = True)
    BaseShape = ""
    TargetShape = ""
    for item in ShapeNodeList:
        if mc.getAttr(item + ".intermediateObject"):
            continue
        else:
            TargetShape = item

    #find corresponding division planes
    divisionPlaneList = mc.ls(TargetShape + "_DivisionPlane_*", tr = True)
    if not len(divisionPlaneList):
        mc.error("no divisiton plane exist")
        return
    
    #Find BaseShape:
    BaseShape = mc.getAttr(TargetShape + "_DivisionPlane_1.baseShape")
    
    #find number of divistions specified:
    NumberOfDivisions = len(divisionPlaneList)

    #get base and target position and their vertex List:
    BasePosition = getTranslateNodePostion(BaseShape)
    TargetPosition = getTranslateNodePostion(TargetShape)
    BaseVertList = GetVertexLocations(BaseShape)
    TargetVertList = GetVertexLocations(TargetShape)
    
    #get Bounding box
    boundingBoxInfo = GetBoundingBox(BaseVertList, TargetVertList, BasePosition, TargetPosition)
    boundingBox = boundingBoxInfo[0]
    bIsBoundingBoxValid = boundingBoxInfo[1]

    print "base shape is: " + BaseShape
    print "Target Shape is: " + TargetShape
    print "Division Planes are:", divisionPlaneList 
    print "Number of Divisiion is:", str(NumberOfDivisions)
    
    newShapeList = []
    lastShape = TargetShape
    for currentDiv in range(0, NumberOfDivisions):
        blendedVerts = CalculateBlend(BaseVertList,TargetVertList, BasePosition, TargetPosition, boundingBox, NumberOfDivisions, currentDiv,divisionPlaneList)
        newShapeList.append(newBlend(blendedVerts, BaseShape, TargetShape, NumberOfDivisions, currentDiv, lastShape))
    
    
    
    
    
    
    
    
    
    
    
    
    
def newBlend(blendedVerts, BaseShape, TargetShape, NumberOfDivisions, currentDiv, lastShape):
    #duplicate and rename:
    newShape = TargetShape.replace("Shape", "") + "_" + str(currentDiv + 1)
    mc.duplicate(BaseShape, n = newShape)
        
    #move vertex:
    for i in range(0, len(blendedVerts)):
        #determine geo Type:
        if mc.objectType(BaseShape,i = "nurbsSurface"):
            print "it is nurbs, let's deal with it latter"
        if mc.objectType(BaseShape,i = "mesh"):   
            vert = newShape + ".vtx[" + str(i) + "]"
            vertPosition = blendedVerts[i]
            mc.xform(vert, ws = True, t = (vertPosition.x, vertPosition.y, vertPosition.z))
    
    
    
# get a list of vetex locations of the blendshape the division plane divisionPlaneList[currentDiv] should generate
def CalculateBlend(BaseVertList,TargetVertList, BasePosition, TargetPosition, boundingBox, NumberOfDivisions, currentDiv,divisionPlaneList):
    blendedVerts = []
    
    #seperate bounding box infomation in variables
    xMin = boundingBox[0]
    xMax = boundingBox[1]
    yMin = boundingBox[2]
    yMax = boundingBox[3]
    zMin = boundingBox[4]
    zMax = boundingBox[5]
    
    #get target and base traslation offset
    offset = TargetPosition - BasePosition
    
    #get current division plane position:
    PlanePosition = getPos(divisionPlaneList[currentDiv])
    
    #find plane shape coverage extremes:
    planeXMid = PlanePosition.x
    planeXMin = 0
    planeXMax = 0
    if currentDiv == 0:
        planeXMin = PlanePosition.x
    else:
        PrevisouPlanePosition = getPos(divisionPlaneList[currentDiv - 1])
        planeXMin = PrevisouPlanePosition.x
    if currentDiv == NumberOfDivisions - 1:
        planeXMax = PlanePosition.x
    else:
        NextPlanePosition = getPos(divisionPlaneList[currentDiv + 1])
        planeXMax = NextPlanePosition.x

    planeXMid -= offset.x
    planeXMin -= offset.x
    planeXMax -= offset.x

    for i in range(0, len(BaseVertList)):
        #adjustedVert is the position of the current vertex that is different between shapes shifted to base shape space
        adjustedVert = TargetVertList[i] - offset
        CurrentVertTranslateX = adjustedVert.x
        #figure out the max reaches the blend shape this division plane generate
        xMinV = planeXMin
        xMidV = planeXMid
        xMaxV = planeXMax
        
        #percentage is the distance percentage form the position of the current division plane to the edge of the current division plane coverage
        #if the vertex is between the min and mid range:
        if (CurrentVertTranslateX > xMinV and CurrentVertTranslateX < xMidV):
            percentage = smoothStep(xMinV, xMidV, CurrentVertTranslateX)
            percentage = 1.0 - percentage
        #if the vertex is between the mid and max range:
        elif (CurrentVertTranslateX > xMidV and CurrentVertTranslateX < xMaxV):
            percentage = smoothStep(xMidV, xMaxV, CurrentVertTranslateX)
        #if the vertex is right on the mid:
        elif (CurrentVertTranslateX == xMidV):
            percentage = 0.0
        #if the vertex is out of the min max range, it should have 0 percentage
        else:
            percentage = 1.0

        # calculate the current vertex postion of the generated blendshape by blending the base vertex position and the target vertex position by percentage
        blendedVerts.append((BaseVertList[i] * percentage) + (adjustedVert * (1-percentage)))
    return blendedVerts

    
def CreatePlaneBtnCmd():
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
    
    print "base shape is: " + BaseShape
    print "Target Shape is: " + TargetShape
    if specifyBaseShape and BaseShape == "":
        BaseShape = BaseShapeFiledText
    if BaseShape == "":
        print mc.error("Cannot Find Baseshape, please specify BaseShape Mannually")
    
    #gether per vertex translation and object translation
    baseVertexLocations= GetVertexLocations(BaseShape)
    targetVertexLocations = GetVertexLocations(TargetShape)
    baseTranslation = getTranslateNodePostion(BaseShape)
    targetTranslation = getTranslateNodePostion(TargetShape)
    
    #printMVector(baseTranslation)
    
    #get the bounding box of the offsetted vertex
    boundingBoxInfo = GetBoundingBox(baseVertexLocations, targetVertexLocations, baseTranslation, targetTranslation)
    boundingBox = boundingBoxInfo[0]
    bIsBoundingBoxValid = boundingBoxInfo[1]
    #print boundingBox, bIsBoundingBoxValid
    
    if(not bIsBoundingBoxValid):
        mc.error("There is no different between seleted shape and base shape")
    
    #create divistion Planes:
    MakeDivistionPlan(boundingBox, baseTranslation, targetTranslation, TargetShape, BaseShape, NumberOfDivision)
    print "Divistion Planes Created Succesfully!"
    mc.select(sel, r=True)
    
#get the world space location of the translatation node of the given shape        
def getTranslateNodePostion(shape):
    translateNode = mc.listRelatives(shape,p = True)[0]
    return getPos(translateNode)
def getPos(translateNode):
    location = mc.xform(translateNode, q = True, ws = True, t= True)
    locationVect = om.MVector(location[0], location[1], location[2])
    return locationVect
    
#return the world space locations of all the vertex on the shape as a list     
def GetVertexLocations(shape):
    #Basic Variables:
    vertexAmount = 0
    #get Translateion node for future use
    translateNode = mc.listRelatives(shape, p = True)[0]
    
    #determine if it is a Nurbs or Mesh
    if mc.objectType(shape,i = "nurbsSurface"):
        vertexAmount = GetNurbsVertexCount(translateNode)
    elif mc.objectType(shape,i = "mesh"):
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
        vertexLocationVect = om.MVector(vertexLocation[0], vertexLocation[1], vertexLocation[2])
        vertexLocationList.append(vertexLocationVect) 
    return vertexLocationList
    

#TODO this only support plane surfaces like ribbon
#return how many CV a Nurbs surface has
def GetNurbsVertexCount(surfaceName):
    TempGeo = mc.nurbsToPoly(surfaceName, f = 3, ch = False)
    geoVertCont = mc.polyEvaluate(TempGeo, v = True)
    mc.delete(TempGeo)
    return geoVertCont
    
#get the furest x, y, z, reach of all the area that base and target are different in base mesh space. also returns true if there is any different
def GetBoundingBox(baseVertPositionList, targetVertPositionList, baseTranslation, targetTranslation):
    boundingBox = []
    xMin = 999999
    xMax = -999999
    yMin = 999999
    yMax = -999999
    zMin = 999999
    zMax = -999999
    
    bHasAnyDifferent = False
    
    offset = targetTranslation - baseTranslation
    for i in range(0, len(baseVertPositionList)):
        #move target vert into the same as base vert
        adjustedVert = targetVertPositionList[i] - offset
        #find out if target vertex is different to base vertex
        difftolerance = 0.001
        baseVertex = baseVertPositionList[i]
        
        b_XIsDifferent = (adjustedVert.x < (baseVertex.x - difftolerance) or adjustedVert.x > (baseVertex.x + difftolerance))
        b_YIsDifferent = (adjustedVert.y < (baseVertex.y - difftolerance) or adjustedVert.y > (baseVertex.y + difftolerance))
        b_ZIsDifferent = (adjustedVert.z < (baseVertex.z - difftolerance) or adjustedVert.z > (baseVertex.z + difftolerance))
        
        bIsVertexDifferent = b_XIsDifferent or b_YIsDifferent or b_ZIsDifferent
        
        if bIsVertexDifferent:
            bHasAnyDifferent = True
            if adjustedVert.x < xMin:
                xMin = adjustedVert.x
            if adjustedVert.x > xMax:
                xMax = adjustedVert.x
            if adjustedVert.y < yMin:
                yMin = adjustedVert.y
            if adjustedVert.y > yMax:
                yMax = adjustedVert.y
            if adjustedVert.z < zMin:
                zMin = adjustedVert.z
            if adjustedVert.z > zMax:
                zMax = adjustedVert.z
    
    boundingBox.append(xMin)
    boundingBox.append(xMax)
    boundingBox.append(yMin)
    boundingBox.append(yMax)
    boundingBox.append(zMin)
    boundingBox.append(zMax)
    
    return boundingBox, bHasAnyDifferent

#create divistion planes and return their name as a list
def MakeDivistionPlan(boundingBox, basePosition, targetPosition, targetShape, baseShape, numOfDivision):
    Planes = []
    
    #get the offset:
    offset = targetPosition - basePosition
    #figure out dimensions:
    #x lenght of bounding box
    width = boundingBox[1] - boundingBox[0]
    #y length of bounding box
    height = boundingBox[3] - boundingBox[2]
    #z lenght of bounding box
    depth = boundingBox[5] - boundingBox[4]
    
    #find the posiiton bounding box on target mesh
    TargetBoundingBoxYPovit = ((boundingBox[2] + boundingBox[3])/2.0) + offset.y
    TargetBoundingBoxZPovit = ((boundingBox[4] + boundingBox[5])/2.0) + offset.z
    TargetBoundingBoxXPovit = ((boundingBox[0] + boundingBox[1])/2.0) + offset.x
    
    planGrpName = targetShape + "_DivistionPlaneGrp"
    #create an empty grp
    mc.group(n = planGrpName, em = True)
    
    #start making planes
    for i in range(0, numOfDivision):  
        #create the plane
        CreatePlaneResult = mc.polyPlane(n = targetShape + "_DivisionPlane_" + str(i + 1), ax = (1,0,0), w = depth*1.1, h = height * 1.1, sx = 1, sy = 1, ch = False)
        PlaneName = CreatePlaneResult[0]
        #Find the Translate.X of the plane: 
        PlaneXPosition = (width/(numOfDivision - 1.0))*i + TargetBoundingBoxXPovit - 0.5 * width
        #move the planeto the right place
        mc.move(PlaneXPosition, TargetBoundingBoxYPovit, TargetBoundingBoxZPovit, PlaneName)        
        
        #lock and hide unwanted attributes    
        mc.setAttr(PlaneName + ".r",l = True, k = False)
        mc.setAttr(PlaneName + ".s",l = True, k = False)  
        mc.setAttr(PlaneName + ".v",l = True, k = False) 
        mc.setAttr(PlaneName + ".tz",l = True, k = False) 
        mc.setAttr(PlaneName + ".ty",l = True, k = False) 
    
    #add baseShapeAttribute for futrue reference on the first plane:
        if i == 0:
            mc.addAttr(PlaneName, ln = "baseShape", dt = "string")
            mc.setAttr(PlaneName + ".baseShape", baseShape, type = "string")
            
        Planes.append(PlaneName)
        mc.parent(PlaneName, planGrpName)
    
    #Center poivots
    mc.xform(planGrpName,cp = True)
    #parent to targetShape
    #mc.parent(planGrpName, targetShape)
    return Planes
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    