#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#DEPENDENCIAS: python-pillow
#TODO
#testar se a pasta do slim pode ser lida
#random
#remover dependencia do imagemagick
#ler arquivos de texto com o read()
import os, subprocess, configparser, getpass, argparse, sys, imghdr, PIL
from PIL import Image

VERSION="0.9"

CONFIG="/home/%s/.config/nitroslim/nitroslim.conf" %getpass.getuser()

####config parse############
Configure = configparser.ConfigParser()
Configure.read(CONFIG)
BLUR=Configure["Image"]["Blur"]#5
CONTRASTE=Configure["Image"]["Contrast"]#-5
BRILHOAUTO=Configure["Image"]["Brightness"]#auto/manual
BRILHOMANUALNUM=Configure["Image"]["BrightnessManual"]#-5
RESOLUCAOAUTO=Configure["Image"]["Resolution"]#auto/manual
RESOLUCAOMANUALNUM=Configure["Image"]["ResolutionManual"]#1280x720
#other
PROGRAMA=Configure["Other"]["DefaultProgram"]#remover
DESTINO=Configure["Other"]["LxdeBackgroudFolder"]

############################

#theme name from slim config file#
(SLIMTHEMENAME, err) = subprocess.Popen("""awk '/current_theme/ { print $2}' /etc/slim.conf""", shell=True, stdout=subprocess.PIPE).communicate()
SLIMTHEMENAME=SLIMTHEMENAME.decode().strip()

DESTINO="/usr/share/slim/themes/%s/background.jpg" %SLIMTHEMENAME
#move previous wallpaper
FILESTHEMEFOLDER=os.listdir("""/usr/share/slim/themes/%s/""" %SLIMTHEMENAME)
FILESTHEMETOMOVE=[]
#~ if "bkpbackground
#~ for i in FILESTHEMEFOLDER:
	#~ if i.startswith("background.") is True and imghdr.what("""/usr/share/slim/themes/%s/%s""" %(SLIMTHEMENAME,i)) != None:
		#~ os.rename("""/usr/share/slim/themes/%s/%s""" %(SLIMTHEMENAME,i), """/usr/share/slim/themes/%s/bkp%s""" %(SLIMTHEMENAME,i))



#wallpaper from app folder
if PROGRAMA == "anypaper":
	SOFTCONFIG="/home/%s/.anypaper/anypaperrc" %getpass.getuser()
	(WALLPAPERLINK, err) = subprocess.Popen("""awk '/DefaultFile:/ {print $2}' %s""" %SOFTCONFIG, shell=True, stdout=subprocess.PIPE).communicate()
	WALLPAPERLINK=WALLPAPERLINK.decode().strip()
	
elif PROGRAMA == "nitrogen":
	SOFTCONFIG="/home/%s/.config/nitrogen/bg-saved.cfg" %getpass.getuser()
	(WALLPAPERLINK, err) = subprocess.Popen("""awk '/file=/ {print $0}' %s""" %SOFTCONFIG, shell=True, stdout=subprocess.PIPE).communicate()
	WALLPAPERLINK=WALLPAPERLINK.decode().split("=")[1].strip("\n")
	RESIZELIST=['--set-centered','--set-scaled','--set-tiled','--set-zoom','--set-zoom-fill']

####testar dependências####
DEPENDENCIAS={"convert":'You must install "imagemagick" (pacman -S imagemagick)',"xrandr":'You must install "xrandr" (pacman -S xorg-xrandr)', "anypaper":'You must install "anypaper" (yaourt -S anypaper)', "slim":'You must install "slim" (pacman -S slim)'}
    
######DEFINIR PARA PEGAR ESTE VALOR AUTOMATICAMENTE DA PASTA DE CONFIGURAÇÃO DO ANYPAPE
	
########################################################################
##############DEF FUNCTIONS#############################################

def IsInstalled(program):#check depencencies#
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return(program)
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return(exe_file)

    raise(ValueError())

def getRES(a,b): #get resolution
	if a == "auto":
		#return res from xrandr
		(Xrand,err) = subprocess.Popen("""xrandr --verbose | awk '/*current/ {print $1}'""", shell=True, stdout=subprocess.PIPE).communicate()
		RESOLUCAO=Xrand.decode().strip()
		return(RESOLUCAO.split("x"))
		#testando se é int#
		try:
			for i in RESOLUCAO:
				int(i)
			bypass=False
		except:
			bypass=True
	elif a == "manual" or bypass is True:
		if "x" in b:
			SCX=b.split("x")[0]
			SCY=b.split("x")[1]
			print(SCY)
			try:
				test=int(SCX)
				test=int(SCY)
			except ValueError:
				print("Wrong resolution format. Ex: 1280x720")
				exit(1)
		else:
			print("Wrong resolution format. Ex: 1280x720")
			exit(1)
		RESOLUCAO=b.split("x")
		return(RESOLUCAO)
		
#~ def Conversor(DefWallpaperlink, DefBrilhodest, DefContraste, defScreenx, defScreeny, defBlur, defSlimthemename, DefResize, Dest):#converter imagem com o imagemagick
	#~ if DefResize == "--set-zoom-fill":#--bg-scale on anypaper
		#~ print("kek")
		#~ Scale="""-gravity center -resize  %sx -crop x%s+0+0""" %(defScreenx,defScreeny)
		#~ Command="""convert '%s' -brightness-contrast %sx%s %s -blur %sx%s '%s'""" %(DefWallpaperlink, DefBrilhodest, DefContraste, Scale, defBlur, defBlur, Dest)
		#~ print(Command)	
		#~ os.system(Command)
	#~ elif DefResize == "--set-centered": #--normal on anypaper
		#~ print("kek")
		#~ # teste.jpg -gravity center -crop 1366x768+0+0 kek.jpg
		#~ Command="""convert '%s' -brightness-contrast %sx%s -blur %sx%s -gravity center -crop %sx%s+0+0 '%s'"""	%(DefWallpaperlink, DefBrilhodest, DefContraste, defBlur, defBlur, defScreenx,defScreeny, Dest)
		#~ print(Command)	
		#~ os.system(Command)		
	#~ elif DefResize == "--set-scaled":
		#~ #convert teste.jpg -resize 1366x768\! kek.jpg
		#~ Command="""convert '%s' -brightness-contrast %sx%s -blur %sx%s -resize %sx%s\! '%s'"""	%(DefWallpaperlink, DefBrilhodest, DefContraste, defBlur, defBlur, defScreenx,defScreeny, Dest)
		#~ print(Command)	
		#~ os.system(Command)
	#~ else:
		#~ print("!")

def CheckIfIsIMG(a):#check if file is image(exit)
	if os.path.exists(a) is True:
		if os.path.isfile(a) is True or os.path.islink(a) is True and os.path.isdir(a) is False:
			try:
				test=imghdr.what(a)
				if test == None:
					raise(ValueError())
				else:
					return(a)
			except:
				print("ERROR: the selected file isn't an image.")
				exit(1)
		else:
			print("ERROR: the selected file is a folder.")
			exit(1)
	else:
		print("ERROR: no such file or directory")
		exit(1)

def TestColor(cor): #check if input colors are valid
	corMod=cor.split("=")[1]
	if "#" in corMod and len(corMod) == 7 or len(corMod) == 4:
		return(corMod)
	else:
		print("ERROR: wrong color format, must be hex: Ex: #000000")
		exit(1)
			
def TestResize(resArg, listadesizes): #check if nitrogen args are valid
	if PROGRAMA == "nitrogen":
		MATCH=False
		for i in listadesizes:
			if i.strip("--") == resArg:
				MATCH=True
		if MATCH is False:
			print("ERROR: Wrong argument for set, the available args for Nitrogen are: set-centered, set-scaled, set-tiled, set-zoom, set-zoom-fill")
			exit(1)
		else:
			return(resArg)
			
#PIL Functions

def ApplyGaussianBlur(File,Radius):
	from PIL import ImageFilter
	blurred_image = File.filter(ImageFilter.GaussianBlur(radius=Radius))
	return(blurred_image)

def ApplyContrast(File,Value):
	from PIL import ImageEnhance
	contrast = ImageEnhance.Contrast(File)
	contrast = contrast.enhance(Value)
	return(contrast)

def AutoBrightness( im_file ):#get auto brightness value (grey value)
   im = Image.open(im_file).convert('L')
   stat = ImageStat.Stat(im)
   perc=int(stat.mean[0]*100/255)
   return(perc)
   
def ApplyBrightness(File,Value):#0-2
	from PIL import ImageEnhance
	brightness = ImageEnhance.Brightness(File)
	brightness = brightness.enhance(Value)
	return(brightness)
	
def SetWallpaper(Programa, ProgArg, BGColor, Wallpaper):  #(PROGRAMA,PROGRAMARGUMENT,COLOR,WALLPAPERLINK
	if Programa == "nitrogen":
		#py --nitrogen set-zoom set-color=#000 ~img.jpg
		if BGColor != None:
			os.system("nitrogen --%s --set-color=%s '%s'"	%(ProgArg, BGColor, Wallpaper))
		else:
			os.system("nitrogen --%s '%s'"	%(ProgArg, Wallpaper))

def CropWallpaper( File, Resolution, Resize, Color ):
	ResolutionINT=[ int(Resolution[0]), int(Resolution[1]) ]
	if Resize == "set-centered":
		new_im = Image.new('RGB', ResolutionINT)
		new_im.paste(Color, None)
		Center = [int( round(ResolutionINT[0]/2, 0) ), int( round(ResolutionINT[1]/2, 0) )]
		FileRes = File.size
		new_im.paste(SourceIMG, ( int(Center[0]-FileRes[0]/2), int(Center[1]-FileRes[1]/2) ) )
		return(new_im)
	elif Resize == "set-scaled":
		return( File.resize( ResolutionINT, Image.ANTIALIAS) )
	elif Resize == "set-tiled":
		from PIL import ImageDraw
		( width, height ) = File.size
		new_im = Image.new('RGB', ResolutionINT)
		for i in range(0,ResolutionINT[0],width):
			for j in range(0, ResolutionINT[1], height):
				new_im.paste(SourceIMG, (int(i),int(j)))
		return(new_im)
	elif Resize == "set-zoom":
		new_im = Image.new('RGB', ResolutionINT)
		new_im.paste(Color, None)
		FileRes = File.size
		
		def Mode1():
			Multiplier=ResolutionINT[0]/FileRes[0]
			Width=Multiplier*FileRes[0]
			Height=Multiplier*FileRes[1]
			YAlign= int(round((ResolutionINT[1]/2)-(Height/2), 0))
			img_new_res = File.resize( (int(round(Width,0)),int(round(Height,0)) ) , Image.ANTIALIAS)
			new_im.paste(img_new_res, (0,YAlign))
			return(new_im)
			
		def Mode2():
			Multiplier=ResolutionINT[1]/FileRes[1]
			Width=Multiplier*FileRes[0]
			Height=Multiplier*FileRes[1]
			XAlign= int(round((ResolutionINT[0]/2)-(Width/2), 0))
			img_new_res = File.resize( (int(round(Width,0)),int(round(Height,0)) ) , Image.ANTIALIAS)
			new_im.paste(img_new_res, (XAlign,0))
			return(new_im)
			
		if FileRes[0] > FileRes[1] :
			return(Mode1())
		elif FileRes[0] < FileRes[1]:
			return(Mode2())
		else:
			if ResolutionINT[0] > ResolutionINT[1] or ResolutionINT[0] == ResolutionINT[1]:
				return(Mode2())
			else:
				return(Mode1())
	elif Resize == "set-zoom-fill":
		new_im = Image.new('RGB', ResolutionINT)
		new_im.paste(Color, None)
		FileRes = File.size
		
		def Mode1():
			Multiplier=ResolutionINT[0]/FileRes[0]
			Width=Multiplier*FileRes[0]
			Height=Multiplier*FileRes[1]
			YAlign= int(round((ResolutionINT[1]/2)-(Height/2), 0))
			img_new_res = File.resize( (int(round(Width,0)),int(round(Height,0)) ) , Image.ANTIALIAS)
			new_im.paste(img_new_res, (0,YAlign))
			return(new_im)
			
		def Mode2():
			Multiplier=ResolutionINT[1]/FileRes[1]
			Width=Multiplier*FileRes[0]
			Height=Multiplier*FileRes[1]
			XAlign= int(round((ResolutionINT[0]/2)-(Width/2), 0))
			img_new_res = File.resize( (int(round(Width,0)),int(round(Height,0)) ) , Image.ANTIALIAS)
			new_im.paste(img_new_res, (XAlign,0))
			return(new_im)
			
		if FileRes[0] > FileRes[1]:
			if ResolutionINT[0] < ResolutionINT[1]:
				return(Mode2())
			elif ResolutionINT[0] > ResolutionINT[1]:
				return(Mode1())
		elif FileRes[0] < FileRes[1]:
			if ResolutionINT[0] < ResolutionINT[1]:
				return(Mode2())
			elif ResolutionINT[0] > ResolutionINT[1]:
				return(Mode1())				
		else:
			if ResolutionINT[0] > ResolutionINT[1] or ResolutionINT[0] == ResolutionINT[1]:
				return(Mode1())
			else:
				return(Mode2())


def GetSizeAndColorNitrogen( File ):
	NitrogenConfig = open(File,'r')
	NitrogenConfigLinhas=NitrogenConfig.readlines()
	NitrogenConfig.close()
	for i in NitrogenConfigLinhas:
		if i.startswith("mode="):
			mode=int(i.split("=")[1].strip("\n"))
		if i.startswith("bgcolor="):
			color=i.split("=")[1].strip("\n")
	ModesDict={0:"set-scaled", 1:"set-tiled", 2:"set-centered", 3:"set-zoom", 5:"set-zoom-fill"}
	return([ModesDict[mode],color])

#Set

########################################################################
###call dependencies check###
for i in DEPENDENCIAS:
	try:
		test=IsInstalled(i)
	except:
		print("ERROR: /usr/bin/%s not found. %s" %(i, DEPENDENCIAS[i]))
		exit()
	
####args parse##############

#se não possuir argumentos, rodar o programa seletor e aplicar opções do conf file#

if len(sys.argv) == 1:
	RESOLUCAO=getRES(RESOLUCAOAUTO,RESOLUCAOMANUALNUM)
	#chamar o programa
	os.system(PROGRAMA) #selecionar wallpaper e sair#
	SizeAndColor=GetSizeAndColorNitrogen(SOFTCONFIG)
	PROGRAMARGUMENT=SizeAndColor[0]
	COLOR=SizeAndColor[1]
	SetWallpaper( PROGRAMA, PROGRAMARGUMENT, COLOR, WALLPAPERLINK )
	SourceIMG = Image.open( WALLPAPERLINK ) #open file
	#####cropar de acordo com a seleção!
	SourceIMG = CropWallpaper( SourceIMG, RESOLUCAO, PROGRAMARGUMENT, COLOR )
	SourceIMG = ApplyBrightness( SourceIMG,float(BRILHOMANUALNUM) )
	SourceIMG = ApplyContrast(SourceIMG,float(CONTRASTE))
	SourceIMG = ApplyGaussianBlur(SourceIMG,float(BLUR))
	SourceIMG.save(DESTINO) 
	exit(0)

parser = argparse.ArgumentParser(description='A program to share a wallpaper beetwhen slim and nitrogen,anypaper or feh. It uses imagemagick to autocorrect brighness and add blur to the wallpaper on slim.\nConfig file at: %s' %CONFIG)

parser.add_argument('--blur', '-b', metavar="N", help='apply blur radius manually. Ex: -b 2',  type=int)

parser.add_argument('--contrast', '-c', metavar="N", help='apply contrast manually. Ex: -c 10',  type=int)

parser.add_argument('--brightness', '-br', metavar="N", help='apply brightness manually. Ex: -br -10 or -br a and the program will try to get the best value for your image')

parser.add_argument('--resolution', '-re', metavar="N", help='select resolution manually, do not needed with anypaper. Ex: -re 1280x720')

parser.add_argument('--random', '-r', metavar="N", nargs='+', help='ONLY WITH FEH: selects a random wallpaper from selected folders. The wallpaper is set in both, slim and desktop. Ex: -r ~/Pictures/CoolWallopapers ~/Pictures/AnimeWallpapers ...')

parser.add_argument('--nitrogen', '-ni', metavar="N", nargs='+', help='Set a picture as wallpaper with Nitrigen. The wallpaper is alsho shared with Slim. Use Nitrogen arguments without "--" on the start (see more on nitrogen --help). Ex: nitroslim --nitrogen set-zoom ~/CoolPic.jpg or nitroslim --nitrogen set-centered set-color=#ffffff  ~/CoolPic.jpg')

#passar os arguments
args = parser.parse_args()
#testar os argumentos

RodarSeletor=True
if args.nitrogen is not None:
	PROGLIST=args.nitrogen
	if len(PROGLIST) == 3:
		COLOR=TestColor(PROGLIST[1])#test if has a valid color
		WALLPAPERLINK=CheckIfIsIMG(PROGLIST[2])#test if is a valid file
		PROGRAMARGUMENT=TestResize(PROGLIST[0],RESIZELIST)
		RodarSeletor=False
	elif len(args.nitrogen) == 2:#no bg color, testar se há opções listadas
		COLOR=None
		pass
	

if args.brightness != None:
	brvar=args.brightness
	if brvar == "a" or brvar == "A" or brvar == "auto": #foi selecionado o modo automatico
		pass
		#chamar brilho automatico
	else:
		#testar se é numero
		try:
			test=int(brvar)
			BRILHOMANUALNUM=brvar
		except:
			print("ERROR: brightness must be an integer or 'a' for auto mode")
			exit(1)
print(PROGRAMARGUMENT)
if args.resolution != None:#adicionar mais testes
	RESOLUCAO=getRES("manual",args.resolution)
else:
	RESOLUCAO=getRES("auto","r")

if args.random != None:#testar se existem imagens dentro da pasta 
	FolderRand=args.random
	if os.path.isdir(FolderRand):
		SOURCERANDONFOLDER=args.random[0]#pasta dos wallpapers que serão randomizados
	else:
		print("you can only randomize images from a folder")


###############################################
#######rodar com as configurações definidas####


if RodarSeletor == True:
	#~ os.system(PROGRAMA)
	Conversor(WALLPAPERLINK, BRILHOMANUALNUM, CONTRASTE, RESOLUCAO[0], RESOLUCAO[1], BLUR, SLIMTHEMENAME, RESIZE, DESTINO)
else:#wallpaper foi inserido manualmente usando o programa desejado
	SetWallpaper(PROGRAMA,PROGRAMARGUMENT,COLOR,WALLPAPERLINK)
	SourceIMG = Image.open(WALLPAPERLINK) #open file
	print(PROGRAMARGUMENT)
	#####cropar de acordo com a seleção!
	SourceIMG = CropWallpaper( SourceIMG, RESOLUCAO, PROGRAMARGUMENT, COLOR )
	SourceIMG = ApplyBrightness(SourceIMG,float(BRILHOMANUALNUM))
	SourceIMG = ApplyContrast(SourceIMG,float(CONTRASTE))
	SourceIMG = ApplyGaussianBlur(SourceIMG,float(BLUR))
	print(DESTINO)
	SourceIMG.save(DESTINO) #salvar
