import sys
from PyQt5.QtWidgets import QApplication, QWidget,QStackedWidget, QMainWindow,QTabWidget, QPushButton, QLabel, QLineEdit,QSlider, QVBoxLayout, QHBoxLayout, QCheckBox, QMessageBox, QComboBox
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage
from pyautogui import ImageNotFoundException
from PyQt5.QtCore import Qt
import time
import string
import random   
import pyautogui

import win32api
import ctypes
from ctypes import wintypes,windll

user32 = windll.user32
from PIL import ImageGrab, ImageOps, Image
import pydirectinput
from threading import Thread,Timer
from functools import partial
from interception import *
from pynput.keyboard import Listener,Key, Controller, KeyCode
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.HayaliAlancik = None
        self.HpMakro = 0
        self.MpMakro = 0
        self.birkerebasildi = 0
        self.birkerebasildi2 = 0
        self.MakroMpKordinat = None
        self.MakroHpKordinat = None
        self.MpRenk = None
        self.HpRenk = None
        self.basladi = 0
        self.ciftele = 0
        self.makrodevrede = 0
        self.hangisiicin = ["Ben"]
        self.simdiki_foto = 0 
        self.Hp = 0
        self.sefer = 1
        
        self.DebuffOnline = 0
        self.DebuffList = []
        self.Title = None
        self.page4SilOnline = 0
        self.ilkalan = 0
        self.Title = self.random_name()
        self.setWindowTitle(self.Title)
        self.GizleKey = None
        self.GizleSeciyor = 0
        self.DebuffKey = None
        self.hidemi = 0
        self.Mp = 0
        self.BaslatKeySeciyor = 0
        self.MpKordinat = None
        self.HpKordinat = None
        self.Torment = 0
        self.Malice = 0
        self.Parasite = 0
        self.Superior = 0
        self.Massive = 0
        self.Subside = 0
        # Ana widget oluştur
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.Otomatik = 0
        # Ana düzen oluştur
        self.layout = QVBoxLayout(self.central_widget)
        # Tab Widget oluştur
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        # Sayfa 1
        self.page1 = QWidget()
        self.tab_widget.addTab(self.page1, "Sil")
        self.page1_layout = QVBoxLayout(self.page1)

        # Checkbox'ları ve butonları ekle
        self.SilmeCheckBox = QCheckBox('Silme Makrosu Aktif/Kapalı')
        self.page1_layout.addWidget(self.SilmeCheckBox)
        
        self.OtomatikCheckBox = QCheckBox('Otomatik Sil Aktif/Kapalı')
        self.page1_layout.addWidget(self.OtomatikCheckBox)

    
        self.selectButton = QPushButton('Skill Seç')
        self.page1_layout.addWidget(self.selectButton)
            
        self.ListeSifirlaButon = QPushButton('Skilleri Sıfırla')
        self.page1_layout.addWidget(self.ListeSifirlaButon)
        self.ListeSifirlaButon.clicked.connect(self.ListeSifirlaButonClick)
        self.pixmap = QPixmap(None)  # Resmin dosya yolunu 
        self.otohppixmap = QPixmap(None)
        self.otomppixmap = QPixmap(None)
        self.label = QLabel()
        self.label.setPixmap(self.pixmap)
        self.page1_layout.addWidget(self.label)
        



        self.ileri = QPushButton('Sonraki Skille Bak')
        self.page1_layout.addWidget(self.ileri)
        self.geri = QPushButton('Önceki Skille Bak')
        self.page1_layout.addWidget(self.geri)
        self.ileri.clicked.connect(self.sonrakifoto)
        self.geri.clicked.connect(self.oncekifoto)
        
        self.selectkeyButton = QPushButton('Tuş Seç')
        self.page1_layout.addWidget(self.selectkeyButton)
        self.page1TusSil = QPushButton('Tuşu Sıfırla')
        self.page1_layout.addWidget(self.page1TusSil)
        self.page1TusSil.clicked.connect(self.page1TusSilClick)
        self.silSpeedLabel = QLabel('Sil HIZ: 1 ', self)

        self.page1_layout.addWidget(self.silSpeedLabel)
        self.SilMs = 0.01
        self.KalkanMs = 0.01
        # Slider oluştur
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(1)
        self.slider.setMaximum(1000)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.valueChanged.connect(self.sliderValueChanged)
        self.page1_layout.addWidget(self.slider)

        # Bağlantıları ekle
        self.selectButton.clicked.connect(self.selectButtonClicked)
        self.selectkeyButton.clicked.connect(self.selectKeyClicked)
        self.SilmeCheckBox.stateChanged.connect(self.SilmeChange)
        self.OtomatikCheckBox.stateChanged.connect(self.OtomatikCheckBoxChange)
        

        # Sayfa 2
        self.page2 = QWidget()
        self.tab_widget.addTab(self.page2, "Kalkan İtem Tak/Çıkar")
        self.page2_layout = QVBoxLayout(self.page2)
        self.page2.setLayout(self.page2_layout)
        self.KalkanTak = QLabel('TEK EL KALKAN TAK/ÇIKAR')
        self.page2_layout.addWidget(self.KalkanTak)
        self.KalkanButton = QPushButton('Kalkan Kordinat Seç')
        self.page2_layout.addWidget(self.KalkanButton)

        self.selectKalkanKey = QPushButton('Tuş Seç')
        self.page2_layout.addWidget(self.selectKalkanKey)

        self.kalkanTusSifirla = QPushButton('Tuşu Sıfırla')
        self.page2_layout.addWidget(self.kalkanTusSifirla)
        self.kalkanTusSifirla.clicked.connect(self.kalkanTusSifirlaClick)

        #self.page2KalkanTusSil()

        self.KalkanTak = QLabel('ÇİFT EL KALKAN TAK/ÇIKAR')
        self.page2_layout.addWidget(self.KalkanTak)
        self.ciftElKalkan = QPushButton('Çift El Kalkan Tuş')
        self.page2_layout.addWidget(self.ciftElKalkan)
        self.ciftelkalkantussifirla = QPushButton('Tuşu Sıfırla')
        self.page2_layout.addWidget(self.ciftelkalkantussifirla)
        self.ciftelkalkantussifirla.clicked.connect(self.ciftelkalkantussifirlaClick)
        self.ciftelKalkanKordinatButon = QPushButton('Kalkan Kordinat Seç')
        self.page2_layout.addWidget(self.ciftelKalkanKordinatButon)
        self.ciftelKalkanKordinat = None
        self.ciftelKalkanKordinatSeciyor = 0
        self.ciftelKalkanKordinatButon.clicked.connect(self.ciftelKalkanKordinatButonClicked)
        
        
        self.KalkanTak = QLabel('ÇİFT TEK EL İTEM DEĞİŞTİRME')
        self.page2_layout.addWidget(self.KalkanTak)
        self.Esya1 = QPushButton('Sağ El İtem Kordinat')
        self.page2_layout.addWidget(self.Esya1)

        self.Esya2 = QPushButton('Sol El İtem Kordinat')
        self.page2_layout.addWidget(self.Esya2)

        self.CiftEleButton = QPushButton('Çift El Tuşu')
        self.page2_layout.addWidget(self.CiftEleButton)
        self.CiftEleTusSifirla = QPushButton('Tuşu Sıfırla')
        self.page2_layout.addWidget(self.CiftEleTusSifirla)
        self.CiftEleTusSifirla.clicked.connect(self.CiftEleTusSifirlaClick)

        self.kalkanSpeedLabel = QLabel('Kalkan HIZ: 1', self)
        self.page2_layout.addWidget(self.kalkanSpeedLabel)
        
        
        self.kalkanSlider = QSlider(Qt.Horizontal, self)
        self.kalkanSlider.setMinimum(1)
        self.kalkanSlider.setMaximum(1000)
        self.kalkanSlider.setTickInterval(1)
        self.kalkanSlider.setTickPosition(QSlider.TicksBelow)
        self.kalkanSlider.valueChanged.connect(self.kalkanSliderChanged)
        self.page2_layout.addWidget(self.kalkanSlider)


        
        self.KalkanButton.clicked.connect(self.KalkanButtonClicked)
        self.selectKalkanKey.clicked.connect(self.KalkanKeyClicked)
        self.ciftElKalkan.clicked.connect(self.ciftElKalkanClicked)
        self.Esya1.clicked.connect(self.Esya1Clicked)
        self.Esya2.clicked.connect(self.Esya2Clicked)
        self.CiftEleButton.clicked.connect(self.CiftEleButtonClicked)
        self.HpKey = Key.f1
        
        
        
        
        
        self.page3 = QWidget()
        self.tab_widget.addTab(self.page3, "OTO-POT-MANA")
        self.page3_layout = QVBoxLayout(self.page3)
        self.page3.setLayout(self.page3_layout)
                
        self.lbl = QLabel('OTO HP ', self)
        self.page3_layout.addWidget(self.lbl)
        
        
        self.HpCheckBox = QCheckBox('OTO-HP Açık/Kapalı')
        self.page3_layout.addWidget(self.HpCheckBox)
        self.HpCheckBox.stateChanged.connect(self.HpCheckBoxChange)
        
        self.HpCombo = QComboBox()
        self.HpCombo.addItems(["F1","F2","F3","F4","F5","F6","F7","F8"])
        self.HpCombo.currentIndexChanged.connect(self.HpComboChange)
        self.page3_layout.addWidget(self.HpCombo)
        self.otohpfoto = QLabel()
        self.otohpfoto.setPixmap(self.otohppixmap)
        self.lblc = QLabel("Yukarıdaki seçilen renk sizin HP rengi olmalıdır. Hatalıysa tekrar alın!")
        self.page3_layout.addWidget(self.otohpfoto)
        self.page3_layout.addWidget(self.lblc)
        self.lbl = QLabel("HP Pot Seçin:")
        self.page3_layout.addWidget(self.lbl)
        self.HangiPotinput = QLineEdit()
        self.page3_layout.addWidget(self.HangiPotinput)
        self.lbl = QLabel('OTO MP ', self)
        self.page3_layout.addWidget(self.lbl)
        self.MpCheckBox = QCheckBox('OTO-MP Açık/Kapalı')
        self.page3_layout.addWidget(self.MpCheckBox)
        self.MpCheckBox.stateChanged.connect(self.MpCheckBoxChange)
        self.MpCombo = QComboBox()
        self.MpCombo.addItems(["F1","F2","F3","F4","F5","F6","F7","F8"])
        self.MpCombo.currentIndexChanged.connect(self.MpComboChange)
        self.page3_layout.addWidget(self.MpCombo)
        self.otompfoto = QLabel()
        self.otompfoto.setPixmap(self.otomppixmap)
        self.lblc = QLabel("Yukarıdaki seçilen renk sizin MP rengi olmalıdır. Hatalıysa tekrar alın!")
        self.page3_layout.addWidget(self.otompfoto)
        self.page3_layout.addWidget(self.lblc)
        self.lbl = QLabel("MP Pot Seçin:")
        self.page3_layout.addWidget(self.lbl)
        
        self.MpPotinput = QLineEdit()
        self.page3_layout.addWidget(self.MpPotinput)
        
        self.page3TekElCheckbox = QCheckBox('Tek El Kalkan Tak/Çıkar')
        self.page3_layout.addWidget(self.page3TekElCheckbox)
        self.page3CiftElCheckbox = QCheckBox('Çift El Kalkan Tak/Çıkar')
        self.page3_layout.addWidget(self.page3CiftElCheckbox)
        self.page3CiftElCheckbox.clicked.connect(self.page3CiftElCheckboxChange)
        self.page3TekElCheckbox.clicked.connect(self.page3TekElCheckboxChange)
        self.page3CiftElFuncCheckbox = QCheckBox('Çift Tek El İtem Değiştirme')
        self.page3_layout.addWidget(self.page3CiftElFuncCheckbox)






        self.SpamHpCheckbox = QCheckBox('OTO-HP Makro Açık/Kapalı')
        self.SpamHpCheckbox.stateChanged.connect(self.MakroHpChange)
        self.page3_layout.addWidget(self.SpamHpCheckbox)
        self.makrohppixmap = QPixmap(None)
        self.makrohpfoto = QLabel()
        self.makrohpfoto.setPixmap(self.makrohppixmap)
        self.page3_layout.addWidget(self.makrohpfoto)


        self.SpamMpCheckbox = QCheckBox("OTO-MP Makro Açık/Kapalı")
        self.page3_layout.addWidget(self.SpamMpCheckbox)
        self.makromppixmap = QPixmap(None)
        self.makrompfoto = QLabel()
        self.makrompfoto.setPixmap(self.makromppixmap)
        self.page3_layout.addWidget(self.makrompfoto)
        self.SpamMpCheckbox.stateChanged.connect(self.MakroMpChange)

        


        self.SpamMakro1 = QLineEdit()
        self.SpamMakroMs1 = QLineEdit()
        self.SpamMakro2 = QLineEdit()
        self.SpamMakroMs2 = QLineEdit()
        self.SpamMakro3 = QLineEdit()
        self.SpamMakroMs3 = QLineEdit()        
        self.SpamSurekliCheckbox = QCheckBox('Sürekli Bas/1 Kere Bas')
        self.page3_layout.addWidget(self.SpamSurekliCheckbox)
        self.page3_layout.addWidget(self.SpamMakro1)
        self.page3_layout.addWidget(self.SpamMakroMs1)

        self.page3_layout.addWidget(self.SpamMakro2)
        self.page3_layout.addWidget(self.SpamMakroMs2)
        self.page3_layout.addWidget(self.SpamMakro3)
        self.page3_layout.addWidget(self.SpamMakroMs3)
        self.SpamMakroMs1.setText("0.1")
        self.SpamMakroMs2.setText("0.1")
        self.SpamMakroMs3.setText("0.1")
        self.SpamMakroF = QComboBox()
        self.SpamMakroF.addItems(["Seçili Değil","F1","F2","F3","F4","F5","F6","F7","F8"])
        self.SpamMakroKey = None
        self.SpamMakroF.currentIndexChanged.connect(self.SpamMakroFChange)        
        self.page3_layout.addWidget(self.SpamMakroF)                
        self.page4 = QWidget()
        self.tab_widget.addTab(self.page4, "Debuff Tepki")
        self.page4_layout = QVBoxLayout(self.page4)
        self.page4.setLayout(self.page4_layout)
        
        
        self.DebuffAcikCheckBox = QCheckBox('Debuff Tepki Açık/Kapalı')
        self.DebuffAcikCheckBox.clicked.connect(self.DebuffAcikClicked)
        self.DebuffAcikCheckBox.stateChanged.connect(self.DebuffAcikChange)
        

        self.page4_layout.addWidget(self.DebuffAcikCheckBox)
        self.TormentCheckbox = QCheckBox('Torment')
        self.page4_layout.addWidget(self.TormentCheckbox)
        
        self.MaliceCheckbox = QCheckBox('Malice')
        self.page4_layout.addWidget(self.MaliceCheckbox)
        
        self.ParasiteCheckbox = QCheckBox('Parasite')
        self.page4_layout.addWidget(self.ParasiteCheckbox)
        
        self.SuperiorCheckbox = QCheckBox('Superior')
        self.page4_layout.addWidget(self.SuperiorCheckbox)
        
        self.MassiveCheckbox = QCheckBox('Massive')
        self.page4_layout.addWidget(self.MassiveCheckbox)
        self.SubsideCheckbox = QCheckBox('Subside')
        self.page4_layout.addWidget(self.SubsideCheckbox)
        
        self.lbl = QLabel('Yapacağı İşlemler')
        self.page4_layout.addWidget(self.lbl)
        self.kerebbascheckbox = QCheckBox('1 kere bas')
        self.kerebbascheckbox.stateChanged.connect(self.birkerebascheckboxchange)
        self.page4_layout.addWidget(self.kerebbascheckbox)

        self.sefercheckbox = QCheckBox('Sürekli bas')
        self.sefercheckbox.stateChanged.connect(self.sefercheckboxChange)
        self.page4_layout.addWidget(self.sefercheckbox)
        self.sefercheckbox.setChecked(True)

        self.page4TekElKalkanOnline = 0
        self.page4TekElKalkan = QCheckBox('Tek El Kalkan Tak/Çıkar')
        self.page4TekElKalkan.clicked.connect(self.page4TekElKalkanClicked)
        self.page4TekElKalkan.stateChanged.connect(self.page4TekElKalkanChange)
        self.page4_layout.addWidget(self.page4TekElKalkan)
        
        self.page4CiftElKalkanOnline = 0
        self.page4CiftElKalkan = QCheckBox('Çift El Kalkan Tak/Çıkar')
        self.page4CiftElKalkan.clicked.connect(self.page4CiftElKalkanClicked)
        self.page4CiftElKalkan.stateChanged.connect(self.page4CiftElKalkanChange)
        self.page4_layout.addWidget(self.page4CiftElKalkan)
        
        
        self.page4SilOnline = 0
        self.page4Sil = QCheckBox('Sil Açık/Kapalı')
        self.page4_layout.addWidget(self.page4Sil)
        
        self.page4Sil.stateChanged.connect(self.page4SilChange)
        self.page4Sil.clicked.connect(self.page4SilClicked)

        self.TormentCheckbox.stateChanged.connect(self.TormentCheckboxchange)
        self.MaliceCheckbox.stateChanged.connect(self.MaliceCheckboxchange)
        self.ParasiteCheckbox.stateChanged.connect(self.ParasiteCheckboxchange)
        self.SuperiorCheckbox.stateChanged.connect(self.SuperiorCheckboxchange)
        self.MassiveCheckbox.stateChanged.connect(self.MassiveCheckboxchange)
        self.SubsideCheckbox.stateChanged.connect(self.SubsideCheckboxchange)
        
        
        self.DebuffCombo = QComboBox()
        self.DebuffCombo.addItems(["Seçili Değil","F1","F2","F3","F4","F5","F6","F7","F8"])
        self.DebuffCombo.currentIndexChanged.connect(self.DebuffComboChange)
        
        # Dış düzen oluştur
        self.lbl = QLabel('Tuş Bas:')      
        self.page4_layout.addWidget(self.lbl)

        self.DebuffPotinput = QLineEdit()
        self.page4_layout.addWidget(self.DebuffPotinput)
        self.page4_layout.addWidget(self.DebuffCombo)
        external_layout = QVBoxLayout()
            
        # SolEl ve Envater düzeni oluştur
        solel_envanter_layout = QHBoxLayout()

        # SolEl düzeni oluştur
        solel_layout = QVBoxLayout()
        self.aciklama = QLabel("                                        Kordinat seçmek için 'CTRL' tuşunu kullanmalısınız!")
        solel_layout.addWidget(self.aciklama)
        self.SolEl = QCheckBox('Sol El')
        solel_layout.addWidget(self.SolEl)
        self.SolEl.stateChanged.connect(self.SolElChange)
        self.TutBox = QCheckBox('Tut')
        self.TutBox.stateChanged.connect(self.TutBoxChange)
        solel_layout.addWidget(self.TutBox)
        solel_envanter_layout.addLayout(solel_layout)

        # Envater düzeni oluştur
        envanter_layout = QVBoxLayout()
        self.EnvanterCheckBox = QCheckBox('Envanter Sürekli Açık')
        envanter_layout.addWidget(self.EnvanterCheckBox)
        

 
        self.EnvanterAcKapatCheckbox = QCheckBox('Envanter Kapat')
        envanter_layout.addWidget(self.EnvanterAcKapatCheckbox)
        self.EnvanterAcKapatCheckbox.stateChanged.connect(self.EnvanterAcKapatClicked)
        self.EnvanterCheckBox.stateChanged.connect(self.EnvanterCheckBoxChange)
        solel_envanter_layout.addLayout(envanter_layout)
        self.EnvanterCheckBox.setChecked(True)
        
        

        # SolEl ve Envater düzenini dış düzene ekleyin
        external_layout.addLayout(solel_envanter_layout)
        
        DurdurBaslatLayout = QHBoxLayout()
        durdur_layout = QVBoxLayout()

        self.GizleButon = QPushButton('Gizle Tuşu Seçin')
        self.GizleButon.clicked.connect(self.GizleButonClicked)
        durdur_layout.addWidget(self.GizleButon)
        self.BaslatKey = None
        self.BaslatKeyButon = QPushButton('Başlat/Durdur Tuş seçin')
        self.BaslatKeyButon.clicked.connect(self.BaslatKeyButonClicked)
        durdur_layout.addWidget(self.BaslatKeyButon)
        
        self.ConfigKaydet = QPushButton('Ayarları Kaydet')
        self.ConfigYukle = QPushButton('Ayarları Yükle')
        self.ConfigKaydet.clicked.connect(self.AyarlariKaydets)
        self.ConfigYukle.clicked.connect(self.AyarlariYukle)

        durdur_layout.addWidget(self.ConfigKaydet)
        durdur_layout.addWidget(self.ConfigYukle)
        DurdurBaslatLayout.addLayout(durdur_layout)
       
        self.durum = QLabel('Durum: Çalışmıyor')
        durdur_layout.addWidget(self.durum)
        external_layout.addLayout(DurdurBaslatLayout)
        
        
        
        
        
        self.page5 = QWidget()
        self.tab_widget.addTab(self.page5, "Makro Tuşları")
        self.page5_layout = QVBoxLayout(self.page5)
        self.page5.setLayout(self.page5_layout)
        
        
        self.MakroTusuCheckbox1 = QCheckBox('Makro Tuşu 1')
        self.MakroTusuCheckbox2 = QCheckBox('Makro Tuşu 2')
        self.MakroTusuCheckbox3 = QCheckBox('Makro Tuşu 3')
        self.MakroTusuCheckbox4 = QCheckBox('Makro Tuşu 4')
        self.MakroTusuCheckbox5 = QCheckBox('Makro Tuşu 5')




        self.MakroSurekliBas1 = QCheckBox('Sürekli Bas')
        self.MakroSurekliBas2 = QCheckBox('Sürekli Bas')
        self.MakroSurekliBas3 = QCheckBox('Sürekli Bas')
        self.MakroSurekliBas4 = QCheckBox('Sürekli Bas')
        self.MakroSurekliBas5 = QCheckBox('Sürekli Bas')
        
        
   
        self.MakroTusuText1 = QLineEdit()
        self.MakroTusuText2 = QLineEdit()
        self.MakroTusuText3 = QLineEdit()
        self.MakroTusuText4 = QLineEdit()
        self.MakroTusuText5 = QLineEdit()
        
        self.MakroMs1 = QSlider(Qt.Horizontal, self)
        self.MakroMs2 = QSlider(Qt.Horizontal, self)
        self.MakroMs3 = QSlider(Qt.Horizontal, self)
        self.MakroMs4 = QSlider(Qt.Horizontal, self)
        self.MakroMs5 = QSlider(Qt.Horizontal, self)
        
        self.MakroMss1 = 0.001
        self.MakroMss2 = 0.001
        self.MakroMss3 = 0.001
        self.MakroMss4 = 0.001
        self.MakroMss5 = 0.001

        self.lbl1 = QLabel('MS: 1')
        self.lbl2 = QLabel('MS: 1')
        self.lbl3 = QLabel('MS: 1')
        self.lbl4 = QLabel('MS: 1')
        self.lbl5 = QLabel('MS: 1')
        



        
        self.MakroCombo1 = QComboBox()
        self.MakroCombo1.addItems(["Seçili Değil","F1","F2","F3","F4","F5","F6","F7","F8"])
        
        self.MakroCombo2 = QComboBox()
        self.MakroCombo2.addItems(["Seçili Değil","F1","F2","F3","F4","F5","F6","F7","F8"])
        
        self.MakroCombo3 = QComboBox()
        self.MakroCombo3.addItems(["Seçili Değil","F1","F2","F3","F4","F5","F6","F7","F8"])
        
        self.MakroCombo4 = QComboBox()
        self.MakroCombo4.addItems(["Seçili Değil","F1","F2","F3","F4","F5","F6","F7","F8"])
        
        self.MakroCombo5 = QComboBox()
        self.MakroCombo5.addItems(["Seçili Değil","F1","F2","F3","F4","F5","F6","F7","F8"])
        
        self.MakroMs1.setMinimum(1)
        self.MakroMs1.setMaximum(1000)
        self.MakroMs1.setTickInterval(1)
        self.MakroMs1.setTickPosition(QSlider.TicksBelow)
        self.MakroMs1.valueChanged.connect(self.MakroMs1ValueChanged)
        

        self.MakroMs2.setMinimum(1)
        self.MakroMs2.setMaximum(1000)
        self.MakroMs2.setTickInterval(1)
        self.MakroMs2.setTickPosition(QSlider.TicksBelow)
        self.MakroMs2.valueChanged.connect(self.MakroMs2ValueChanged)

        self.MakroMs3.setMinimum(1)
        self.MakroMs3.setMaximum(1000)
        self.MakroMs3.setTickInterval(1)
        self.MakroMs3.setTickPosition(QSlider.TicksBelow)
        self.MakroMs3.valueChanged.connect(self.MakroMs3ValueChanged)

        self.MakroMs4.setMinimum(1)
        self.MakroMs4.setMaximum(1000)
        self.MakroMs4.setTickInterval(1)
        self.MakroMs4.setTickPosition(QSlider.TicksBelow)
        self.MakroMs4.valueChanged.connect(self.MakroMs4ValueChanged)

        self.MakroMs5.setMinimum(1)
        self.MakroMs5.setMaximum(1000)
        self.MakroMs5.setTickInterval(1)
        self.MakroMs5.setTickPosition(QSlider.TicksBelow)
        self.MakroMs5.valueChanged.connect(self.MakroMs5ValueChanged)

        self.makrodevrekey = None
        self.makrodevreTusSifirla = QPushButton("Tuşu Sıfırla")
        self.makrodevreTusSecButton = QPushButton("Makro Başlat/Durdur Tuşu Seç")
        self.makrodevreTusSeciyor = 0
        self.makrodevreTusSecButton.clicked.connect(self.makrodevreTusSecButtonClick)

        self.page5_layout.addWidget(self.makrodevreTusSifirla)
        self.makrodevreTusSifirla.clicked.connect(self.makrodevreTusSifirlaClick)        
        self.page5_layout.addWidget(self.makrodevreTusSecButton)
        

        self.page5_layout.addWidget(self.MakroTusuCheckbox1)
        self.page5_layout.addWidget(self.MakroSurekliBas1)
        self.page5_layout.addWidget(self.MakroCombo1)
        self.MakroCombo1Key = None
        self.MakroCombo2Key = None
        self.MakroCombo3Key = None
        self.MakroCombo4Key = None
        self.MakroCombo5Key = None



        self.page5_layout.addWidget(self.MakroTusuText1)
        self.page5_layout.addWidget(self.lbl1)
        self.page5_layout.addWidget(self.MakroMs1)
        
        self.page5_layout.addWidget(self.MakroTusuCheckbox2)
        self.page5_layout.addWidget(self.MakroSurekliBas2)
        self.page5_layout.addWidget(self.MakroCombo2)
        self.page5_layout.addWidget(self.MakroTusuText2)
        self.page5_layout.addWidget(self.lbl2)
        self.page5_layout.addWidget(self.MakroMs2)
        
        self.page5_layout.addWidget(self.MakroTusuCheckbox3)
        self.page5_layout.addWidget(self.MakroSurekliBas3)
        self.page5_layout.addWidget(self.MakroCombo3)
        self.page5_layout.addWidget(self.MakroTusuText3)
        self.page5_layout.addWidget(self.lbl3)
        self.page5_layout.addWidget(self.MakroMs3)
        

        self.page5_layout.addWidget(self.MakroTusuCheckbox4)
        self.page5_layout.addWidget(self.MakroSurekliBas4)
        self.page5_layout.addWidget(self.MakroCombo4)
        self.page5_layout.addWidget(self.MakroTusuText4)
        self.page5_layout.addWidget(self.lbl4)
        self.page5_layout.addWidget(self.MakroMs4)
        
        self.page5_layout.addWidget(self.MakroTusuCheckbox5)
        self.page5_layout.addWidget(self.MakroSurekliBas5)
        self.page5_layout.addWidget(self.MakroCombo5)
        self.page5_layout.addWidget(self.MakroTusuText5)
        self.page5_layout.addWidget(self.lbl5)
        self.page5_layout.addWidget(self.MakroMs5)
        self.MakroCombo1.currentIndexChanged.connect(self.MakroCombo1Change)
        self.MakroCombo2.currentIndexChanged.connect(self.MakroCombo2Change)
        self.MakroCombo3.currentIndexChanged.connect(self.MakroCombo3Change)
        self.MakroCombo4.currentIndexChanged.connect(self.MakroCombo4Change)
        self.MakroCombo5.currentIndexChanged.connect(self.MakroCombo5Change)

        # TabWidget düzenini ekleyelim
        self.layout.addWidget(self.tab_widget)

        # Dış düzeni ana düzene ekleyelim
        self.layout.addLayout(external_layout)

        self.SilmeSeciyor = 0
        self.Silme = 0
        self.ciftElSeciyor = 0
        self.ciftElTus = None
        self.KalkanTus = None
        self.SilmeTusSeciyor = 0
        self.SilmeTus = None
        self.Esya1Kordinat = None
        self.Esya1Seciyor = 0
        self.Esya2Kordinat = None
        self.Esya2Seciyor = 0
        self.mouseContext = interception()
        self.mouse = 0
        for i in range(MAX_DEVICES):
            if interception.is_mouse(i):
                self.mouse = i
                break
        if (self.mouse == 0):
            print("Fare bulunamadı")
            exit(0)


        self.Envanter = 0
        self.Sol = 0
        self.SolKordinat = None
        self.KalkanSeciyor = 0
        self.KalkanTusSeciyor = 0
        self.KalkanKordinat = None
        self.CiftEleTusSeciyor = 0
        self.CiftEleTus = None
        self.EnvanterAcKapat = 0
        self.TekElEsyaSeciyor = 0
        self.TekElEsyaKordinat = None
        self.birkerebas = 0
        self.birkerebasliste = []
        self.skill_images = []  # Fotoğraf dosyalarını saklayacak liste
        # Pencerenin boyutunu ayarlama
        self.setGeometry(100, 100, 380, 500)
        self.start_key_listener()
    
    def AyarlariYukle(self):
        try:
            with open("config.conf", "r") as config_file:
                for line in config_file:
                    key, value = line.strip().split("=")
                    if key == "SilMs":
                        self.SilMs = float(value)
                    elif key == "SilmeTus":
                        self.SilmeTus = value
                    elif key == "EnvanterAcKapat":
                        self.EnvanterAcKapatCheckbox.setChecked(bool(int(value)))
                    elif key == "Envanter":
                        self.EnvanterCheckBox.setChecked(bool(int(value)))
                    elif key == "GizleKey":
                        self.GizleKey = value
                    elif key == "GizleText":
                        self.GizleButon.setText(value)
                    elif key == "BaslatKey":
                        self.BaslatKey = value
                    elif key == "BaslatText":
                        self.BaslatKeyButon.setText(value)
                    elif key == "CiftElTus":
                        self.ciftElTus = value
                    elif key == "CiftElText":
                        self.ciftElKalkan.setText(value)
                    elif key == "CiftEleTus":
                        self.CiftEleTus = value
                    elif key == "CiftEleButton":
                        self.CiftEleButton.setText(value)
                    elif key == "KalkanTus":
                        self.KalkanTus = value
                    elif key == "KalkanTusText":
                        self.selectKalkanKey.setText(value)
                    elif key == "HpKey":
                        self.HpCombo.setCurrentIndex(int(value))
                    elif key == "MpKey":
                        self.MpCombo.setCurrentIndex(int(value))
                    elif key == "HangiPotinput":
                        self.HangiPotinput.setText(value)
                    elif key == "MpPotInput":
                        self.MpPotinput.setText(value)
                    elif key == "Esya1KordinatText":
                        self.Esya1.setText(value)
                    elif key == "Esya2KordinatText":
                        self.Esya2.setText(value)
                    elif key == "SilSpeedText":
                        self.silSpeedLabel.setText(value)
                    elif key == "SilSpeedMs":
                        self.SilMs = int(value)
                    elif key == "KalkanSpeedText":
                        self.kalkanSpeedLabel.setText(value)
                    elif key == "KalkanSpeedMs":
                        self.KalkanMs = float(value)
                    elif key == "page3TekElKalkanTakCikar":
                        self.page3TekElCheckbox.setChecked(bool(int(value)))
                    elif key == "page3CiftElCheckbox":
                        self.page3CiftElCheckbox.setChecked(bool(int(value)))
                    elif key == "page3CiftElFuncCheckbox":
                        self.page3CiftElFuncCheckbox.setChecked(bool(int(value)))
                    elif key == "MakroTusuCheckbox1":
                        self.MakroTusuCheckbox1.setChecked(bool(int(value)))
                    elif key == "MakroTusuCheckbox2":
                        self.MakroTusuCheckbox2.setChecked(bool(int(value)))
                    elif key == "MakroTusuCheckbox3":
                        self.MakroTusuCheckbox3.setChecked(bool(int(value)))
                    elif key == "MakroTusuCheckbox4":
                        self.MakroTusuCheckbox4.setChecked(bool(int(value)))
                    elif key == "MakroTusuCheckbox5":
                        self.MakroTusuCheckbox5.setChecked(bool(int(value)))
                    elif key == "DebuffAcikCheckBox":
                        self.DebuffAcikCheckBox.setChecked(bool(int(value)))
                    elif key == "TormentCheckbox":
                        self.TormentCheckbox.setChecked(bool(int(value)))
                    elif key == "MaliceCheckbox":
                        self.MaliceCheckbox.setChecked(bool(int(value)))
                    elif key == "ParasiteCheckbox":
                        self.ParasiteCheckbox.setChecked(bool(int(value)))
                    elif key == "SuperiorCheckbox":
                        self.SuperiorCheckbox.setChecked(bool(int(value)))
                    elif key == "MassiveCheckbox":
                        self.MassiveCheckbox.setChecked(bool(int(value)))
                    elif key == "SubsideCheckbox":
                        self.SubsideCheckbox.setChecked(bool(int(value)))
                    elif key == "kerebbascheckbox":
                        self.kerebbascheckbox.setChecked(bool(int(value)))
                    elif key == "sefercheckbox":
                        self.sefercheckbox.setChecked(bool(int(value)))
                    elif key == "page4TekElKalkan":
                        self.page4TekElKalkan.setChecked(bool(int(value)))
                    elif key == "page4CiftElKalkan":
                        self.page4CiftElKalkan.setChecked(bool(int(value)))
                    elif key == "page4Sil":
                        self.page4Sil.setChecked(bool(int(value)))
                    elif key == "DebuffPotinput":
                        self.DebuffPotinput.setText(value)
                    elif key == "DebuffComboCurrentIndex":
                        self.DebuffCombo.setCurrentIndex(int(value))
                    elif key == "MakroDevreKey":
                        self.makrodevrekey = value
                    elif key == "MakroDevreText":
                        self.makrodevreTusSecButton.setText(value)
                    elif key == "MakroCombo1":
                        self.MakroCombo1.setCurrentIndex(int(value))
                    elif key == "MakroCombo2":
                        self.MakroCombo2.setCurrentIndex(int(value))
                    elif key == "MakroCombo3":
                        self.MakroCombo3.setCurrentIndex(int(value))
                    elif key == "MakroCombo4":
                        self.MakroCombo4.setCurrentIndex(int(value))
                    elif key == "MakroCombo5":
                        self.MakroCombo5.setCurrentIndex(int(value))
                    elif key == "MakroTusuText1":
                        self.MakroTusuText1.setText(value)
                    elif key == "MakroTusuText2":
                        self.MakroTusuText2.setText(value)
                    elif key == "MakroTusuText3":
                        self.MakroTusuText3.setText(value)
                    elif key == "MakroTusuText4":
                        self.MakroTusuText4.setText(value)
                    elif key == "MakroTusuText5":
                        self.MakroTusuText5.setText(value)
                    elif key == "MakroSurekliBas1":
                        self.MakroSurekliBas1.setChecked(bool(int(value)))
                    elif key == "MakroSurekliBas2":
                        self.MakroSurekliBas2.setChecked(bool(int(value)))
                    elif key == "MakroSurekliBas3":
                        self.MakroSurekliBas3.setChecked(bool(int(value)))
                    elif key == "MakroSurekliBas4":
                        self.MakroSurekliBas4.setChecked(bool(int(value)))
                    elif key == "MakroSurekliBas5":
                        self.MakroSurekliBas5.setChecked(bool(int(value)))
                    elif key == "MakroMs1":
                        self.MakroMs1.setValue(int(value))
                    elif key == "MakroMs2":
                        self.MakroMs2.setValue(int(value))
                    elif key == "MakroMs3":
                        self.MakroMs3.setValue(int(value))
                    elif key == "MakroMs4":
                        self.MakroMs4.setValue(int(value))
                    elif key == "MakroMs5":
                        self.MakroMs5.setValue(int(value))
        except Exception as e:
            print(str(e))
            QMessageBox.warning(self, "Uyarı", f"Ayarlar yüklenirken bir hata oluştu: {str(e)}")


    def AyarlariKaydets(self):
     try:
        with open("config.conf", "w") as config_file:
            config_file.write(f"SilMs={self.SilMs}\n")
            config_file.write(f"SilmeTus={self.SilmeTus}\n")
            config_file.write(f"EnvanterAcKapat={1 if self.EnvanterAcKapatCheckbox.isChecked() else 0}\n")
            config_file.write(f"Envanter={1 if self.EnvanterCheckBox.isChecked() else 0}\n")
            config_file.write(f"GizleKey={self.GizleKey}\n")
            config_file.write(f"GizleText={self.GizleButon.text()}\n")
            config_file.write(f"BaslatKey={self.BaslatKey}\n")
            config_file.write(f"BaslatText={self.BaslatKeyButon.text()}\n")
            config_file.write(f"CiftElTus={self.ciftElTus}\n")
            config_file.write(f"CiftElText={self.ciftElKalkan.text()}\n")
            config_file.write(f"CiftEleTus={self.CiftEleTus}\n")
            config_file.write(f"CiftEleButton={self.CiftEleButton.text()}\n")
            config_file.write(f"KalkanTus={self.KalkanTus}\n")
            config_file.write(f"KalkanTusText={self.selectKalkanKey.text()}\n")
            config_file.write(f"HpKey={self.HpCombo.currentIndex()}\n")
            config_file.write(f"MpKey={self.MpCombo.currentIndex()}\n")
            config_file.write(f"HangiPotinput={self.HangiPotinput.text()}\n")
            config_file.write(f"MpPotInput={self.MpPotinput.text()}\n")
            if self.KalkanKordinat is not None:
                config_file.write(f"KalkanKordinat.x={self.KalkanKordinat.x}\n")
                config_file.write(f"KalkanKordinat.y={self.KalkanKordinat.y}\n")
            if self.SolKordinat is not None:                
                config_file.write(f"SolElKordinat.x={self.SolKordinat.x}\n")
                config_file.write(f"SolElKordinat.y={self.SolKordinat.y}\n")
            config_file.write(f"SolElKordinatText={self.SolEl.text()}\n")
            if self.ciftelKalkanKordinat is not None:
              config_file.write(f"CifElKalkanKordinat.x={self.ciftelKalkanKordinat.x}\n")
              config_file.write(f"CifElKalkanKordinat.y={self.ciftelKalkanKordinat.y}\n")
            if self.Esya1Kordinat is not None:  
                config_file.write(f"Esya1Kordinat.x={self.Esya1Kordinat.x}\n")
                config_file.write(f"Esya1Kordinat.y={self.Esya1Kordinat.y}\n")
            if self.Esya2Kordinat is not None:
                config_file.write(f"Esya2Kordinat.x={self.Esya2Kordinat.x}\n")
                config_file.write(f"Esya2Kordinat.y={self.Esya2Kordinat.y}\n")
            config_file.write(f"Esya1KordinatText={self.Esya1.text()}\n"),
            config_file.write(f"Esya2KordinatText={self.Esya2.text()}\n")
            config_file.write(f"SilSpeedText={self.silSpeedLabel.text()}\n")
            config_file.write(f"SilSpeedMs={self.SilMs}\n")
            config_file.write(f"KalkanSpeedText={self.kalkanSpeedLabel.text()}\n")
            config_file.write(f"KalkanSpeedMs={self.KalkanMs}\n")
            config_file.write(f"page3TekElKalkanTakCikar={1 if self.page3TekElCheckbox.isChecked() else 0}\n")
            config_file.write(f"page3CiftElCheckbox={1 if self.page3CiftElCheckbox.isChecked() else 0}\n")
            config_file.write(f"page3CiftElFuncCheckbox={1 if self.page3CiftElFuncCheckbox.isChecked() else 0}\n")
            config_file.write(f"MakroTusuCheckbox1={1 if self.MakroTusuCheckbox1.isChecked() else 0}\n")
            config_file.write(f"MakroTusuCheckbox2={1 if self.MakroTusuCheckbox2.isChecked() else 0}\n")
            config_file.write(f"MakroTusuCheckbox3={1 if self.MakroTusuCheckbox3.isChecked() else 0}\n")
            config_file.write(f"MakroTusuCheckbox4={1 if self.MakroTusuCheckbox4.isChecked() else 0}\n")
            config_file.write(f"MakroTusuCheckbox5={1 if self.MakroTusuCheckbox5.isChecked() else 0}\n")
            config_file.write(f"DebuffAcikCheckBox={1 if self.DebuffAcikCheckBox.isChecked() else 0}\n")
            config_file.write(f"TormentCheckbox={1 if self.TormentCheckbox.isChecked() else 0}\n")
            config_file.write(f"MaliceCheckbox={1 if self.MaliceCheckbox.isChecked() else 0}\n")
            config_file.write(f"ParasiteCheckbox={1 if self.ParasiteCheckbox.isChecked() else 0}\n")
            config_file.write(f"SuperiorCheckbox={1 if self.SuperiorCheckbox.isChecked() else 0}\n")
            config_file.write(f"MassiveCheckbox={1 if self.MassiveCheckbox.isChecked() else 0}\n")
            config_file.write(f"SubsideCheckbox={1 if self.SubsideCheckbox.isChecked() else 0}\n")
            config_file.write(f"kerebbascheckbox={1 if self.kerebbascheckbox.isChecked() else 0}\n")
            config_file.write(f"sefercheckbox={1 if self.sefercheckbox.isChecked() else 0}\n")
            config_file.write(f"page4TekElKalkan={1 if self.page4TekElKalkan.isChecked() else 0}\n")
            config_file.write(f"page4CiftElKalkan={1 if self.page4CiftElKalkan.isChecked() else 0}\n")
            config_file.write(f"page4Sil={1 if self.page4Sil.isChecked() else 0}\n")
            config_file.write(f"DebuffPotinput={self.DebuffPotinput.text()}\n")
            config_file.write(f"DebuffComboCurrentIndex={self.DebuffCombo.currentIndex()}\n")
            config_file.write(f"MakroDevreKey={self.makrodevrekey}\n")
            config_file.write(f"MakroDevreText={self.makrodevreTusSecButton.text()}\n")
            config_file.write(f"MakroCombo1={self.MakroCombo1.currentIndex()}\n")
            config_file.write(f"MakroCombo2={self.MakroCombo2.currentIndex()}\n")
            config_file.write(f"MakroCombo3={self.MakroCombo3.currentIndex()}\n")
            config_file.write(f"MakroCombo4={self.MakroCombo4.currentIndex()}\n")
            config_file.write(f"MakroCombo5={self.MakroCombo5.currentIndex()}\n")
            config_file.write(f"MakroTusuText1={self.MakroTusuText1.text()}\n")
            config_file.write(f"MakroTusuText2={self.MakroTusuText2.text()}\n")
            config_file.write(f"MakroTusuText3={self.MakroTusuText3.text()}\n")
            config_file.write(f"MakroTusuText4={self.MakroTusuText4.text()}\n")
            config_file.write(f"MakroTusuText5={self.MakroTusuText5.text()}\n")
            config_file.write(f"MakroSurekliBas1={1 if self.MakroSurekliBas1.isChecked() else 0}\n")
            config_file.write(f"MakroSurekliBas2={1 if self.MakroSurekliBas2.isChecked() else 0}\n")
            config_file.write(f"MakroSurekliBas3={1 if self.MakroSurekliBas3.isChecked() else 0}\n")
            config_file.write(f"MakroSurekliBas4={1 if self.MakroSurekliBas4.isChecked() else 0}\n")
            config_file.write(f"MakroSurekliBas5={1 if self.MakroSurekliBas5.isChecked() else 0}\n")
            config_file.write(f"MakroMs1={self.MakroMs1.value()}\n")
            config_file.write(f"MakroMs2={self.MakroMs2.value()}\n")
            config_file.write(f"MakroMs3={self.MakroMs3.value()}\n")
            config_file.write(f"MakroMs4={self.MakroMs4.value()}\n")
            config_file.write(f"MakroMs5={self.MakroMs5.value()}\n")

        QMessageBox.information(self, "Bilgi", "Ayarlar başarıyla kaydedildi.")
     except Exception as e:
        print(str(e))
        QMessageBox.warning(self, "Uyarı", f"Ayarlar kaydedilirken bir hata oluştu: {str(e)}")



    def makrodevreTusSifirlaClick(self):
        self.makrodevrekey = None
        self.makrodevreTusSecButton.setText("Makro Başlat/Durdur Tuşu Seç")
    def makrodevreTusSecButtonClick(self):
        self.makrodevreTusSeciyor = 1
    def page3CiftElCheckboxChange(self, state):
        if self.ciftelKalkanKordinat is None:
                self.page3CiftElCheckbox.setChecked(False)
                QMessageBox.information(self, "Bilgi1", "Kalkan Tak/Çıkar sayfasından Kalkan kordinatı seçmeyi unutmayın.")
                return
        if self.page3CiftElCheckbox.isChecked():
            self.page3TekElCheckbox.setChecked(False)
        else:
            if self.KalkanKordinat is not None:
               self.page3TekElCheckbox.setChecked(True)


    def page3TekElCheckboxChange(self, state):
        if self.KalkanKordinat is None:
                self.page3TekElCheckbox.setChecked(False)
                QMessageBox.information(self, "Bilgi2", "Kalkan Tak/Çıkar sayfasından Kalkan kordinatı seçmeyi unutmayın.")
                return
        if self.page3TekElCheckbox.isChecked():
            self.page3CiftElCheckbox.setChecked(False)
        else:
            if self.ciftelKalkanKordinat is not None:
               self.page3CiftElCheckbox.setChecked(True)


    def MakroCombo1Change(self, index):
        if index == 0:
            self.MakroCombo1Key = None
        elif index == 1:
            self.MakroCombo1Key = Key.f1
        elif index == 2:
            self.MakroCombo1Key = Key.f2
        elif index == 3:
            self.MakroCombo1Key = Key.f3
        elif index == 4:
            self.MakroCombo1Key = Key.f4
        elif index == 5:
            self.MakroCombo1Key = Key.f5
        elif index == 6:
            self.MakroCombo1Key = Key.f6
        elif index == 7:
            self.MakroCombo1Key = Key.f7
        elif index == 8:
            self.MakroCombo1Key = Key.f8       
        
    def SpamMakroFChange(self, index):
        if index == 0:
            self.SpamMakroKey = None
        elif index == 1:
            self.SpamMakroKey = Key.f1
        elif index == 2:
            self.SpamMakroKey = Key.f2
        elif index == 3:
            self.SpamMakroKey = Key.f3
        elif index == 4:
            self.SpamMakroKey = Key.f4
        elif index == 5:
            self.SpamMakroKey = Key.f5
        elif index == 6:
            self.SpamMakroKey = Key.f6
        elif index == 7:
            self.SpamMakroKey = Key.f7
        elif index == 8:
            self.SpamMakroKey = Key.f8               

    def MakroCombo2Change(self, index):
        if index == 0:
            self.MakroCombo2Key = None
        elif index == 1:
            self.MakroCombo2Key = Key.f1
        elif index == 2:
            self.MakroCombo2Key = Key.f2
        elif index == 3:
            self.MakroCombo2Key = Key.f3
        elif index == 4:
            self.MakroCombo2Key = Key.f4
        elif index == 5:
            self.MakroCombo2Key = Key.f5
        elif index == 6:
            self.MakroCombo2Key = Key.f6
        elif index == 7:
            self.MakroCombo2Key = Key.f7
        elif index == 8:
            self.MakroCombo2Key = Key.f8        
    def MakroCombo3Change(self, index):
        if index == 0:
            self.MakroCombo3Key = None
        elif index == 1:
            self.MakroCombo3Key = Key.f1
        elif index == 2:
            self.MakroCombo3Key = Key.f2
        elif index == 3:
            self.MakroCombo3Key = Key.f3
        elif index == 4:
            self.MakroCombo3Key = Key.f4
        elif index == 5:
            self.MakroCombo3Key = Key.f5
        elif index == 6:
            self.MakroCombo3Key = Key.f6
        elif index == 7:
            self.MakroCombo3Key = Key.f7
        elif index == 8:
            self.MakroCombo3Key = Key.f8        
    def MakroCombo4Change(self, index):
        if index == 0:
            self.MakroCombo4Key = None
        elif index == 1:
            self.MakroCombo4Key = Key.f1
        elif index == 2:
            self.MakroCombo4Key = Key.f2
        elif index == 3:
            self.MakroCombo4Key = Key.f3
        elif index == 4:
            self.MakroCombo4Key = Key.f4
        elif index == 5:
            self.MakroCombo4Key = Key.f5
        elif index == 6:
            self.MakroCombo4Key = Key.f6
        elif index == 7:
            self.MakroCombo4Key = Key.f7
        elif index == 8:
            self.MakroCombo4Key = Key.f8        
    def MakroCombo5Change(self, index):
        if index == 0:
            self.MakroCombo5Key = None
        elif index == 1:
            self.MakroCombo5Key = Key.f1
        elif index == 2:
            self.MakroCombo5Key = Key.f2
        elif index == 3:
            self.MakroCombo5Key = Key.f3
        elif index == 4:
            self.MakroCombo5Key = Key.f4
        elif index == 5:
            self.MakroCombo5Key = Key.f5
        elif index == 6:
            self.MakroCombo5Key = Key.f6
        elif index == 7:
            self.MakroCombo5Key = Key.f7
        elif index == 8:
            self.MakroCombo5Key = Key.f8     


    def Makro1(self):
        if self.basladi == 0: return
        if self.MakroTusuCheckbox1.isChecked() and self.makrodevrede == 1:  
                time.sleep(self.MakroMss1)
                klavye = Controller()
                if self.MakroCombo1Key is not None:
                    klavye.press(self.MakroCombo1Key)
                    time.sleep(0.03)
                    klavye.release(self.MakroCombo1Key)
                for char in self.MakroTusuText1.text():
                    klavye.press(char)
                    klavye.release(char)
        if self.MakroSurekliBas1.isChecked():          
            Timer(0, self.Makro1).start()

    def Makro2(self):
        if self.basladi == 0: return
        if self.MakroTusuCheckbox2.isChecked() and self.makrodevrede == 1:
            
            time.sleep(self.MakroMss2)
            klavye = Controller()
            if self.MakroCombo1Key is not None:
                klavye.press(self.MakroCombo2Key)
                time.sleep(0.03)
                klavye.release(self.MakroCombo2Key)
            for char in self.MakroTusuText2.text():
                klavye.press(char)
                klavye.release(char)
        if self.MakroSurekliBas2.isChecked():          
            Timer(0, self.Makro2).start()
    def Makro3(self):
        if self.basladi == 0: return
        if self.MakroTusuCheckbox3.isChecked() and self.makrodevrede == 1:
            time.sleep(self.MakroMss3)
            klavye = Controller()
            if self.MakroCombo3Key is not None:
                klavye.press(self.MakroCombo3Key)
                time.sleep(0.03)
                klavye.release(self.MakroCombo3Key)
            for char in self.MakroTusuText3.text():
                klavye.press(char)
                klavye.release(char)
        if self.MakroSurekliBas3.isChecked():          
            Timer(0, self.Makro3).start()        
    def Makro4(self):
        if self.basladi == 0: return
        if self.MakroTusuCheckbox4.isChecked() and self.makrodevrede == 1:
            time.sleep(self.MakroMss4)
            klavye = Controller()
            if self.MakroCombo4Key is not None:
                klavye.press(self.MakroCombo4Key)
                time.sleep(0.03)
                klavye.release(self.MakroCombo4Key)
            for char in self.MakroTusuText4.text():
                klavye.press(char)
                klavye.release(char)
        if self.MakroSurekliBas4.isChecked():          
            Timer(0, self.Makro4).start()     
    def Makro5(self):
        if self.basladi == 0: return
        if self.MakroTusuCheckbox5.isChecked() and self.makrodevrede == 1:
            time.sleep(self.MakroMss5)
            klavye = Controller()
            if self.MakroCombo5Key is not None:
                klavye.press(self.MakroCombo5Key)
                time.sleep(0.03)
                klavye.release(self.MakroCombo5Key)
            for char in self.MakroTusuText5.text():
                klavye.press(char)
                klavye.release(char)
        if self.MakroSurekliBas5.isChecked():          
            Timer(0, self.Makro5).start()                        
    def IslemYap(self, text, mss, combo_key):
        klavye = Controller()
        if combo_key is not None:
        #    print(combo_key)
            klavye.press(combo_key)
            time.sleep(0.03)
            klavye.release(combo_key)
        for char in text:
            time.sleep(mss)
            klavye.press(char)
            
            klavye.release(char)
            
        print("islem bitti")
    def ciftelKalkanKordinatButonClicked(self):
        self.ciftelKalkanKordinatSeciyor = 1
    def ListeSifirlaButonClick(self):
        self.skill_images = []
        self.simdiki_foto = 0   
        Empty = QPixmap()
        self.label.setPixmap(Empty)
        QMessageBox.information(self,"Bilgi","Tüm skiller sıfırlandı.")
    def sonrakifoto(self):
        if self.simdiki_foto < len(self.skill_images) - 1:
            self.simdiki_foto += 1  
            self.foto_goster(self.skill_images[self.simdiki_foto])
        else:
            QMessageBox.warning(self, "Uyarı", "Daha fazla ileri yok.")

    def oncekifoto(self):
        if self.simdiki_foto > 0:
            self.simdiki_foto -= 1
            if self.skill_images:
                self.foto_goster(self.skill_images[self.simdiki_foto])
        else:
            QMessageBox.warning(self, "Uyarı", "Daha fazla geri yok.")
    def sefercheckboxChange(self, state):
        if state == QtCore.Qt.Checked:
            self.sefer = 1
            self.kerebbascheckbox.setChecked(False)
            self.birkerebas = 0
        else:   
            self.sefer = 0

            self.kerebbascheckbox.setChecked(True)
            self.birkerebas = 1
    def birkerebascheckboxchange(self, state):
      
        if state == QtCore.Qt.Checked:
            self.birkerebas = 1
            self.sefercheckbox.setChecked(False)
            self.sefer = 0
        else:
            self.birkerebas = 0
            self.sefercheckbox.setChecked(True)
            self.sefer = 1


    def foto_goster(self, pil_image):
        q_image = QImage(pil_image.tobytes(), pil_image.width, pil_image.height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.label.setPixmap(pixmap)
    def page4SilClicked(self):
        if self.skill_images == [] or self.HayaliAlancik is None:
                QMessageBox.warning(self,"Hata!","Skill veya Alan seçilmemiş.")
                self.page4Sil.setChecked(False)
                return                
    def page4SilChange(self, state):

        if state == QtCore.Qt.Checked:
                self.page4SilOnline = 1

        else:
            self.page4SilOnline = 0
    def BaslatKeyButonClicked(self):
        self.BaslatKeySeciyor = 1
    def DebuffAcikClicked(self):
        if self.HayaliAlancik is None:
                QMessageBox.warning(self,"Hata!","Önce 'Sil' sayfasından alan seçin.")
                self.DebuffAcikCheckBox.setChecked(False)
                return


    def DebuffAcikChange(self,state):
        if state == QtCore.Qt.Checked:
            self.DebuffOnline = 1
            if self.page4SilOnline == 1:
                thrdb = Thread(target=self.find_and_move_to_image)
                thrdb.start()
                                                # Klavye işlemleri
            klavye = Controller()
            print("Debuff tuşlarına basılıyor")
            if self.DebuffKey is not None:
                klavye.press(self.DebuffKey)
                time.sleep(0.03)
                klavye.release(self.DebuffKey)
                        
            for char in self.DebuffPotinput.text():
                            print("tusa basildi:", char)
                            klavye.press(char)
                            time.sleep(0.03)
                            klavye.release(char)
                        

            if self.page4TekElKalkanOnline == 1:
                            thrds = Thread(target=self.TekElKalkanTakCikar)
                            thrds.start()
                            #pyautogui.moveTo((location[0],location[1]))
            if self.page4CiftElKalkan.isChecked():
                            thrda = Thread(target=self.DigerTakCikar)
                            thrda.start()
     


        else:
            self.DebuffOnline = 0
    def GizleButonClicked(self):
        self.GizleSeciyor = 1
    def random_name(self,length=6):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length)) # 6 uzunlukta random Program ismi üretir.
    def page4TekElKalkanClicked(self):
        if self.KalkanKordinat is None:
                        #self.page4TekElKalkan.setChecked(False)
                        QMessageBox.information(self,"Bilgi","Kalkan Tak/Çıkar sayfasından Kalkan kordinatı seçmeyi unutmayın.")
                        self.page4TekElKalkan.setChecked(False)
                        return                 
    def page4TekElKalkanChange(self, state):    
        if state == QtCore.Qt.Checked:
            self.page4TekElKalkanOnline = 1
            self.page4CiftElKalkanOnline = 0
            self.page4CiftElKalkan.setChecked(False)
        else:
            self.page4TekElKalkanOnline = 0

    def page4CiftElKalkanChange(self, state):
        if state == QtCore.Qt.Checked:
            self.page4CiftlKalkanOnline = 1
            self.page4TekElKalkanOnline = 0 
            self.page4TekElKalkan.setChecked(False)
        else:
            self.page4TekElKalkanOnline = 1
            
    def page4CiftElKalkanClicked(self):
        if self.SolKordinat is None or self.ciftelKalkanKordinat is None:
                        #self.page4TekElKalkan.setChecked(False)
                        QMessageBox.information(self,"Bilgi","Sol El Kordinatı veya Kalkan Kordinatı alınmamış. Ayarlarınızı eksiksiz yapın.")
                        self.page4CiftElKalkan.setChecked(False)
                        return         
    def MpComboChange(self,index):
        if index == 0:
            self.MpKey = Key.f1
        elif index == 1:
            self.MpKey = Key.f2
        elif index == 2:
            self.MpKey = Key.f3
        elif index == 3:
            self.MpKey = Key.f4
        elif index == 4:
            self.MpKey = Key.f5
        elif index == 5:
            self.MpKey = Key.f6
        elif index == 6:
            self.MpKey = Key.f7
        elif index == 7:
            self.MpKey = Key.f8
            
            
    def TutBoxChange(self,state):
        if state == QtCore.Qt.Checked:
                        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
        self.show()

    def DebuffComboChange(self, index):
        if index == 0:
            self.DebuffKey = None
        elif index == 1:
            self.DebuffKey = Key.f1
        elif index == 2:
            self.DebuffKey = Key.f2
        elif index == 3:
            self.DebuffKey = Key.f3
        elif index == 4:
            self.DebuffKey = Key.f4
        elif index == 5:
            self.DebuffKey = Key.f5
        elif index == 6:
            self.DebuffKey = Key.f6
        elif index == 7:
            self.DebuffKey = Key.f7
        elif index == 8:
            self.DebuffKey = Key.f8
            
            
    def HpComboChange(self, index):
        if index == 0:
            self.HpKey = Key.f1
        elif index == 1:
            self.HpKey = Key.f2
        elif index == 2:
            self.HpKey = Key.f3
        elif index == 3:
            self.HpKey = Key.f4
        elif index == 4:
            self.HpKey = Key.f5
        elif index == 5:
            self.HpKey = Key.f6
        elif index == 6:
            self.HpKey = Key.f7
        elif index == 7:
            self.HpKey = Key.f8
    def MpFunc(self):
        if self.basladi == 0: return
        if self.Mp == 0 or self.MpKordinat is None: return
        
        try:
            x,y = self.MpKordinat
            pixel_color = self.get_pixel(x,y)
            print(pixel_color)
            if pixel_color is None:
                if self.page3CiftElCheckbox.isChecked():
                    thrd = Thread(target=self.DigerTakCikar)
                    thrd.start()
                if self.page3TekElCheckbox.isChecked():
                    thrd1 = Thread(target=self.TekElKalkanTakCikar)
                    thrd1.start()
                klavye = Controller()
                klavye.press(self.MpKey)
                time.sleep(0.03)
                klavye.release(self.MpKey)
                for char in self.MpPotinput.text():
                    klavye.press(char)
                    time.sleep(0.03)
                    klavye.release(char)
                print("agaa")
        except Exception as e:
            print("Hata Mp Func",e)
            
       # MpFunc = Thread(target=self.MpFunc)
        #MpFunc.start()
        if self.HpCheckBox.isChecked():
                    HpFunc = Thread(target=self.HpFunc)
                    HpFunc.start()
        else:
                    MpFunc = Thread(target=self.MpFunc)
                    MpFunc.start()

    def MakroHpFunc(self):
        if self.basladi == 0: return
        if self.HpMakro == 0 or self.MakroHpKordinat is None: return 
        x,y = self.MakroHpKordinat
        pixel_color = self.get_pixel(x,y)
        klavye = Controller()   
            #print(pixel_color)
        if pixel_color is None:
            
                    if self.SpamMakroKey is not None:                                  
                        klavye.press(self.SpamMakroKey)
                        time.sleep(0.03)
                        klavye.release(self.SpamMakroKey)
                    for char in self.SpamMakro1.text():
                        time.sleep(float(self.SpamMakroMs1.text())) 
                        klavye.press(char)
                        time.sleep(0.03)
                        klavye.release(char)
                    for char in self.SpamMakro2.text():
                        time.sleep(float(self.SpamMakroMs2.text())) 
                        klavye.press(char)
                        time.sleep(0.03)
                        klavye.release(char)   
                    for char in self.SpamMakro3.text():
                        time.sleep(float(self.SpamMakroMs3.text())) 
                        klavye.press(char)
                        time.sleep(0.03)
                        klavye.release(char)    
        else:
                thrd = Thread(target=self.MakroHpFunc)
                thrd.start()                                                                      
        
        
    def MakroMpFunc(self):
        if self.basladi == 0: return
        if self.MpMakro == 0 or self.MakroMpKordinat is None: return 
        try:
            x,y = self.MakroMpKordinat
            pixel_color = self.get_pixel(x,y)
            if pixel_color is None:
                    if self.SpamSurekliCheckbox.isChecked():
                        klavye = Controller()                                       
                        klavye.press(self.SpamMakroKey)
                        time.sleep(0.03)
                        klavye.release(self.SpamMakroKey)

                        for char in self.SpamMakro1.text():
                            klavye.press(char)
                            time.sleep(0.03)
                            klavye.release(char)
                        for char in self.SpamMakro2.text():
                            klavye.press(char)
                            time.sleep(0.03)
                            klavye.release(char)   
                        for char in self.SpamMakro3.text():
                            klavye.press(char)
                            time.sleep(0.03)
                            klavye.release(char)   
                    else:
                        klavye = Controller()                                       
                        klavye.press(self.SpamMakroKey)
                        time.sleep(0.03)
                        klavye.release(self.SpamMakroKey)

                        for char in self.SpamMakro1.text():
                            klavye.press(char)
                            time.sleep(0.03)
                            klavye.release(char)
                        for char in self.SpamMakro2.text():
                            klavye.press(char)
                            time.sleep(0.03)
                            klavye.release(char)   
                        for char in self.SpamMakro3.text():
                            klavye.press(char)
                            time.sleep(0.03)
                            klavye.release(char)   
                            thrd = Thread(target=self.MakroMpFunc)
                            thrd.start()
            else:
                thrd = Thread(target=self.MakroMpFunc)
                thrd.start()
        except Exception as e:
            print("Hata: MakroMpFunc")  
            
    def HpFunc(self):
        if self.basladi == 0: return
        if self.Hp == 0 or self.HpKordinat is None: return
        try:
            x,y = self.HpKordinat
            pixel_color = self.get_pixel(x,y)
            if pixel_color is None:
                if self.page3CiftElCheckbox.isChecked():
                    thrd = Thread(target=self.DigerTakCikar)
                    thrd.start()
                if self.page3TekElCheckbox.isChecked():
                    thrd1 = Thread(target=self.TekElKalkanTakCikar)
                    thrd1.start()
                if self.page3CiftElFuncCheckbox.isChecked():
                    thrd2 = Thread(target=self.find_and_move_to_image)
                    thrd2.start()
                    
                klavye = Controller()
                klavye.press(self.HpKey)
                time.sleep(0.03)
                klavye.release(self.HpKey)
                for char in self.HangiPotinput.text():
                    klavye.press(char)
                    time.sleep(0.03)
                    klavye.release(char)
                print("agaass")
        except Exception as e:
            print("Hata Hp Func",e)
            
        if self.MpCheckBox.isChecked():
                    MpFunc = Thread(target=self.MpFunc)
                    MpFunc.start()
        else:
                    HpFunc = Thread(target=self.HpFunc)
                    HpFunc.start()
                    
    def HpCheckBoxChange(self,state):
        if state == QtCore.Qt.Checked:
            self.Hp = 1
            QMessageBox.information(self,"Bilgi","Sınır belirlemek için CTRL basın.")
        else:
            self.Hp = 0
            self.HpCheckBox.setText("OTO-HP Açık/Kapalı")
            self.HpKordinat = None
    def MakroHpChange(self, state):
        if state == QtCore.Qt.Checked:
            self.HpMakro = 1
            QMessageBox.information(self,"Bilgi","Sınır belirlemek için CTRL basın.")     
        else:
            self.HpMakro = 0
            self.SpamHpCheckbox.setText("OTO-HP Makro Açık/Kapalı")       
            self.MakroHpKordinat = None
    def MakroMpChange(self, state):
        if state == QtCore.Qt.Checked:
            self.MpMakro = 1
            QMessageBox.information(self,"Bilgi","Sınır belirlemek için CTRL basın.")     
        else:
            self.MpMakro = 0
            self.SpamHpCheckbox.setText("OTO-HP Makro Açık/Kapalı")       
            self.MakroMpKordinat = None            
    def TormentCheckboxchange(self,state):
        if state == QtCore.Qt.Checked:
            self.Torment = 1
            self.DebuffList.append("torment.png")
        else:
            self.Torment = 0
            self.DebuffList.remove("torment.png")
            
    def MaliceCheckboxchange(self,state):
        if state == QtCore.Qt.Checked:
            self.Malice = 1
            self.DebuffList.append("malice.png")
        else:
            self.Malice = 0
            self.DebuffList.remove("malice.png")
            
    def ParasiteCheckboxchange(self,state):
        if state == QtCore.Qt.Checked:
            self.Parasite = 1
            self.DebuffList.append("parasite.png")
        else:
            self.Parasite = 0
            self.DebuffList.remove("parasite.png")
            
    def SuperiorCheckboxchange(self,state):
        if state == QtCore.Qt.Checked:
            self.Superior = 1
            self.DebuffList.append("superior.png")
        else:
            self.Superior = 0   
            self.DebuffList.remove("superior.png")
            
    def MassiveCheckboxchange(self,state):
        if state == QtCore.Qt.Checked:
            self.Massive = 1
            self.DebuffList.append("massive.png")
        else:
            self.Massive = 0   
            self.DebuffList.remove("massive.png")
            
            
    def SubsideCheckboxchange(self,state):
        if state == QtCore.Qt.Checked:
            self.Subside = 1
            self.DebuffList.append("subside.png")
        else:
            self.Subside = 0   
            self.DebuffList.remove("subside.png")
            
            
            
            
                  
            
            
            
            
            
            
            
            
            
    def MpCheckBoxChange(self,state):
        if state == QtCore.Qt.Checked:
            self.Mp = 1
            QMessageBox.information(self,"Bilgi","Sınır belirlemek için CTRL basın.")
        else:
            self.Mp = 0
            self.MpCheckBox.setText("OTO-MP Açık/Kapalı")
            self.MpKordinat = None
            
            
    def MakroMs1ValueChanged(self):
            value = self.MakroMs1.value()
            ms = (value / 1000)
            self.lbl1.setText(f"MS: {value}")
            self.MakroMss1 = ms
    def MakroMs2ValueChanged(self):
            value = self.MakroMs2.value()
            ms = (value / 1000)
            self.lbl2.setText(f"MS: {value}")
            self.MakroMss2 = ms
    def MakroMs3ValueChanged(self):
            value = self.MakroMs3.value()
            ms = (value / 1000)
            self.lbl3.setText(f"MS: {value}")
            self.MakroMss3 = ms
    def MakroMs4ValueChanged(self):
            value = self.MakroMs4.value()
            ms = (value / 1000)
            self.lbl4.setText(f"MS: {value}")
            self.MakroMss4 = ms
    def MakroMs5ValueChanged(self):
            value = self.MakroMs5.value()
            ms = (value / 1000)
            self.lbl5.setText(f"MS: {value}")
            self.MakroMss5 = ms


            
    def sliderValueChanged(self):
        value = self.slider.value()
        ms = (value / 1000)
        self.silSpeedLabel.setText(f"Silme HIZ: {value}")
        self.SilMs = ms
        print(ms)
    def kalkanSliderChanged(self):
        value = self.kalkanSlider.value()
        ms = (value / 1000)
        self.kalkanSpeedLabel.setText(f"Kalkan HIZ: {value}")
        self.KalkanMs = ms
        print(ms)
        
    def CiftEleTusSifirlaClick(self):
        self.CiftEleTus = None
        self.CiftEleButton.setText("Çift El Tuşu")




    def CiftEleButtonClicked(self):
        if not self.SolEl.isChecked():
           QMessageBox.information(self,"Bilgi","Aşşağıdan 'Sol El' i tikleyip Sol El kordinatı almayı unutmayın")
        self.CiftEleTusSeciyor = 1
    def Esya1Clicked(self):   
        if not self.SolEl.isChecked():
           QMessageBox.information(self,"Bilgi","Aşşağıdan 'Sol El' i tikleyip Sol El kordinatı almayı unutmayın")
        self.Esya1Seciyor = 1
    
    def Esya2Clicked(self):  
        if not self.SolEl.isChecked():
           QMessageBox.information(self,"Bilgi","Aşşağıdan 'Sol El' i tikleyip Sol El kordinatı almayı unutmayın")
        self.Esya2Seciyor = 1
        
    def ciftElKalkanClicked(self):
        if not self.SolEl.isChecked():
           QMessageBox.information(self,"Bilgi","Aşşağıdan 'Sol El' i tikleyip Sol El kordinatı almayı unutmayın")
        self.ciftElSeciyor = 1
        
    def SilmeChange(self,state):
        if state == QtCore.Qt.Checked:
            self.Silme = 1
  
        else:
            self.Silme = 0
    def OtomatikCheckBoxChange(self,state):
        if state == QtCore.Qt.Checked:
            self.Otomatik = 1


        else:
            self.Otomatik = 0
    def KalkanKeyClicked(self):
        self.KalkanTusSeciyor = 1

    def kalkanTusSifirlaClick(self):
            self.KalkanTus = None
            self.selectKalkanKey.setText("Tuş Seç")

    def ciftelkalkantussifirlaClick(self):
            self.ciftElTus = None
            self.ciftElKalkan.setText("Çift El Kalkan Tuş")

    def EnvanterAcKapatClicked(self,state):
        if state == QtCore.Qt.Checked:
            self.EnvanterAcKapat = 1
            self.Envanter = 0
            self.EnvanterCheckBox.setChecked(False)
        else:
            self.EnvanterAcKapat = 0
            self.Envanter = 1
            self.EnvanterCheckBox.setChecked(True)
    def EnvanterCheckBoxChange(self,state):
        if state == QtCore.Qt.Checked:
            self.Envanter = 1
            self.EnvanterAcKapat = 0
            self.EnvanterAcKapatCheckbox.setChecked(False)
        else:
            self.Envanter = 0
            self.EnvanterAcKapat = 1
            self.EnvanterAcKapatCheckbox.setChecked(True)
        """ 
                (25, 25, 25),
                (39, 39, 39),
                (51, 51, 51),
                (51, 51, 51),
                (39, 39, 39),
                (25, 25, 25),
                (63, 124, 173), (62, 123, 172), (62, 122, 171), (61, 121, 170), (60, 120, 169), (59, 119, 168), (63, 122, 169), (117, 159, 193), (182, 204, 222), (223, 232, 240), (239, 244, 248), (241, 245, 248), (240, 245, 248), (242, 246, 249), (253, 254, 254), (255, 255, 255), (255, 254, 251), (255, 246, 202), (255, 230, 117), (62, 123, 171), (61, 122, 170), (59, 120, 168), (98, 146, 185), (221, 231, 240), (254, 254, 255), (255, 254, 250), (255, 252, 237), (255, 250, 226), (255, 250, 224), (255, 250, 223), (255, 249, 221), (255, 247, 209), (255, 241, 176), (255, 231, 121), (255, 228, 103), (255, 227, 101), (61, 122, 171), (60, 121, 169), (60, 120, 168), (116, 158, 193), (247, 249, 251), (255, 255, 253), (255, 245, 194), (255, 235, 133), (255, 232, 117), (255, 232, 115), (255, 231, 113), (255, 231, 111), (255, 230, 110), (255, 230, 108), (255, 229, 107), (255, 228, 105), (255, 227, 102), (255, 227, 100), (255, 226, 98), (95, 144, 183), (246, 249, 251), (255, 253, 243), (255, 238, 150), (255, 232, 114), (255, 230, 109), (255, 229, 108), (255, 229, 106), (255, 228, 104), (255, 226, 99), (255, 225, 96), (60, 121, 170), (66, 124, 171), (255, 237, 147), (255, 231, 112), (255, 229, 105), (255, 226, 97), (255, 225, 95), (255, 224, 93), (254, 255, 255), (255, 246, 197), (255, 224, 91), (58, 118, 167), (190, 210, 226), (255, 236, 137), (255, 230, 111), (255, 225, 94), (255, 224, 92), (255, 223, 91), (255, 223, 89), (59, 118, 166), (255, 252, 239), (255, 225, 97), (255, 223, 90), (255, 223, 88), (255, 222, 87), (58, 118, 166), (65, 122, 168), (248, 250, 252), (255, 222, 88), (255, 222, 86), (255, 221, 84), (57, 117, 165), (66, 122, 168), (255, 250, 222), (255, 224, 94), (255, 221, 85), (255, 220, 82), (56, 116, 164), (65, 121, 167), (255, 221, 83), (255, 220, 81), (255, 219, 80), (56, 115, 163), (64, 121, 166), (255, 219, 79), (255, 219, 77), (55, 114, 162), (64, 120, 165), (255, 220, 80), (255, 219, 78), (255, 218, 77), (255, 218, 75), (54, 113, 161), (63, 119, 165), (255, 228, 102), (255, 220, 83), (255, 218, 76), (255, 218, 74), (255, 217, 73), (68, 122, 167), (76, 128, 170), (249, 250, 252), (255, 249, 222), (255, 224, 95), (255, 225, 100), (255, 224, 99), (255, 224, 97), (255, 223, 96), (255, 222, 94), (255, 222, 92), (255, 222, 91), (255, 221, 90), (255, 220, 88), (255, 220, 86), (255, 219, 85), (255, 219, 83), (255, 236, 160), (255, 249, 220), (255, 231, 134), (255, 244, 197), (255, 243, 197), (255, 243, 196), (255, 243, 195), (255, 242, 194), (255, 242, 193), (255, 242, 192), (255, 241, 192), (255, 241, 191), (255, 217, 72), (255, 216, 70), (255, 215, 68), (255, 215, 67), (255, 214, 65), (255, 214, 63), (246, 246, 246), (255, 249, 219), (255, 217, 74), (255, 216, 71), (255, 215, 66), (255, 214, 64), (255, 213, 63), (255, 213, 61), (255, 248, 219), (255, 215, 69), (255, 213, 62), (255, 213, 60), (255, 212, 59), (255, 248, 218), (255, 220, 92), (255, 243, 198), (255, 248, 223), (255, 233, 154), (255, 216, 69), (255, 217, 76), (255, 250, 232), (255, 233, 153), (255, 249, 223), (255, 223, 108), (255, 255, 254), (255, 248, 225), (254, 254, 254), (255, 254, 248), (255, 220, 95), (255, 254, 253), (255, 245, 208), (101, 101, 101), (200, 200, 200), (255, 234, 148), (255, 214, 66), (255, 212, 60), (255, 238, 179), (255, 252, 242), (255, 222, 105), (145, 145, 145), (255, 251, 234), (255, 212, 61), (255, 222, 104), (255, 228, 131), (255, 216, 77), (255, 215, 71), (104, 104, 104), (224, 224, 224), (255, 248, 222), (255, 214, 70), (255, 243, 202), (229, 243, 255), (233, 245, 255), (253, 254, 255), (255, 252, 240), (255, 232, 142), (255, 225, 116), (235, 246, 255), (255, 250, 230), (255, 233, 151), (255, 221, 94), (255, 216, 72), (255, 217, 81), (255, 229, 137), (251, 253, 255), (255, 249, 227), (255, 239, 180), (255, 229, 134), (255, 221, 101), (255, 216, 76), (255, 213, 64), (255, 221, 99), (255, 238, 176), (255, 249, 226), (255, 254, 249),
                (0, 0, 0)]: # Boş slotların pixel renkleri.
        """
    def get_pixel(self,x,y):
        pixel_color = pyautogui.pixel(int(x), int(y))
        if pixel_color not in [(13, 13, 13),
            (25, 25, 25),
            (39, 39, 39),
            (51, 51, 51),
            (51, 51, 51),
            (39, 39, 39),
            (25, 25, 25),
            (63, 124, 173), (62, 123, 172), (62, 122, 171), (61, 121, 170), (60, 120, 169), (59, 119, 168), (63, 122, 169), (117, 159, 193), (182, 204, 222), (223, 232, 240), (239, 244, 248), (241, 245, 248), (240, 245, 248), (242, 246, 249), (253, 254, 254), (255, 255, 255), (255, 254, 251), (255, 246, 202), (255, 230, 117), (62, 123, 171), (61, 122, 170), (59, 120, 168), (98, 146, 185), (221, 231, 240), (254, 254, 255), (255, 254, 250), (255, 252, 237), (255, 250, 226), (255, 250, 224), (255, 250, 223), (255, 249, 221), (255, 247, 209), (255, 241, 176), (255, 231, 121), (255, 228, 103), (255, 227, 101), (61, 122, 171), (60, 121, 169), (60, 120, 168), (116, 158, 193), (247, 249, 251), (255, 255, 253), (255, 245, 194), (255, 235, 133), (255, 232, 117), (255, 232, 115), (255, 231, 113), (255, 231, 111), (255, 230, 110), (255, 230, 108), (255, 229, 107), (255, 228, 105), (255, 227, 102), (255, 227, 100), (255, 226, 98), (95, 144, 183), (246, 249, 251), (255, 253, 243), (255, 238, 150), (255, 232, 114), (255, 230, 109), (255, 229, 108), (255, 229, 106), (255, 228, 104), (255, 226, 99), (255, 225, 96), (60, 121, 170), (66, 124, 171), (255, 237, 147), (255, 231, 112), (255, 229, 105), (255, 226, 97), (255, 225, 95), (255, 224, 93), (254, 255, 255), (255, 246, 197), (255, 224, 91), (58, 118, 167), (190, 210, 226), (255, 236, 137), (255, 230, 111), (255, 225, 94), (255, 224, 92), (255, 223, 91), (255, 223, 89), (59, 118, 166), (255, 252, 239), (255, 225, 97), (255, 223, 90), (255, 223, 88), (255, 222, 87), (58, 118, 166), (65, 122, 168), (248, 250, 252), (255, 222, 88), (255, 222, 86), (255, 221, 84), (57, 117, 165), (66, 122, 168), (255, 250, 222), (255, 224, 94), (255, 221, 85), (255, 220, 82), (56, 116, 164), (65, 121, 167), (255, 221, 83), (255, 220, 81), (255, 219, 80), (56, 115, 163), (64, 121, 166), (255, 219, 79), (255, 219, 77), (55, 114, 162), (64, 120, 165), (255, 220, 80), (255, 219, 78), (255, 218, 77), (255, 218, 75), (54, 113, 161), (63, 119, 165), (255, 228, 102), (255, 220, 83), (255, 218, 76), (255, 218, 74), (255, 217, 73), (68, 122, 167), (76, 128, 170), (249, 250, 252), (255, 249, 222), (255, 224, 95), (255, 225, 100), (255, 224, 99), (255, 224, 97), (255, 223, 96), (255, 222, 94), (255, 222, 92), (255, 222, 91), (255, 221, 90), (255, 220, 88), (255, 220, 86), (255, 219, 85), (255, 219, 83), (255, 236, 160), (255, 249, 220), (255, 231, 134), (255, 244, 197), (255, 243, 197), (255, 243, 196), (255, 243, 195), (255, 242, 194), (255, 242, 193), (255, 242, 192), (255, 241, 192), (255, 241, 191), (255, 217, 72), (255, 216, 70), (255, 215, 68), (255, 215, 67), (255, 214, 65), (255, 214, 63), (246, 246, 246), (255, 249, 219), (255, 217, 74), (255, 216, 71), (255, 215, 66), (255, 214, 64), (255, 213, 63), (255, 213, 61), (255, 248, 219), (255, 215, 69), (255, 213, 62), (255, 213, 60), (255, 212, 59), (255, 248, 218), (255, 220, 92), (255, 243, 198), (255, 248, 223), (255, 233, 154), (255, 216, 69), (255, 217, 76), (255, 250, 232), (255, 233, 153), (255, 249, 223), (255, 223, 108), (255, 255, 254), (255, 248, 225), (254, 254, 254), (255, 254, 248), (255, 220, 95), (255, 254, 253), (255, 245, 208), (101, 101, 101), (200, 200, 200), (255, 234, 148), (255, 214, 66), (255, 212, 60), (255, 238, 179), (255, 252, 242), (255, 222, 105), (145, 145, 145), (255, 251, 234), (255, 212, 61), (255, 222, 104), (255, 228, 131), (255, 216, 77), (255, 215, 71), (104, 104, 104), (224, 224, 224), (255, 248, 222), (255, 214, 70), (255, 243, 202), (229, 243, 255), (233, 245, 255), (253, 254, 255), (255, 252, 240), (255, 232, 142), (255, 225, 116), (235, 246, 255), (255, 250, 230), (255, 233, 151), (255, 221, 94), (255, 216, 72), (255, 217, 81), (255, 229, 137), (251, 253, 255), (255, 249, 227), (255, 239, 180), (255, 229, 134), (255, 221, 101), (255, 216, 76), (255, 213, 64), (255, 221, 99), (255, 238, 176), (255, 249, 226), (255, 254, 249),
            (0, 0, 0)]: # Boş slotların pixel renkleri.

            return pixel_color
        return None
    def SolTut(self):
        mstroke_down = mouse_stroke(interception_mouse_state.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN.value,
                                    interception_mouse_flag.INTERCEPTION_MOUSE_MOVE_RELATIVE.value,
                                    0,
                                    0,
                                    0,
                                    0)
        self.mouseContext.send(self.mouse, mstroke_down)  # Fare vuruşunu gönderiyoruz, sağ click basıldı


    def SolBirak(self):
        mstroke_up = mouse_stroke(interception_mouse_state.INTERCEPTION_MOUSE_LEFT_BUTTON_UP.value,
                                  interception_mouse_flag.INTERCEPTION_MOUSE_MOVE_RELATIVE.value,
                                  0,
                                  0,
                                  0,
                                  0)

        self.mouseContext.send(self.mouse, mstroke_up)  # Fare vuruşunu gönderiyoruz, sağ  click bırakıldı 
    def SagClick(self):
        mstroke_down = mouse_stroke(interception_mouse_state.INTERCEPTION_MOUSE_RIGHT_BUTTON_DOWN.value,
                                    interception_mouse_flag.INTERCEPTION_MOUSE_MOVE_RELATIVE.value,
                                    0,
                                    0,
                                    0,
                                    0)
        self.mouseContext.send(self.mouse, mstroke_down)  # Fare vuruşunu gönderiyoruz, sağ click basıldı
        time.sleep(0.02)
        mstroke_up = mouse_stroke(interception_mouse_state.INTERCEPTION_MOUSE_RIGHT_BUTTON_UP.value,
                                  interception_mouse_flag.INTERCEPTION_MOUSE_MOVE_RELATIVE.value,
                                  0,
                                  0,
                                  0,
                                  0)

        self.mouseContext.send(self.mouse, mstroke_up)  # Fare vuruşunu gönderiyoruz, sağ  click bırakıldı 
      
    def SolClick(self):
        mstroke_down = mouse_stroke(interception_mouse_state.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN.value,
                                    interception_mouse_flag.INTERCEPTION_MOUSE_MOVE_RELATIVE.value,
                                    0,
                                    0,
                                    0,
                                    0)
        self.mouseContext.send(self.mouse, mstroke_down)  # Fare vuruşunu gönderiyoruz, sol düğme basıldı
        time.sleep(0.02)
   
        mstroke_up = mouse_stroke(interception_mouse_state.INTERCEPTION_MOUSE_LEFT_BUTTON_UP.value,
                                  interception_mouse_flag.INTERCEPTION_MOUSE_MOVE_RELATIVE.value,
                                  0,
                                  0,
                                  0,
                                  0)
        self.mouseContext.send(self.mouse, mstroke_up)  # Fare vuruşunu gönderiyoruz, sol düğme bırakıldı

    def FuncBaslat(self):
        if self.HpKordinat is not None:
                    HpFunc = Thread(target=self.HpFunc)
                    HpFunc.start()

        if self.SpamHpCheckbox.isChecked():
            MakroHpFunc = Thread(target=self.MakroHpFunc)
            MakroHpFunc.start()
        
        if self.SpamMpCheckbox.isChecked():
            MakroMpFunc = Thread(target=self.MakroMpFunc)
            MakroMpFunc.start()


        if self.MpKordinat is not None:
                    MpFunc = Thread(target=self.MpFunc)
                    MpFunc.start()  
        if self.makrodevrede == 1:
            thrid = Thread(target=self.MakroFunc)
            thrid.start()
        if self.DebuffOnline == 1:
            debufthrd = Thread(target=self.DebuffTepki)
            debufthrd.start()    
        if self.Silme == 1 and self.Otomatik == 1:
            thrd = Thread(target=self.find_and_move_to_image)
            thrd.start()      

    def MakroFunc(self):
                if self.makrodevrede == 1 and self.basladi == 1:
                    if self.MakroTusuCheckbox1.isChecked():
                        thrd1 = Thread(target=self.Makro1)
                        thrd1.start()
                    if self.MakroTusuCheckbox2.isChecked():
                        thrd2 = Thread(target=self.Makro2)
                        thrd2.start() 
                    if self.MakroTusuCheckbox3.isChecked():                   
                        thrd3 = Thread(target=self.Makro3)
                        thrd3.start()
                    if self.MakroTusuCheckbox4.isChecked():    
                        thrd4 = Thread(target=self.Makro4)
                        thrd4.start()
                    if self.MakroTusuCheckbox5.isChecked():    
                        thrd5 = Thread(target=self.Makro5)
                        thrd5.start()                                                                           
    def key_listener_thread(self):
        def on_press(key):
            if key == Key.ctrl_l:
                if self.Sol == 1:
                    self.Sol = 0
                    self.SolKordinat = pyautogui.position()
                    self.SolEl.setText("Sol El [KORDİNAT SEÇİLDİ]")
                    print(self.SolKordinat)
                
                elif self.SilmeSeciyor == 1:
                    self.capture_skill()
                    self.SilmeSeciyor = 0
                elif self.ciftelKalkanKordinatSeciyor == 1:
                    self.ciftelKalkanKordinat = pyautogui.position()
                    print("Cift el kalkan kordinat belirlendi.")
                    self.ciftelKalkanKordinatButon.setText("Kalkan Kordinat Seç [Kordinat Seçildi]")
                    self.ciftelKalkanKordinatSeciyor = 0
                elif self.KalkanSeciyor == 1:
                    self.KalkanKordinat = pyautogui.position()
                    print("Kalkan kordinatı belirlendi.")
                    self.KalkanButton.setText("Kalkan Kordinat Seç [Kordinat Seçildi]")
                    self.KalkanSeciyor = 0
                elif self.Esya1Seciyor == 1:
                    self.Esya1Kordinat = pyautogui.position()
                    self.Esya1Seciyor = 0
                    self.Esya1.setText("Sağ El İtem Kordinat [Kordinat Seçildi]")
                    
                elif self.Esya2Seciyor == 1:
                    self.Esya2Kordinat = pyautogui.position()
                    self.Esya2Seciyor = 0
                    self.Esya2.setText("Sol El İtem Kordinat [Kordinat Alındı]")
                elif self.HpMakro == 1 and self.MakroHpKordinat is None:
                    ilkkordinat = pyautogui.position()
                    renk = ImageGrab.grab().getpixel(ilkkordinat)
                    print(renk)
                    while renk == (0,0,0) or renk == (14,14,14) or renk == (153,153,154 ) or renk == (255,255,255) or renk == (221,221,221) or renk == (102,102,102) or renk == (51,51,51) or renk == (153,153,153) or renk == (187, 187, 187):
                    #while renk == (255,255,255) or renk == (103,103,102) or renk == (2,1,2) or renk == (3,0,0) or renk == (3,2,0) or renk == (154,153,153) or  renk == (54,53,54) or renk ==(3,2,1) or renk == (2,0,0) or renk == (1,1,1) or renk == (2,1,1) or renk == (139,102,102) or renk == (1,1,4) or renk == (102, 102, 102) or renk == (2, 2, 13) or renk == (153,153,153) or renk == (103,104,110) or renk == (221,221,221)  or renk == (52,53,57) or renk ==(0,0,0) or renk == (107, 110, 141) or renk == (103, 104, 110):
                        ilkkordinat = (ilkkordinat[0] - 1, ilkkordinat[1])
                        renk = ImageGrab.grab().getpixel(ilkkordinat)
                        print("-1  verdim",renk)
                    
                    self.MakroHpKordinat = ilkkordinat
              #      win32api.SetCursorPos((ilkkordinat))
                    self.SpamHpCheckbox.setText("OTO-HP Makro Açık/Kapalı [SINIR SEÇİLDİ]")
                    self.makrohpfoto.setStyleSheet(f"background-color: rgb{renk};")
                elif self.MpMakro == 1 and self.MakroMpKordinat is None:
                    ilkkordinat = pyautogui.position()
                    renk = ImageGrab.grab().getpixel(ilkkordinat)
                    print(renk)
                    while renk == (0,0,0) or renk == (14,14,14) or renk == (153,153,154 ) or renk == (255,255,255) or renk == (221,221,221) or renk == (102,102,102) or renk == (51,51,51) or renk == (153,153,153) or renk == (187, 187, 187):
                    #while renk == (255,255,255) or renk == (103,103,102) or renk == (2,1,2) or renk == (3,0,0) or renk == (3,2,0) or renk == (154,153,153) or  renk == (54,53,54) or renk ==(3,2,1) or renk == (2,0,0) or renk == (1,1,1) or renk == (2,1,1) or renk == (139,102,102) or renk == (1,1,4) or renk == (102, 102, 102) or renk == (2, 2, 13) or renk == (153,153,153) or renk == (103,104,110) or renk == (221,221,221)  or renk == (52,53,57) or renk ==(0,0,0) or renk == (107, 110, 141) or renk == (103, 104, 110):
                        ilkkordinat = (ilkkordinat[0] - 1, ilkkordinat[1])
                        renk = ImageGrab.grab().getpixel(ilkkordinat)
                        print("-1  verdim",renk)
                    
                    self.MakroMpKordinat = ilkkordinat
              #      win32api.SetCursorPos((ilkkordinat))
                    self.SpamMpCheckbox.setText("OTO-MP Makro Açık/Kapalı [SINIR SEÇİLDİ]")
                    self.makrompfoto.setStyleSheet(f"background-color: rgb{renk};")

                elif self.Hp == 1 and self.HpKordinat is None:
                    ilkkordinat = pyautogui.position()
                    renk = ImageGrab.grab().getpixel(ilkkordinat)
                    print(renk)
                    self.HpRenk = None
                    while renk == (0,0,0) or renk == (14,14,14) or renk == (153,153,154 ) or renk == (255,255,255) or renk == (221,221,221) or renk == (102,102,102) or renk == (51,51,51) or renk == (153,153,153) or renk == (187, 187, 187):
                    #while renk == (255,255,255) or renk == (103,103,102) or renk == (2,1,2) or renk == (3,0,0) or renk == (3,2,0) or renk == (154,153,153) or  renk == (54,53,54) or renk ==(3,2,1) or renk == (2,0,0) or renk == (1,1,1) or renk == (2,1,1) or renk == (139,102,102) or renk == (1,1,4) or renk == (102, 102, 102) or renk == (2, 2, 13) or renk == (153,153,153) or renk == (103,104,110) or renk == (221,221,221)  or renk == (52,53,57) or renk ==(0,0,0) or renk == (107, 110, 141) or renk == (103, 104, 110):
                        ilkkordinat = (ilkkordinat[0] - 1, ilkkordinat[1])
                        renk = ImageGrab.grab().getpixel(ilkkordinat)
                        print("-1  verdim",renk)
                    
                    self.HpKordinat = ilkkordinat
                    self.HpRenk = renk
              #      win32api.SetCursorPos((ilkkordinat))
                    self.HpCheckBox.setText("OTO-HP Açık/Kapalı [SINIR SEÇİLDİ]")
                    self.otohpfoto.setStyleSheet(f"background-color: rgb{self.HpRenk};")
                elif self.Mp == 1 and self.MpKordinat is None:
                    ilkkordinat = pyautogui.position()
                    renk = ImageGrab.grab().getpixel(ilkkordinat)
                    print("Mp renk:",renk)
                    self.MpRenk = None
                    while renk == (0,0,0) or renk == (255,255,255) or renk == (14,14,14) or renk == (153,153,154 ) or renk == (221,221,221) or renk == (102,102,102) or renk == (51,51,51) or renk == (153,153,153) or renk == (187, 187, 187):
                        ilkkordinat = (ilkkordinat[0] - 1, ilkkordinat[1])
                        renk = ImageGrab.grab().getpixel(ilkkordinat)
                        print("-1  verdim mp",renk)
                    win32api.SetCursorPos((ilkkordinat))
                    self.MpRenk = renk
                    self.MpKordinat = ilkkordinat
                    self.MpCheckBox.setText("OTO-MP Açık/Kapalı [SINIR SEÇİLDİ]")
                    self.otompfoto.setStyleSheet(f"background-color: rgb{self.MpRenk};")
                                                 

            if self.SilmeTus is not None:
                if hasattr(key, 'char') and key.char == self.SilmeTus or hasattr(key, 'name') and key.name == self.SilmeTus:
                    thrd = Thread(target=self.find_and_move_to_image)
                    thrd.start()
                    #self.find_and_move_to_image()
            if self.makrodevrekey is not None:
                    if hasattr(key,'char') and key.char == self.makrodevrekey or hasattr(key,'name') and key.name == self.makrodevrekey:
                        if self.makrodevrede == 1:
                            self.makrodevrede = 0
                        else:
                            self.makrodevrede = 1
                            thrid = Thread(target=self.MakroFunc)
                            thrid.start()
                            #self.MakroFunc()
            if self.BaslatKey is not None:
                    if hasattr(key,'char') and key.char == self.BaslatKey or hasattr(key,'name') and key.name == self.BaslatKey:
                        if self.basladi == 0:
                            self.basladi = 1
                            self.durum.setText("Durum: Çalışıyor")
                            funcbaslatthrd = Thread(target=self.FuncBaslat)
                            funcbaslatthrd.start()
                        else:
                            self.basladi = 0
                            self.birkerebasildi = 0
                            self.birkerebasildi2 = 0
                            for debuff in self.DebuffList:
                                    if debuff in self.birkerebasliste:
                                        self.birkerebasliste.remove(debuff)     
                                        print("birkere bas liste silindi")
                                    if debuff in self.hangisiicin:
                                        self.hangisiicin.remove(debuff)                                     
                            self.durum.setText("Durum: Çalışmıyor")
                            
            if self.ciftElTus is not None:
                if hasattr(key, 'char') and key.char == self.ciftElTus or hasattr(key, 'name') and key.name == self.ciftElTus:    
                        thrd = Thread(target=self.DigerTakCikar)
                        thrd.start()
            if self.KalkanTus is not None:
                if hasattr(key, 'char') and key.char == self.KalkanTus or hasattr(key, 'name') and key.name == self.KalkanTus: 
                    kalkanthrd = Thread(target=self.TekElKalkanTakCikar)
                    kalkanthrd.start()
            if self.KalkanTusSeciyor == 1:
                try:
                    if hasattr(key, 'char'):
                        if self.KeyKullaniyormu(key.char):
                            self.KalkanTus = key.char
                    else:
                        if self.KeyKullaniyormu(key.name):
                            self.KalkanTus = key.name
                    self.selectKalkanKey.setText(f"Tuş Seç [{self.KalkanTus}]")
                    self.KalkanTusSeciyor = 0
                except Exception as e:
                    print("Hata[2]:", e) 
            if self.CiftEleTus is not None:
                if hasattr(key, 'char') and key.char == self.CiftEleTus or hasattr(key, 'name') and key.name == self.CiftEleTus: 
                        ciftelekalkanthrd = Thread(target=self.CiftEleKalkanTakCikar)
                        ciftelekalkanthrd.start()
            if self.GizleKey is not None:
                    if hasattr(key, 'char') and key.char == self.GizleKey or hasattr(key, 'name') and key.name == self.GizleKey: 
                        if self.hidemi == 1:
                            self.setWindowTitle(self.Title)                            
                            self.show()
                            self.hidemi = 0

                        else:
                            self.setWindowTitle("")                            
                            self.hide()
                            self.hidemi = 1


            if self.makrodevreTusSeciyor == 1:
                try:
                    if hasattr(key, 'char'):
                        if self.KeyKullaniyormu(key.char):
                            self.makrodevrekey = key.char
                    else:
                        if self.KeyKullaniyormu(key.name):
                            self.makrodevrekey = key.name
                    self.makrodevreTusSecButton.setText(f"Başlat Tuşu: [{self.makrodevrekey}]")
                    self.makrodevreTusSeciyor = 0
                except Exception as e:
                    print("Hata[2]:", e) 

            if self.CiftEleTusSeciyor == 1:
                try:
                    if hasattr(key, 'char'):
                        if self.KeyKullaniyormu(key.char):
                            self.CiftEleTus = key.char
                    else:
                        if self.KeyKullaniyormu(key.name):
                            self.CiftEleTus = key.name
                    self.CiftEleButton.setText(f"Çift El Tuşu [{self.CiftEleTus}]")
                    self.CiftEleTusSeciyor = 0
                except Exception as e:
                    print("Hata[2]:", e) 
            if self.GizleSeciyor == 1:
                try:
                    if hasattr(key,'char'):
                        if self.KeyKullaniyormu(key.char):
                            self.GizleKey = key.char
                    else:
                        if self.KeyKullaniyormu(key.name):
                            self.GizleKey = key.name
                    self.GizleSeciyor = 0
                    self.GizleButon.setText(f"Gizle Tuşu Seçin [{self.GizleKey}]")
                    
                except Exception as e:
                    print("Hata: gizle seciyor")
                    
            if self.ciftElSeciyor == 1:
                try:
                    if hasattr(key, 'char'):
                        if self.KeyKullaniyormu(key.char):
                            self.ciftElTus = key.char
                    else:
                        if self.KeyKullaniyormu(key.name):
                            self.ciftElTus = key.name
                    self.ciftElKalkan.setText(f"Çift El Kalkan Tuş [{self.ciftElTus}]")
                    self.ciftElSeciyor = 0
                except Exception as e:
                    print("Hata[2]:", e)
            if self.SilmeTusSeciyor == 1:
               try:
                if hasattr(key, 'char'):
                    if self.KeyKullaniyormu(key.char):
                        self.SilmeTus = key.char
                else:
                    if self.KeyKullaniyormu(key.name):
                        self.SilmeTus = key.name
                print(self.SilmeTus)
                self.SilmeTusSeciyor = 0
                self.selectkeyButton.setText(f"Tuş Seç [{self.SilmeTus}]")
               except Exception as e:
                print("Hata:", e) 
                
            if self.BaslatKeySeciyor == 1:
               try:
                if hasattr(key, 'char'):
                    if self.KeyKullaniyormu(key.char):
                        self.BaslatKey = key.char
                else:
                    if self.KeyKullaniyormu(key.name):
                        self.BaslatKey = key.name
                self.BaslatKeySeciyor = 0
                self.BaslatKeyButon.setText(f"Başlat/Durdur Tuş seçin [{self.BaslatKey}]")
               except Exception as e:
                print("Hata:", e) 
        with Listener(on_press=on_press) as listener: # sürekli tuş girişlerini dinler.
            listener.join()
    def KeyKullaniyormu(self, key):
        keys = [self.GizleKey, self.SpamMakroKey, self.makrodevrekey, self.DebuffKey, self.BaslatKey, self.ciftElTus, self.KalkanTus, self.SilmeTus, self.CiftEleTus]
        
        for k in keys:
            if k is not None and k == key:
                
                print(k, "key kullanılıyor")
               # QMessageBox.information(self, "Uyarı", "Girdiğiniz tuşlardan en az biri zaten kullanımda.")
                return False  # Eğer eşleşen bir tuş bulunduysa True döndür
        return True  # Eğer eşleşen bir tuş bulunamadıysa False döndür
    def TekElKalkanTakCikar(self):
        if self.basladi == 0: return
        if self.KalkanKordinat is not None:
                    print("evet")
                    if self.EnvanterAcKapat == 1:
                        pydirectinput.keyDown('i')
                        time.sleep(0.01)
                        pydirectinput.keyUp('i')
                    pyautogui.moveTo((self.KalkanKordinat)) 
                    time.sleep(self.KalkanMs)
                    self.SagClick()
                    time.sleep(0.06)
                    if self.EnvanterAcKapat == 1:
                        pydirectinput.keyDown('i')
                        pydirectinput.keyUp('i')
                    win32api.SetCursorPos((self.KalkanKordinat[0] - 200, self.KalkanKordinat[1]))
    def DigerTakCikar(self):
                    if self.basladi == 0: return
                    if self.ciftelKalkanKordinat is None: return
                    print("devre")
                    if self.EnvanterAcKapat == 1:
                        pydirectinput.keyDown('i')
                        time.sleep(0.01)
                        pydirectinput.keyUp('i')
                    pyautogui.moveTo((self.ciftelKalkanKordinat))
                    time.sleep(self.KalkanMs)
                    self.SolTut()
                    time.sleep(0.03)
                    pyautogui.moveTo((self.SolKordinat))
                    time.sleep(self.KalkanMs)
                    self.SolBirak()
                    time.sleep(self.KalkanMs)
                    if self.EnvanterAcKapat == 1:
                        pydirectinput.keyDown('i')
                        time.sleep(0.01)
                        pydirectinput.keyUp('i')
                    win32api.SetCursorPos((self.ciftelKalkanKordinat[0] - 200, self.ciftelKalkanKordinat[1]))
    def CiftEleKalkanTakCikar(self):
        if self.basladi == 0: return
        if self.Esya1Kordinat is not None and self.Esya2Kordinat is not None:
                    print("tkeelceşce")
                    if self.EnvanterAcKapat == 0:
                        pydirectinput.keyDown('i')
                        time.sleep(0.01)
                        pydirectinput.keyUp('i')
                    if self.ciftele == 0:
                        pyautogui.moveTo((self.Esya1Kordinat))
                        time.sleep(self.KalkanMs)
                        self.SagClick()
                        time.sleep(0.03)
                        pyautogui.moveTo((self.Esya2Kordinat))
                        time.sleep(self.KalkanMs)
                        self.SagClick()
                        self.ciftele = 1
                        time.sleep(0.06)
                    else:
                        
                        pyautogui.moveTo((self.SolKordinat))
                        time.sleep(self.KalkanMs)
                        self.SagClick()
                        time.sleep(0.03)
                        pyautogui.moveTo((self.Esya1Kordinat))
                        time.sleep(self.KalkanMs)
                        self.SagClick()
                        self.ciftele = 0
                        time.sleep(0.06)
                    if self.EnvanterAcKapat == 1:
                            pydirectinput.keyDown('i')
                            pydirectinput.keyUp('i')         
                    win32api.SetCursorPos((self.Esya1Kordinat[0] - 30, self.Esya1Kordinat[1]))
     


    def start_key_listener(self):
        thread = Thread(target=self.key_listener_thread)
        thread.start() # Tuşları dinlemeyi açıyoruz. F1,CTRL,F11,F2,F3,Gizle gibi fonksiyonlar buradan devreye giriyor.
    def KalkanButtonClicked(self):
        if not self.SolEl.isChecked():
            QMessageBox.information(self,"Bilgi","Aşşağıdan 'Sol El' i tikleyip Sol El kordinatı almayı unutmayın"  )
        self.KalkanSeciyor = 1
    def selectButtonClicked(self):
        self.SilmeSeciyor = 1
    def SolElChange(self,state):
        if state == QtCore.Qt.Checked:
            self.Sol = 1
            QMessageBox.information(self,"Bilgi","Sol El slotuna gidip CTRL tuşuna basarak kordinatı seçin.")
        else:
            self.Sol = 0




    def capture_skill(self):
        # Fare imlecinin bulunduğu konumu al
        mouse_x, mouse_y = pyautogui.position()

        # Hayali çerçevenin boyutu
        frame_size = 25
    
        # Çerçeve alanını belirle
        frame_area = (
            mouse_x - frame_size // 2,
            mouse_y - frame_size // 2,
            mouse_x + frame_size // 2, #+ 1100 // 2,
            mouse_y + frame_size // 2
        )
#1100,100

        screenshot = ImageGrab.grab()
        frame_image = screenshot.crop(frame_area)
    #    test_image = screenshot.crop(test_area)
        self.skill_images.append(frame_image)
        q_image = QImage(frame_image.tobytes(), frame_image.width, frame_image.height, QImage.Format_RGB888)
        # QPixmap oluşturun ve QLabel'a ayarlayın
        pixmap = QPixmap.fromImage(q_image)
        self.label.setPixmap(pixmap)    
        print("Skill bölgesi kaydedildi."),
        self.simdiki_foto +=1
        self.SilmeSeciyor = 0
        if self.ilkalan == 0:
            self.HayaliAlan()
    
    
    def DebuffTepki(self):
        if not self.basladi or not self.DebuffOnline:
            return
        try:
            for debuff in self.DebuffList:
                self.handleDebuff(debuff)
        except Exception as e:
            print("Debuff tepki hata: ", e)

        Thread(target=self.DebuffTepki).start()

    def handleDebuff(self, debuff):
        try:
            location = pyautogui.locateOnScreen(debuff, region=self.HayaliAlancik, confidence=0.75)
            if location is not None:
                if self.basladi == 0:
                    return
                if self.birkerebas == 1:
                    if debuff in self.birkerebasliste:
                        print("atladim yapcak bisi yok")
                        return
                        
                # Debuff'u işle

                print("Debuff tespit edildi:", debuff)
                if self.page4SilOnline == 1:
                    Thread(target=self.find_and_move_to_image).start()
                    print(debuff, " için sil işlemleri")
                # Klavye işlemleri
                klavye = Controller()
                if self.DebuffKey is not None:
                    klavye.press(self.DebuffKey)
                    time.sleep(0.03)
                    klavye.release(self.DebuffKey)
                for char in self.DebuffPotinput.text():
                    klavye.press(char)
                    time.sleep(0.03)
                    klavye.release(char)
                if self.page4CiftElKalkan.isChecked():
                    if self.birkerebas == 0 and debuff in self.birkerebasliste:
                        print("return")
                        return
                    asd = Thread(target=self.DigerTakCikar)
                    asd.start()
                    print(debuff, " için2 çiftel kalkan işlemleri")
                if self.page4TekElKalkanOnline == 1:            
                    if self.birkerebas == 0 and debuff in self.birkerebasliste:
                        print("return2")
                        return                     
                    sad = Thread(target=self.TekElKalkanTakCikar)
                    sad.start()
                    print(debuff, " için tekel kalkan işlemleri")   


                if self.birkerebas == 0:
                    if debuff not in self.birkerebasliste:
                        self.birkerebasliste.append(debuff)
                
                          
                # Debuff'u listeye ekle
                self.hangisiicin.append(debuff)
                if self.birkerebas == 1:
                    if debuff not in self.birkerebasliste:   
                       self.birkerebasliste.append(debuff)
                if self.basladi == 0:
                    if debuff in self.birkerebasliste:
                        if self.birkerebas == 1:
                            self.birkerebasliste.remove(debuff)
                            print("silindi")
        except ImageNotFoundException:
            print("Ekranda debuff bulunamadı:", debuff)
            if debuff in self.hangisiicin:
                self.hangisiicin.remove(debuff)
                if debuff in self.birkerebasliste:
                    self.birkerebasliste.remove(debuff)
    def HayaliAlan(self):
        mouse_x, mouse_y = pyautogui.position()
        frame_width = 1100
        frame_height = 100
        frame_center_x = mouse_x
        frame_center_y = mouse_y
        screen_width, screen_height = pyautogui.size()
        frame_left = max(0, frame_center_x - frame_width // 2)
        frame_top = max(0, frame_center_y - frame_height // 2)
        frame_right = min(screen_width, frame_center_x + frame_width // 2)
        frame_bottom = min(screen_height, frame_center_y + frame_height // 2)
        frame_area = (frame_left, frame_top, frame_right, frame_bottom)
        print(frame_area)
        screenshot = ImageGrab.grab()
        frame_image = screenshot.crop(frame_area)
        self.HayaliAlancik = frame_area
        print("Hayali alan seçildi")
        frame_image.save("alan.png")
    def find_and_move_to_image(self):
        if self.basladi == 0: return
        if self.HayaliAlancik is None:
            return
        if self.Silme == 0: return
        print("devre")
        try:
            # Kaydedilen fotoğrafların kontrolü
            if self.skill_images:
                for saved_image in self.skill_images:
                    try:
                        # Ekran görüntüsü içinde kaydedilen fotoğrafın konumunu bul
                        locations = pyautogui.locateOnScreen(saved_image, region=self.HayaliAlancik, confidence=0.8)
                        print("asd", locations)
                        if locations: 
                            if isinstance(locations, tuple):
                                # Tek bir koordinat noktası varsa
                                konum = locations[:2]
                                win32api.SetCursorPos((konum[0] + 12, konum[1]))
                                print("koum:",konum)
                                time.sleep(self.SilMs)
                                self.SolClick()
                                time.sleep(0.03)
                                self.SolClick()
                                print(f"{saved_image} fotoğrafının sol üst köşesine hareket edildi.")
                             
                        else:
                            print(f"{saved_image} fotoğrafı bulunamadı.")
                            pass
                    except ImageNotFoundException:
                        print(saved_image,"Bulunamadi")
            else:
                print("Kaydedilmiş fotoğraf bulunmuyor.")
                pass
        
        except Exception as e:
            print("Hata:", e)

        if self.Otomatik == 1:

            thrds = Thread(target=self.find_and_move_to_image)
            thrds.start()

    def selectKeyClicked(self):
        # Tuş seçme butonuna tıklandığında yapılacak işlemleri burada yazın
     #   QMessageBox.information(self, "Bilgi", "F gibi özel tuşlar seçemezsiniz. Sadece HARF seçin.")
        self.SilmeTusSeciyor = 1
    def page1TusSilClick(self):
        self.SilmeTus = None
        self.selectkeyButton.setText("Tuşu Seç")
if __name__ == '__main__':
    kernel32 = ctypes.WinDLL("kernel32")
    user32 = ctypes.WinDLL("user32")
    SW_HIDE = 0
    hWnd = kernel32.GetConsoleWindow()
  #  if hWnd:
   #    user32.ShowWindow(hWnd, SW_HIDE) 
    app = QApplication([])
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
