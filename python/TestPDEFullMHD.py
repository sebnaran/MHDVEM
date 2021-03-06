from PDEClass import PDEFullMHD
from Functions import *
from MeshHelios import HeliosMesh
import pickle
import numpy as np
import math
def ProcessedMesh(Pfile):
    with open(Pfile, "rb") as fp:   # Unpickling
        N,E,EE,B,O = pickle.load(fp)
    return N,E,EE,B,O

def RetrieveAMRMesh(Pfile):
    with open(Pfile, "rb") as fp:   # Unpickling
        N,E,EE,B,O,BT,LR,C = pickle.load(fp)
    return N,E,EE,B,O,BT,LR,C

#1
def test_init():
    Nodes         = [[-1,-1],[0,-1],[1,-1],[-1,0],[0,0],[1,0],[-1,1],[0,1],[1,1]]
    EdgeNodes     = [[0,1],[4,1],[8,5],[4,7],[7,8],[6,7],[3,6],[0,3],[5,2],[1,2],[3,4],[4,5]]
    ElementEdges  = [[9,8,11,1],[0,1,10,7],[10,3,5,6],[11,2,4,3]]                                     
    NumBoundaryNodes = [0,1,2,3,5,6,7,8] 
    Orientations  = [[1,-1,-1,1],[1,-1,-1,-1],[1,1,-1,-1],[1,-1,-1,-1]]
    TestMesh      = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)

    def Inu(xv):
        return np.array([1,1])
    def InB(xv):
        return np.array([1,1])
    Re, Rm, dt, theta = 1, 1, 0.5, 0.5
    TestPDE = PDEFullMHD(TestMesh,Re,Rm,Inu,InB,dt,theta)
    assert ( np.all(TestPDE.unx == np.array([1,1,1,1,1,1,1,1,1])) )
#2
# def test_concatenate():
#     Nodes         = [[-1,-1],[0,-1],[1,-1],[-1,0],[0,0],[1,0],[-1,1],[0,1],[1,1]]
#     EdgeNodes     = [[0,1],[4,1],[8,5],[4,7],[7,8],[6,7],[3,6],[0,3],[5,2],[1,2],[3,4],[4,5]]
#     ElementEdges  = [[9,8,11,1],[0,1,10,7],[10,3,5,6],[11,2,4,3]]                                     
#     NumBoundaryNodes = [0,1,2,3,5,6,7,8] 
#     Orientations  = [[1,-1,-1,1],[1,-1,-1,-1],[1,1,-1,-1],[1,-1,-1,-1]]
#     TestMesh      = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)

#     def Inu(xv):
#         return np.array([1,1])
#     def InB(xv):
#         return np.array([1,1])
#     Re, Rm, dt, theta = 1, 1, 0.5, 0.5
#     TestPDE = PDEFullMHD(TestMesh,Re,Rm,Inu,InB,dt,theta)

#     x = np.array([1,1,1,1,1,1,1,1,1,1,-1,-1,-1,1,-1,-1,1,1,-1,-1,-1,-1,0,0,0,0,0])
#     y = TestPDE.MHDConcatenate()
#     assert(np.all(x==y))
# #3
# def test_UpdateInterior():
#     Nodes         = [[-1,-1],[0,-1],[1,-1],[-1,0],[0,0],[1,0],[-1,1],[0,1],[1,1]]
#     EdgeNodes     = [[0,1],[4,1],[8,5],[4,7],[7,8],[6,7],[3,6],[0,3],[5,2],[1,2],[3,4],[4,5]]
#     ElementEdges  = [[9,8,11,1],[0,1,10,7],[10,3,5,6],[11,2,4,3]]                                     
#     NumBoundaryNodes = [0,1,2,3,5,6,7,8] 
#     Orientations  = [[1,-1,-1,1],[1,-1,-1,-1],[1,1,-1,-1],[1,-1,-1,-1]]
#     TestMesh      = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)

#     def Inu(xv):
#         return np.array([1,1])
#     def InB(xv):
#         return np.array([1,1])
#     Re, Rm, dt, theta = 1, 1, 0.5, 0.5
#     PDE = PDEFullMHD(TestMesh,Re,Rm,Inu,InB,dt,theta)

#     x = np.array([5,6,1,3,4,5,-1,-2,-3,4,-5,-6,7,8,-9,-10,-11,-1,3,1,2,3,4])
#     PDE.MHDUpdateInt(x,PDE.unx,PDE.uny,PDE.umx.PDE.uny,PDE.B,PDE.E,PDE.p)
#     y = PDE.DirichletConcatenate(PDE.unx,PDE.uny,PDE.umx.PDE.umy,PDE.B,PDE.E,PDE.p)
    
#     assert(np.all(x==y))
#4
def test_Divu1():
    Nodes         = [[-1,-1],[0,-1],[1,-1],[-1,0],[0,0],[1,0],[-1,1],[0,1],[1,1]]
    EdgeNodes     = [[0,1],[4,1],[8,5],[4,7],[7,8],[6,7],[3,6],[0,3],[5,2],[1,2],[3,4],[4,5]]
    ElementEdges  = [[9,8,11,1],[0,1,10,7],[10,3,5,6],[11,2,4,3]]                                     
    NumBoundaryNodes = [0,1,2,3,5,6,7,8] 
    Orientations  = [[1,-1,-1,1],[1,-1,-1,-1],[1,1,-1,-1],[1,-1,-1,-1]]
    TestMesh      = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)

    def Inu(xv):
        return np.array([1,1])
    def InB(xv):
        return np.array([1,1])
    Re, Rm, dt, theta = 1, 1, 0.5, 0.5
    TestPDE = PDEFullMHD(TestMesh,Re,Rm,Inu,InB,dt,theta)

    testans,A = TestPDE.DIVu(0,TestPDE.unx,TestPDE.uny,TestPDE.umx,TestPDE.umy)
    assert (abs(testans)<1E-5)
#5
def test_Divu2():
    Nodes         = [[-1,-1],[0,-1],[1,-1],[-1,0],[0,0],[1,0],[-1,1],[0,1],[1,1]]
    EdgeNodes     = [[0,1],[4,1],[8,5],[4,7],[7,8],[6,7],[3,6],[0,3],[5,2],[1,2],[3,4],[4,5]]
    ElementEdges  = [[9,8,11,1],[0,1,10,7],[10,3,5,6],[11,2,4,3]]                                     
    NumBoundaryNodes = [0,1,2,3,5,6,7,8] 
    Orientations  = [[1,-1,-1,1],[1,-1,-1,-1],[1,1,-1,-1],[1,-1,-1,-1]]
    TestMesh      = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)

    def Inu(xv):
        return np.array([xv[1]**2,xv[0]**2])
    def InB(xv):
        return np.array([1,1])
    Re, Rm, dt, theta = 1, 1, 0.5, 0.5
    TestPDE = PDEFullMHD(TestMesh,Re,Rm,Inu,InB,dt,theta)
    lunx,luny,lumx,lumy = TestPDE.GetLocalTVhDOF(0,TestPDE.unx,TestPDE.uny,TestPDE.umx,TestPDE.umy)
    testans,A = TestPDE.DIVu(0,lunx,luny,lumx,lumy)
    assert (abs(testans)<1E-5)
#6
def test_EhVhInProd():
    Nodes         = [[-1,-1],[0,-1],[1,-1],[-1,0],[0,0],[1,0],[-1,1],[0,1],[1,1]]
    EdgeNodes     = [[0,1],[4,1],[8,5],[4,7],[7,8],[6,7],[3,6],[0,3],[5,2],[1,2],[3,4],[4,5]]
    ElementEdges  = [[9,8,11,1],[0,1,10,7],[10,3,5,6],[11,2,4,3]]                                     
    NumBoundaryNodes = [0,1,2,3,5,6,7,8] 
    Orientations  = [[1,-1,-1,1],[1,-1,-1,-1],[1,1,-1,-1],[1,-1,-1,-1]]
    TestMesh      = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)

    def Inu(xv):
        return np.array([1,1])
    def InB(xv):
        return np.array([1,1])
    Re, Rm, dt, theta = 1, 1, 0.5, 0.5
    TestPDE = PDEFullMHD(TestMesh,Re,Rm,Inu,InB,dt,theta)

    LocB = TestPDE.GetLocalEhDOF(0,TestPDE.B)
    A1 = LocB.dot(TestPDE.MEList[0].dot(LocB))

    E    = [1 for i in range(len(TestMesh.Nodes))]
    LocE = TestPDE.GetLocalVhDOF(0,E)
    A2   = LocE.dot( TestPDE.MVList[0].dot(LocE) )

    def Bv(xv):
        return np.array([1,2])
    
    Barr    = TestPDE.MagDOFs(Bv)
    LocBarr = TestPDE.GetLocalEhDOF(0,Barr)
    A3      = LocBarr.dot( TestPDE.MEList[0].dot(LocBarr))

    def Es(xv):
        return xv[0]

    Earr    = TestPDE.NodalDOFs(Es,TestMesh.Nodes)
    LocEarr = TestPDE.GetLocalVhDOF(0,Earr)
    A4      = LocEarr.dot( TestPDE.MVList[0].dot(LocE))

    assert( abs(A1-2)<1E-5 and abs(A2-1)<1E-5 and abs(A3-5)<1E-5 and abs(A4-1/2)<1E-5)

# def test_TVSGandH():
#     Nodes         = [[-1,-1],[0,-1],[1,-1],[-1,0],[0,0],[1,0],[-1,1],[0,1],[1,1]]
#     EdgeNodes     = [[0,1],[4,1],[8,5],[4,7],[7,8],[6,7],[3,6],[0,3],[5,2],[1,2],[3,4],[4,5]]
#     ElementEdges  = [[9,8,11,1],[0,1,10,7],[10,3,5,6],[11,2,4,3]]                                     
#     NumBoundaryNodes = [0,1,2,3,5,6,7,8] 
#     Orientations  = [[1,-1,-1,1],[1,-1,-1,-1],[1,1,-1,-1],[1,-1,-1,-1]]
#     TestMesh      = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)

#     def Inu(xv):
#         return np.array([xv[0],0])
#     def InB(xv):
#         return np.array([1,1])
#     Re, Rm, dt, theta = 1, 1, 0.5, 0.5

#     TestPDE = PDEFullMHD(TestMesh,Re,Rm,Inu,InB,dt,theta)
#     G      = TestPDE.GISTVList[0]
#     G      = np.linalg.inv(G)
#     for i in range(12):
#         print('Row'+str(i))
#         print(G[i])
#     assert (1==1)
#7
def testProjector1():
    Nodes         = [[-1,-1],[0,-1],[1,-1],[-1,0],[0,0],[1,0],[-1,1],[0,1],[1,1]]
    EdgeNodes     = [[0,1],[4,1],[8,5],[4,7],[7,8],[6,7],[3,6],[0,3],[5,2],[1,2],[3,4],[4,5]]
    ElementEdges  = [[9,8,11,1],[0,1,10,7],[10,3,5,6],[11,2,4,3]]                                     
    NumBoundaryNodes = [0,1,2,3,5,6,7,8] 
    Orientations  = [[1,-1,-1,1],[1,-1,-1,-1],[1,1,-1,-1],[1,-1,-1,-1]]
    TestMesh      = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)

    def Inu(xv):
        return np.array([xv[1]+xv[0]+1,xv[1]+xv[0]+1])

    def InB(xv):
        return np.array([1,1])
    Re, Rm, dt, theta = 1, 1, 0.5, 0.5
    TestPDE = PDEFullMHD(TestMesh,Re,Rm,Inu,InB,dt,theta)
    GI      = TestPDE.GISTVList[0]
    Element = TestMesh.ElementEdges[0]
    lunx,luny,lumx,lumy = TestPDE.GetLocalTVhDOF(0,TestPDE.unx,TestPDE.uny,TestPDE.umx,TestPDE.umy)
    xP,yP,A,V,E         = TestMesh.Centroid(Element,TestMesh.Orientations[0])
    Bu                  = TestPDE.TVhSemiInProdColumn(Element,0,lunx,luny,lumx,lumy,xP,yP,A,E)
    Ans     = GI.dot(Bu)
    RealAns = np.array([1,1,1,1,1,1,0,0,0,0,0,0])

    diff    = Ans-RealAns
    norm    = 0
    for v in diff:
        norm = norm+v**2
    assert (math.sqrt(norm)<1E-5)
#8
def test_TVhSemiInnerProd1():
    Nodes         = [[-1,-1],[0,-1],[1,-1],[-1,0],[0,0],[1,0],[-1,1],[0,1],[1,1]]
    EdgeNodes     = [[0,1],[4,1],[8,5],[4,7],[7,8],[6,7],[3,6],[0,3],[5,2],[1,2],[3,4],[4,5]]
    ElementEdges  = [[9,8,11,1],[0,1,10,7],[10,3,5,6],[11,2,4,3]]                                     
    NumBoundaryNodes = [0,1,2,3,5,6,7,8] 
    Orientations  = [[1,-1,-1,1],[1,-1,-1,-1],[1,1,-1,-1],[1,-1,-1,-1]]
    TestMesh      = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)

    def Inu(xv):
        return np.array([xv[0],xv[1]])
    def InB(xv):
        return np.array([1,1])
    Re, Rm, dt, theta = 1, 1, 0.5, 0.5
    TestPDE = PDEFullMHD(TestMesh,Re,Rm,Inu,InB,dt,theta)
    
    lunx,luny,lumx,lumy = TestPDE.GetLocalTVhDOF(0,TestPDE.unx,TestPDE.uny,TestPDE.umx,TestPDE.umy)
    Ans                 = TestPDE.TVhSemiInProd( 0,lunx,luny,lumx,lumy,lunx,luny,lumx,lumy)

    assert (abs(Ans-2)<1E-5)

def test_TVhInProd1():
    Nodes         = [[-1,-1],[0,-1],[1,-1],[-1,0],[0,0],[1,0],[-1,1],[0,1],[1,1]]
    EdgeNodes     = [[0,1],[4,1],[8,5],[4,7],[7,8],[6,7],[3,6],[0,3],[5,2],[1,2],[3,4],[4,5]]
    ElementEdges  = [[9,8,11,1],[0,1,10,7],[10,3,5,6],[11,2,4,3]]                                     
    NumBoundaryNodes = [0,1,2,3,5,6,7,8] 
    Orientations  = [[1,-1,-1,1],[1,-1,-1,-1],[1,1,-1,-1],[1,-1,-1,-1]]
    TestMesh      = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)

    def Inu(xv):
        return np.array([1,1])
    def InB(xv):
        return np.array([1,1])
    Re, Rm, dt, theta = 1, 1, 0.5, 0.5
    TestPDE = PDEFullMHD(TestMesh,Re,Rm,Inu,InB,dt,theta)
    
    lunx,luny,lumx,lumy = TestPDE.GetLocalTVhDOF(0,TestPDE.unx,TestPDE.uny,TestPDE.umx,TestPDE.umy)
    Ans                 = TestPDE.TVhInProd( 0,lunx,luny,lumx,lumy,lunx,luny,lumx,lumy)

    assert (abs(Ans-2)<1E-5)

def test_Quadrature():
    Nodes         = [[-1,-1],[0,-1],[1,-1],[-1,0],[0,0],[1,0],[-1,1],[0,1],[1,1]]
    EdgeNodes     = [[0,1],[4,1],[8,5],[4,7],[7,8],[6,7],[3,6],[0,3],[5,2],[1,2],[3,4],[4,5]]
    ElementEdges  = [[9,8,11,1],[0,1,10,7],[10,3,5,6],[11,2,4,3]]                                     
    NumBoundaryNodes = [0,1,2,3,5,6,7,8] 
    Orientations  = [[1,-1,-1,1],[1,-1,-1,-1],[1,1,-1,-1],[1,-1,-1,-1]]
    TestMesh      = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)

    def Inu(xv):
        return np.array([1,1])
    def InB(xv):
        return np.array([1,1])
    Re, Rm, dt, theta = 1, 1, 0.5, 0.5
    TestPDE = PDEFullMHD(TestMesh,Re,Rm,Inu,InB,dt,theta)
    xxxxP,yyyyP,xxyyP,xyyyP,xxxyP = 0,0,0,0,0
    xxxP,yyyP,xyyP,xxyP           = 0,0,0,0
    for u in range(6):
        x,y   = TestPDE.xs[u],TestPDE.ys[u]

        xxxxP = xxxxP+TestPDE.ws[u]*(x**4)
        yyyyP = yyyyP+TestPDE.ws[u]*(y**4)
        xxyyP = xxyyP+TestPDE.ws[u]*(x**2)*(y**2)
        xyyyP = xyyyP+TestPDE.ws[u]*(x)*(y**3)
        xxxyP = xxxyP+TestPDE.ws[u]*(x**3)*(y)
        xxxP  = xxxP+TestPDE.ws[u]*(x**3)
        yyyP  = yyyP+TestPDE.ws[u]*(y**3)
        xyyP  = xyyP+TestPDE.ws[u]*(x)*(y**2)
        xxyP  = xxyP+TestPDE.ws[u]*(x**2)*(y)
    assert (abs(xxxxP-1/30) <1E-5)
    assert (abs(yyyyP-1/30) <1E-5)
    assert (abs(xxyyP-1/180)<1E-5)
    assert (abs(xxxyP-1/120)<1E-5)
    assert (abs(xyyyP-1/120)<1E-5)
    assert (abs(xxxP-1/20)<1E-5)
    assert (abs(yyyP-1/20)<1E-5)
    assert (abs(xxyP-1/60)<1E-5)
    assert (abs(xyyP-1/60)<1E-5)

def test_TVhInProd2():
    Nodes         = [[-1,-1],[0,-1],[1,-1],[-1,0],[0,0],[1,0],[-1,1],[0,1],[1,1]]
    EdgeNodes     = [[0,1],[4,1],[8,5],[4,7],[7,8],[6,7],[3,6],[0,3],[5,2],[1,2],[3,4],[4,5]]
    ElementEdges  = [[9,8,11,1],[0,1,10,7],[10,3,5,6],[11,2,4,3]]                                     
    NumBoundaryNodes = [0,1,2,3,5,6,7,8] 
    Orientations  = [[1,-1,-1,1],[1,-1,-1,-1],[1,1,-1,-1],[1,-1,-1,-1]]
    TestMesh      = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)

    def Inu(xv):
        return np.array([1,1])
    def InB(xv):
        return np.array([1,1])
    Re, Rm, dt, theta = 1, 1, 0.5, 0.5
    TestPDE = PDEFullMHD(TestMesh,Re,Rm,Inu,InB,dt,theta)
    
    K = TestPDE.KTVList[0]
    assert(abs(K[0,0]-1)    <1E-5) #Area
    assert(abs(K[1,3]-1/2)  <1E-5) #xP*A
    assert(abs(K[1,5]+1/2)  <1E-5) #yP*A
    assert(abs(K[2,2]-1/3)  <1E-5) #xxP
    assert(abs(K[4,4]-1/3)  <1E-5) #yyP
    assert(abs(K[2,4]+1/4)  <1E-5) #xyP       
    assert(abs(K[6,6]-0.2)  <1E-5) #xxxxP
    assert(abs(K[8,8]-0.2)  <1E-5) #yyyyP
    assert(abs(K[10,10]-1/9)<1E-5) #xxyyP

    assert(abs(K[8,10]+1/8) <1E-5) #xyyyP
    assert(abs(K[6,10]+1/8) <1E-5) #xxxyP
    assert(abs(K[5,7]+1/6)  <1E-5) #xxyP
    assert(abs(K[4,10]-1/6) <1E-5) #xyyP
    assert(abs(K[3,7]-1/4)  <1E-5) #xxxP
    assert(abs(K[4,8]+1/4)  <1E-5) #yyyP

def test_TVhInProd3():
    Nodes            = [[-1,-1],[0,-1],[1,-1],[-1,0],[0,0],[1,0],[-1,1],[0,1],[1,1]]
    EdgeNodes        = [[0,1],[4,1],[8,5],[4,7],[7,8],[6,7],[3,6],[0,3],[5,2],[1,2],[3,4],[4,5]]
    ElementEdges     = [[9,8,11,1],[0,1,10,7],[10,3,5,6],[11,2,4,3]]                                     
    NumBoundaryNodes = [0,1,2,3,5,6,7,8] 
    Orientations     = [[1,-1,-1,1],[1,-1,-1,-1],[1,1,-1,-1],[1,-1,-1,-1]]
    TestMesh         = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)

    def Inu(xv):
        return np.array([1,1])
    def InB(xv):
        return np.array([1,1])
    Re, Rm, dt, theta = 1, 1, 0.5, 0.5
    TestPDE = PDEFullMHD(TestMesh,Re,Rm,Inu,InB,dt,theta)
    
    Norm = TestPDE.TVhL2Norm(TestPDE.unx,TestPDE.uny,TestPDE.umx,TestPDE.umy)
    assert(abs(Norm**2-8)<1E-5)

def test_TVhInProd4():
    Nodes            = [[-1,-1],[0,-1],[1,-1],[-1,0],[0,0],[1,0],[-1,1],[0,1],[1,1]]
    EdgeNodes        = [[0,1],[4,1],[8,5],[4,7],[7,8],[6,7],[3,6],[0,3],[5,2],[1,2],[3,4],[4,5]]
    ElementEdges     = [[9,8,11,1],[0,1,10,7],[10,3,5,6],[11,2,4,3]]                                     
    NumBoundaryNodes = [0,1,2,3,5,6,7,8] 
    Orientations     = [[1,-1,-1,1],[1,-1,-1,-1],[1,1,-1,-1],[1,-1,-1,-1]]
    TestMesh         = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)

    def Inu(xv):
        return np.array([xv[1]**2,xv[0]**2])
    def InB(xv):
        return np.array([1,1])
    Re, Rm, dt, theta = 1, 1, 0.5, 0.5
    TestPDE = PDEFullMHD(TestMesh,Re,Rm,Inu,InB,dt,theta)
    
    Norm = TestPDE.TVhL2Norm(TestPDE.unx,TestPDE.uny,TestPDE.umx,TestPDE.umy)
    assert(abs(Norm**2-8/5)<1E-5)

def test_TVhInProd5():
    Pfile = 'PertPQh=0.166666.txt'
    Nodes,EdgeNodes,ElementEdges,BoundaryNodes,Orientations = ProcessedMesh(Pfile)
    TestMesh         = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)

    def Inu(xv):
        return np.array([xv[1]**2,xv[0]**2])
    def InB(xv):
        return np.array([1,1])

    Re, Rm, dt, theta = 1, 1, 0.5, 0.5
    TestPDE = PDEFullMHD(TestMesh,Re,Rm,Inu,InB,dt,theta)
    
    Norm = TestPDE.TVhL2Norm(TestPDE.unx,TestPDE.uny,TestPDE.umx,TestPDE.umy)
    assert(abs(Norm**2-8/5)<1E-5)

# def test_TVhH1InProd1():
#     #Pfile = 'PertPQh=0.166666.txt'
#     Pfile = 'PertPQh=0.010989.txt'
#     Nodes,EdgeNodes,ElementEdges,BoundaryNodes,Orientations = ProcessedMesh(Pfile)
#     TestMesh         = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)

#     def Inu(xv):
#         return np.array([xv[1]**2,xv[0]**2])
#     def InB(xv):
#         return np.array([1,1])

#     Re, Rm, dt, theta = 1, 1, 0.5, 0.5
#     TestPDE = PDEFullMHD(TestMesh,Re,Rm,Inu,InB,dt,theta)
    
#     Norm = TestPDE.TVhH1Norm(TestPDE.unx,TestPDE.uny,TestPDE.umx,TestPDE.umy)
#     assert(abs(Norm**2-32/3)<1E-2)

# def test_TVhH1InProd2():
#     #Pfile = 'PertPQh=0.166666.txt'
#     #Pfile = 'PertPQh=0.010989.txt'
#     Pfile = 'PertPQh=0.021739.txt'
#     #Pfile = 'PTh=0.0062613.txt'
#     #Pfile = 'PTh=0.101015.txt'
#     Nodes,EdgeNodes,ElementEdges,BoundaryNodes,Orientations = ProcessedMesh(Pfile)
#     TestMesh         = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)

#     def Inu(xv):
#         return np.array([xv[0]**2,xv[1]**2])
#     def InB(xv):
#         return np.array([1,1])

#     Re, Rm, dt, theta = 1, 1, 0.5, 0.5
#     TestPDE = PDEFullMHD(TestMesh,Re,Rm,Inu,InB,dt,theta)
    
#     Norm = TestPDE.TVhH1Norm(TestPDE.unx,TestPDE.uny,TestPDE.umx,TestPDE.umy)
#     assert(abs(Norm**2-32/3)<1E-2)

def test_K():
    #Pfile = 'PertPQh=0.166666.txt'
    #Pfile = 'PertPQh=0.010989.txt'
    #Pfile = 'PertPQh=0.021739.txt'
    #Pfile = 'PTh=0.0062613.txt'
    #Pfile = 'PTh=0.101015.txt'
    #Nodes,EdgeNodes,ElementEdges,BoundaryNodes,Orientations = ProcessedMesh(Pfile)
    Nodes,EdgeNodes,ElementEdges,BoundaryNodes,Orientations,BottomToTop,LeftToRight,Corners = RetrieveAMRMesh("AMRmesh.txt")
    TestMesh         = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)

    def Inu(xv):
        return np.array([xv[0]**2,xv[1]**2])
    def InB(xv):
        return np.array([1,1])

    Re, Rm, dt, theta = 1, 1, 0.5, 0.5
    TestPDE = PDEFullMHD(TestMesh,Re,Rm,Inu,InB,dt,theta)
    ElNum = 2666
    unx=[9.95387052e-05, 1.05068267e-04, 0.00000000e+00, 0.00000000e+00]
    uny=[ 6.20418750e-05, -1.75573587e-05,  0.00000000e+00,  0.00000000e+00]
    umx=[-0.01369914,  0.01384285,  0.,          0.01320039]
    umy=[1.58572374e-13, 2.08943973e-13, 0.00000000e+00, 7.27751193e-14]
    Element = TestPDE.Mesh.ElementEdges[ElNum]
    xP,yP,A,V,E = TestPDE.Mesh.Centroid(Element,TestPDE.Mesh.Orientations[ElNum])
    Bu          = TestPDE.TVhSemiInProdColumn(Element,ElNum,unx,uny,umx,umy,xP,yP,A,E)
    H, GI    = TestPDE.HSTVList[ElNum],TestPDE.GISTVList[ElNum]
    Piu      = GI.dot(Bu)
    p = Piu.dot( H.dot(Piu) )
    K       = TestPDE.KTVList[ElNum]

    #print('Piu='+str(Piu))
    #print('H='+str(H))
    #print('HPiu='+str( H.dot(Piu) ) )
    #print(V)
    assert(abs(K[0,0]-0.01)    <1E-5) #Area
    assert(abs(K[1,3]+0.00875) <1E-5) #xP*A
    assert(abs(K[1,5]-0.009)   <1E-5) #yP*A
    assert(abs(K[2,2]-0.00765833)  <1E-5) #xxP
    assert(abs(K[4,4]-0.0081333)  <1E-5) #yyP
    assert(abs(K[2,4]+0.007875)  <1E-5) #xyP 
    #assert p>0

def test_L2H1Norms():
    theta,dt,T = 1/2,0.001,0.5
    Re,Rm,theta   = 1, 1, 0.5
    MTypes  = ['Onlyone']
    #MTypes = ['Trig','Quad','Vor']
    #MTypes = ['Vor']
    def InB(xv):
        return np.array([0,math.cos(xv[0])])

    def exactu(xv):
        #return np.array([math.sin(xv[1])**2,math.cos(xv[0])**2])
        return np.array([xv[1]**2,xv[0]**2])
    def exactp(xv):
        return 2*xv[0]+2*xv[1]
    for MType in MTypes:
        if MType == 'Onlyone':
            ProcessedFiles = ['PTh=0.101015.txt']
            dx = [0.10101525445522107]
        #ProcessedFiles = ['PertPQh=0.021739.txt']
        #ProcessedFiles = ['AMRMesh']
        #dx = [0.021739]
        if MType == 'Trig':
            ProcessedFiles = ['PTh=0.101015.txt','PTh=0.051886.txt','PTh=0.0251418.txt','PTh=0.0125255.txt',\
                          'PTh=0.0062613.txt']

            dx = [0.10101525445522107, 0.05018856132284956, 0.025141822757713456, 0.012525468249897755,\
         0.006261260829309998]

        if MType == 'Quad':
            ProcessedFiles = ['PertPQh=0.166666.txt','PertPQh=0.0833333.txt','PertPQh=0.043478.txt',\
                      'PertPQh=0.021739.txt','PertPQh=0.010989.txt']

            dx = [0.16666666666666666, 0.08333333333333333, 0.043478260869565216, 0.021739130434782608,\
         0.010989010989010988]
        if MType == 'Vor':
            ProcessedFiles = ['PVh=0.128037.txt','PVh=0.0677285.txt','PVh=0.0345033.txt','PVh=0.0174767.txt',\
                      'PVh=0.0087872.txt']

            dx = [0.12803687993289598, 0.06772854614785964, 0.03450327796711771, 0.017476749542968805,\
        0.008787156237382746]

        i = 0
        #print(MType)
        for Pfile in ProcessedFiles:
            #print('\n dx='+str(dx[i]))
            Nodes,EdgeNodes,ElementEdges,BoundaryNodes,Orientations = ProcessedMesh(Pfile)
        #Nodes,EdgeNodes,ElementEdges,BoundaryNodes,Orientations,BottomToTop,LeftToRight,Corners = RetrieveAMRMesh("AMRmesh.txt")
            Mesh = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)
            dt = dx[i]**2
            PDE    = PDEFullMHD(Mesh,Re,Rm,exactu,InB,dt,theta)
            PDE.SetFlowBC(exactu)
            PDE.FlowComputeBC(0)
        #PDE.unx,PDE.uny,PDE.umx,PDE.umy = PDE.FlowupdateBC(PDE.unx,PDE.uny,PDE.umx,PDE.umy)
            PDE.p = PDE.PhDOF(exactp)
            #y     = PDE.FlowG(PDE.FlowConcatenate())
            ynx,yny,ymx,ymy = PDE.unx,PDE.uny,PDE.umx,PDE.umy
        #err = PDE.TVhL2Norm(ynx,yny,ymx,ymy) v
            H1err = PDE.TVhH1Norm(ynx,yny,ymx,ymy)

            L2err = PDE.TVhL2Norm(ynx,yny,ymx,ymy)

            perr = PDE.PhL2Norm(PDE.p)
            j = 0
            zr = sum(PDE.p)
            
            #print('H1Err='+str(abs(H1err-math.sqrt(4-math.sin(4)))))
            #print('L2Err='+str(abs(L2err-math.sqrt(3+math.sin(4)/4))))
            #print('H1Err='+str(abs(H1err-math.sqrt(32/3))))
            #print('L2Err='+str(abs(L2err-math.sqrt(8/5))))
            #print('perr='+str(perr))
            #print('sum='+str(zr))
            assert(abs(L2err**2-8/5) <1E-5)
            assert(abs(H1err**2-32/3)<1E-5)
            assert(abs(perr**2-32/3) <3E-1)

def test_PiRTB():
    Nodes            = [[-1,-1],[0,-1],[1,-1],[-1,0],[0,0],[1,0],[-1,1],[0,1],[1,1]]
    EdgeNodes        = [[0,1],[4,1],[8,5],[4,7],[7,8],[6,7],[3,6],[0,3],[5,2],[1,2],[3,4],[4,5]]
    ElementEdges     = [[9,8,11,1],[0,1,10,7],[10,3,5,6],[11,2,4,3]]                                     
    NumBoundaryNodes = [0,1,2,3,5,6,7,8] 
    Orientations     = [[1,-1,-1,1],[1,-1,-1,-1],[1,1,-1,-1],[1,-1,-1,-1]]
    TestMesh         = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)

    def Inu(xv):
        return np.array([xv[1]**2,xv[0]**2])
    def InB(xv):
        return np.array([1,1])

    Re, Rm, dt, theta = 1, 1, 0.5, 0.5
    TestPDE = PDEFullMHD(TestMesh,Re,Rm,Inu,InB,dt,theta)
    locB    = TestPDE.GetLocalEhDOF(0,TestPDE.B)
    Bx,By,n1,n2,n3  = TestPDE.PiRTBnm(locB,TestPDE.unx,0)
    assert (np.all(Bx==np.array([1,1,1,1])))

# def test_J():
#     theta,dt,T = 0.5,0.5,1
#     Re,Rm      = 1,1
#     #MTypes  = ['Onlyone']
#     #MTypes = ['Quad']
#     MTypes = ['Vor']
#     #MTypes = ['Trig','Quad','Vor']
#     def exactu(xv,t):
#         return np.array([math.exp(t)*math.cos(xv[1]),0])
#     def exactB(xv,t):
#         return np.array([0,math.cos(xv[0]+t)])
#     def exactE(xv,t):
#         return math.cos(xv[0]+t)
    
#     def initu(xv):
#         return exactu(xv,0)
#     def initB(xv):
#         return exactB(xv,0)
#     def initE(xv):
#         return exactE(xv,0)

    
#     for MType in MTypes:
#         if MType == 'Onlyone':
#             ProcessedFiles = ['PTh=0.101015.txt']
#             dx = [0.10101525445522107]
#         #ProcessedFiles = ['PertPQh=0.021739.txt']
#         #ProcessedFiles = ['AMRMesh']
#         #dx = [0.021739]
#         if MType == 'Trig':
#             ProcessedFiles = ['PTh=0.101015.txt','PTh=0.051886.txt','PTh=0.0251418.txt','PTh=0.0125255.txt',\
#                           'PTh=0.0062613.txt']

#             dx = [0.10101525445522107, 0.05018856132284956, 0.025141822757713456, 0.012525468249897755,\
#          0.006261260829309998]

#         if MType == 'Quad':
#             ProcessedFiles = ['PertPQh=0.166666.txt','PertPQh=0.0833333.txt','PertPQh=0.043478.txt',\
#                       'PertPQh=0.021739.txt','PertPQh=0.010989.txt']

#             dx = [0.16666666666666666, 0.08333333333333333, 0.043478260869565216, 0.021739130434782608,\
#          0.010989010989010988]
#         if MType == 'Vor':
#             ProcessedFiles = ['PVh=0.128037.txt','PVh=0.0677285.txt','PVh=0.0345033.txt','PVh=0.0174767.txt',\
#                       'PVh=0.0087872.txt']

#             dx = [0.12803687993289598, 0.06772854614785964, 0.03450327796711771, 0.017476749542968805,\
#         0.008787156237382746]
#         y = 0
#         for Pfile in ProcessedFiles:
#             Nodes,EdgeNodes,ElementEdges,BoundaryNodes,Orientations = ProcessedMesh(Pfile)
#             #Nodes,EdgeNodes,ElementEdges,BoundaryNodes,Orientations,BottomToTop,LeftToRight,Corners = RetrieveAMRMesh("AMRmesh.txt")
#             Mesh = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)
#             dt = dx[y]**2
#             y  = y+1
#             print(Pfile)
#             def ut(xv):
#                 return exactu(xv,dt)
#             def Bt(xv):
#                 return exactB(xv,dt)
#             def Et(xv):
#                 return exactE(xv,theta*dt)

#             def f(xv,t):
#                 y1 = math.cos(t+xv[0])**2-math.cos(xv[1])+2*math.exp(t)*math.cos(xv[1])\
#                 +math.exp(t)*math.cos(xv[1])*math.cos(t+xv[0])**2
#                 #y1 = -math.cos(xv[1])+2*math.exp(t)*math.cos(xv[1])
#                 y2 = xv[0]*math.sin(xv[1])
#                 return np.array([y1,y2])
#             def h(xv,t):
#                 return math.cos(t+xv[0])*(1+math.exp(t)*math.cos(xv[1]))+math.sin(t+xv[0])
    
#             def J(xv):
#                 t = dt*theta
#                 return math.cos(t+xv[0])+math.exp(t)*math.cos(t+xv[0])*math.cos(xv[1])

#             def JxB(xv):
#                 t = dt*theta
#                 u = -(math.cos(t+xv[0])**2)*(1+math.exp(t)*math.cos(xv[1]))
#                 return np.array([u,0])
#             PDE    = PDEFullMHD(Mesh,Re,Rm,initu,initB,dt,theta)
#             PDE.SetMHDBCandSource(exactu,exactE,f,h)
#             PDE.MHDComputeBC(0)
#             PDE.MHDComputeSources(0)

#             tempxun  = PDE.NodalDOFs(ut,Mesh.Nodes)
#             unx,uny  = PDE.DecompIntoCoord(tempxun)
#             tempxum  = PDE.NodalDOFs(ut,Mesh.MidNodes)
#             umx,umy  = PDE.DecompIntoCoord(tempxum)
#             B        = PDE.MagDOFs(Bt)
#             E        = PDE.NodalDOFs(Et,Mesh.Nodes)
#             eJn      = PDE.NodalDOFs(J,Mesh.Nodes)
#             eJm      = PDE.NodalDOFs(J,Mesh.MidNodes)
            
#             tempJxBn    = PDE.NodalDOFs(JxB,Mesh.Nodes)
#             eJxBnx,eJxBny = PDE.DecompIntoCoord(tempJxBn)
#             tempJxBm    = PDE.NodalDOFs(JxB,Mesh.MidNodes)
#             eJxBmx,eJxBmy = PDE.DecompIntoCoord(tempJxBm)

#             Bth   = (1-theta)*PDE.B+theta*B
#             unxth = (1-theta)*PDE.unx+theta*unx
#             unyth = (1-theta)*PDE.uny+theta*uny
#             umxth = (1-theta)*PDE.umx+theta*umx
#             umyth = (1-theta)*PDE.umy+theta*umy
#             JNorm = 0
#             JxBNorm = 0
#             for i in range(len(Mesh.ElementEdges)):
#                 locBth                              = PDE.GetLocalEhDOF(i,Bth)
#                 RTBthetax,RTBthetay = PDE.PiRTBn(locBth,i)
#                 locEn                               = PDE.GetLocalVhDOF(i,E) 
#                 loceJn                              = PDE.GetLocalVhDOF(i,eJn)
#                 locunthx,locunthy,locumthx,locumthy = PDE.GetLocalTVhDOF(i,unxth,unyth,umxth,umyth)
#                 elocJxBnx,elocJxBny,elocJxBmx,elocJxBmy = PDE.GetLocalTVhDOF(i,eJxBnx,eJxBny,eJxBmx,eJxBmy)
#                 RTBthetanx,RTBthetany,RTBthetamx,RTBthetamy,locEm = PDE.PiRTBnm(locBth,E,i)
                
#                 Jn    = locEn+PDE.Cross2Dto1D(locunthx,locunthy,RTBthetanx,RTBthetany)
#                 Jm    = locEm+PDE.Cross2Dto1D(locumthx,locumthy,RTBthetamx,RTBthetamy)

#                 JxBnx,JxBny = PDE.Cross1Dto2D(Jn,RTBthetanx,RTBthetany)
#                 JxBmx,JxBmy = PDE.Cross1Dto2D(Jm,RTBthetamx,RTBthetamy)
#                 cnx,cny = JxBnx-elocJxBnx, JxBny-elocJxBny
#                 cmx,cmy = JxBmx-elocJxBmx, JxBmy-elocJxBmy
#                 JNorm = JNorm + (Jn-loceJn).dot( PDE.MVList[i].dot(Jn-loceJn))
#                 JxBNorm = JxBNorm + PDE.TVhInProd(i,cnx,cny,cmx,cmy,cnx,cny,cmx,cmy)
#             JNorm   = math.sqrt(JNorm)
#             #print('J='+str(JNorm))
#             JxBNorm = math.sqrt(JxBNorm)
#             print('JxB='+str(JxBNorm))
#             assert (1==1)
def test_parallelG():
    theta,dt,T = 0.5,0.5,1
    Re,Rm      = 1,1
    #MTypes  = ['Onlyone']
    #MTypes = ['Quad']
    #MTypes = ['Vor']
    MTypes = ['Trig','Quad','Vor']
    def exactu(xv,t):
        return np.array([math.exp(t)*math.cos(xv[1]),0])

    def exactB(xv,t):   
        return np.array([0,math.cos(xv[0]+t)])
    def exactE(xv,t):
        return math.cos(xv[0]+t)
    def exactp(xv,t):
        return -xv[0]*math.cos(xv[1])
    def f(xv,t):
        y1 = math.cos(t+xv[0])**2-math.cos(xv[1])+2*math.exp(t)*math.cos(xv[1])\
         +math.exp(t)*math.cos(xv[1])*math.cos(t+xv[0])**2
        #y1 = -math.cos(xv[1])+2*math.exp(t)*math.cos(xv[1])
        y2 = xv[0]*math.sin(xv[1])
        return np.array([y1,y2])
    def h(xv,t):
            return math.cos(t+xv[0])*(1+math.exp(t)*math.cos(xv[1]))+math.sin(t+xv[0])

    def initu(xv):
        return exactu(xv,0)
    def initB(xv):
        return exactB(xv,0)
    def initE(xv):
        return exactE(xv,0)
    def initp(xv):
        return exactp(xv,0)


    
    for MType in MTypes:
        if MType == 'Onlyone':
            ProcessedFiles = ['PTh=0.101015.txt']
            dx = [0.10101525445522107]
        #ProcessedFiles = ['PertPQh=0.021739.txt']
        #ProcessedFiles = ['AMRMesh']
        #dx = [0.021739]
        if MType == 'Trig':
            ProcessedFiles = ['PTh=0.101015.txt','PTh=0.051886.txt','PTh=0.0251418.txt','PTh=0.0125255.txt',\
                          'PTh=0.0062613.txt']

            dx = [0.10101525445522107, 0.05018856132284956, 0.025141822757713456, 0.012525468249897755,\
         0.006261260829309998]

        if MType == 'Quad':
            ProcessedFiles = ['PertPQh=0.166666.txt','PertPQh=0.0833333.txt','PertPQh=0.043478.txt',\
                      'PertPQh=0.021739.txt','PertPQh=0.010989.txt']

            dx = [0.16666666666666666, 0.08333333333333333, 0.043478260869565216, 0.021739130434782608,\
         0.010989010989010988]
        if MType == 'Vor':
            ProcessedFiles = ['PVh=0.128037.txt','PVh=0.0677285.txt','PVh=0.0345033.txt','PVh=0.0174767.txt',\
                      'PVh=0.0087872.txt']

            dx = [0.12803687993289598, 0.06772854614785964, 0.03450327796711771, 0.017476749542968805,\
        0.008787156237382746]
        i = 0
        for Pfile in ProcessedFiles:
            Nodes,EdgeNodes,ElementEdges,BoundaryNodes,Orientations = ProcessedMesh(Pfile)
            #Nodes,EdgeNodes,ElementEdges,BoundaryNodes,Orientations,BottomToTop,LeftToRight,Corners = RetrieveAMRMesh("AMRmesh.txt")
            Mesh = HeliosMesh(Nodes,EdgeNodes,ElementEdges,Orientations)
            dt = dx[i]**2
            i = i+1
            PDE    = PDEFullMHD(Mesh,Re,Rm,initu,initB,dt,theta)
            PDE.SetMHDBCandSource(exactu,exactE,f,h)
            PDE.MHDComputeBC(0)
            PDE.MHDComputeSources(0)
            def ut(xv):
                return exactu(xv,dt)
            def Bt(xv):
                return exactB(xv,dt)
            def Et(xv):
                return exactE(xv,theta*dt)
            def pt(xv):
                return exactp(xv,theta*dt)
            tempxun   = PDE.NodalDOFs(ut,Mesh.Nodes)
            xunx,xuny = PDE.DecompIntoCoord(tempxun)
            tempxum   = PDE.NodalDOFs(ut,Mesh.MidNodes)
            xumx,xumy = PDE.DecompIntoCoord(tempxum)
            xB        = PDE.MagDOFs(Bt)
            xE        = PDE.NodalDOFs(Et,Mesh.Nodes)
            xp        = PDE.PhDOF(pt)
            yp        = PDE.pMHDG(PDE.MHDConcatenate(xunx,xuny,xumx,xumy,xB,xE,xp),Gunx)