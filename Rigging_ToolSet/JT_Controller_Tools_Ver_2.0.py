#developed by professor Li, free to use and modify
import maya.cmds as mc

#Data and Object Types:
class ControllerTypes:
    Circle = 1
    Sphere = 2
    

class globalMem:
    ControllerList = []
    curentController = 0
    bJtConvention = True


#global Variables
globalMemories = globalMem()

windowID = "JT_Controller_Tool_Set"
if(mc.window(windowID,q = True, exists = True)):
    mc.deleteUI(windowID)
    
if(mc.dockControl("dockWindows",q = True, exists = True)):
    mc.deleteUI("dockWindows")

window = mc.window(windowID, title = "JT Controller Tool Sets", rtf = True)

windowLayout = mc.columnLayout()
DockButton = mc.button(l = "dock UI", c = "dockWindow()", w=300)
#create Controller Section UI
controllerCreationLayout = mc.frameLayout(l ="Create Controllers", cll= True, w = 300)
controllerSubLayout = mc.rowColumnLayout(nc = 3, columnWidth =[(1, 120)])

mc.text(l = "Naming Conventions: ")
jtConvention = mc.checkBox(l = "jt Convention",v = True, onc = "ToggleJTConvention()", ofc = "ToggleJTConvention()")
mc.separator(st = "none", h = 10)
mc.text(l = "joint pre or Subfix: ")
jointFix = mc.textField(en = False)
mc.separator(st = "none", h = 10)
mc.text(l = "control pre or Subfix: ")
ControllerFix = mc.textField(en = False)
mc.separator(st = "none", h = 10)

mc.text(l = "locator pre or Subfix: ")
locatorFix = mc.textField(en = False)
mc.separator(st = "none", h = 10)

mc.text(l = "chose controller type: ", al = "right")
controllerShapeSelection = mc.radioCollection()
circleShape = mc.radioButton(l = "Circle", sl = True)
sphereShape = mc.radioButton(l = "Sphere")
mc.text(l = "controller Radius:", al = "right")
controllerRadiusField = mc.floatField(v = 1)
mc.separator(st = "none", h = 10)
GroupJntsOnlyCB = mc.checkBox(l = "Grp joints Only", v = False)
mc.separator(st = "none", h = 10)
mc.separator(st = "none", h = 10)

ControlMethodRC = mc.radioCollection()
ParentJntRB = mc.radioButton("Parent",l = "Parent", sl = True)
ConstraintJntsOnlyRB = mc.radioButton("Constraint",l = "Constraint", sl = False, onc = "constraintOn()", ofc = "ConstraintOff()")
ConnectJntRB = mc.radioButton("Connect",l = "connect", sl = False, onc = "ConnectOn()", ofc = "ConnectOff()")

mc.setParent(controllerCreationLayout)
ConstraintSelection = mc.rowColumnLayout(nc = 4)
mc.setParent(controllerCreationLayout)
mc.rowColumnLayout(nc = 2, cw = [(1, 150), (2, 150)])
createControllerButton = mc.button(l="Create", c = "createControlButtonCommand()")
createJntBtn = mc.button(l = "Create Jnt", c = "createJntUnderSelection()")
mc.setParent(controllerCreationLayout)
mc.text(l = "select Controllers and then Skin: ")
mc.rowColumnLayout(nc = 2)
FollowSkinOrientationCB = mc.checkBox(l = "Orientation", v = False)
FollowSkinCtrlButton = mc.button(l = "Make Follow Skin", c = "attachControllersToSkin()", w = 200)

#mirror Facial Controller section UI
mc.setParent(windowLayout)
FCSectionLayout = mc.frameLayout(l ="Mirror Controller", cll= True, w = 300)
FCMainLayout = mc.columnLayout() 
mc.text(l = "select top grps of controllers, jnts, and other relatives: ")
gatherInfoLayout = mc.rowColumnLayout(nc = 3)
mc.text("controls: ")
ctrlTextField = mc.textField(w = 215, ed = False)
assignCtrlBtn = mc.button(l = "<<<", c = "assignTextField(ctrlTextField)")
mc.text(l = "skin: ")
skinTextField = mc.textField(w = 215, ed = False)
assignSkinBtn = mc.button(l = "<<<", c = "assignTextField(skinTextField)")
mc.setParent(FCMainLayout)
mirrorSectionLayout = mc.rowColumnLayout(nc = 5)
mc.text(l = "mirror across:      ")
mirrorModeRC = mc.radioCollection()
mc.radioButton("XY", w = 30)
mc.radioButton("YZ", w = 30, sl = True)
mc.radioButton("XZ", w = 30)
PosToNageCB = mc.checkBox(l = "positive to negative", v = True)
mc.setParent(FCMainLayout)
excutionLayout = mc.rowColumnLayout(nc = 2)
mirrorButton = mc.button(l = "mirror",w = 150, c = "MirrorFacialRig()")
cancelButton = mc.button(l = "cancel",w = 150, c = "closMCWIDWindow()")

#tweek controller section UI
mc.setParent(windowLayout)
controlerTweekLayout = mc.frameLayout(l ="Tweek Controllers", cll= True, w = 300)
mc.text(l = "select the controllers and then: ")
conrollerTweekSubLayout = mc.rowColumnLayout(nc = 4, columnWidth = [(1, 70), (2, 70), (3, 70), (4, 70)])
TweekStartButton = mc.button(l = "start", c = "startTweekControllers()")
TweekNextButton = mc.button(l = "next", c = "TweekNextController()")
TweekPreviousButton = mc.button(l = "previous", c = "TweekPreviousController()") 
TweekOverButton = mc.button(l = "Finished", c = "TweekFinished()")


#Connector Section UI
mc.setParent(windowLayout)
ConnectorSecLayout = mc.frameLayout(l = "Easy Connection", w = 300, cll = True)
ConnectorSubLayout = mc.rowColumnLayout(nc = 5, columnWidth = [(1, 50), (2, 50), (3, 50), (4, 50), (5, 80)])
TxCheckBox = mc.checkBox(l = "X", v = True, ofc = "TCheckAllOff()")
TyCheckBox = mc.checkBox(l = "Y", v = True, ofc = "TCheckAllOff()")
TzCheckBox = mc.checkBox(l = "Z", v = True, ofc = "TCheckAllOff()")
TaCheckBox = mc.checkBox(l = "All", v = True, onc = "TCheckAllOn()", ofc = "TCheckOffAll()")
connectTransBtn = mc.button(l = "Connect Translate", w = 100, c = "ConnectTranslate()")

RxCheckBox = mc.checkBox(l = "X", v = True, ofc = "RCheckAllOff()")
RyCheckBox = mc.checkBox(l = "Y", v = True, ofc = "RCheckAllOff()")
RzCheckBox = mc.checkBox(l = "Z", v = True, ofc = "RCheckAllOff()")
RaCheckBox = mc.checkBox(l = "All", v = True, onc = "RCheckAllOn()", ofc = "RCheckOffAll()")
connectRotBtn = mc.button(l = "Connect Rotation", w = 100, c = "ConnectRotation()")

SxCheckBox = mc.checkBox(l = "X", v = True, ofc = "SCheckAllOff()")
SyCheckBox = mc.checkBox(l = "Y", v = True, ofc = "SCheckAllOff()")
SzCheckBox = mc.checkBox(l = "Z", v = True, ofc = "SCheckAllOff()")
SaCheckBox = mc.checkBox(l = "All", v = True, onc = "SCheckAllOn()", ofc = "SCheckOffAll()")
connectScaleBtn = mc.button(l = "Connect Scale", w = 100, c = "ConnectScale()")

mc.setParent(ConnectorSecLayout)
ExtraConnectBtnLayout = mc.rowColumnLayout(nc = 2, columnWidth = [(1, 150),(2,150)])
connectAllChannel = mc.button(l = "Connect All", w = 100, c = "ConnectAllChannel()")
connectVis = mc.button(l = "Connect Visibility", w = 100, c = "ConnectVisibility()")

#create jnt along crv section UI
mc.setParent(windowID)
ContJntAlongCrvLayout = mc.frameLayout(l = "create joints along curve", cll = True, w = 300)
mc.rowColumnLayout(nc = 4, columnWidth = [(1, 70), (2, 70), (3, 70), (4, 90)])
mc.text(l ="joint name:")
jointNameTextField = mc.textField()
mc.text(l = "joint amount: ")
jointAmountIntField = mc.intField(v = 3)
mc.text(l = "joint radius: ")
jointRadiusFloatField = mc.floatField(v = 1.0)
mc.text(l = "locator size: ")
locatorSizeFloatField = mc.floatField(v = 1.0)

mc.setParent(ContJntAlongCrvLayout)
mc.text(l = "use the Naming Convention undern the Create Controllers")
createJointAlongCrvBtn = mc.button(l = "create joints", c = "createJnt()")

#create ribbon based on curve selected section UI
mc.setParent(windowID)
RibbonUILayout = mc.frameLayout(l = "create ribbon", cll = True, w = 300)
mc.text(l = "select curve or nothing: ")
mc.rowColumnLayout(nc = 4)
mc.text(l = "bind joint count: ")
bindJntCountIntField = mc.intField(w = 50, v = 6)
mc.text(l = "control joint count: ")
ctrlJntCountIntField = mc.intField(w = 50, v = 3)
mc.text(l = "ribbon width: ")
RibbonWidthFloatField = mc.floatField(v = 0.5, w = 20)
mc.setParent(RibbonUILayout)
mc.rowColumnLayout(nc = 2)
mc.text(l = "ribbon name base: ")
RibbonNameField = mc.textField(w = 200)
mc.setParent(RibbonUILayout)
mc.rowLayout(nc = 6)
mc.text(l = "Direction: ")
ribbonDirectionRC = mc.radioCollection()
mc.radioButton("X")
mc.radioButton("Y", sl = True)
mc.radioButton("Z")
keepCrvCB = mc.checkBox(l = "keep curve", v = True)
usingNurbsCB = mc.checkBox( l = "use nurbs", v = False)
mc.setParent(RibbonUILayout)
mc.rowColumnLayout(nc = 3)
CreateCtrlCB = mc.checkBox(l = "Create Controllers", v = True)
ParentToHierachyCB = mc.checkBox(l = "Parent To Hierachy", v = False, onc = "ParentToHierachyCBOnCmd()", ofc = "ParentToHierachyCBOffCmd()")
mc.setParent(RibbonUILayout)
mc.rowColumnLayout(nc = 3)
parentJntText = mc.text(l = "parent Joint:", vis = False)
parentJntTextField = mc.textField(vis = False, ed = False, w = 200)
parentJntAssignTextFieldBtn = mc.button(l = "<<<", vis = False, c = "assignTextField(parentJntTextField)")
#useNurbs = mc.checkBox(l = "use nurbs", v = False)
mc.setParent(RibbonUILayout)
createRibbonBtn = mc.button(l = "Create Ribbon", c = "createRibbonBtnCmd()")

#Advanced connection section UI
mc.setParent(windowLayout)
AdvConnectLayout = mc.frameLayout(l = "Advanced Connection", cll = True, w = 300)
mc.rowColumnLayout(nc = 3)
mc.text(l = "connectFrom: ")
connectFromTextField = mc.textField(w = 190, ed = False)
CFassignButton = mc.button(l = "<<<", c = "setTextField(GetSelectedAttribute(), connectFromTextField)")
mc.text(l = "connectTo: ")
connectToTextField = mc.textField(w = 190, ed = False)
CTassignButton = mc.button(l = "<<<", c = "setTextField(GetSelectedAttribute(), connectToTextField)")

mc.setParent(AdvConnectLayout)
mc.rowColumnLayout(nc = 6)
PositiveNegativeRC = mc.radioCollection()
mc.radioButton("Pos", sl = True)
mc.radioButton("Neg")
mc.text(l = "factors:")
TfactorField = mc.floatField(v = 1.0)
SfactorField = mc.floatField(v = 1.0)
RfactorField = mc.floatField(v = 1.0)
mc.setParent(AdvConnectLayout)
AdvConnnectApplyBtn = mc.button(l = "Apply Connection", w = 300, c = "AdvConnectBtn()")


#Change Color Override section UI
mc.setParent(windowLayout)
ChangeColorOWLayout = mc.frameLayout(l = "change color override", cll = True, w = 300)
mc.rowColumnLayout(nc = 4)
colorPickRC = mc.radioCollection()
mc.radioButton("Red", sl = True);
mc.radioButton("Green");
mc.radioButton("Blue");
mc.radioButton("Yellow");
mc.setParent(ChangeColorOWLayout)
mc.columnLayout()
mc.button(l = "change", w = 300, c = "changeColorBtnCmd()")
mc.showWindow(windowID)

####################################################################################
### Methods
####################################################################################
def changeColorOverride(obj, colorCode):
    shapes = mc.listRelatives(obj, s = True)
    for item in shapes:
        mc.setAttr(item + ".overrideEnabled", 1)
        mc.setAttr(item +".overrideColor", colorCode)   
        
def changeColorBtnCmd():
    selection = mc.ls(sl = True)
    colorChoice = mc.radioCollection(colorPickRC, q = True, sl = True)
    if colorChoice == "Red":
        colorCode = 13
    elif colorChoice == "Green":
        colorCode = 14
    elif colorChoice == "Blue":
        colorCode = 6
    else:
        colorCode = 17
    for item in selection:
        changeColorOverride(item, colorCode);
def GetSelectedAttribute():
    selectedObj = mc.ls(sl = True)[0]
    Attr = mc.channelBox("mainChannelBox", q = True, sma = True)[0]
    selectedObjAttr = selectedObj + "." + Attr
    return selectedObjAttr
    
def setTextField(content, textFieldToSet):
    mc.textField(textFieldToSet, e = True, tx = content)
      
def getText(textFieldToGet):
    return mc.textField(textFieldToGet, q = True, tx = True)

def createClamp(name, clampPos):
    if not mc.objExists(name):
        mc.createNode("clamp", n = name)
        if clampPos:
            mc.setAttr(name + ".maxR", 10000)
            mc.setAttr(name + ".maxG", 10000)
            mc.setAttr(name + ".maxB", 10000)        
        else:
            mc.setAttr(name + ".minR", -10000)
            mc.setAttr(name + ".minG", -10000)
            mc.setAttr(name + ".minB", -10000)
def createInvertMD(name):
    if not mc.objExists(name):
        mc.createNode("multiplyDivide", n = name)
        mc.setAttr(name + ".input2X", -1)
        mc.setAttr(name + ".input2Y", -1)
        mc.setAttr(name + ".input2Z", -1)

def ConnectAttrCheck(connectFrom, connectTo):
    if not mc.isConnected(connectFrom, connectTo, iuc = True):
        print "here we go"
        mc.connectAttr(connectFrom, connectTo)
    else:
        print "already connected"
        
def createScaleMD(name, factor):
    if not mc.objExists(name):
        mc.createNode("multiplyDivide", n = name)
    mc.setAttr(name + ".input2X", factor)
    mc.setAttr(name + ".input2Y", factor)
    mc.setAttr(name + ".input2Z", factor)
    
        


def AdvConnectBtn():
    #gather info:
    connectFromAttr = getText(connectFromTextField)
    connectToAttr = getText(connectToTextField)
    connectFromObj = connectFromAttr.split(".")[0]
    connectToObj = connectToAttr.split(".")[0]
    connectFromAttrSingle = connectFromAttr.split(".")[-1]
    print connectFromAttrSingle
    PositiveNegativeRCSelection = mc.radioCollection(PositiveNegativeRC, q = True, sl = True)
    bUsePositive = False
    if PositiveNegativeRCSelection == "Pos":
        bUsePositive = True
    TfactorValue = mc.floatField(TfactorField, q = True, v = True)
    SfactorValue = mc.floatField(SfactorField, q = True, v = True)
    RfactorValue = mc.floatField(RfactorField, q = True, v = True)
        
    #construct node name
    TransFactor = "MD_TransFactor_" + connectFromObj
    ScaleFactor = "MD_ScaleFactor_" + connectFromObj
    RotFactor = "MD_RotFactor_" + connectFromObj
    
    NegClampTrans = "Clamp_Neg_Trans_" + connectFromObj
    NegClampScale = "Clamp_Neg_Scale_" + connectFromObj
    NegClampRot = "Clamp_Neg_Rot_" + connectFromObj
    NegMDTrans = "MD_Neg_Trans_" + connectFromObj
    NegMDScale = "MD_Neg_Scale_" + connectFromObj
    NegMDRot = "MD_Neg_Rot_" + connectFromObj
    
    PosClampTrans = "Clamp_Pos_Trans_" + connectFromObj
    PosClampScale = "Clamp_Pos_Scale_" + connectFromObj
    PosClampRot = "Clamp_Pos_Rot_" + connectFromObj

    #createNodes:
    createScaleMD(TransFactor, TfactorValue)
    createScaleMD(ScaleFactor, SfactorValue)
    createScaleMD(RotFactor, RfactorValue)
    
    createClamp(NegClampTrans, False)
    createClamp(NegClampScale, False)
    createClamp(NegClampRot, False)
    createClamp(PosClampTrans, True)
    createClamp(PosClampScale, True)
    createClamp(PosClampRot, True)
    
    createInvertMD(NegMDTrans)
    createInvertMD(NegMDScale)
    createInvertMD(NegMDRot)
    
    #connect Attributes:
    ConnectAttrCheck(connectFromObj + ".translate", TransFactor + ".input1")
    ConnectAttrCheck(connectFromObj + ".scale", ScaleFactor + ".input1")
    ConnectAttrCheck(connectFromObj + ".rotate", RotFactor + ".input1")
    
       
    ConnectAttrCheck(TransFactor + ".output", NegClampTrans + ".input")
    ConnectAttrCheck(ScaleFactor + ".output", NegClampScale + ".input")
    ConnectAttrCheck(RotFactor + ".output", NegClampRot + ".input")
    
    ConnectAttrCheck(TransFactor + ".output", PosClampTrans + ".input")
    ConnectAttrCheck(ScaleFactor + ".output", PosClampScale + ".input")
    ConnectAttrCheck(RotFactor + ".output", PosClampRot + ".input")
    
    ConnectAttrCheck(NegClampTrans + ".output", NegMDTrans + ".input1")
    ConnectAttrCheck(NegClampScale + ".output", NegMDScale + ".input1")
    ConnectAttrCheck(NegClampRot + ".output", NegMDRot + ".input1")
    
    #finally apply connect to desired attrbute
    if connectFromAttrSingle == "tx" and bUsePositive:
        ConnectAttrCheck(PosClampTrans + ".outputR", connectToAttr)
    elif connectFromAttrSingle == "ty" and bUsePositive:    
        ConnectAttrCheck(PosClampTrans + ".outputG", connectToAttr)
    elif connectFromAttrSingle == "tz" and bUsePositive:    
        ConnectAttrCheck(PosClampTrans + ".outputB", connectToAttr)
    
    elif connectFromAttrSingle == "sx" and bUsePositive:    
        ConnectAttrCheck(PosClampScale + ".outputR", connectToAttr)
    elif connectFromAttrSingle == "sy" and bUsePositive:    
        ConnectAttrCheck(PosClampScale + ".outputG", connectToAttr)
    elif connectFromAttrSingle == "sz" and bUsePositive:    
        ConnectAttrCheck(PosClampScale + ".outputB", connectToAttr)
    
    elif connectFromAttrSingle == "rx" and bUsePositive:    
        ConnectAttrCheck(PosClampRot + ".outputR", connectToAttr)    
    elif connectFromAttrSingle == "ry" and bUsePositive:    
        ConnectAttrCheck(PosClampRot + ".outputG", connectToAttr)  
    elif connectFromAttrSingle == "rz" and bUsePositive:    
        ConnectAttrCheck(PosClampRot + ".outputB", connectToAttr)   
    
    elif connectFromAttrSingle == "tx" and not bUsePositive:    
        ConnectAttrCheck(NegMDTrans + ".outputX", connectToAttr)
    elif connectFromAttrSingle == "ty" and not bUsePositive:    
        ConnectAttrCheck(NegMDTrans + ".outputY", connectToAttr)
    elif connectFromAttrSingle == "tz" and not bUsePositive:    
        ConnectAttrCheck(NegMDTrans + ".outputZ", connectToAttr)
        
    elif connectFromAttrSingle == "sx" and not bUsePositive:    
        ConnectAttrCheck(NegMDScale + ".outputX", connectToAttr)        
    elif connectFromAttrSingle == "sy" and not bUsePositive:    
        ConnectAttrCheck(NegMDScale + ".outputY", connectToAttr)        
    elif connectFromAttrSingle == "sz" and not bUsePositive:    
        ConnectAttrCheck(NegMDScale + ".outputZ", connectToAttr)
           
    elif connectFromAttrSingle == "rx" and not bUsePositive:    
        ConnectAttrCheck(NegMDRot + ".outputX", connectToAttr)        
    elif connectFromAttrSingle == "ry" and not bUsePositive:    
        ConnectAttrCheck(NegMDRot + ".outputY", connectToAttr)        
    elif connectFromAttrSingle == "rz" and not bUsePositive:    
        ConnectAttrCheck(NegMDRot + ".outputZ", connectToAttr)
    
def clearTransformInputs(obj):
    mc.delete(obj + ".tx", icn = True)
    mc.delete(obj + ".ty", icn = True)
    mc.delete(obj + ".tz", icn = True)
    mc.delete(obj + ".rx", icn = True)
    mc.delete(obj + ".ry", icn = True)
    mc.delete(obj + ".rz", icn = True)
    mc.delete(obj + ".sx", icn = True)
    mc.delete(obj + ".sy", icn = True)
    mc.delete(obj + ".sz", icn = True)

def createJntUnderObj(obj, nameBase = None, radius = 1):
    mc.select(obj, r = True)
    #determine Name
    if nameBase == None:
        jntName = "jt_" + obj.replace("ac_", "")
    else:
        jntName = "jt_" + nameBase
    locName = jntName.replace("jt_", "loc_")
    grpName = jntName + "_grp"
    
    mc.joint(n = jntName, rad = radius)
    mc.spaceLocator( n = locName) 
    locatorShape = mc.listRelatives(locName, s = True)[0]
    mc.setAttr(locatorShape + ".visibility", 0)
    mc.group(n = grpName)
    
    mc.matchTransform(grpName, obj)
    mc.parent(grpName, obj)
    mc.parent(jntName, locName)
    return jntName, locName, grpName
    

        
    
def constraintToCurve(obj, crv, uValue = 0.5, freeChannel = False):
    motionPath = mc.pathAnimation(obj, crv, f = True, fm = True)
    MotionPathAnimationInput = motionPath + "_uValue.output"
    mc.disconnectAttr(MotionPathAnimationInput, motionPath + ".uValue")
    mc.setAttr(motionPath + ".uValue", uValue)    
    if freeChannel:
        print "freeing channel"
        clearTransformInputs(obj)
        mc.delete(motionPath)

def ParentToHierachyCBOnCmd():
    mc.text(parentJntText, e = True, vis = True)
    mc.textField(parentJntTextField, e = True, vis = True)  
    mc.button(parentJntAssignTextFieldBtn, e = True, vis = True)

def ParentToHierachyCBOffCmd():
    mc.text(parentJntText, e = True, vis = False)
    mc.textField(parentJntTextField, e = True, vis = False)  
    mc.button(parentJntAssignTextFieldBtn, e = True, vis = False)

def createRibbonBtnCmd():
    #gather info:
    bindJntCount = mc.intField(bindJntCountIntField, q = True, v = True)
    ctrlJntCount = mc.intField(ctrlJntCountIntField, q = True, v = True)
    ribbonWidth = mc.floatField(RibbonWidthFloatField, q = True, v = True)
    ribbonNameBase = mc.textField(RibbonNameField, q = True, tx = True)
    ribbonName = "ribbon_" + ribbonNameBase
    bindJntNameBase = "jt_" + ribbonNameBase + "_bind"
    ctrlJntNameBase = "jt_" + ribbonNameBase + "_drv"
    ribbonDirectionQuery = mc.radioCollection(ribbonDirectionRC, q = True, sl = True)
    ribbonDirection = [0, 0, 0]
    if ribbonDirectionQuery == "X":
        ribbonDirection[0] = 1.0
    elif ribbonDirectionQuery == "Y":
        ribbonDirection[1] = 1.0
    else:
        ribbonDirection[2] = 1.0
    shouldKeepCrv = mc.checkBox(keepCrvCB, q = True, v = True)
    useNurbs = mc.checkBox(usingNurbsCB, q = True, v = True)
    CreateCtrollers = mc.checkBox(CreateCtrlCB, q = True, v = True)
    ParentToHierachy = mc.checkBox(ParentToHierachyCB, q = True, v = True)
    
    #create ribbon nurbs
    selection = mc.ls(sl = True) or []
    if len(selection) and not useNurbs:
        # "create a ribbon using crv selected"
        BaseCurve = selection[0]
        mc.select(BaseCurve, r = True)
        mc.rebuildCurve(BaseCurve, ch = False, s = bindJntCount, d = 3)
        mc.makeIdentity(BaseCurve, apply = True)
        curveOne = mc.duplicate(BaseCurve)
        curveTwo = mc.duplicate(BaseCurve)
        mc.select(curveOne, r = True)
        mc.move(ribbonDirection[0]/2 * ribbonWidth, ribbonDirection[1]/2 * ribbonWidth, ribbonDirection[2]/2 * ribbonWidth, ws = True)
        mc.select(curveTwo, r = True)
        mc.move(-1 * ribbonDirection[0]/2 * ribbonWidth, -1 * ribbonDirection[1]/2 * ribbonWidth, -1 * ribbonDirection[2]/2 * ribbonWidth, ws = True)
        print ""
        mc.loft(curveTwo, curveOne, n = ribbonName, ch = False, rsn = True)
        mc.rebuildSurface(ribbonName,ch = False, su = bindJntCount, sv = 1, du = 3, dv = 3)
        #clean up:
        mc.delete(curveOne)
        mc.delete(curveTwo)
    elif len(selection) and useNurbs:
    		#use the nurbs selected
        ribbonNurbs = mc.ls(sl = True)[0]
        mc.rename(ribbonNurbs, ribbonName)
        # crete a curve here as the base curve
        mc.select(ribbonName + ".v[0.5]", r = True)
        BaseCurve = mc.duplicateCurve(ribbonName + ".v[0.5]", ch = False) 
        
    else:
        #create a ribbon from scratch
        ribbonNurbs = mc.nurbsPlane(u = bindJntCount,ax = (ribbonDirection[0], ribbonDirection[1], ribbonDirection[2]), n = ribbonName, lr = 1.0/bindJntCount, w = bindJntCount)
        # crete a curve here as the base curve
        mc.select(ribbonName + ".v[0.5]", r = True)
        BaseCurve = mc.duplicateCurve(ribbonName + ".v[0.5]", ch = False) 
    

    #start creating folicles and jnts:
    folicleList = []
    bindJntList = []
    bindJntLocList = []
    bindJntGrpList = []
    for iter in range(1, bindJntCount + 1):
        folicleU = 1.0/(bindJntCount - 1.0) * (iter - 1)
        folicle = createFolicle(ribbonName, folicleU, 0.5, iter)
        folicleList.append(folicle[1])
        bindJntHierachy = createJntUnderObj(folicle[1], folicle[1].replace("follicle_", ""), ribbonWidth/2)
        bindJnt = bindJntHierachy[0]
        bindJntLoc = bindJntHierachy[1]
        bindJntGrp = bindJntHierachy[2]
        
        bindJntList.append(bindJnt)
        bindJntLocList.append(bindJntLoc)
        bindJntGrpList.append(bindJntGrp)

    #start create control jnts:
    ctrlJntGrpList = []
    ctrlJntLocList = []
    ctrlJntList = []
    ctrlJntFolicleList = []
    for iter in range(1, ctrlJntCount + 1):
        #gather info
        ctrlJntName =  ctrlJntNameBase + "_" + str(iter).zfill(2)
        uValue = 1.0/(ctrlJntCount - 1.0) * (iter - 1)
        
        mc.select(cl = True)
        mc.joint(n = ctrlJntName, rad = ribbonWidth)
        ctrlJntList.append(ctrlJntName)
        jntGrpList = groupJntHierachy(ctrlJntName)
        jntGrp = jntGrpList[0]
        jntLocName = jntGrpList[1]
        ctrlJntGrpList.append(jntGrp)
        ctrlJntLocList.append(jntLocName)
        #new way of aligning to ribbon surface orientation
        folicleU = 1.0/(ctrlJntCount - 1.0) * (iter - 1)
        folicle = createFolicle(ribbonName, folicleU, 0.5, iter, "jt_temp_")
        mc.matchTransform(jntGrp, folicle[1])
        mc.delete(folicle)
    
    #bind ctrl jnts with ribbon:
    mc.select(ctrlJntList, r = True)
    mc.select(ribbonName, add = True)
    mc.skinCluster()
    
    #clean up and orgnization:
    if not shouldKeepCrv:
        mc.delete(BaseCurve)
    TopGrpList = []
    follicleGrpName = ribbonName + "_follicles_grp"
    mc.group(folicleList,n = follicleGrpName)
    ctrlGrpName = ribbonName + "_skin_jt_grp"
    mc.group(ctrlJntGrpList, n = ctrlGrpName)
    TopGrpList.append(follicleGrpName)
    TopGrpList.append(ctrlGrpName)
    TopGrpList.append(ribbonName)
    
    #if single hierachy needed:
    if ParentToHierachy:
        parentJnt = mc.textField(parentJntTextField, q = True, tx = True)
        for iter in range(0, len(folicleList)):
            mc.parent(bindJntList[iter], parentJnt)
            mc.parentConstraint(folicleList[iter], bindJntList[iter])
            
        mc.delete(bindJntLocList)
        mc.delete(bindJntGrpList)
        
        #do constraints:
        mc.parentConstraint(parentJnt, ctrlGrpName, mo = True)
    
    #if create controllers:
    if CreateCtrollers:
        mc.select(cl = True)
        mc.select(ctrlJntLocList)
        controllerGrpList = createControlButtonCommand()
        controllerTopGrpName = "ac_" + ribbonName + "_grp"
        mc.group(controllerGrpList, n = controllerTopGrpName)
        if ParentToHierachy:
            mc.parentConstraint(parentJnt, controllerTopGrpName, mo = True)
        TopGrpList.append(controllerTopGrpName)
    #final grping
    mc.group(TopGrpList, n = ribbonName + "_grp")
    
#create jnt along crv funcion
def createJnt():

    curveSelected = mc.ls(sl = True)[0]
    jntBaseName = mc.textField(jointNameTextField, q = True, tx = True)
    jntAmount = mc.intField(jointAmountIntField, q = True, v = True)
    jntRadius = mc.floatField(jointRadiusFloatField, q = True, v = True)
    locSize = mc.floatField(locatorSizeFloatField, q= True, v= True)
    
    for iter in range(0, jntAmount):
        jointName = jntBaseName + "_" + str(iter + 1).zfill(2)
        if jntAmount == 1:
            uValue = 0.5
        else:
            uValue = 1.0/(jntAmount-1.0) * iter
        
        mc.select(cl = True)
        mc.joint( n = jointName, rad = jntRadius)
        jntGrp = groupJntHierachy(jointName, locSize)[0]
        constraintToCurve(jntGrp, curveSelected, uValue)
    
def groupJntHierachy(jnt, locSize = 1.0):
    print "grouping"
    jntFix = "jt_"
    ctlFix = "ac_"
    locFix = "loc_"
    
    if globalMemories.bJtConvention == False:
        jntFix = mc.textField(jointFix, q = True, tx = True)
        ctlFix = mc.textField(ControllerFix, q = True, tx = True)
        locFix = mc.textField(locatorFix, q = True, tx = True)
        
    nameBase = jnt.replace(jntFix, "").replace("_bind", "").replace("_drv", "")
    locatorName = locFix + nameBase
    groupName = nameBase + "_grp"

    mc.spaceLocator(n = locatorName)
    mc.setAttr(locatorName + ".localScaleX", locSize)
    mc.setAttr(locatorName + ".localScaleY", locSize)
    mc.setAttr(locatorName + ".localScaleZ", locSize)
    
    mc.select(locatorName, r = True)
    mc.group(n = groupName)
    mc.parent(jnt, locatorName)
    return groupName, locatorName
    

def createControlButtonCommand():
    selection = mc.ls(sl = True)
    controllersList = []
    
    jntFix = "jt_"
    ctlFix = "ac_"
    locFix = "loc_"
    ControllerGrpList = []
    
    if globalMemories.bJtConvention == False:
        jntFix = mc.textField(jointFix, q = True, tx = True)
        ctlFix = mc.textField(ControllerFix, q = True, tx = True)
        locFix = mc.textField(locatorFix, q = True, tx = True)
        
    for item in selection:
        nameBase = item.replace(jntFix, "").replace("_bind", "").replace("_drv", "")
        controllerName = ctlFix + nameBase
        locatorName = locFix + controllerName
        groupName = controllerName + "_grp"
        controllerRadius = mc.floatField(controllerRadiusField, q= True, v = True)
        ControllerGrpList.append(groupName)
        bGrpJntOnly = mc.checkBox(GroupJntsOnlyCB, q = True, v = True)
        #bConstraintJntOnly = mc.checkBox(ConstraintJntsOnlyCB, q = True, v = True) 
       
        controller = ""
       
        #determine the control users want to use:
        if  bGrpJntOnly == False:

            #We have to Create Controller, fisrt check controller type and create controller:
            isControllerCircle = mc.radioButton(circleShape, q= True, sl = True)
            if isControllerCircle:
                controller = mc.circle(n = controllerName, r = controllerRadius)
            else:
                controller = mc.sphere(n = controllerName, r = controllerRadius)  
            
            #create other elements:
            mc.spaceLocator(n = locatorName)
            mc.setAttr(locatorName + "Shape.visibility", 0)
            mc.parent(controllerName, locatorName)
            mc.select(locatorName, r = True)
            mc.group(n = groupName)
            mc.matchTransform(groupName, item)
            
            #now determine how we control the joints           
            
            controlMethod = mc.radioCollection(ControlMethodRC, q = True, sl = True)
            
            
            if controlMethod == "Constraint":
                # user want to only constraint joint, we do constraints
                ConstraintSelection = mc.radioCollection("rs", q = True, sl = True)
                if ConstraintSelection == "PrbID":
                    mc.pointConstraint(controllerName, item)
                if ConstraintSelection == "PobID":
                    mc.parentConstraint(controllerName, item)
                if ConstraintSelection == "OobID":
                    mc.orientConstraint(controllerName, item)  
                if mc.checkBox("scaleCB", q = True, v = True):
                    mc.scaleConstraint(controllerName, item)
            elif controlMethod == "Parent":
                # user wants to parent the joint we parent the joint to the controller
                mc.parent(item, controllerName)
            else:
                #user want's to do connection:
                ConnectAllChannel(controllerName,item)
            controllersList.append(controllerName)

        else:
            #we only need to group joint
            mc.spaceLocator(n = locatorName)
            mc.select(locatorName, r = True)
            mc.group(n = groupName)
            mc.matchTransform(groupName, item)
            mc.parent(item, locatorName)
    return ControllerGrpList
        
        
def tweekController(controllerToTweek):
    mc.select(controllerToTweek, r = True)
    mc.selectMode(component = True)
    

def startTweekControllers():
    globalMemories.ControllerList = mc.ls(sl = True)
    tweekController(globalMemories.ControllerList[0])
    globalMemories.curentController = 0
    
def TweekNextController():
    if globalMemories.curentController == (len(globalMemories.ControllerList) - 1):
        globalMemories.curentController = 0
        tweekController(globalMemories.ControllerList[0])
    else:
        tweekController(globalMemories.ControllerList[globalMemories.curentController + 1])
        globalMemories.curentController += 1

def TweekPreviousController():
    if globalMemories.curentController == 0:
        globalMemories.curentController = len(globalMemories.ControllerList) - 1
        tweekController(globalMemories.ControllerList[-1])
    else:
        tweekController(globalMemories.ControllerList[globalMemories.curentController - 1])
        globalMemories.curentController -= 1

def TweekFinished():
    mc.selectMode(object = True)
    mc.select(globalMemories.ControllerList, r= True)
    
def ToggleJTConvention():
    globalMemories.bJtConvention = not globalMemories.bJtConvention
    if globalMemories.bJtConvention == False:
        mc.textField(jointFix, e = True, en = True)
        mc.textField(ControllerFix, e = True, en = True)
        mc.textField(locatorFix, e = True, en = True)
    else:
        mc.textField(jointFix, e = True, en = False)
        mc.textField(ControllerFix, e = True, en = False)
        mc.textField(locatorFix, e = True, en = False)
         
def constraintOn():
    RadioSelectionID = "rs"
    PrbID = "PrbID"
    PobID = "PobID"
    OobID = "OobID"
    
    mc.setParent(ConstraintSelection)
    if mc.radioCollection(RadioSelectionID,q = True, exists = True):
        mc.deleteUI(PrbID, ctl = True)
        mc.deleteUI(PobID, ctl = True)
        mc.deleteUI(OobID, ctl = True)
        mc.deleteUI(RadioSelectionID)
        mc.deleteUI("scaleCB")
    
    mc.radioCollection(RadioSelectionID)
    mc.radioButton(PrbID, l = "Point")
    mc.radioButton(PobID, l = "Parent")
    mc.radioButton(OobID, l = "Orient")
    mc.checkBox("scaleCB" ,l = "Scale")
    
def ConstraintOff():
    RadioSelectionID = "rs"
    PrbID = "PrbID"
    PobID = "PobID"
    OobID = "OobID"
    
    mc.deleteUI(PrbID, ctl = True)
    mc.deleteUI(PobID, ctl = True)
    mc.deleteUI(OobID, ctl = True)
    mc.deleteUI(RadioSelectionID)
    mc.deleteUI("scaleCB")
    
def ConnectOn():
    textID = "CTID"
    
    mc.setParent(ConstraintSelection)
    if mc.text(textID, q = True, exists = True):
        mc.deleteUI(textID)
    mc.text(textID, l = "use the settings under Easy Connection")
    
def ConnectOff():
    textID = "CTID"
    if mc.text(textID, q = True, exists = True):
        mc.deleteUI(textID)
    
     
def dockWindow():
    allowedAreas = ['right', 'left']
    if mc.dockControl("dockWindows", q= True, exists = True):
        return
    mc.dockControl( "dockWindows",l = "JT Controller Tool Sets",area='left', content=window, allowedArea=allowedAreas )
    
def TCheckAllOff():
    mc.checkBox(TaCheckBox, e = True, v = False)
def SCheckAllOff():
    mc.checkBox(SaCheckBox, e = True, v = False)
def RCheckAllOff():
    mc.checkBox(RaCheckBox, e = True, v = False)

def TCheckAllOn():
    mc.checkBox(TxCheckBox, e = True, v = True)
    mc.checkBox(TyCheckBox, e = True, v = True)
    mc.checkBox(TzCheckBox, e = True, v = True)
def RCheckAllOn():
    mc.checkBox(RxCheckBox, e = True, v = True)
    mc.checkBox(RyCheckBox, e = True, v = True)
    mc.checkBox(RzCheckBox, e = True, v = True)
def SCheckAllOn():
    mc.checkBox(SxCheckBox, e = True, v = True)
    mc.checkBox(SyCheckBox, e = True, v = True)
    mc.checkBox(SzCheckBox, e = True, v = True)
    
def TCheckOffAll():
    mc.checkBox(TxCheckBox, e = True, v = False)
    mc.checkBox(TyCheckBox, e = True, v = False)
    mc.checkBox(TzCheckBox, e = True, v = False)
def RCheckOffAll():
    mc.checkBox(RxCheckBox, e = True, v = False)
    mc.checkBox(RyCheckBox, e = True, v = False)
    mc.checkBox(RzCheckBox, e = True, v = False)
def SCheckOffAll():
    mc.checkBox(SxCheckBox, e = True, v = False)
    mc.checkBox(SyCheckBox, e = True, v = False)
    mc.checkBox(SzCheckBox, e = True, v = False)
    
def ConnectTranslate(connectFrom = None, connectTo = None):
    if connectFrom == None and connectTo == None:
        connectFrom = mc.ls(sl = True)[0]
        connectTo = mc.ls(sl = True)[1]
    
    if mc.checkBox(TxCheckBox, q = True, v = True) and (not mc.isConnected(connectFrom + ".tx", connectTo + ".tx")):
        mc.connectAttr(connectFrom + ".tx", connectTo + ".tx")
    if mc.checkBox(TyCheckBox, q = True, v = True) and (not mc.isConnected(connectFrom + ".ty", connectTo + ".ty")):
        mc.connectAttr(connectFrom + ".ty", connectTo + ".ty")
    if mc.checkBox(TzCheckBox, q = True, v = True) and (not mc.isConnected(connectFrom + ".tz", connectTo + ".tz")):
        mc.connectAttr(connectFrom + ".tz", connectTo + ".tz")

    
def ConnectRotation(connectFrom = None, connectTo = None):
    if connectFrom == None and connectTo == None:
        connectFrom = mc.ls(sl = True)[0]
        connectTo = mc.ls(sl = True)[1]
    
    if mc.checkBox(RxCheckBox, q = True, v = True) and (not mc.isConnected(connectFrom + ".rx", connectTo + ".rx")):
        mc.connectAttr(connectFrom + ".rx", connectTo + ".rx")
    if mc.checkBox(RyCheckBox, q = True, v = True) and (not mc.isConnected(connectFrom + ".ry", connectTo + ".ry")):
        mc.connectAttr(connectFrom + ".ry", connectTo + ".ry")
    if mc.checkBox(RzCheckBox, q = True, v = True) and (not mc.isConnected(connectFrom + ".rz", connectTo + ".rz")):
        mc.connectAttr(connectFrom + ".rz", connectTo + ".rz")

    
def ConnectScale(connectFrom = None, connectTo = None):
    if connectFrom == None and connectTo == None:
        connectFrom = mc.ls(sl = True)[0]
        connectTo = mc.ls(sl = True)[1]
    
    if mc.checkBox(SxCheckBox, q = True, v = True) and (not mc.isConnected(connectFrom + ".sx", connectTo + ".sx")):
        mc.connectAttr(connectFrom + ".sx", connectTo + ".sx")
    if mc.checkBox(SyCheckBox, q = True, v = True) and (not mc.isConnected(connectFrom + ".sy", connectTo + ".sy")):
        mc.connectAttr(connectFrom + ".sy", connectTo + ".sy")
    if mc.checkBox(SzCheckBox, q = True, v = True) and (not mc.isConnected(connectFrom + ".sz", connectTo + ".sz")):
        mc.connectAttr(connectFrom + ".sz", connectTo + ".sz")

    
def ConnectVisibility(connectFrom = None, connectTo = None):
    if connectFrom == None and connectTo == None:
        connectFrom = mc.ls(sl = True)[0]
        connectTo = mc.ls(sl = True)[1]
    
    if not mc.isConnected(connectFrom + ".v", connectTo + ".v"):
        mc.connectAttr(connectFrom + ".v", connectTo + ".v")
    
def ConnectAllChannel(connectFrom = None, connectTo = None):    
    ConnectTranslate(connectFrom, connectTo)
    ConnectRotation(connectFrom, connectTo)
    ConnectScale(connectFrom, connectTo)
    

def createJntUnderSelection():
    selection = mc.ls(sl = True)
    jntRadius = mc.floatField(controllerRadiusField, q = True, v = True)
    for item in selection:
        jntCollection = createJntUnderObj(item, None, jntRadius)
        mc.parent(jntCollection[2], w = True)
        loc = jntCollection[1]
        print loc
        ConnectAllChannel(item, loc)


def attachControllersToSkin():
    selected = mc.ls(sl = True)
    FolicleIndex = 1;
    bShouldConstrainOrientation = mc.checkBox(FollowSkinOrientationCB, q = True, v = True)
    
    for item in selected:
    	#if the item is the mesh then do noting
    	if item == selected[-1]:
    		continue
    	Controller = item
    	geoName = selected[-1]
    
    	Positionlocator = mc.spaceLocator()
    	
    	mc.matchTransform(Positionlocator, Controller)
    	
    	closestPoint = mc.createNode('closestPointOnMesh')
    	
    	#get the location of the locator
    	locatorPosition = mc.xform(Positionlocator, t = True, q= True, ws = True)
    	
    	#Setup the closestPosition Node:
    	mc.connectAttr(geoName + ".outMesh", closestPoint + ".inMesh")
    	mc.setAttr(closestPoint + ".inPositionX", locatorPosition[0])
    	mc.setAttr(closestPoint + ".inPositionY", locatorPosition[1])
    	mc.setAttr(closestPoint + ".inPositionZ", locatorPosition[2])
    	
    	mc.delete(Positionlocator)
    	
    	#get the uv coordinate of the point
    	u = mc.getAttr(closestPoint + ".result.parameterU")
    	v = mc.getAttr(closestPoint + ".result.parameterV")
    	mc.delete(closestPoint)
    	
    	#start setting up groups
    	circleName = Controller
    	mc.select(circleName, r=True)
    	
    	mc.group(n = circleName + "_compensate_grp")
    	mc.group(n = circleName + "_protect_grp")
    	mc.group(n = circleName + "_follow_grp")
    	
    	mc.parent(circleName + "_protect_grp", w = True)
    	
    	#create the follow:
        '''
        #this was the old constrain way, looks like it has porformance issues:
    	constraint = mc.pointOnPolyConstraint(geoName, circleName + "_follow_grp", mo = False, name = circleName + "_popConst")
    	mc.setAttr(circleName + "_popConst." + geoName + "U0", u)
    	mc.setAttr(circleName + "_popConst." + geoName + "V0", v)
    	
    	mc.delete(circleName + "_follow_grp.rx",icn = True)
    	mc.delete(circleName + "_follow_grp.ry",icn = True)
    	mc.delete(circleName + "_follow_grp.rz",icn = True)
    	
    	mc.setAttr(circleName + "_follow_grp.rx", 0)
    	mc.setAttr(circleName + "_follow_grp.ry", 0)
    	mc.setAttr(circleName + "_follow_grp.rz", 0)
    	'''
    	Folicle = createFolicle(geoName, u, v, FolicleIndex, circleName, False)[0]
    	if bShouldConstrainOrientation:
    	    mc.parentConstraint(Folicle.replace("Shape", ""), circleName + "_follow_grp")
    	else:
    	    mc.pointConstraint(Folicle.replace("Shape", ""), circleName + "_follow_grp")
    	    
    	#do the compensation:
    	MD = mc.createNode('multiplyDivide', n = circleName + "_compensate")
    	mc.setAttr(MD + ".input2X", -1)
    	mc.setAttr(MD + ".input2Y", -1)
    	mc.setAttr(MD + ".input2Z", -1)
    	
    	mc.connectAttr(circleName + ".tx", MD + ".input1X")
    	mc.connectAttr(circleName + ".ty", MD + ".input1Y")
    	mc.connectAttr(circleName + ".tz", MD + ".input1Z")
    	
    	
    	mc.connectAttr(MD + ".outputX", circleName + "_compensate_grp.tx")
    	mc.connectAttr(MD + ".outputY", circleName + "_compensate_grp.ty")
    	mc.connectAttr(MD + ".outputZ", circleName + "_compensate_grp.tz")
    	
    	mc.parent(circleName + "_protect_grp", circleName + "_follow_grp")
    	
    	#Update index
    	FolicleIndex += 1

def assignTextField(Field):
    selection = mc.ls(sl = True)
    selectionString = ", ".join(selection)
    mc.textField(Field, e = True, tx = selectionString)

def closMCWIDWindow():
    if mc.window(windowID, q = True, exists = True):
        mc.deleteUI(windowID)
        
def printList(listToPrint):
    for item in listToPrint:
      print item


#MIRROR Controller section Fuction:
def duplicateList(list):
    #duplicate special first
    """
    settings will be 
    duplicate input graph
    will return the top node dupilcated
    """
    mc.select(list, r = True)
    duplication = mc.duplicate(rr = True, un = True)
    return duplication
    
#renaming:
"""
swap out l with r or L with R
"""
def searchAndReplaceNames(objList, serachFor = "_l_", replaceWith = "_r_", hierachy = True):
    
    for item in objList:
        children = mc.listRelatives(item, ad = True, f = True) or []
        objList = objList + children
        
    objList.sort(key = len, reverse = True)
    newObjList = []
    for item in objList:

        itemShortName = item.split("|")[-1]
        itemNewName = itemShortName.replace(serachFor, replaceWith)

        mc.rename(item,itemNewName)
        
        newObjList.append(itemNewName)
        
    
    return newObjList
    

def mirrorListToOtherSide(list, side = "YZ"):
    mc.group(n = "mirrorGrp", w = True, em = True)
    mc.parent(list, "mirrorGrp")
    if side == "YZ":
        mc.setAttr("mirrorGrp.sx", -1)
    elif side == "XY":
        mc.setAttr("mirrorGrp.sz", -1)
    else:
        mc.setAttr("mirrorGrp.sy", -1)
        
    mc.ungroup("mirrorGrp")
     
def findBindJnts(list):
    bindJntList = []
    for item in list:
        children = mc.listRelatives(item, ad = True) or []
        
        for child in children:
            if "jt_" in child and "bind" in child:
                #need uniqueness
                if not child in bindJntList:
                    bindJntList.append(child)

    return bindJntList
            

def MirrorFacialRig():
    mirrorCtrlString = mc.textField(ctrlTextField, q = True, tx = True)
    skin = mc.textField(skinTextField, q = True, tx = True)
    mirrorDirection = mc.radioCollection( mirrorModeRC, q = True, sl = True)
    if len(mirrorCtrlString) == 0:
        mirrorList = mc.ls(sl = True)
    else:
        mirrorList = mirrorCtrlString.split(", ")
    #add mirror at the back of the nameing so we dont get wired clashing:
    for index in range(0, len(mirrorList)):
        item = mirrorList[index]
        mc.rename(item, item + "_mirror")
        mirrorList[index] = item + "_mirror"
      
    duplication = duplicateList(mirrorList)
    
         
    MirrorList = []
    for item in duplication:
        if "ac" in item or "loc" in item or "crv" in item:
            MirrorList.append(item)
    mirrorListToOtherSide(MirrorList, mirrorDirection)       
    
    #rename first to make evryting unique

    newNames = searchAndReplaceNames(duplication)
    newNames = searchAndReplaceNames(newNames, "l_", "r_")
    newNames = searchAndReplaceNames(newNames, "L_", "R_")
    
    #bind new jnts to skin and mirror weight from the other side
    if len(skin) > 0:
        bindJnts = findBindJnts(newNames)
        #get skin cluster name:
        skinHistoryList = mc.listHistory(skin)
        for item in skinHistoryList:
            if mc.nodeType(item) == "skinCluster":
    	        skinClusterName = item
        
        printList(bindJnts)
        for jnt in bindJnts:
            mc.skinCluster(skinClusterName, e = True ,lw = True, wt = 0, ai = jnt)
        bMirrorInverse = mc.checkBox(PosToNageCB, q= True, v = True)
        mc.copySkinWeights(ss = skinClusterName, ds = skinClusterName, mirrorMode = mirrorDirection, mirrorInverse = not bMirrorInverse)
    
    #rename everything back:
    for item in mirrorList:
        oldname = item[:-7]
        print oldname
        mc.rename(item, oldname)
        
    for item in duplication:
        mirroredName = item.replace("l_", "r_").replace("L_", "R_")
        newName = mirroredName[:-8]
        mc.rename(mirroredName, newName)
    
    createInvertMD(NegMDTrans)
    createInvertMD(NegMDScale)
    createInvertMD(NegMDRot)
    
    #connect Attributes:
    ConnectAttrCheck(connectFromObj + ".translate", TransFactor + ".input1")
    ConnectAttrCheck(connectFromObj + ".scale", ScaleFactor + ".input1")
    ConnectAttrCheck(connectFromObj + ".rotate", RotFactor + ".input1")
    
       
    ConnectAttrCheck(TransFactor + ".output", NegClampTrans + ".input")
    ConnectAttrCheck(ScaleFactor + ".output", NegClampScale + ".input")
    ConnectAttrCheck(RotFactor + ".output", NegClampRot + ".input")
    
    ConnectAttrCheck(TransFactor + ".output", PosClampTrans + ".input")
    ConnectAttrCheck(ScaleFactor + ".output", PosClampScale + ".input")
    ConnectAttrCheck(RotFactor + ".output", PosClampRot + ".input")
    
    ConnectAttrCheck(NegClampTrans + ".output", NegMDTrans + ".input1")
    ConnectAttrCheck(NegClampScale + ".output", NegMDScale + ".input1")
    ConnectAttrCheck(NegClampRot + ".output", NegMDRot + ".input1")
    
    #finally apply connect to desired attrbute
    if connectFromAttrSingle == "tx" and bUsePositive:
        ConnectAttrCheck(PosClampTrans + ".outputR", connectToAttr)
    elif connectFromAttrSingle == "ty" and bUsePositive:    
        ConnectAttrCheck(PosClampTrans + ".outputG", connectToAttr)
    elif connectFromAttrSingle == "tz" and bUsePositive:    
        ConnectAttrCheck(PosClampTrans + ".outputB", connectToAttr)
    
    elif connectFromAttrSingle == "sx" and bUsePositive:    
        ConnectAttrCheck(PosClampScale + ".outputR", connectToAttr)
    elif connectFromAttrSingle == "sy" and bUsePositive:    
        ConnectAttrCheck(PosClampScale + ".outputG", connectToAttr)
    elif connectFromAttrSingle == "sz" and bUsePositive:    
        ConnectAttrCheck(PosClampScale + ".outputB", connectToAttr)
    
    elif connectFromAttrSingle == "rx" and bUsePositive:    
        ConnectAttrCheck(PosClampRot + ".outputR", connectToAttr)    
    elif connectFromAttrSingle == "ry" and bUsePositive:    
        ConnectAttrCheck(PosClampRot + ".outputG", connectToAttr)  
    elif connectFromAttrSingle == "rz" and bUsePositive:    
        ConnectAttrCheck(PosClampRot + ".outputB", connectToAttr)   
    
    elif connectFromAttrSingle == "tx" and not bUsePositive:    
        ConnectAttrCheck(NegMDTrans + ".outputX", connectToAttr)
    elif connectFromAttrSingle == "ty" and not bUsePositive:    
        ConnectAttrCheck(NegMDTrans + ".outputY", connectToAttr)
    elif connectFromAttrSingle == "tz" and not bUsePositive:    
        ConnectAttrCheck(NegMDTrans + ".outputZ", connectToAttr)
        
    elif connectFromAttrSingle == "sx" and not bUsePositive:    
        ConnectAttrCheck(NegMDScale + ".outputX", connectToAttr)        
    elif connectFromAttrSingle == "sy" and not bUsePositive:    
        ConnectAttrCheck(NegMDScale + ".outputY", connectToAttr)        
    elif connectFromAttrSingle == "sz" and not bUsePositive:    
        ConnectAttrCheck(NegMDScale + ".outputZ", connectToAttr)
           
    elif connectFromAttrSingle == "rx" and not bUsePositive:    
        ConnectAttrCheck(NegMDRot + ".outputX", connectToAttr)        
    elif connectFromAttrSingle == "ry" and not bUsePositive:    
        ConnectAttrCheck(NegMDRot + ".outputY", connectToAttr)        
    elif connectFromAttrSingle == "rz" and not bUsePositive:    
        ConnectAttrCheck(NegMDRot + ".outputZ", connectToAttr)
    
def createFolicle(SurfaceToCreateOn, uValue, vValue, index, follicleNameBase = "", ribbon = True):
    #figure the name of the folicle
    if ribbon == True:
        folicleName = SurfaceToCreateOn.replace("ribbon_", "follicle_") + follicleNameBase + "_ribbonShape_" + str(index).zfill(2)
    else:
        #we are doing geometry:
        folicleName = SurfaceToCreateOn + follicleNameBase + "_folicleShape_" + str(index).zfill(2)
    #create the folicle
    newFolicleShape = mc.createNode('follicle', n = folicleName)
    newFolicle = mc.listRelatives(newFolicleShape, p = True)[0]
    print newFolicle + "_gaga"
    print newFolicleShape + "_gaga"
    
    #connect the nessary attributes:
    if ribbon == True:
        print "nurbs is being used"
        mc.connectAttr(SurfaceToCreateOn + "Shape.local", newFolicleShape + ".inputSurface")
    else:
        print "geo is being used"
        #find the correct shape
        DeformationShape = ""
        shapes = mc.listRelatives(SurfaceToCreateOn,s = True)
        for item in shapes:
            if not (mc.getAttr(item + ".intermediateObject")):
                DeformationShape = item
        mc.connectAttr(DeformationShape + ".outMesh", newFolicleShape + ".inputMesh")
    SurfaceShape = mc.listRelatives(SurfaceToCreateOn, s=True)[0]    
    mc.connectAttr(SurfaceShape + ".worldMatrix[0]", newFolicleShape + ".inputWorldMatrix")
    mc.connectAttr(newFolicle + ".outRotate", newFolicle + ".rotate" )
    mc.connectAttr(newFolicle + ".outTranslate", newFolicle + ".translate" )
    
    #set UV value:
    mc.setAttr(newFolicle + ".parameterU", uValue)
    mc.setAttr(newFolicle + ".parameterV", vValue)
    
    return newFolicleShape, newFolicle
   

        
        
    
