import cv2
import numpy as np
from imutils import contours
from imutils.perspective import four_point_transform
import imutils
import cv2
import matplotlib.pyplot as plt
import numpy as np
from imutils import contours
from imutils.perspective import four_point_transform,order_points
import imutils

cevap_anahtar={0:2,1:1,2:2,3:3,4:1,5:4,6:4,7:3,8:1,9:1,10:0,11:0,12:2,13:1,14:2,15:3,16:4,17:4,18:4,19:3,20:2,21:1,22:0,23:0,24:0,25:4,26:2,27:3,28:4,29:4,30:4,31:3,32:2,33:1,34:0,35:0,36:1,37:2,38:3,39:4} #,
alfabe={0:'A',1:'B',2:'C',3:'Ç',4:'D',5:'E',6:'F',7:'G',8:'Ğ',9:'H',10:'I',11:'İ',12:'J',13:'K',14:'L',15:'M',16:'N',17:'O',18:'Ö',19:'P',20:'Q',21:'R',22:'S',23:'Ş',24:'T',25:'U',26:'Ü',27:'V',28:'W',29:'Y',30:'Z',31:'X'}
def cevap_islemleri(isim,coords):
    a=0

    thresh=cv2.threshold(isim,179,255,cv2.THRESH_BINARY_INV)[1]
    coords=contours.sort_contours(coords,method="top-to-bottom")[0]
    for (s,i) in enumerate(np.arange(0,len(coords),20)):
        cevap=None
        cnt=contours.sort_contours(coords[i:i+30])[0]
        toplam_beyaz=None

        for (j,c) in enumerate(cnt):
            maske=np.zeros(thresh.shape,dtype=np.uint8)

            cv2.drawContours(maske,[c],0,(255,255,255),thickness=-1)
            maske=cv2.bitwise_and(thresh,thresh,mask=maske)

            a+=1
            toplam_beyaz=cv2.countNonZero(maske)
            if cevap is None or toplam_beyaz>cevap[0]:

                cevap=(toplam_beyaz,j,s)



def cevap_contour_bul(isim,isim_gri):
    coord=[]
    thresholded=cv2.adaptiveThreshold(isim_gri,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,9,8)





    contour=cv2.findContours(thresholded,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)




    x_coords=[(0,0)]
    sayac=0
    contour=imutils.grab_contours(contour)
    contour=contours.sort_contours(contour,method="top-to-bottom")[0]
    for c in contour:
        approx=cv2.approxPolyDP(c,0.0001*cv2.arcLength(c,True),True)
        area=cv2.contourArea(approx)

        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)

        if  area<1500 and area>250 and ar>=0.9 and ar<=1.1:





            box=cv2.minAreaRect(approx)
            box=cv2.boxPoints(box)
            box=np.array(box,dtype=np.int)
            M=cv2.moments(box)

            x=int(M['m10']/M['m00'])
            y=int(M['m01']/M['m00'])

            res=tekrar_bul(x_coords,x)
            if res is False and abs(x_coords[-1][1]-y)<35:
                coord.append(approx)
                x_coords.append((x,y))
                sayac+=1
                #cv2.drawContours(isim,[box],0,(255,0,0),thickness=3)
                #cv2.drawContours(isim,[approx],0,(0,0,255),thickness=2)
            elif abs(x_coords[-1][1]-y)>=35:
                coord.append(approx)
                x_coords=[(0,0)]
                sayac+=1
                x_coords.append((x,y))
                #cv2.drawContours(isim,[box],0,(255,0,0),thickness=3)
                #cv2.drawContours(isim,[approx],0,(0,0,255),thickness=2)



            else:
                continue
    return coord



def ters_bul(kagit,areas):
    ret=False
    #print(areas[0][0])
    if areas[0][0]!=1 and areas[0][1]+areas[1][1]>2300000:
        kagit=imutils.rotate(kagit,angle=180)
        print("Kağıdı ters koymuşsunuz,çevrildi")
        ret=True
        return ret,kagit
    else:
        return ret,kagit




def kagit_bul(image,gray):
    thr=cv2.threshold(gray,150,255,cv2.THRESH_BINARY)[1]

    contour=cv2.findContours(thr,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    contour=imutils.grab_contours(contour)
    contour=sorted(contour,key=cv2.contourArea,reverse=True)
    for c in contour:
        approx=cv2.approxPolyDP(c,0.02*cv2.arcLength(c,True),True)
        if len(approx)==4:

            #cv2.drawContours(image,[approx],0,(0,255,0),thickness=3)
            break



    warp=four_point_transform(image,approx.reshape(4,2))
    warp_gri=four_point_transform(gray,approx.reshape(4,2))
    return warp,warp_gri
def soru_grup_contour_bul(resim,gri):
    thr2=cv2.threshold(gri,0,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)[1]

    can=cv2.Canny(thr2,50,100)
    can=cv2.dilate(can,None,iterations=3)


    coords=[]
    cont=cv2.findContours(can,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    cont=imutils.grab_contours(cont)
    for c in cont:
        approx=cv2.approxPolyDP(c,0.0001*cv2.arcLength(c,True),True)
        area=cv2.contourArea(approx)

        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)

        if cv2.contourArea(c)>30 and ar>=0.9 and ar<=1.1:
            box=cv2.minAreaRect(approx)
            box=cv2.boxPoints(box)
            box=np.array(box,dtype=np.int)
            if cv2.contourArea(box)>150:
                coords.append(approx)
                cv2.drawContours(resim,[box],0,(0,0,255),thickness=3)
    if len(coords)==5:
        return coords
    else:
        return 0
def tekrar_bul(array,koordinat):
    for c in array:
        if koordinat==c[0] or abs(koordinat-c[0])<15:
            return True #Tekrar var
        else:
            pass
    return False
def contour_bul(isim,isim_gri,karmasiklik=0):
    coord=[]
    thr6=cv2.adaptiveThreshold(isim_gri,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,9,8)
   #thr6=cv2.threshold(isim_gri,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    ar_value=200
    #if karmasiklik==1:
    #    ar_value=800




    cont=cv2.findContours(thr6,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)




    x_coords=[(0,0)]
    sayac=0
    cont=imutils.grab_contours(cont)
    cont=contours.sort_contours(cont,method="top-to-bottom")[0]
    for c in cont:
        approx=cv2.approxPolyDP(c,0.0001*cv2.arcLength(c,True),True)
        area=cv2.contourArea(approx)

        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)

        if  area<1300 and area>300 and ar>=0.9 and ar<=1.1:





            box=cv2.minAreaRect(approx)
            box=cv2.boxPoints(box)
            box=np.array(box,dtype=np.int)
            M=cv2.moments(box)

            x=int(M['m10']/M['m00'])
            y=int(M['m01']/M['m00'])
         #   print(x,y)
            res=tekrar_bul(x_coords,x)
            if res is False and abs(x_coords[-1][1]-y)<35:
                coord.append(approx)
                x_coords.append((x,y))
                sayac+=1
                #cv2.drawContours(isim,[box],0,(255,0,0),thickness=3)
                #cv2.drawContours(isim,[approx],0,(0,0,255),thickness=2)
            elif abs(x_coords[-1][1]-y)>=35:
                coord.append(approx)
                x_coords=[(0,0)]
                sayac+=1
                x_coords.append((x,y))
                #cv2.drawContours(isim,[box],0,(255,0,0),thickness=3)
                #cv2.drawContours(isim,[approx],0,(0,0,255),thickness=2)



            else:
                continue
    return coord,thr6

def contour_cizdir(resim,cont,isim="default"):
    for c in cont:
        cv2.drawContours(resim,[c],0,(0,255,0),thickness=4)

    #print(f"Bulunan contour sayısı: {len(cont)}")


def bolge_bul(resim,gri):
    bolgeler={}
    thr2=cv2.adaptiveThreshold(gri,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,9,8)
    areas=[]
    cont=cv2.findContours(thr2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    cont=imutils.grab_contours(cont)
    temp=[]
    cont=contours.sort_contours(cont,"top-to-bottom")[0]
    a=0
    for c in cont:
        approx=cv2.approxPolyDP(c,0.009*cv2.arcLength(c,True),True)
        if cv2.contourArea(approx)>10050 and len(approx)==4:

            a+=1

            M=cv2.moments(approx)
            x=int(M['m10']/M['m00'])
            y=int(M['m01']/M['m00'])
            #areas.append([a,cv2.contourArea(approx)])
            #cv2.putText(resim,"{}".format(a),(x,y),fontFace=cv2.FONT_HERSHEY_COMPLEX,fontScale=4,color=(255,0,0),thickness=3)
            temp.append(approx.reshape(4,2))
            areas.append([a,cv2.contourArea(approx)])

            #cv2.drawContours(resim,[approx],0,(255,0,0),thickness=3)

    #cv2.imshow("resim_olge",imutils.resize(resim,height=650))
    if len(temp)>=5:
        bolgeler={'isim':temp[0],'ogrno':temp[1],'sinav_turu':temp[2],'soru_grubu':temp[3],'ogretim_onay':temp[4],'cevaplar':temp[5]}
    areas=sorted(areas,key=lambda x:x[1],reverse=True)
    return bolgeler,areas
def cevap_islemleri(cevap,coords,col_no=1):
    iki_cevap=0
    bos=0
    dogru=0
    q_no=0
    yanlıs=0
    if col_no==1:
        pass
    elif col_no==2:
        q_no=30
    elif col_no==3:
        q_no=60
    elif col_no==4:
        q_no=90
    yanit=[]
    #cevap=cv2.cvtColor(cevap,cv2.COLOR_BGR2GRAY)
    thresh=cv2.threshold(cevap,180,255,cv2.THRESH_BINARY_INV)[1]

    coords=contours.sort_contours(coords,method="top-to-bottom")[0]
    for (s,i) in enumerate(np.arange(0,len(coords),5)):
        cevap=None
        cnt=contours.sort_contours(coords[i:i+5])[0]
        toplam_beyaz=None
        say=0

        for (j,c) in enumerate(cnt):
            if len(cevap_anahtar)<=q_no+s:
                return (dogru,yanlıs,bos,iki_cevap)

            maske=np.zeros(thresh.shape,dtype=np.uint8)

            cv2.drawContours(maske,[c],0,(255,255,255),thickness=-1)
            maske=cv2.bitwise_and(thresh,thresh,mask=maske)
            plt.imshow(maske,cmap='gray')
            #plt.show()

            toplam_beyaz=cv2.countNonZero(maske)
            #print(toplam_beyaz,j)
            if cevap is None or toplam_beyaz>cevap[0]:

                cevap=(toplam_beyaz,j,q_no+s)
            if toplam_beyaz>800:
                say+=1
        if say>1: #İKİ ŞIK İŞARETLEME DURUMU
            iki_cevap+=1
            continue
        elif cevap[0]<800:# BOŞ BIRAKMA DURUMU
            bos+=1
            continue
        else:
            if cevap_anahtar[q_no+s]== cevap[1]:
                #print(cevap_anahtar[q_no+s],cevap[1])

                dogru+=1
            else:
                yanlıs+=1

    '''
    NUMBER OF TRUE,FALSE,NOT MARKED AND MARKED MORE THAN 1
    '''
    return(dogru,yanlıs,bos,iki_cevap)



def isim_islemleri(isim,coords,thresh):
    a=0
    yanit=[]
    ad_str=""
    coords=contours.sort_contours(coords,method="left-to-right")[0]
    for (s,i) in enumerate(np.arange(0,len(coords),32)):
        cevap=None
        cnt=contours.sort_contours(coords[i:i+32],method="top-to-bottom")[0]
        toplam_beyaz=None

        for (j,c) in enumerate(cnt):
            maske=np.zeros(thresh.shape,dtype=np.uint8)

            cv2.drawContours(maske,[c],0,(255,255,255),thickness=-1)
            maske=cv2.bitwise_and(thresh,thresh,mask=maske)
            #plt.imshow(maske,cmap='gray')
            #plt.show()
            #a+=1
            toplam_beyaz=cv2.countNonZero(maske)
            #print(toplam_beyaz,j)
            if cevap is None or toplam_beyaz>cevap[0]:

                cevap=(toplam_beyaz,j,s)
           # print("cevap",cevap)
        if cevap[0]>500:
            yanit.append(alfabe[cevap[1]])

        elif cevap[0]<600:
            yanit.append(" ")
    for s in yanit:
        ad_str+=s

    return ad_str
def cevap_kolon(cevap):
    pts1=np.array([(2,50),(300,50),(2,1545),(300,1545)])
    pts2=np.array([(300,50),(600,50),(302,1545),(602,1545)])
    pts3=np.array([(600,50),(900,50),(602,1545),(902,1545)])
    pts4=np.array([(900,50),(1200,50),(902,1545),(1202,1545)])

    col1=four_point_transform(cevap,pts1)
    col2=four_point_transform(cevap,pts2)
    col3=four_point_transform(cevap,pts3)
    col4=four_point_transform(cevap,pts4)
    return col1,col2,col3,col4
def cevap_gri(col1,col2,col3,col4):
    '''
    KOLONLARI GRİ YAPMAK İÇİN,MAİNDE YER KAPLAMASIN

    '''
    col1_gri=cv2.cvtColor(col1,cv2.COLOR_BGR2GRAY)
    col2_gri=cv2.cvtColor(col2,cv2.COLOR_BGR2GRAY)
    col3_gri=cv2.cvtColor(col3,cv2.COLOR_BGR2GRAY)
    col4_gri=cv2.cvtColor(col4,cv2.COLOR_BGR2GRAY)
    return col1_gri,col2_gri,col3_gri,col4_gri
def cevap_contour(col1,col2,col3,col4):
    col1_gri,col2_gri,col3_gri,col4_gri=cevap_gri(col1,col2,col3,col4)
    col1_coord=cevap_contour_bul(col1,col1_gri)
    col2_coord=cevap_contour_bul(col2,col1_gri)
    col3_coord=cevap_contour_bul(col3,col1_gri)
    col4_coord=cevap_contour_bul(col4,col1_gri)
    return col1_coord,col2_coord,col3_coord,col4_coord

def ogrno_islemleri(ogrno,ogrno_gri,coords):

    yanit=""

    thresh=cv2.threshold(ogrno_gri,180,255,cv2.THRESH_BINARY_INV)[1]
    coords=contours.sort_contours(coords,method="left-to-right")[0]
    for (s,i) in enumerate(np.arange(0,len(coords),10)):
        cevap=None
        cnt=contours.sort_contours(coords[i:i+10],method="top-to-bottom")[0]
        toplam_beyaz=None

        for (j,c) in enumerate(cnt):
            maske=np.zeros(thresh.shape,dtype=np.uint8)

            cv2.drawContours(maske,[c],0,(255,255,255),thickness=-1)
            maske=cv2.bitwise_and(thresh,thresh,mask=maske)
            plt.imshow(maske,cmap='gray')
            #plt.show()

            toplam_beyaz=cv2.countNonZero(maske)

            if cevap is None or toplam_beyaz>cevap[0]:

                cevap=(toplam_beyaz,j,s)

        if cevap[0]>500:
            yanit+=str(cevap[1])
    print("Okul Numarası:",yanit)
def sinav_islemleri(sinav,sinav_gri,coords):
    yanit=["QUİZ","ARA","FİNAL","BÜTÜNLEME"]

    thresh=cv2.threshold(sinav_gri,180,255,cv2.THRESH_BINARY_INV)[1]
    coords=contours.sort_contours(coords,method="top-to-bottom")[0]
    for (s,i) in enumerate(np.arange(0,len(coords),10)):
        cevap=None
        cnt=contours.sort_contours(coords[i:i+10],method="left-to-right")[0]
        toplam_beyaz=None

        for (j,c) in enumerate(cnt):
            maske=np.zeros(thresh.shape,dtype=np.uint8)

            cv2.drawContours(maske,[c],0,(255,255,255),thickness=-1)
            maske=cv2.bitwise_and(thresh,thresh,mask=maske)
            plt.imshow(maske,cmap='gray')
            #plt.show()

            toplam_beyaz=cv2.countNonZero(maske)

            if cevap is None or toplam_beyaz>cevap[0]:

                cevap=(toplam_beyaz,j,s)
        return yanit[cevap[1]]
def sorugrup_islemleri(soru,soru_gri,coords):

    yanit=["A","B","C","D","E"]
    sayac=0
    thresh=cv2.threshold(soru_gri,180,255,cv2.THRESH_BINARY_INV)[1]
    coords=contours.sort_contours(coords,method="top-to-bottom")[0]
    for (s,i) in enumerate(np.arange(0,len(coords),10)):
        cevap=None
        cnt=contours.sort_contours(coords[i:i+10],method="left-to-right")[0]
        toplam_beyaz=None

        for (j,c) in enumerate(cnt):
            maske=np.zeros(thresh.shape,dtype=np.uint8)

            cv2.drawContours(maske,[c],0,(255,255,255),thickness=-1)
            maske=cv2.bitwise_and(thresh,thresh,mask=maske)
            plt.imshow(maske,cmap='gray')
            #plt.show()
            sayac+=1
            toplam_beyaz=cv2.countNonZero(maske)

            if cevap is None or toplam_beyaz>cevap[0]:

                cevap=(toplam_beyaz,j,s)
        if sayac==5:
            break
        print(cevap)
    if cevap[0]>500:
        return yanit[cevap[1]]
    #print("tespit edilemedi")
    return "Tespit edilemedi"



####################################################################
def main_starter(bos_kagit,dolu_kagit):
    image=cv2.imread(bos_kagit)
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)


    kagit,kagit_gri=kagit_bul(image,gray)

    bolgeler,areas=bolge_bul(kagit,kagit_gri)

    '''
    FIND SCHOOL NUMBER PART
    '''

    ogrno_bos=four_point_transform(kagit,bolgeler['ogrno'])
    ogrno_bos_gri=four_point_transform(kagit_gri,bolgeler['ogrno'])
    ogrno_coord,ogrno_thresh=contour_bul(ogrno_bos,ogrno_bos_gri)
    contour_cizdir(ogrno_bos_gri,ogrno_coord,"ogrenci numarası")
    #v2.imshow("ogrno",imutils.resize(ogrno_bos,height=400))



    '''
    DIVIDE ANSWER PART INTO 4 SLICES AND FIND ONE BY ONE
    '''


    cevap_bos=four_point_transform(kagit,bolgeler['cevaplar'])
    cevap_bos_gri=four_point_transform(kagit_gri,bolgeler['cevaplar'])

    col1,col2,col3,col4=cevap_kolon(cevap_bos)
    col1_gri,col2_gri,col3_gri,col4_gri=cevap_gri(col1,col2,col3,col4)

    col1_coord,col2_coord,col3_coord,col4_coord=cevap_contour(col1,col2,col3,col4)
    #contour_cizdir(col1,col1_coord)
    #cevap_islemleri(col2_gri,coord_cevap)

    '''
    EXAM TYPE FIND PART
    '''

    sinav_bos=four_point_transform(kagit,bolgeler['sinav_turu'])
    sinav_bos_gri=four_point_transform(kagit_gri,bolgeler['sinav_turu'])
    sinav_coord,sinav_thresh=contour_bul(sinav_bos,sinav_bos_gri)

    sinav_islemleri(sinav_bos,sinav_bos_gri,sinav_coord)
    #cv2.imshow("sınav türü",sinav_bos_gri)




    '''
    
    OTHER PARTS THAT ON PAPER 
    '''

    sorugrup_bos=four_point_transform(kagit,bolgeler['soru_grubu'])
    sorugrup_bos_gri=four_point_transform(kagit_gri,bolgeler['soru_grubu'])

    sorugrup_coord,sorugrup_thresh=contour_bul(sorugrup_bos,sorugrup_bos_gri,1)
    coors=soru_grup_contour_bul(sorugrup_bos,sorugrup_bos_gri)
    soru_cont,soru_thr=contour_bul(sorugrup_bos,sorugrup_bos_gri,1)



    ###############################

    ogretim_bos=four_point_transform(kagit,bolgeler['ogretim_onay'])
    ogretim_bos_gri=four_point_transform(kagit_gri,bolgeler['ogretim_onay'])
    ogret_cont,ogret_thr=contour_bul(ogretim_bos,ogretim_bos_gri,1)
















    '''
    
    NAME FIND PART.
    '''

    isim_bos=four_point_transform(kagit,bolgeler['isim'])
    isim_bos_gri=cv2.cvtColor(isim_bos,cv2.COLOR_BGR2GRAY)
    coord_isim, thres=contour_bul(isim_bos, isim_bos_gri)
    #contour_cizdir(isim_bos,coord,"isim_bos")
    #cevap_islemleri(cevap_bos_gri,coord)











    ##############################################

    resim=cv2.imread(dolu_kagit)
    resim_gri=cv2.cvtColor(resim,cv2.COLOR_BGR2GRAY)
    warp2,warp2_gri=kagit_bul(resim,resim_gri)


    bolgeler2,areas2=bolge_bul(warp2,warp2_gri)

    ret,warp2=ters_bul(warp2,areas2)



    '''
    TERS İSE TEKRAR BOLGELERİ BUL
    '''
    if ret==True:
        warp2_gri=cv2.cvtColor(warp2,cv2.COLOR_BGR2GRAY)
        bolgeler2,areas2=bolge_bul(warp2,warp2_gri)


    else:
        pass

    isim_dolu=four_point_transform(warp2,bolgeler2['isim'])
    isim_dolu_gri=cv2.cvtColor(isim_dolu,cv2.COLOR_BGR2GRAY)

    contour_cizdir(isim_dolu,coord_isim,"dolu_kagit_contourlu")
    '''
    OGRETİM ONAY DOLU KAGIT
    '''


    ogretim_dolu=four_point_transform(warp2,bolgeler2['ogretim_onay'])
    ogretim_dolu_gri=cv2.cvtColor(ogretim_dolu,cv2.COLOR_BGR2GRAY)
    ogret_onay=sorugrup_islemleri(ogretim_dolu,ogretim_dolu_gri,ogret_cont)
    print("Öğretim Onayı:",ogret_onay)

    #cv2.drawContours(ogretim_dolu,ogret_cont,-1,(255,0,0),thickness=3)
    #cv2.imshow("ogretc",ogretim_dolu)

    #ogretim_onayı=sorugrup_islemleri(ogretim_dolu,ogretim_dolu_gri,ogretimonay_coord)



    sorugrup_dolu=four_point_transform(warp2,bolgeler2['soru_grubu'])
    sorugrup_dolu_gri=cv2.cvtColor(sorugrup_dolu,cv2.COLOR_BGR2GRAY)
    soru_tur=sorugrup_islemleri(sorugrup_dolu,sorugrup_dolu_gri,soru_cont)
    print("Soru Grubu",soru_tur)






    thresh_dolu=cv2.threshold(isim_dolu_gri,0,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)[1]
    isim_str=isim_islemleri(isim_dolu_gri,coord_isim,thresh_dolu)
    print(isim_str)


    sinav_dolu=four_point_transform(warp2,bolgeler2['sinav_turu'])
    sinav_dolu_gri=cv2.cvtColor(sinav_dolu,cv2.COLOR_BGR2GRAY)
    sinav_turu=sinav_islemleri(sinav_dolu,sinav_dolu_gri,sinav_coord)
    print("Sınav Türü: ",sinav_turu)



    ogrno_dolu=four_point_transform(warp2,bolgeler2['ogrno'])
    ogrno_dolu_gri=cv2.cvtColor(ogrno_dolu,cv2.COLOR_BGR2GRAY)

    ogrno_islemleri(ogrno_dolu,ogrno_dolu_gri,ogrno_coord)

    cevap_dolu=four_point_transform(warp2,bolgeler2['cevaplar'])
    cevap_dolu_gri=cv2.cvtColor(cevap_dolu,cv2.COLOR_BGR2GRAY)
    col1_dolu,col2_dolu,col3_dolu,col4_dolu=cevap_kolon(cevap_dolu)

    col1_gri_dolu,col2_gri_dolu,col3_gri_dolu,col4_gri_dolu=cevap_gri(col1_dolu,col2_dolu,col3_dolu,col4_dolu)

    #contour_cizdir(col1_dolu,col1_coord,"colon1 dolu")
    if len(cevap_anahtar)<=30:

        basarim=cevap_islemleri(col1_gri_dolu,col1_coord,1)

    elif len(cevap_anahtar)<=60:
        basarim1=cevap_islemleri(col1_gri_dolu,col1_coord,1)
        basarim2=cevap_islemleri(col2_gri_dolu,col2_coord,2)
        basarim=(basarim1[0]+basarim2[0],basarim1[1]+basarim2[1],basarim1[2]+basarim2[2],basarim1[3]+basarim2[3])
        #print(basarim)
    elif len(cevap_anahtar)<=90:
        basarim1=cevap_islemleri(col1_gri_dolu,col1_coord,1)
        basarim2=cevap_islemleri(col2_gri_dolu,col2_coord,2)
        basarim3=cevap_islemleri(col3_gri_dolu,col3_coord,3)
        basarim=basarim1+basarim2+basarim3
    elif len(cevap_anahtar)<=120:
        basarim1=cevap_islemleri(col1_gri_dolu,col1_coord,1)
        basarim2=cevap_islemleri(col2_gri_dolu,col2_coord,2)
        basarim3=cevap_islemleri(col3_gri_dolu,col3_coord,3)
        basarim4=cevap_islemleri(col4_gri_dolu,col4_coord,4)
        basarim=basarim1+basarim2+basarim3+basarim4








    print(f"Doğru cevap sayısı:{basarim[0]}\nYanlış cevap sayısı:{basarim[1]}\nBoş sayısı:{basarim[2]}\nİki cevap işaret:{basarim[3]}")

    cv2.waitKey()
    cv2.destroyAllWindows()




if __name__ == '__main__':
    bos_kagit="optic_empty.jpg"
    dolu_kagit="optic_marked.jpg"
    main_starter(bos_kagit,dolu_kagit)
    
