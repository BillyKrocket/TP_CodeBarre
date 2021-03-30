### GENERATION DE CODE BARRE

from PIL import Image, ImageDraw

## Définition des constantes

HAUTEUR = 300
LARGEUR = 1000
MARGE = 15
LARGEUR_BARRE = LARGEUR // (12*7 +3 +5 +3) # Un code EAN13 est composé de 95 barres noires ou blanches


# Définition des tables de convertions décimal/binaire EAN13
A = ['0001101','0011001','0010011','0111101','0100011','0110001','0101111','0111011','0110111','0001011']
B = ['0100111','0110011','0011011','0100001','0011101','0111001','0000101','0010001','0001001','0010111']
C = ['1110010','1100110','1101100','1000010','1011100','1001110','1010000','1000100','1001000','1110100']
liste_des_encodages = [ [A,A,A,A,A,A] , [A,A,B,A,B,B] , [A,A,B,B,A,B] , [A,A,B,B,B,A] , [A,B,A,A,B,B] ,
                        [A,B,B,A,A,B] , [A,B,B,B,A,A] , [A,B,A,B,A,B] , [A,B,A,B,B,A] , [A,B,B,A,B,A] ]

## Début du programme principal ecriture de code barre

def generationCodeBarre():
    delimiteur = '101'
    separateur = '01010'
    code = str(input('Veuillez entrer un code qui deviendra un magnifique code barre : '))
    if True:
        encodage = liste_des_encodages[int(code[0])]
        code = code[1:]
        code_barre = ''
        code_barre += delimiteur
        for i in range(6):
            code_barre += encodage[i][int(code[i])]
        code_barre += separateur
        for i in range(6, 12):
            code_barre += C[int(code[i])]
        code_barre += delimiteur
        return code_barre
    else:
        return False

def clef(code_a_12_chiffres):
    x = 0
    y = 0
    compteur = 1
    for i in reversed(str(code_a_12_chiffres)):
        if compteur % 2 == 0:
            x += int(i)
        else:
            y += int(i)
        compteur += 1
    z = x + 3*y
    if int(str(z)[-1]) > 5:
        m = round(z, -1)
    else:
        m = round(z, -1) + 10
    somme_de_controle = m - z
    return int(str(code_a_12_chiffres) + str(somme_de_controle))


def testValidite(code):
    somme_de_controle = clef(int(code[:-1]))
    if somme_de_controle == int(code):
        return True
    else:
        return False

def dessin():
    im = Image.new("RGB",(LARGEUR,HAUTEUR ),"white")
    code = generationCodeBarre()
    if code is False:
        print('ERREUR : le code entre est invalide')
    else:
        compteur = 0
        for i in code:
            if int(i) == 0 :
                couleur = "white"
            else :
                couleur = "black"
            ImageDraw.Draw(im).rectangle(((LARGEUR_BARRE*compteur+MARGE,MARGE),(LARGEUR_BARRE*(compteur+1)+MARGE-1,HAUTEUR-MARGE) ),fill=couleur)
            compteur += 1
    print("Et voila le travail !")
    im.show()

## Définition fonction lecture code barre

def parcours(image):
    largeur, hauteur = image.size
    hauteur = hauteur // 2 # +50 est du a l'image degeu avec un gros flash qui fausse la lecture du code barre
    seuil = 255 // 2 - 1
    liste = []
    for i in range(largeur):
        pixel = image.getpixel((i, hauteur))
        if pixel < seuil:
            liste.append('1')
        else:
            liste.append('0')
    return liste

def epuration(liste):
    result = packing(liste)
    index_delimiteur, taille_bande = trouveDelimiteur(result)
    result = result[index_delimiteur:]
    code_barre = ""
    compteur = 95
    index = 0
    while compteur != 0:
        compteur -= int(round(len(result[index]) / taille_bande))
        code_barre += result[index][0] * (int(round(len(result[index]) / taille_bande)))
        index += 1
    return code_barre

def packing(liste):
    result = []
    liste_tmp = []
    nb = liste[0]
    compteur = 0
    for i in liste:
        if nb != i:
            result.append(liste_tmp)
            liste_tmp = []
            liste_tmp.append(i)
            nb = i
        else:
            liste_tmp.append(i)
        compteur += 1
    result.append(liste_tmp)
    return result

def trouveDelimiteur(liste):
    compteur = 0
    index = 0
    delimiteur = 0
    for i in liste:
        marge = []
        if i[0] == '1':
            for loop in range(int(len(i) - (len(i)*0.25)), int(len(i) + (len(i)*0.25)) + 1):
                marge.append(loop)
            if len(liste[compteur + 1]) in marge and len(liste[compteur + 2]) in marge and liste[compteur + 1][0] == '0' and liste[compteur + 2][0] == '1':
                return compteur, len(i) #len(i) correspondant a la taille d'une bande
        index += len(i)
        compteur += 1


def decoupage(part):
    liste = []
    for i in range(7, 49, 7):
        liste.append(part[i-7:i])
    return liste

def lectureCode(image):
    code = epuration(parcours(image))
    code = code[3:-3]
    part1 = decoupage(code[:7*6])
    part2 = decoupage(code[7*6 + 5:])
    encodage = []
    code_decimal = ""
    for i in part1:
        if i in A:
            code_decimal += str(A.index(i))
            encodage.append(A)
        else:
            code_decimal += str(B.index(i))
            encodage.append(B)
    premiere_valeur = str(liste_des_encodages.index(encodage))
    for i in part2:
        code_decimal += str(C.index(i))
    return premiere_valeur + code_decimal

### Le main Q

def main():
    print('Si vous voulez decoder un code barre, taper 1')
    print('Si vous voulez encoder un code barre, taper 2')
    choix = int(input("\nVeuillez ecrire 1 ou 2 : "))
    print('-------------------------------------------------')
    if choix == 1:
        nom = str(input("Veuillez fournir le nom de l'image a decoder : "))
        image = Image.open(nom)
        image = image.convert('L') #L est le mot clef correspondant au nuance de gris
        print("Le code decimal correspondant a l'image est :",lectureCode(image))
        image.show()
    else:
        dessin()

main()
