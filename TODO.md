# PyK150 TODO List

## Completed Tasks ✅

### Pin Numaralandırması ve Görünürlük
- [x] Pin numaralandırmasını micropro.exe ile uyumlu hale getir
- [x] Yeşil yazıların görünürlüğünü artır
- [x] Pin numaralandırmasını normal çip standardına göre düzenle (sol 1-9, sağ 10-18)
- [x] Turuncu pin bilgilerini basitleştir ve anlaşılır hale getir
- [x] Canvas boyutunu artırarak yeşil yazıların kesilmesini önle

## Current Status
Tüm pin numaralandırma ve görünürlük sorunları çözüldü. PyK150 artık:
- **Normal çip standardına uygun pin numaralandırması** kullanıyor:
  - Sol taraf: 1, 2, 3, 4, 5, 6, 7, 8, 9 (yukarıdan aşağıya)
  - Sağ taraf: 18, 17, 16, 15, 14, 13, 12, 11, 10 (alttan yukarıya)
- **ZIF socket uyumluluğu**: Chip Pin 1, ZIF Pin 2'ye denk geliyor
- Daha parlak ve okunabilir yeşil yazılar gösteriyor
- Basitleştirilmiş ve anlaşılır pin bilgileri sunuyor
- Canvas boyutu artırılarak tüm metinler tam görünüyor

## Next Steps
Kullanıcı test edebilir ve ek iyileştirmeler için geri bildirim verebilir.
