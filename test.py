from tanglegramClassv2 import *
#
#
#
#
#Tanglegrams for Case 1, r=1
#
#
#
#
#
#baseline setup from drawing
a1 = 'a1'
b1 = 'b1'
c1 = 'c1'
d1 = 'd1'
x1 = 'x1'
y1 = 'y1'
z11 = 'z11'
alpha1 = 'alpha1'
beta1 = 'beta1'
a2 = 'a2'
b2 = 'b2'
c2 = 'c2'
d2 = 'd2'
x2 = 'x2'
y2 = 'y2'
z12 = 'z12'
alpha2 = 'alpha2'
beta2 = 'beta2'

#posible left starting trees
((c1,d1),(a1,(z11,(x1,b1))))
(c1,(d1,(a1,(z11,(x1,b1)))))
(c1,(a1,(d1,(z11,(x1,b1)))))
(a1,(c1,(d1,(z11,(x1,b1)))))
(a1,((c1,d1),(z11,(x1,b1))))
#possible starting right trees
(a2,(x2,((c2,d2),(z12,b1))))
(a2,(x2,(c2,(d2,(z12,b1)))))
#starting matching
{a1:a2, b1:b2, c1:c2, d1:d2, x1:x2, y1:y2, z11:z12}






#g on opposite boundary than e and on left

#
#starting trees
#
#posible left starting trees
LC = ((z11,y1),(x1,b1))
L1 = ((c1,d1),(a1,LC))
L2 = (c1,(d1,(a1,LC)))
L3 = (c1,(a1,(d1,LC)))
L4 = (a1,(c1,(d1,LC)))
L5 = (a1,((c1,d1),LC))
#possible starting right trees
RC = (z12,b1)
R1 = (a2,(x2,((c2,d2),RC)))
R2 = (a2,(x2,(c2,(d2,RC))))
#starting matching
{a1:a2, b1:b2, c1:c2, d1:d2, x1:x2, y1:y2, z11:z12}


#analysis in the paper claimed that in case s4 and s5 that an additional edge is needed, as well as in cases s1, s3, and s4
#
#
#s1,s3,s4: add the edge alpha1-alpha2
#
#
LC11 = ((alpha1,(z11,y1)),(x1,b1))
LC12 = (((z11,alpha1),y1),(x1,b1))
LC13 = ((z11,(alpha1,y1)),(x1,b1))
LC14 = ((z11,y1)),(alpha1,(x1,b1))
L11 = ((c1,d1),(a1,LC11))
L12 = ((c1,d1),(a1,LC12))
L13 = ((c1,d1),(a1,LC13))
L14 = ((c1,d1),(a1,LC14))
L21 = (c1,(d1,(a1,LC11)))
L22 = (c1,(d1,(a1,LC12)))
L23 = (c1,(d1,(a1,LC13)))
L24 = (c1,(d1,(a1,LC14)))
L31 = (c1,(a1,(d1,LC11)))
L32 = (c1,(a1,(d1,LC12)))
L33 = (c1,(a1,(d1,LC13)))
L34 = (c1,(a1,(d1,LC14)))
L41 = (a1,(c1,(d1,LC11)))
L42 = (a1,(c1,(d1,LC12)))
L43 = (a1,(c1,(d1,LC13)))
L44 = (a1,(c1,(d1,LC14)))
L51 = (a1,((c1,d1),LC11))
L52 = (a1,((c1,d1),LC12))
L53 = (a1,((c1,d1),LC13))
L54 = (a1,((c1,d1),LC14))


RC1 = ((alpha2,z12),b2)
RC2 = (z12,(alpha2,b2))
R11 = (a2,(x2,((c2,d2),RC1)))
R12 = (a2,(x2,((c2,d2),RC2)))
R21 = (a2,(x2,(c2,(d2,RC1))))
R22 = (a2,(x2,(c2,(d2,RC2))))


M = {a1:a2, b1:b2, c1:c2, d1:d2, x1:x2, y1:y2, z11:z12, alpha1:alpha2}

#s1 - add y
RC1 = ((alpha2,z12),b2)
RC2 = (z12,(alpha2,b2))
R11 = ((a2,y2),(x2,((c2,d2),RC1)))
R12 = ((a2,y2),(x2,((c2,d2),RC2)))
R21 = ((a2,y2),(x2,(c2,(d2,RC1))))
R22 = ((a2,y2),(x2,(c2,(d2,RC2))))


#when alpha's left-edge is A_{1,L,2} then the right-edge can be either sort
LEFTS1 = {L11, L12, L13, L21, L22, L23, L31, L32,L33,L41, L42, L43, L51, L52, L53}
RIGHTS1 = {R11, R12, R21, R22}

#when alpha's left-edge is A_{2,L,2} then the right-edge must be A_{1,R,1}
LEFTS2 = {L14, L24, L34, L44}
RIGHTS2 = {R11, R21}


for leftTree in LEFTS1:
    for rightTree in RIGHTS1:
        Tanglegram = T(createBinaryTree(leftTree), createBinaryTree(rightTree), M)
        if Tanglegram.crossingNumber() <= 1:
            print(leftTree)
            print(rightTree)
            print()
            Tanglegram.TESTcrossingNumber()
            quit()

for leftTree in LEFTS2:
    for rightTree in RIGHTS2:
        Tanglegram = T(createBinaryTree(leftTree), createBinaryTree(rightTree), M)
        if Tanglegram.crossingNumber() <= 1:
            print(leftTree)
            print(rightTree)
            print()
            Tanglegram.TESTcrossingNumber()
            quit()















#
#
#
#
#Tanglegrams for Case 1, r=2
#
#
#
#
#