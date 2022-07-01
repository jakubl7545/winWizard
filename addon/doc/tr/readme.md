# Win Wizard #

* Yazar: Oriol Gómez, şu anki kod sahibi Łukasz Golonka
* NVDA uyumluluğu: 2019.3 ve üzeri sürümleri
* İndir [kararlı sürüm][1]

This add-on allows you to perform some operations on the focused window or
the process associated with it.  When killing a process, or showing / hiding
a window a confirmation beep is played when the action succeeds.  If you
find this annoying you can disable these beeps in the Win Wizard's settings
panel available from NVDA's settings dialog.

## Kısayollar:
Tüm kısayollar girdi hareketleri iletişim kutusundaki WinWizard
kategorisinden değiştirilebilir.
### Pencere gizleme ve gizli pencereleri gösterme:
* NVDA+Windows+1'den 0'a kadar sayılar - basılan sayıya denk gelen yuvadaki
  pencereyi gizler
* NVDA+Windows+Sol ok - önceki gizli pencere grubuna gider.
* NVDA+Windows+Sağ ok - sonraki gizli pencere grubuna gider.
* Windows+Shift+H - odaklanan pencereyi gizler ve pencereyi boş olan ilk
  yuvaya koyar
* NVDA+Windows+H - en son gizlenen pencereyi gösterir
* Windows+Shift+L - tüm gizli pencerelerin listesini gruplanmış şekilde
  gösterir (varsayılan olarak son gizli pencere seçilir)

### İşlemleri yönetme:
* Windows+F4 - odaklanılan pencereyle ilişkili işlemi sonlandırır
* NVDA+Windows+P - odaklanılan pencereyle ilişkili işlemin önceliğini
  değiştirebileceğiniz bir iletişim kutusu açar

### Çeşitli kısayollar:
* NVDA+Windows+TAB - switches between top level windows of the current
  program (useful in foobar2000, Back4Sure etc.)
* CTRL+ALT+T - üzerinde bulunulan programın pencere başlığını değiştirir

## Değişiklikler:

### Changes for 5.0.4:

* Compatibility with NVDA 2022.1
* It is now possible to disable confirmation beeps in the add-ons settings
  panel
* Update translations

### 5.0.3 için değişiklikler

* NVDA 2021.1 ile uyumluluk

### 5.0.2 için değişiklikler:

* First release available from the add-ons website

[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=winwizard
