from MeshHelios import HeliosMesh
import math
import numpy as np

class PDEFullMHD(object):
    def __init__(self,Mesh,Re,Rm,Inu,InB,dt,theta):
        #The Following values are useful for the implementation of some quadrature rules 
        self.pt0, self.w0  = -1, 1/21
        self.pt1, self.w1 = -math.sqrt((5/11)+(2/11)*math.sqrt(5/3)), (124-7*math.sqrt(15))/350
        self.pt2, self.w2 = -math.sqrt((5/11)-(2/11)*math.sqrt(5/3)), (124+7*math.sqrt(15))/350
        self.pt3, self.w3 = 0, 256/525
        self.pt4, self.w4 = math.sqrt((5/11)-(2/11)*math.sqrt(5/3)), (124+7*math.sqrt(15))/350
        self.pt5, self.w5  = math.sqrt((5/11)+(2/11)*math.sqrt(5/3)), (124-7*math.sqrt(15))/350
        self.pt6, self.w6 = 1, 1/21

        self.Mesh, self.Re, self.Rm, self.dt, self.theta  = Mesh, Re, Rm, dt, theta
        #We initialize the dofs
        #The boundary values on the vel and elec fields are decoupled from the
        #internal values. Thus, we will keep track of 4 arrays, they are:
        #dofs for elec field,
        #dof of the pressure and magnetic field.
        #the dofs for the vel fields are stored in two arrays, x and y comp
        tempun  = self.NodalDOFs(Inu,self.Mesh.Nodes)
        self.unx,self.uny  = self.DecompIntoCoord(tempun)
        tempum  = self.NodalDOFs(Inu,self.Mesh.MidNodes)
        self.unx, self.umy = self.DocompIntoCoord(tempum)
        self.B             = self.MagDOFs(InB)
        self.p             = np.zeros(len(Mesh.ElementEdges))
        self.E             = np.zeros(len(self.Mesh.Nodes))
        
        self.MEList     = []
        self.MVList     = []
        for i in range(len(self.Mesh.ElementEdges)):
            tempME,tempMV = self.ElecMagStandMassMat(self.Mesh.ElementEdges[i],self.Mesh.Orientations[i])
            self.MEList.append(tempME)
            self.MVList.append(tempMV)
    ##################################################################################
    ##################################################################################    
    #Initiation of Boundary Conditions/DifferentTypes of Simulations and their updates
    def SetConvTestBCAndSource(self,f,g,h,ub,Eb):
        self.f, self.g, self.h, self.ub, self.Eb = f, g, h, ub, Eb  #source terms and BC
        self.DirichletUpdateSources( self.theta*self.dt) #Initiatiates, assumes that this was done at the init time

        
        #The expectation is that all these functions return np.arrays

    #The following routines update the dofs of the bc and sources
    def DirichletUpdateSources(self,t):
        self.updatef(t+self.theta*self.dt)
        self.updateg(t+self.theta*self.dt) 
        self.updateh(t+self.theta*self.dt)

    def updatef(self,t):
        def dummyf(xv):
            return self.f([xv[0],xv[1],t])
        self.fdof = self.NodalDOFs(dummyf,self.Mesh.Nodes)
    
    def updateg(self,t):
        def dummyg(xv):
            return self.g([xv[0],xv[1],t])
        self.gdof = self.MagDOFs(dummyg)
    
    def updateh(self,t):
        def dummyh(xv):
            return self.h([xv[0],xv[1],t])
        self.hdof = self.NodalDOFs(dummyh,self.Mesh.Nodes)

    def DirichletupdateBC(self,t):
        def dummyubn(xv):
            return self.ub([xv[0],xv[1],t])
        def dummyubnp1(xv):
            return self.ub([xv[0],xv[1],t+self.dt*self.theta])
        def dummyEb(xv):
            return self.Eb([xv[0],xv[1],t])
   
        tempubn               = self.NodalDOFs(dummyubn,self.Mesh.BNodes)
        tempubnx,tempubny     = self.DecompIntoCoord(tempubn)
        #tempubnp1             = self.NodalDOFs(dummyubnp1,self.Mesh.BNodes)
        #tempubnp1x,tempubnp1y = self.DecompIntoCoord(temp1ubnp1)
        tempEb                = self.NodalDOFs(dummyEb,self.Mesh.BNodes)
        
        j = 0
        for i in self.Mesh.NumBoundaryNodes:
            self.ux[i] = tempubnx[j]
            self.uy[i] = tempubny[j]
            self.E[i]  = tempEb[j]
            j = j+1
        
    ##################################################################################
    ##################################################################################    
    #Compute DOFs from func
    def NodalDOFs(self,Func,Nodes):
        #This function computes the dof of the init cond on the vel field.
        return np.array([Func(Node) for Node in Nodes])

    def DecompIntoCoord(self,Array):
        #This function will, given a list of pairs return two arrays.
        #The first and second components.
        arrayx = [x[0] for x in Array]
        Arrayy = [x[1] for x in Array]
        return arrayx,Arrayy

    def MagDOFs(self,Func):
    #This computes the dofs of the initial magnetic field
    #This routine could be sped up by vectorizing. For our purposes this
    #this is not necessary
        N    = len(self.Mesh.EdgeNodes)
        proj = np.zeros(N)

        for i in range(N):
            x1      = self.Mesh.Nodes[self.Mesh.EdgeNodes[i][0]][0]
            y1      = self.Mesh.Nodes[self.Mesh.EdgeNodes[i][0]][1]
            x2      = self.Mesh.Nodes[self.Mesh.EdgeNodes[i][1]][0]
            y2      = self.Mesh.Nodes[self.Mesh.EdgeNodes[i][1]][1]
            lengthe = math.sqrt((x2-x1)**2+(y2-y1)**2)
            etimesnormal = [y2-y1,x1-x2]

            [Fx0,Fy0] = Func([x1,y1])
            [Fx1,Fy1] = Func([(x1*(1-self.pt1)+x2*(1+self.pt1))/2,(y1*(1-self.pt1)+y2*(1+self.pt1))/2])
            [Fx2,Fy2] = Func([(x1*(1-self.pt2)+x2*(1+self.pt2))/2,(y1*(1-self.pt2)+y2*(1+self.pt2))/2])
            [Fx3,Fy3] = Func([0.5*(x1+x2),0.5*(y1+y2)])
            [Fx4,Fy4] = Func([(x1*(1-self.pt4)+x2*(1+self.pt4))/2,(y1*(1-self.pt4)+y2*(1+self.pt4))/2])
            [Fx5,Fy5] = Func([(x1*(1-self.pt5)+x2*(1+self.pt5))/2,(y1*(1-self.pt5)+y2*(1+self.pt5))/2])
            [Fx6,Fy6] = Func([x2,y2])

            proj[i] = (self.w0*Fx0+self.w1*Fx1+self.w2*Fx2+self.w3*Fx3+self.w4*Fx4+self.w5*Fx5+self.w6*Fx6)*etimesnormal[0]
            proj[i] = proj[i] +(self.w0*Fy0+self.w1*Fy1+self.w2*Fy2+self.w3*Fy3+self.w4*Fy4+self.w5*Fy5+self.w6*Fy6)*etimesnormal[1]
            proj[i] = proj[i]/(2*lengthe)   
        return proj

    ##################################################################################
    ##################################################################################    
    #These functions work as an interface with the solver class.
    def DirichletConcatenate(self):
        #This function returns an array that concatenates all the unknowns
        intux = [self.ux[i] for i in self.Mesh.NumInternalNodes]
        intuy = [self.uy[i] for i in self.Mesh.NumInternalNodes]
        intE  = [self.E[i] for i in self.Mesh.NumInternalNodes]
        return np.concatenate((intux,intuy,self.B,intE,self.p), axis=None)
    
    def NumDirichletDOF(self):
        return 3*len(self.Mesh.NumInternalNodes)+len(self.Mesh.EdgeNodes)+len(self.Mesh.ElementEdges)

    def DirichletUpdateInterior(self,x):
        cut1 = len(self.Mesh.NumInternalNodes) #Number of internal dof for ux
        cut2 = 2*cut1                          #Number of internal dof for uy
        cut3 = cut2+len(self.B)                #Number of dofs for B
        cut4 = cut3+cut1                       #The number of internal dofs for E is the same as for the vel field.
        Cutx = np.split(x,[cut1,cut2,cut3,cut4])
        j = 0
        for i in self.Mesh.NumInternalNodes:
            self.ux[i] = Cutx[0][j]
            self.uy[i] = Cutx[1][j]
            self.E[i]  = Cutx[3][j]
            j = j+1
        
        self.B = Cutx[2]
        self.p = Cutx[4]
        
    def GDirichlet(self,x):
        return x
    
    #########################################################################################
    #########################################################################################
    #The following routines will, given a cell compute each of the bilinear forms in the var form.
    #Construct MFD-type matrices
    def LocalMassMatrix(self,N,R,n,A):
        #Given the matrices N,R as defined in Ch.4 of MFD book and the dimension
        #of the reconstruction space this function assembles the local mass matrix
        #The formula is M=M0+M1 where M0=R(N^T R)^-1R^T and M1=lamb*DD^T where the 
        #columns of D span the null-space of N^T and lamb=2*trace(M0)/n 
        #n is the dimension of the reconstruction space
        #nu is the average, over the element, of the diffusion coefficient
        #A is the area of the element
    
        #These commands compute M0
        M0    = np.matmul(np.transpose(N),R) 
        M0    = np.linalg.inv(M0)
        M0    = np.matmul(R,M0)
        M0    = np.matmul(M0,np.transpose(R))
    
        M1    = np.linalg.inv(np.transpose(N).dot(N))
        M1    = np.identity(n)-N.dot(M1).dot(np.transpose(N))
    
        gamma = np.trace(R.dot(np.transpose(R)))/(n*A)
        #And finally we put the two matrices together
        return M0+M1*gamma

    ############Electromagnetics
    def ElecMagStandMassMat(self,Element,Ori):
        n                = len(Element)
        NE               = np.zeros((n,2))
        RE               = np.zeros((n,2))
        xP,yP,A,Vertices,Edges = self.Mesh.Centroid(Element,Ori)
        for i in range(n):
            x1 = Vertices[i][0]
            y1 = Vertices[i][1]
            x2 = Vertices[i+1][0]
            y2 = Vertices[i+1][1]
            lengthEdge = math.sqrt((x2-x1)**2+(y2-y1)**2)
            NE[i][0] = (y2-y1)*Ori[i]*lengthEdge**-1
            NE[i][1] = (x1-x2)*Ori[i]*lengthEdge**-1
            RE[i][0] = (0.5*(x1+x2)-xP)*Ori[i]*lengthEdge #These formulas are derived in the tex-document
            RE[i][1] = (0.5*(y1+y2)-yP)*Ori[i]*lengthEdge
        
        NV = np.ones( (n,1))
        RV = np.zeros((n,1))
        
        x1n = Vertices[n-1][0] #first vertex of n-1th-edge
        y1n = Vertices[n-1][1]
    
        x2n = Vertices[0][0]
        y2n = Vertices[0][1] #second vertex of n-1th edge
    
        x11 = x2n #first vertex of first edge
        y11 = y2n
    
        x21 = Vertices[1][0]
        y21 = Vertices[1][1]  #second vertex of first edge
    
        omegan2 = (x2n-x1n)*((yP-y2n)+(2*yP-y1n-y2n))/6
        omega11 = (x21-x11)*((yP-y11)+(2*yP-y11-y21))/6
        RV[0] = omegan2+omega11
   
        for i in range(1,n):
        
            x1iminusone = Vertices[i-1][0] #first vertex of i-1th-edge
            y1iminusone = Vertices[i-1][1]
               
            x2iminusone = Vertices[i][0]    
            y2iminusone = Vertices[i][1] #second vertex of i-1th edge

            x1i = x2iminusone #first vertex of i+1 edge
            y1i = y2iminusone
    
            x2i = Vertices[i+1][0] #second vertex of i+1 edge
            y2i = Vertices[i+1][1]  
        
            omega2iminusone = (x2iminusone-x1iminusone)*((yP-y2iminusone)+\
                                                   (2*yP-y1iminusone-y2iminusone))/6
            omega1i = (x2i-x1i)*((yP-y1i)+(2*yP-y2i-y1i))/6   
        
            RV[i] = omega2iminusone+omega1i
        ME = self.LocalMassMatrix(NE,RE,n,A)
        MV = self.LocalMassMatrix(NV,RV,n,A)
        return ME,MV

    def BDivSquared(self):
        #This function computes the divergence of B.
        D      = 0
        DivMat = self.BDiv()
        divB   = DivMat.dot(self.B)
        for k in range(len(divB)):
            D = D + k 
        return D
    
    def BDiv(self):
        NEl = len(self.Mesh.ElementEdges)
        NE  = len(self.Mesh.EdgeNodes)
        div = np.zeros((NEl,NE))
        for i in range(NEl):
            Element = self.Mesh.ElementEdges[i]
            N       = len(Element)
            Ori     = self.Mesh.Orientations[i]
            for j in range(N):
                Node1 = self.Mesh.EdgeNodes[Element[j]][0]
                Node2 = self.Mesh.EdgeNodes[Element[j]][1]

                x1    = self.Mesh.Nodes[Node1][0]
                y1    = self.Mesh.Nodes[Node1][1] #these formulas are derived in the pdf document
                x2    = self.Nodes[Node2][0]
                y2    = self.Nodes[Node2][1]

                lengthe           = math.sqrt((x2-x1)**2+(y2-y1)**2)
                div[i,Element[j]] = Ori[j]*lengthe
        return div
    ######################################################################################
    #Fluid Flow
    def PhInProd(self,Element,ElementNumber):
        #This function integrates two function in Ph over the provided element.
        #The first function is p and the second is 1 over this element and zero over the rest.
        A,V,E = self.Mesh.Area(self,Element,self.Mesh.Orientations[ElementNumber])
        return A*self.p[ElementNumber]
    
    def TVhSemiInProd(self,Element):
        #This function computes the semi inner product between the vel field v and
        #a function whose dofs are one at one node and zero at the rest.
        return 1