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





#
#
#g on opposite boundary than e and on left
#
#

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
LC14 = (((z11,y1)),(alpha1,(x1,b1)))
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
#
#s1 - add y
#
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

#check
TwoCrossingChecker(LEFTS1, RIGHTS1, [M])
TwoCrossingChecker(LEFTS2, RIGHTS2, [M])
print("s = 1 case is done")
print()


#
#s3 - add y
#
RC1 = ((alpha2,z12),b2)
RC2 = (z12,(alpha2,b2))
R11 = (a2,(y2,(x2,((c2,d2),RC1))))
R12 = (a2,(y2,(x2,((c2,d2),RC2))))
R21 = (a2,(y2,(x2,(c2,(d2,RC1)))))
R22 = (a2,(y2,(x2,(c2,(d2,RC2)))))


#when alpha's left-edge is A_{1,L,2} then the right-edge can be either sort
LEFTS1 = {L11, L12, L13, L21, L22, L23, L31, L32,L33,L41, L42, L43, L51, L52, L53}
RIGHTS1 = {R11, R12, R21, R22}

#when alpha's left-edge is A_{2,L,1} then the right-edge must be A_{1,R,1}
LEFTS2 = {L14, L24, L34, L44}
RIGHTS2 = {R11, R21}

#check
TwoCrossingChecker(LEFTS1, RIGHTS1, [M])
TwoCrossingChecker(LEFTS2, RIGHTS2, [M])
print("s = 3 case is done")
print()





#
#
#s5: add the edge beta1-beta2
#we deal with this separately, since s4 has the alpha edge and s5 does not
#
#
LC11 = (((z11,y1)),(beta1,(x1,b1)))
LC12 = (((z11,y1)),((beta1,x1),b1))
LC13 = (((z11,y1)),((beta1,b1),x1))
LC14 = ((beta1,(z11,y1)),(x1,b1))
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


RC1 = ((beta2,z12),b2)
RC2 = (z12,(beta2,b2))
R11 = (a2,(x2,((c2,d2),RC1)))
R12 = (a2,(x2,((c2,d2),RC2)))
R21 = (a2,(x2,(c2,(d2,RC1))))
R22 = (a2,(x2,(c2,(d2,RC2))))


M = {a1:a2, b1:b2, c1:c2, d1:d2, x1:x2, y1:y2, z11:z12, beta1:beta2}
#
#s5 - add y
#
RC1 = (z12,(beta2,b2))
RC2 = ((beta2,z12),b2)
R11 = (a2,(x2,(y2,((c2,d2),RC1))))
R12 = (a2,(x2,(y2,((c2,d2),RC2))))
R21 = (a2,(x2,(y2,(c2,(d2,RC1)))))
R22 = (a2,(x2,(y2,(c2,(d2,RC2)))))


#when alpha's left-edge is A_{1,L,1} then the right-edge can be either sort
LEFTS1 = {L11, L12, L13, L21, L22, L23, L31, L32,L33,L41, L42, L43, L51, L52, L53}
RIGHTS1 = {R11, R12, R21, R22}

#when alpha's left-edge is A_{1,L,2} then the right-edge must be A_{1,R,2}
LEFTS2 = {L14, L24, L34, L44}
RIGHTS2 = {R11, R21}

#check
TwoCrossingChecker(LEFTS1, RIGHTS1, [M])
TwoCrossingChecker(LEFTS2, RIGHTS2, [M])
print("s = 5 case is done")
print()





#
#
#s4: add the edge beta1-beta2 and the alpha1-alpha2 edges
#we only need to add both in the case where the edge-type of alpha does not satisfy the beta constraints
#
#
def addLeftClade(clade):
    cases = set()
    cases.add(((c1,d1),(a1,clade)))
    cases.add((c1,(d1,(a1,clade))))
    cases.add((c1,(a1,(d1,clade))))
    cases.add((a1,(c1,(d1,clade))))
    cases.add((a1,((c1,d1),clade)))

    return cases

def addRightClade(clade):
    cases = set()
    cases.add(((a2,y2),(x2,((c2,d2),clade))))
    cases.add(((a2,y2),(x2,(c2,(d2,clade)))))

    return cases

LEFTS = []
RIGHTS = []


#a in A_{1,L,1}, b in A_{1,L,2}
LC01 = ((alpha1,(x1,b1)),(beta1,(z11,y1)))
#this case is impossible to occur since T^{x,y} is planar



#both in A_{1,L,1}

#
LC11 = ((alpha1,((beta1,x1),b1)),(z11,y1))
LC12 = ((alpha1,(x1,(beta1,b1))),(z11,y1))
LC13 = ((alpha1,(beta1,(x1,b1))),(z11,y1))

RC111 = ((alpha2,z12),(beta2,b2))
RC112 = ((beta2,(alpha2,z12)),b2)
RC113 = (((alpha2,beta2),z12),b2)

newLefts = set().union(*[addLeftClade(LC11), addLeftClade(LC12), addLeftClade(LC13)])
LEFTS.append(newLefts)
newRights = set().union(*[addRightClade(RC111), addRightClade(RC112), addRightClade(RC113)])
RIGHTS.append(newRights)
#

#
LC14 = ((beta1,(alpha1,(x1,b1))),(z11,y1))

RC141 = ((alpha2,(beta2,z12)),b2)
RC142 = (((alpha2,beta2),z12),b2)

newLefts = addLeftClade(LC14)
LEFTS.append(newLefts)
newRights = set().union(*[addRightClade(RC141), addRightClade(RC142)])
RIGHTS.append(newRights)
#

#
LC15 = (((alpha1,beta1),(x1,b1)),(z11,y1))

RC151 = ((alpha2,z12),(beta2,b2))
RC152 = ((beta2,(alpha2,z12)),b2)
RC153 = (((alpha2,beta2),z12),b2)
RC154 = ((alpha2,(beta2,z12)),b2)
newLefts = addLeftClade(LC15)
LEFTS.append(newLefts)
newRights = set().union(*[addRightClade(RC151), addRightClade(RC152), addRightClade(RC153), addRightClade(RC154)])
RIGHTS.append(newRights)
#



#b in A_{1,L,1}, a in A_{1,L,2}
LC21 = ((alpha1,(z11,y1)),(beta1,(x1,b1)))
LC22 = ((alpha1,(z11,y1)),((beta1,x1),b1))
LC23 = ((alpha1,(z11,y1)),((beta1,b1),x1))
LC24 = (((z11,alpha1),y1),(beta1,(x1,b1)))
LC25 = (((z11,alpha1),y1),((beta1,x1),b1))
LC26 = (((z11,alpha1),y1),((beta1,b1),x1))
LC27 = ((z11,(alpha1,y1)),(beta1,(x1,b1)))
LC28 = ((z11,(alpha1,y1)),((beta1,x1),b1))
LC29 = ((z11,(alpha1,y1)),((beta1,b1),x1))


RC21 = ((alpha2,z12),(beta2,b2))
RC22 = ((beta2,(alpha2,z12)),b2)
RC23 = (((beta2,alpha2),z12),b2)
RC24 = (z12,((beta2,alpha2), b2))
RC25 = (z12,((alpha2,(beta2, b2))))

newLefts = set().union(*[addLeftClade(LC21), addLeftClade(LC22), addLeftClade(LC23), addLeftClade(LC24), addLeftClade(LC25), addLeftClade(LC26), addLeftClade(LC27), addLeftClade(LC28), addLeftClade(LC29)])
LEFTS.append(newLefts)
newRights = set().union(*[addRightClade(RC21), addRightClade(RC22), addRightClade(RC23), addRightClade(RC24), addRightClade(RC25)])
RIGHTS.append(newRights)
#

#both in A_{1,L,2}
#
LC31 = ((beta1,((alpha1,y1),z11)),(x1,b1))
LC32 = ((beta1,(y1,(alpha1,z11))),(x1,b1))
LC33 = ((beta1,(alpha1,(y1,z11))),(x1,b1))


RC311 = ((alpha2,z12),(beta2,b2))
RC312 = ((beta2,(alpha2,z12)),b2)
RC313 = (((beta2,alpha2),z12),b2)

newLefts = set().union(*[addLeftClade(LC31), addLeftClade(LC32), addLeftClade(LC33)])
LEFTS.append(newLefts)
newRights = set().union(*[addRightClade(RC311), addRightClade(RC312), addRightClade(RC313)])
RIGHTS.append(newRights)
#

#
LC34 = ((alpha1,(beta1,(y1,z11))),(x1,b1))

RC341 = (((beta2,alpha2),z12),b2)
RC342 = ((alpha2,(beta2,z12)),b2)

newLefts = addLeftClade(LC34)
LEFTS.append(newLefts)
newRights = set().union(*[addRightClade(RC341), addRightClade(RC342)])
RIGHTS.append(newRights)
#

#
LC35 = (((beta1,alpha1),(y1,z11)),(x1,b1))

RC351 = ((alpha2,z12),(beta2,b2))
RC352 = ((beta2,(alpha2,z12)),b2)
RC353 = (((beta2,alpha2),z12),b2)
RC354 = ((alpha2,(beta2,z12)),b2)

newLefts = addLeftClade(LC35)
LEFTS.append(newLefts)
newRights = set().union(*[addRightClade(RC351), addRightClade(RC352), addRightClade(RC353), addRightClade(RC354)])
RIGHTS.append(newRights)
#

M = {a1:a2, b1:b2, c1:c2, d1:d2, x1:x2, y1:y2, z11:z12, alpha1:alpha2, beta1:beta2}

#check
for i in range(len(LEFTS)):
    TwoCrossingChecker(LEFTS[i], RIGHTS[i], [M])


print("s = 4 ,with alpha!= beta, case is done")
print()









#some overcounting in ways I do not want to fully resolve was done above. Namely, there are times when alpha and beta fill the same role as eachother.
#thus we will take all cases above where alpha fills a beta role, and remove the beta
LEFTS = []
RIGHTS = []

#first way this can happen is if alpha is in A_{1,L,1} and fully above x and b, and then it must go to A_{1,L,2}
LC1 = ((alpha1,(x1,b1)),(z11,y1))
RC1 = ((alpha2,z12),b2)


newLefts = addLeftClade(LC1)
LEFTS.append(newLefts)
newRights = addRightClade(RC1)
RIGHTS.append(newRights)
#

#otherwise alpha is in A_{1,L,2} and fully above y and z, and then it must go to A_{1,L,1}
LC2 = ((x1,b1),(alpha1,(z11,y1)))
RC2 = ((alpha2,b2),z12)


newLefts = addLeftClade(LC2)
LEFTS.append(newLefts)
newRights = addRightClade(RC2)
RIGHTS.append(newRights)
#

M = {a1:a2, b1:b2, c1:c2, d1:d2, x1:x2, y1:y2, z11:z12, alpha1:alpha2}

#check
for i in range(len(LEFTS)):
    TwoCrossingChecker(LEFTS[i], RIGHTS[i], [M])


print("s = 4 ,with alpha= beta, case is done")
print()





#
#
# finally we have the s8 and s11 cases which should work without any edges aside from a,b,z,x,y
#
#
M = {a1:a2, b1:b2, c1:c2, d1:d2, x1:x2, y1:y2, z11:z12}


# s11
LC = ((z11),(x1,b1))
L1 = ((c1,d1),((y1,a1),LC))
L2 = (c1,(d1,((y1,a1),LC)))
L3 = (c1,((y1,a1),(d1,LC)))
L4 = ((y1,a1),(c1,(d1,LC)))
L5 = ((y1,a1),((c1,d1),LC))

RC = ((y2,z12),b2)
R1 = (a2,(x2,((c2,d2),RC)))
R2 = (a2,(x2,(c2,(d2,RC))))


LEFTS = {L1, L2, L3, L4, L5}
RIGHTS = {R1, R2}



#check
TwoCrossingChecker(LEFTS, RIGHTS, [M])
print("s = 11 case is done")
print()




# s8
LC = ((z11),(x1,b1))
L1 = (a1,(y1,(c1,(d1,LC))))
L2 = (a1,(y1,((c1,d1),LC)))

RC = ((y2,z12),b2)
R1 = (a2,(x2,((c2,d2),RC)))
R2 = (a2,(x2,(c2,(d2,RC))))


LEFTS = {L1, L2}
RIGHTS = {R1, R2}



#check
TwoCrossingChecker(LEFTS, RIGHTS, [M])
print("s = 8 case is done")
print()